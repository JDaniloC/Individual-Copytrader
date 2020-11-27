from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import eel, time, threading

def esperar_proximo_minuto():
	time.sleep(
		(datetime.now() + timedelta(seconds = 50)
	).replace(second = 58).timestamp() - time.time())

class IQOption:
    def __init__(self):
        self.API = IQ_Option("daniloedaniel123@gmail.com", "Danilo123")
        self.API.connect()
        self.API.change_balance("PRACTICE")
        self.asset = "EURUSD"
        self.option = "digital"
        self.timeframe = 60
        self.amount = 2
        self.updating = False
    
    def get_candles(self):
        candles = self.API.get_candles(self.asset, self.timeframe, 20, time.time())
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
        menor = 100000

        for candle in result:
            candle['volume'] = round((variancia - candle['volume']) * 100000)
            if candle['dir'] != "doji" and len(str(abs(candle['volume']))) < menor: 
                menor = len(str(abs(candle['volume'])))
            candle['from'] = datetime.fromtimestamp(candle['from']).strftime("%H:%M")

        divisor = 10 ** (menor - 1)
        for candle in result:
            candle['volume'] /= divisor

        return result
    
    def ordem(self, direcao):
        direcao = direcao.lower()
        par, valor = self.asset, self.amount
        tipo, tempo = self.option, self.timeframe // 60
        
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
            time.sleep((tempo * 60) - 10)
            while not status:
                status, lucro = self.API.check_win_digital_v2(identificador)
                time.sleep(0.5)
            if lucro > 0: resultado = "win"
            elif lucro < 0: resultado = "loose"
            else: resultado = "equal"
        
        return resultado, lucro

    def update_candles(self):
        self.updating = True
        while self.updating:
            candles = self.get_candles()
            eel.addCandles(candles)
            time.sleep(5)
            # esperar_proximo_minuto()

api = IQOption()

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
    print(api.ordem(direcao))

eel.init('web')
eel.start('index.html')