from utils.operar import Operacao
import eel, time, json, threading

from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dontpad import Dontpad
from os import listdir

class IQOption:
    def __init__(self):
        self.API = None
        self.id = 0
        self.wait = 3
        self.url = ""
        self.account = "train"

    def change_balance(self, balance):
        if self.API != None:
            if not balance and self.account != "real":
                self.API.change_balance("REAL")
                self.account = "real"
            elif self.account != "train":
                self.API.change_balance("PRACTICE")
                self.account = "train"

    def login(self, email, password):
        config = {
            "scalper_loss": 0,
            "tipo_stop": "fixo", 
            "tipo_soros": "normal", 
            "tipo_conta": "treino",
            "tipo_gale": "martingale",
            "chat_id": "", "token": "",
            "tipo_martin": "agressivo",
            "minimo": 0, "delay": False,
            "scalper_win": 0, "valor": 2, 
            "stoploss": 10, "max_gale": 2,
            "stopwin": 10, "ciclos_gale": [],
            "email": email, "senha": password,
            "max_soros": 0, "ciclos_soros": [], 
            "prestopwin": 0, "prestoploss": False,
            "tipo_par": "auto", "vez_gale": "vela",
        }
        def set_config(_config): 
            if _config == None:
                _config = config
            eel.saveChanges(_config)
        
        try:
            eel.loadConfig()(set_config)
            self.API = Operacao(config)
            self.API.output = addLog
            return True
        except Exception as e:
            print(type(e), e)
            return False

    def ordem(self, par, tipo, direcao, tempo):
        id = self.id
        eel.placeTrade(par.upper(), direcao.upper(), tempo, id)
        self.id += 1

        resultado = self.API.realizar_trade(self.API.valor, 
            par, direcao, tempo, 0.7, tipo)

        eel.setResult(id, resultado.upper())
        eel.updateInfos(self.API.ganho_total, 
            self.API.stopwin, self.API.stoploss)

        return resultado

    def auto_trade(self):
        ultimo = ()
        while (self.API.ganho_total < self.API.stopwin and 
            self.API.ganho_total > -self.API.stoploss):
            response = json.loads(
                Dontpad.read("copytrader/" + self.url))
            try:
                for trade in response['orders']:
                    timestamp = trade['timestamp']
                    if time.time() - timestamp < self.wait + 2:
                        par, tipo = trade['asset'], trade['type']
                        direcao = trade['order']
                        tempo = trade['timeframe']
                        if (par, timestamp) != ultimo:
                            ultimo = (par, timestamp)
                            threading.Thread(
                                target = self.ordem, daemon = True,
                                args=(par, tipo, direcao, tempo)).start()
            except: pass
            time.sleep(self.wait)
        eel.changeStatus()

api = IQOption()
eel.init('web')

def addLog(*args, **kwargs): eel.addLog(*args, *kwargs)

@eel.expose
def verify_connection(email, password):
    if not api.login(email, password):
        return None
    try:
        json.loads(Dontpad.read("copytrader/" + api.url))
        threading.Thread(
            target = api.auto_trade, daemon = True).start()
        return True
    except: return False

def save_config():
    dic = {
        "id": api.url,
        "wait": api.wait,
    }
    with open("config/data.json", "w") as file:
        json.dump(dic, file, indent = 2)
        
@eel.expose
def change_config(config):
    api.API.salvar_variaveis(config)
    api.wait = config["wait"]
    save_config()
    eel.updateInfos(api.API.ganho_total, 
        api.API.stopwin, api.API.stoploss)

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