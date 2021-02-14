import re, traceback
def escreve_erros(erro):
    linhas = " -> ".join(re.findall(
        r'line \d+', str(traceback.extract_tb(erro.__traceback__))))
    with open("errors.log", "a") as file:
        file.write(f"{type(erro)} - {erro}:\n{linhas}\n")

try: 
    from iqoptionapi.stable_api import IQ_Option
    import eel, time, threading, json

    from datetime import datetime, timedelta
    from cryptography.fernet import Fernet
    from dontpad import Dontpad
    from os import listdir

    class IQOption:
        def __init__(self):
            self.API = None
            self.asset = "EURUSD"
            self.option = "digital"
            self.timeframe = 60
            self.amount = 2
            self.updating = False
            self.url = ""
        
        def login(self, email, password):
            self.API = IQ_Option(email, password)
            self.API.connect()
            if self.API.check_connect():
                self.API.change_balance("PRACTICE")
                return True
            return False

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

            factor = total / len(candles)
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
        
        def ordem(self, direcao):
            def enviar_sinal(par, direcao, tempo, tipo):
                Dontpad.write("copytrader/" + self.url, 
                    json.dumps({"orders": [{
                        "asset": par, "order": direcao, "type": tipo,
                        "timeframe": tempo, "timestamp": time.time()
                    }]}
                ))

                eel.animatePopUp("add.svg", "Ordem adicionada!")
                eel.createOrder(par.upper(), direcao.upper(), tipo.capitalize(), tempo * 60)
            
            direcao = direcao.lower()
            par, valor = self.asset, self.amount
            tipo, tempo = self.option, self.timeframe // 60
            
            threading.Thread(target = enviar_sinal, 
                args = (par, direcao, tempo, tipo)).start()

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
        if api.login(email, password):
            return True
        return False

    @eel.expose
    def start_capture():
        threading.Thread(
            target = api.update_candles, daemon=True).start()
    @eel.expose
    def stop_capture():
        api.updating = False
        
    @eel.expose
    def change_asset(asset):
        api.asset = asset['title'].replace(
            "/", "").replace(" (OTC)", "-OTC")
        api.option = asset['option'].lower()
        api.timeframe = asset['timeframe']
        api.amount = asset['amount']

    @eel.expose
    def operate(direcao):
        threading.Thread(
            target=api.ordem, args=(direcao, ),
            daemon = True
        ).start()

    def get_data():
        f = Fernet(b'yqzmMSzGGdoYCfIu_OCE5VEQeDh5v5M6vqjDqhAGYk0=')
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

    def devolve_restante(tempo_restante):
        if  tempo_restante < 0:
            mensagem = "Renove sua licença"
            api.url = None
        else:
            horas_minutos = timedelta(seconds = tempo_restante)
            duracao = str(horas_minutos)[:-7].replace('days', 'dias')
            if "dias" not in duracao:
                duracao += "h"
            mensagem = f"Sua licença dura {duracao}"
        return mensagem

    def procurar_licenca(filetext = ""):
        f = Fernet(b'cHJvN6obAWDiWc5ghyYrPTuPx5x2a8DKr55RVQIMT50=')
        dia, mes, ano = 17, 2, 2021
        email, hora, minuto = "", 0, 0

        def decrypt(text):
            message = f.decrypt(text).decode()
            email, data, horario = message.split("|")
            dia, mes, ano = list(map(int, data.split("/")))
            hora, minuto = list(map(int, horario.split(":")))
            return email, dia, mes, ano, hora, minuto

        if filetext != "":
            try:
                email, dia, mes, ano, hora, minuto = decrypt(
                    filetext.encode("utf-8"))
            except Exception as e: print(type(e), e); filetext = ""
        else:
            try:
                files = listdir(".")
                indice = list(map(lambda x:".key" in x, files)).index(True)
                with open(f"{files[indice]}", "rb") as file:
                    email, dia, mes, ano, hora, minuto = decrypt(file.readline())
            except:
                try:
                    with open("license.key", "rb") as file:
                        message = f.decrypt(file.readline()).decode()
                        dia, mes, ano = list(map(int, message.split("/")))
                except Exception as e: 
                    print(e)
        
        data_final = datetime(ano, mes, dia, hora, minuto)
        tempo_restante = datetime.timestamp(data_final
            ) - datetime.timestamp(datetime.now())

        mensagem = devolve_restante(tempo_restante)
        return mensagem, email, filetext

    @eel.expose
    def search_license(text):
        mensagem, email, filetext = procurar_licenca(text)
        eel.changeLicense(email, mensagem)
        if filetext != "":
            with open("license.key", "wb") as file:
                file.write(filetext.encode("utf-8"))

    get_data()
    with open("config/data.json") as file:
        resultado = json.load(file)
        api.url = resultado['id']

    mensagem, email, caminho = procurar_licenca()
    eel.changeLicense(email, mensagem)
    eel.start('index.html', port = 8001)
except Exception as e:
    escreve_erros(e)