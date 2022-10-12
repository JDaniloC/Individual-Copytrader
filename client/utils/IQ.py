from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import time

class IQ_API:
    def __init__(self, login, senha):
        '''
        Recebe o login, e tenta se conectar
        '''
        self.asset, self.timeframe, self.payout_cache = False, False, {}
        self.API = IQ_Option(login, senha)
        self.last_user_id = 0
        self.placeTrade = lambda *x: print(x)
        self.placeResult = lambda *x: print(x)
        if not self.conectar():
            raise ConnectionError(" ❌ Não conseguiu se conectar, reveja a senha ❌ ")

    def mostrar_mensagem(self, msg): print(msg)
    def conectar(self, tentativas = 5):
        '''
        Método para se conectar a plataforma.

        1 - Verifica se está conectado
        2 - Se não, espera 1 segundo e tenta se conectar

        Params:
            tentativas: Quantas vezes irá tentar se conectar caso falhar
        Return:
            Boolean True/False dependente do sucesso.
        '''
        self.API.connect()
        for tentativas in range(tentativas):
            if self.API.check_connect():
                self.mostrar_mensagem("✅ Conectado com sucesso ✅")
                return True
            else:
                self.mostrar_mensagem(" ⏱ Tentando se conectar ⏱")
                self.API.connect()
                time.sleep(1)
        return False

    def format_dir(self, text):
        return text.replace("CALL", "⬆️").replace("PUT", "⬇️")

    def mudar_treino(self):
        '''
        Muda para a conta treino
        '''
        if self.API.get_balance_mode() != "PRACTICE":
            self.mostrar_mensagem(" - Usando a conta treino -\n")
            self.API.change_balance("PRACTICE")
    
    def mudar_real(self):
        '''
        Muda para a conta real
        '''
        if self.API.get_balance_mode() != "REAL":
            self.mostrar_mensagem(" - Usando a conta real -\n")
            self.API.change_balance("REAL")

    def add_payout_cache(self, paridade, modalidade, payout):
        if paridade not in self.payout_cache:
            self.payout_cache[paridade] = {
                "binary": 0, "digital": 0
            }
        paridade = paridade.upper()
        self.payout_cache[paridade][modalidade] = payout

    def payout_digital(self, paridade):
        '''
        Devolve o payout de uma paridade digital
        '''
        try:
            payout = self.API.get_digital_payout(paridade) / 100
            self.add_payout_cache(paridade, "digital", payout)
            return payout
        except:
            return False

    def payout_binaria(self, paridade, tempo = 1):
        '''
        Devolve o payout de uma paridade binária
        caso não tiver este par, então devolve False
        '''
        payouts = self.API.get_all_profit()
        valor = payouts.get(paridade)
        if valor == None:
            result = False
        else:
            if tempo > 5:
                result = valor['binary'] if valor.get(
                    "binary"
                ) else False
            else:
                result = valor['turbo'] if valor.get(
                    "turbo"
                ) else False
        self.add_payout_cache(paridade, "binary", result)
        return result

    def catalogar_erros(self, mensagem):
        def is_in_list(nome, lista):
            for item in lista:
                if item in nome.lower():
                    return True
            return False
        
        if is_in_list(mensagem, ["is not available", "active_suspended", "active_closed"]):
            mensagem = "Ativo fechado nesta modalidade/timeframe."
        elif "invalid instrument" in mensagem:
            mensagem = "Paridade não encontrada na digital pela IQ." 
        else: "A IQ não permitiu!"
        self.mostrar_mensagem("❌ " + mensagem)

    def ordem(self, paridade, direcao = "call", tempo = 1, 
        valor = 1, tipo = "binary", bloqueador = None, 
        delay = False, scalper = False, trying = False):
        '''
        Faz uma ordem e devolve o resultado.
        Params:
            direcao: "call" para comprar ou "put" para vender
            tempo: 1, 10, 15
            valor: dinheiro investido 2 - saldo
            tipo: binary ou digital
            bloqueador: caso estiver trabalhando com threads, um threading.Lock para não pegar o mesmo resultado.
            delay: tempo para pegar o resultado antes/depois
            Scalper: porcentagem de ganho sobre o valor investido
        return:
            (resultado, lucro)
        '''
        current_id = self.placeTrade(paridade, direcao, tempo, valor)
        direcao = direcao.lower()

        if self.config.get('prestoploss', False) and (
            self.perda_total - valor <= -self.stoploss):
            self.mostrar_mensagem("❌ Pré-stoploss: Fim da operação ❌")
            self.verificar_stop(True)
            self.placeResult(current_id, "error")
            return 'error', 0, tipo
        elif self.config.get('prestopwin', 0) > 0:
            missing = (100 - self.config['prestopwin']) / 100
            if self.ganho_total >= self.stopwin * missing:
                self.mostrar_mensagem("✅ Pré-stopwin: Fim da operação ✅")
                self.verificar_stop(True)
                self.placeResult(current_id, "error")
                return 'error', 0, tipo

        if tipo == "binary" and tempo == 5:
            atual = datetime.utcnow()
            if ((atual.minute % 5 == 4 and atual.second < 30) 
                or atual.minute % 5 < 4): 
                tempo = 5 - (atual.minute % 5)

        with bloqueador:
            if tipo == "binary":
                status, identificador = self.API.buy(
                    valor, paridade, direcao, tempo)
            else:
                status, identificador = self.API.buy_digital_spot_v2(
                    paridade, valor, direcao, tempo)

        if not status:
            if tipo == "digital":
                identificador = str(identificador['message'])
            else: identificador = str(identificador)
            self.catalogar_erros(identificador)
            
            if not trying:
                if self.tipo != "auto": 
                    self.tipo = "binary" if self.tipo == "digital" else "digital"
                tipo = "binary" if tipo == "digital" else "digital"
                
                opcoes_modalidade = self.payout_cache.get(paridade.upper())
                payout_modalidade = opcoes_modalidade.get(tipo) if opcoes_modalidade else 1
                payout_atual = round(payout_modalidade * 100) if payout_modalidade else -1
                if payout_atual >= self.config['minimo']:
                    return self.ordem(paridade, direcao, tempo, valor, 
                        tipo, bloqueador, delay, scalper, True)
                else:
                    self.mostrar_mensagem(f"Payout na {tipo} está abaixo do aceitável {payout_atual}% < {self.config['minimo']}%")
            self.placeResult(current_id, "error")
            return "error", 0, tipo

        self.mostrar_mensagem(f"✅ Trade realizado: {paridade} R$ {valor}")
        lucro = 0
        if delay == False:
            # Versão que pega no histórico
            if tipo == "binary":
                resultado, lucro = self.API.check_win_v4(identificador) 
            else:
                status = False
                time.sleep((tempo * 60) - 10)
                while not status:
                    status, lucro = self.API.check_win_digital_v2(identificador)
                    time.sleep(0.5)
                if lucro > 0:
                    resultado = "win"
                elif lucro < 0:
                    resultado = "loose"
                else:
                    resultado = "equal"
        else:
            # Versão que pega na hora
            resultado, lucro = self.API.check_win_v5(
                identificador, tipo, delay)

        self.placeResult(current_id, resultado)
        return resultado, round(lucro, 2), tipo

    def scalper(self, identificador, valor, infos):
        aberto = True
        win = infos["win"] * valor / 100 if valor != 0 else valor * 2
        loss = infos["loss"] * valor / 100 if valor != 0 else valor * 2
        while aberto:
            atual = self.API.get_digital_spot_profit_after_sale(
                    identificador)
            if (round(atual, 2) >= round(win, 2) or 
                round(atual, 2) <= round(-loss, 2)):
                self.API.close_digital_option(identificador)
            aberto = self.API.get_async_order(
                identificador
            )['position-changed']['msg']['status'] == 'open'
            time.sleep(0.3)

    def esperarAte(self, horas, minutos, segundos = 0, 
        data = (), tolerancia = 0, output = False):
        '''
        Espera até determinada data/hora:minuto:segundo do dia
        Se a data não for passada, será considerada a data atual
        formato da data: (dia, mes, ano)
        '''
        if data == ():
            data = datetime.now()
        else:
            data = datetime(*data[::-1])
        alvo = datetime.fromtimestamp(
            data.replace(
                hour = horas, 
                minute = minutos, 
                second = segundos, 
                microsecond = 0
            ).timestamp() - tolerancia)
        agora = datetime.utcnow().timestamp() - 10800 # -3Horas
        segundos = alvo.timestamp() - agora
        if segundos > 10:
            if output:
                alvo = alvo.fromtimestamp(
                    alvo.timestamp() + tolerancia
                )
                self.mostrar_mensagem(
                    f"\n ⏳ Próxima operação às {alvo.strftime('%H:%M:%S')} ⏳")
            time.sleep(segundos)
            return True
        if segundos > (-10 - tolerancia):
            return True
        return False

    @staticmethod
    def martingale(tipo_martin, payout, 
        perca, valor = 1, lucro = 1):
        '''
        Calcula o martingale onde:
            tipo_martin:
                type: float (valor * tipo_martin)
                type: string
                    simples (valor * 2)
                    agressivo (perca * 2.3)
                    leve (vai manter o lucro inicial)
                    seguro (apenas recupera o valor)
                    porcento (vai aumentar uma porcentagem)
            payout: profit da paridade
            perca: valor perdido
            valor: entrada do valor
            lucro: alvo inicial
        '''

        if type(tipo_martin) == float:
            return round(valor * tipo_martin, 2)
        tipo_martin = tipo_martin.lower()
        if tipo_martin == "agressivo":
            return round(abs(perca) * 2.3, 2)
        elif tipo_martin == "simples":
            return round(valor * 2)
        elif tipo_martin == "leve":
            return (abs(perca) + lucro) / payout
        elif tipo_martin == "seguro":
            return round(abs(perca)/payout, 2)
        elif tipo_martin == "percent":
            return round((abs(perca) + lucro) / payout, 2)
        else:
            return round((abs(perca) + abs(perca) * lucro)/payout, 2)

    def is_number(self, number):
        try:
            float(number)
            return True
        except:
            return False
