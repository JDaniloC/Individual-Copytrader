import re, traceback, csv
from pathlib import Path
from api import Api

def escreve_erros(erro):
    linhas = " -> ".join(re.findall(
        r'line \d+', str(traceback.extract_tb(erro.__traceback__))))
    with open("errors.log", "a") as file:
        file.write(f"{type(erro)} - {erro}:\n{linhas}\n")

try: 
    from iqoptionapi.stable_api import IQ_Option
    import eel, time, threading, json, requests
    from socketclient import WebsocketClient

    from cryptography.fernet import Fernet
    from datetime import datetime

    def timestamp_brazil():
        return datetime.utcnow().timestamp() - 10800

    def pegar_comando_taxas(texto):
        '''
        Recebe um texto e devolve:
        {
            "par": paridade,
            "taxa": int
            "tipo": "taxas"
        }
        '''
        try:
            timeframe = re.search(r'[MH][1-6]?[0-5]', texto.upper())
            if timeframe: 
                texto = re.sub(r'[MH][1-6]?[0-5]', r'', texto.upper())
                if "M" in timeframe[0].upper(): 
                    timeframe = int(timeframe[0].strip("M"))
                else: 
                    timeframe = int(timeframe[0].strip("H")) * 60
            else: timeframe = 0

            primeiro, segundo = re.split(r"[^\w.-]+", texto.strip())
            par = re.search(r'[A-Za-z]{6}(-OTC)?', 
                primeiro.upper().replace("/", ""))
            if not par:
                par = re.search(r'[A-Za-z]{6}(-OTC)?', 
                    segundo.upper().replace("/", ""))[0]
                taxa = float(primeiro)
            else:
                par = par[0]
                taxa = float(segundo)
        except Exception as e:
            print(type(e), e)
            print(f"Revise o comando {texto}")
            return {}
            
        return {
            "par": par, 
            "taxa": taxa, 
            "tipo": "taxas",
            "textHour": "Taxas",
            "timeframe": timeframe,
            "timestamp": timestamp_brazil()
        }

    def pegar_comando_lista(texto):
        def timestamp(data, hora):
            return datetime(
                data[2], data[1], data[0], hora[0], hora[1]
            ).timestamp()
        try:
            data = re.search(r'\d{2}\W\d{2}\W\d{4}', texto)
            if data:
                data = [int(x) for x in re.split(r"\W", data[0])]
            else:
                hoje = datetime.fromtimestamp(timestamp_brazil())
                data = [hoje.day, hoje.month, hoje.year]
            textHour = re.search(r'\d{2}:\d{2}', texto)[0]
            hora = [int(x) for x in re.split(r'\W', textHour)]
            par = re.search(r'[A-Za-z]{6}(-OTC)?', 
                texto.upper().replace("/", ""))[0]
            ordem = re.search(r'CALL|PUT', texto.upper())[0].lower()
            timeframe = re.search(r'[MH][1-6]?[0-5]', texto.upper())
            if timeframe: 
                if "M" in timeframe[0].upper(): 
                    timeframe = int(timeframe[0].strip("M"))
                else: 
                    timeframe = int(timeframe[0].strip("H")) * 60
            else: timeframe = 0
        except Exception as e:
            print(type(e), e)
            return {}

        return {
            "par": par,
            "data": data,
            "hora": hora,
            "ordem": ordem,
            "tipo": "lista",
            "textHour": textHour,
            "timeframe": timeframe,
            "timestamp": timestamp(data, hora)
        }

    def pegar_comando(texto):
        '''
        Verifica se a entrada é de lista ou taxas
        e devolve um dicionário no qual um dos valores
        é {tipo: lista|taxa}.
        '''
        comando = pegar_comando_lista(texto)
        if comando == {}:
            comando = pegar_comando_taxas(texto)
        return comando

    def esperarAte(horas, minutos, data = (), tolerancia = 0):
        if data == ():
            data = datetime.now()
        else:
            data = datetime(*data[::-1])
        alvo = datetime.fromtimestamp(
            data.replace(
                hour = horas, 
                minute = minutos, 
                second = 0, 
                microsecond = 0
            ).timestamp() - tolerancia)
        agora = datetime.utcnow().timestamp() - 10800 # -3Horas
        segundos = alvo.timestamp() - agora
        if segundos > 10:
            eel.createOrder("Esperando...", "", 
                "Lista programada", segundos)
            time.sleep(segundos)
            return True
        if segundos > (-10 - tolerancia):
            return True
        return False

    class IQOption:
        def __init__(self):
            self.API = None
            self.socket = None
            self.asset = "EURUSD"
            self.option = "digital"
            self.timeframe = 60
            self.amount = 2
            self.updating = False
        
        def login(self, email, password):
            with open("./config/data.json") as file:
                config = json.load(file)
            self.API = IQ_Option(email, password)
            self.API.connect()
            if self.API.check_connect():
                self.socket = WebsocketClient(config['ip'], 4949)
                self.socket.connect()
                self.API.change_balance("PRACTICE")
                threading.Thread(
                    target = self.searchTrades, 
                    daemon=True
                ).start()
                return True
            return False

        def seguir_lista(self, lista):
            for index, comando in enumerate(lista):
                if comando["tipo"] == "taxas":
                    eel.selectItemList(index)
                    continue
                data = comando["data"]
                horas, minutos = comando["hora"]
                tempo = (comando['timeframe'] 
                    if comando['timeframe'] != 0 
                    else self.timeframe // 60)

                if esperarAte(horas, minutos, data, 2) and self.updating:
                    par = comando['par']
                    ordem = comando['ordem']
                    threading.Thread(target=api.ordem, 
                        args = (ordem, (par, tempo), False),
                        daemon = True).start()
                eel.selectItemList(index)
                                
                if not self.updating: break

        def get_candles(self):
            candles = self.API.get_candles(
                self.asset, self.timeframe, 20, time.time())
            result = []
            total = 0
            for candle in candles:
                direction = ("call" if candle['open'] < candle['close'] else "put" 
                    if candle['open'] > candle['close'] else "doji")
                volume = candle['open'] - candle['close']
                total += volume
                result.append({'dir': direction, 'volume': volume, "from": candle['from']})

            factor = (total / len(candles)) if len(candles) > 0 else 0
            variancia = 0
            for candle in result:
                variancia += (candle['volume'] - factor) ** 2

            variancia /= len(candles) - 1
            menor = float('inf')

            for candle in result:
                candle['volume'] = round((variancia - candle['volume']) * 100000)
                if (candle['dir'] != "doji" and abs(candle['volume']) < menor 
                    and candle['volume'] != 0):
                    menor = abs(candle['volume'])
                candle['from'] = datetime.fromtimestamp(candle['from']).strftime("%H:%M")

            for candle in result:
                candle['volume'] /= menor

            return result
        
        def searchTrades(self):
            old_trades = {}
            while True:
                for trade in self.API.get_open_trades():
                    trade_id = trade['id']
                    paridade = trade['asset']
                    tempo = trade['timeframe']
                    direcao = trade['direction']
                    if trade_id not in old_trades:
                        old_trades[trade_id] = trade
                        self.enviar_sinal(paridade, direcao, tempo, "binary")
                time.sleep(0.5)

        def path_to_metatrader(self, metatrader_path: str):
            date_string = datetime.now().strftime("%Y%m%d")
            log_file = Path(metatrader_path) / 'Files' / f'{date_string}_retorno.csv'
            return log_file

        def entradas_metatrader(self, metatrader_path: str):
            '''
            Abre o arquivo na pasta do metatrader
            E devolve a lista de entradas.
            '''
            log_file = self.path_to_metatrader(metatrader_path)
            procurando = False
            while not procurando:
                try:
                    with open(log_file) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        csv_reader.__next__()
                        csv_reader = list(csv_reader)
                    return csv_reader
                except PermissionError:
                    time.sleep(0.3)
                except Exception as error:
                    escreve_erros(error)
                    eel.animatePopUp("loss.svg",
                        f"Ocorreu um erro na operação:\n {type(error)}: {error}")
                    procurando = True
            return False
        
        def enviar_metatrader(self, metatrader_path: str,
                                    prev_candles: int = 0,
                                    trade_against: bool = False):
            ultimos = []
            eel.animatePopUp("equal.svg", f"Procurando entradas no metatrader...")
            while True:
                time.sleep(0.5)
                entradas = self.entradas_metatrader(metatrader_path)
                if not entradas: continue
                delay = round(time.time()) - 2

                for entrada in entradas:
                    timestamp, paridade, direcao, timeframe = entrada
                    timestamp, timeframe = int(timestamp), int(timeframe)
                    paridade = paridade.strip().upper()
                    direcao = direcao.upper()

                    if delay <= timestamp and [paridade, timestamp] not in ultimos:
                        if prev_candles > 0:
                            candles = self.API.get_candles(paridade, timeframe,
                                                    prev_candles, time.time())
                            if not candles: continue
                            candle = candles[0]
                            if candle['open'] < candle['close']:
                                direcao = "CALL"
                            elif candle['open'] > candle['close']:
                                direcao = "PUT"
                            else:
                                eel.animatePopUp("equal.svg",
                                                f"A {prev_candles}° anterior deu doji...")
                                continue
                        if trade_against:
                            if direcao == "CALL": direcao = "PUT"
                            else: direcao = "CALL"
                        ultimos.append([paridade, timestamp])
                        eel.animatePopUp("win.svg", f"Metrader: {paridade} {direcao}")
                        self.enviar_sinal(paridade, direcao, timeframe, "digital")

        def enviar_sinal(self, par, direcao, tempo, tipo, send = True):
            if send:
                self.socket.send_message({"orders": [{
                    "asset": par, "order": direcao, "type": tipo,
                    "timeframe": tempo, "timestamp": time.time()
                }]})

            eel.animatePopUp("add.svg", "Ordem adicionada!")
            eel.createOrder(par.upper(), direcao.upper(), 
                tipo.capitalize(), tempo * 60)

        def ordem(self, direcao, data = False, send = True):
            direcao = direcao.lower()
            if data:
                par, tempo = data
            else:    
                par = self.asset
                tempo = self.timeframe // 60
            valor, tipo = self.amount, self.option
            
            threading.Thread(target = self.enviar_sinal, 
                args = (par, direcao, tempo, tipo, send)).start()

            if tipo == "binary" and tempo == 5:
                atual = datetime.utcnow()
                if ((atual.minute % 5 == 4 and atual.second < 30) 
                    or atual.minute % 5 < 4): 
                    tempo = 5 - (atual.minute % 5)

            if tipo == "binary":
                status, identificador = self.API.buy(
                    valor, par, direcao, tempo)
            else:
                status, identificador = self.API.buy_digital_spot(
                    par, valor, direcao, tempo)
                
            if not status:
                return "error", 0

            lucro = 0
            if tipo == "binary":
                resultado, lucro = self.API.check_win_v4(identificador)
            else:
                status = False
                while not status:
                    status, lucro = self.API.check_win_digital_v2(identificador)
                    time.sleep(0.5)
                if lucro > 0: 
                    eel.animatePopUp("win.svg", "Ganhou!")
                    resultado = "win"
                elif lucro < 0: 
                    eel.animatePopUp("loss.svg", "Perdeu...")
                    resultado = "loose"
                else: 
                    eel.animatePopUp("equal.svg", "Doji")
                    resultado = "equal"

            return resultado, lucro

        def update_candles(self):
            self.updating = True
            while self.updating:
                candles = self.get_candles()
                eel.addCandles(candles)
                time.sleep(5)

    api = IQOption()
    eel.init('web')

    @eel.expose
    def login(email, password):
        has_access, message = autenticar_licenca(email)
        if not has_access:
            eel.animatePopUp("loss.svg", message)
            return False

        eel.animatePopUp("add.svg", message)
        if api.login(email, password):
            return True
        return False

    @eel.expose
    def start_capture():
        threading.Thread(
            target = api.update_candles, 
            daemon=True).start()

    @eel.expose
    def stop_capture():
        api.updating = False
        
    @eel.expose
    def change_config(config: dict):
        api.config = config
        Api.write({
            "valor": config["valor"],
            "delay": config["delay"],
            "stopwin": config["stopwin"],
            "stoploss": config["stoploss"],
            "vez_gale": config["vez_gale"],
            "max_gale": config["max_gale"],
            "tipo_stop": config["tipo_stop"],
            "tipo_gale": config["tipo_gale"],
            "max_soros": config["max_soros"],
            "tipo_soros": config["tipo_soros"],
            "prestopwin": config["prestopwin"],
            "tipo_martin": config["tipo_martin"],
            "ciclos_gale": config["ciclos_gale"],
            "prestoploss": config["prestoploss"],
            "ciclos_soros": config["ciclos_soros"]
        })
        
    @eel.expose
    def change_asset(asset):
        api.asset = asset['title'].replace(
            "/", "").replace(" (OTC)", "-OTC")
        api.option = asset['option'].lower()
        api.timeframe = asset['timeframe']
        api.amount = asset['amount']

    @eel.expose
    def start_metatrader(metatrader_path: str, prev_candles: int, trade_against: bool):
        threading.Thread(
            target = api.enviar_metatrader, daemon = True,
            args = (metatrader_path, prev_candles, trade_against),
        ).start()

    @eel.expose
    def operate(direcao):
        threading.Thread(
            target=api.ordem, 
            args = (direcao, False),
            daemon = True
        ).start()

    @eel.expose
    def verificar_lista(texto):
        lista = []
        for entrada in texto.split("\n"):
            if entrada not in ['', '\n']:
                comando = pegar_comando(entrada)
                if comando != {}:
                    lista.append(comando)
        lista.sort(key = lambda x: x["timestamp"])
        return lista

    @eel.expose
    def seguir_lista(lista):
        api.socket.send_message({"orders": lista})
        threading.Thread(
            target=api.seguir_lista, 
            args = (lista, ),
            daemon = True
        ).start()

    def load_bot_data_info():
        f = Fernet(b'Fnj2g3Lvtqg2Prswy6LwtbNGMmDjhVqHk0fsl2vAR_A=')
        try:
            with open("config/data.dll", "rb") as file:
                message = f.decrypt(file.readline()).decode()
                config = json.loads(message)
        except:
            config = {
                "titulo": "Copytrader",
                "login": "CopyClient Login",
                "nome": "CopyTrader",
                "icone": ""
            }
        eel.changeData(config)

    def autenticar_licenca(email):
        validacao, mensagem = False, "Adquira uma licença!"
        try:
            response = requests.get("https://tiagobots.vercel.app/api/clients", 
                params = { "email": email, "botName": "copytrader-adm"}).json()
            if "timestamp" in response and int(response["timestamp"]) > 0:
                validacao, mensagem = True, response["message"]
            else:
                validacao, mensagem = False, "Compre uma licença!"
        except:
            validacao, mensagem = False, "Servidor em manutenção!"
        return validacao, mensagem

    load_bot_data_info()
    eel.start('index.html', port = 8002)
except Exception as e:
    escreve_erros(e)