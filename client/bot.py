from iqoptionapi.stable_api import IQ_Option
import eel, requests, time, json, threading
from datetime import datetime

SERVER_URL = "http://34.69.19.239:8000/"

class IQOption:
    def __init__(self):
        self.API = None
        self.amount = 2
        self.stopwin = 10
        self.stoploss = 10
        self.earn = 0
        self.id = 0
    
    def login(self, email, password):
        self.API = IQ_Option(email, password)
        self.API.connect()
        if self.API.check_connect():
            self.API.change_balance("PRACTICE")
            return True
        return False

    def ordem(self, par, tipo, direcao, tempo):
        id = self.id
        eel.placeTrade(par.upper(), direcao.upper(), tempo, id)
        self.id += 1

        if tipo == "binary" and tempo == 5:
            atual = datetime.utcnow()
            if ((atual.minute % 5 == 4 and atual.second < 30) 
                or atual.minute % 5 < 4): 
                tempo = 5 - (atual.minute % 5)

        if tipo == "binary":
            status, identificador = self.API.buy(
                self.amount, par, direcao, tempo)
        else:
            status, identificador = self.API.buy_digital_spot(
                par, self.amount, direcao, tempo)
            
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
                resultado = "win"
            elif lucro < 0: 
                resultado = "loose"
            else: 
                resultado = "equal"

        if resultado == "win": self.earn += lucro
        elif resultado == "loose": self.earn -= abs(lucro)
        eel.setResult(id, resultado.upper())
        eel.updateInfos(self.earn, self.stopwin, self.stoploss)

        return resultado, lucro

    def auto_trade(self):
        while self.earn < self.stopwin and self.earn < self.stoploss:
            response = json.loads(requests.get(SERVER_URL).text)
            for trade in response['orders']:
                if time.time() - trade['timestamp'] < 5:
                    par, tipo = trade['asset'], trade['type']
                    direcao = trade['order']
                    tempo = trade['timeframe']
                    threading.Thread(target = self.ordem, daemon = True,
                        args=(par, tipo, direcao, tempo)).start()
            time.sleep(5)

api = IQOption()

@eel.expose
def verify_connection(email, password):
    if not api.login(email, password):
        return None
    try:
        requests.get(SERVER_URL)
        threading.Thread(target = api.auto_trade, daemon = True).start()
        return True
    except Exception as e: 
        return False

@eel.expose
def change_config(amount, stopwin, stoploss):
    api.amount = float(amount)
    api.stopwin = float(stopwin)
    api.stoploss = float(stoploss)
    eel.updateInfos(api.earn, api.stopwin, api.stoploss)

eel.init('web')
eel.start('index.html')