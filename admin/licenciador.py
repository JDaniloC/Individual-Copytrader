from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from tkinter import messagebox
from os import path, environ
from tkinter import *
import json

ADMIN_KEY = b'mQsZgZwr59aCrmk6yY5vPkig1jSEybEv7wu0p6FQPsg='
USER_KEY = b'Fnj2g3Lvtqg2Prswy6LwtbNGMmDjhVqHk0fsl2vAR_A='

class Gerador(Frame):
    def __init__(self, janela, timestamp, atual, 
        total, tests, total_tests, expiration):
        super().__init__(janela)        

        for var in ('HOME', 'USERPROFILE', 'HOMEPATH', 'HOMEDRIVE'):
            if environ.get(var) != None:
                self.caminho = environ.get(var)
                try:
                    with open(self.caminho + "/k", "w") as file:
                        file.write("")
                    self.caminho += "/HNRSAGL"
                    break
                except:
                    pass

        self.total_tests = total_tests
        self.expiration = expiration
        self.timestamp = timestamp
        self.pirateado = False
        self.janela = janela
        self.atual = atual
        self.total = total
        self.tests = tests
        if atual == total:
            messagebox.showwarning("LICENCA", 
                "Chegou no limite de licenças compre um novo limite.")
        if expiration - datetime.now().timestamp() < 0:
            messagebox.showwarning("LICENÇA",
                "Chegou ao tempo limite, compre um novo limite!")
        
        self.conferir_integridade()

        self.pack(fill = X, padx = 10, pady = 10)
        self.widgets()

    def conferir_integridade(self):
        '''
        Confere se no arquivo de integridade essa licença já não foi usada.
        '''
        try:
            adicionar = False
            if path.exists(self.caminho):
                with open(self.caminho, "r+") as file:
                    licenses = json.load(file)
                    if self.timestamp in licenses:
                        if licenses[self.timestamp] != self.atual:
                            messagebox.showerror(
                                "PIRATA", 
                                "Incongruência no arquivo de licença. Peça outro.")
                            self.pirateado = True
                    else:
                        adicionar = True
                if adicionar:
                    with open(self.caminho, "w") as file:
                        licenses.update({self.timestamp: self.atual})
                        file.write("")
                        json.dump(licenses, file)
            else:
                with open(self.caminho, "w") as file:
                    json.dump({self.timestamp: self.atual}, file)
        except Exception as e:
            print(e)

    def widgets(self):
        '''
        Instancia todos os widgets e suas respectivas variáveis
        '''
        self.titles = {
            "email": StringVar(),
            "dia": IntVar(value = 1), 
            "mês": IntVar(value = 1),
            "ano": IntVar(value = 2021),
            "hora": IntVar(value = 0), 
            "minuto": IntVar(value = 0)
        }
        limite = self.expiration - datetime.now().timestamp()
        delta = timedelta(seconds = limite)

        Label(self, text = f"{self.atual} de {self.total} licenças geradas"
            ).grid(row = 0, columnspan = 2)
        Label(self, text = f"{self.tests} de {self.total_tests} testes geradas"
            ).grid(row = 1, columnspan = 2)
        Label(self, text = f"{delta if limite > 0 else 'expirado'}"
            ).grid(row = 2, columnspan = 2)
        for indice, nome in enumerate(self.titles):
            Label(self, text = nome).grid(row = indice + 3)
            Entry(self, textvariable = self.titles[nome]).grid(row = indice + 3, column = 1)
        
        self.titles["ranking"] = BooleanVar()
        Checkbutton(self, text = "Top ranking", 
            variable = self.titles["ranking"],
            onvalue = True, offvalue = False,
            ).grid(row = len(self.titles) + 2, columnspan = 2)
        
        button = Button(self, text = "Gerar licença", command = self.gerar)
        outro = Button(self, text = "Gerar teste", command = self.testar)
        if self.atual >= self.total or self.pirateado:
            button.config(state = DISABLED)
        if self.tests >= self.total_tests or self.pirateado:
            outro.config(state = DISABLED)
        if limite < 0:
            button.config(state = DISABLED)
            outro.config(state = DISABLED)
        
        outro.grid(row = 10)
        button.grid(row = 10, column = 1)

    def testar(self):
        '''
        Gera uma licença teste
        '''
        if self.tests < self.total_tests:
            f = Fernet(USER_KEY)
            data = datetime.fromtimestamp(
                datetime.now().timestamp() + 86400 * 3)
            dia = data.day
            mes = data.month
            ano = data.year
            with open("license.key", "wb") as file:
                message = f"{dia}/{mes}/{ano}"
                result = f.encrypt(message.encode())
                file.write(result)
            messagebox.showinfo("Teste", "Arquivo teste gerado.")
            self.tests += 1
            self.garantir_integridade()
        else:
            messagebox.showwarning("Testes", 
        "Você atingiu o máximo de testes gerados. Compre mais licenças.")

    def gerar(self):
        '''
        Pega o valor dos widgets e passa para o criar_licenca
        '''
        if self.atual < self.total:
            email = self.titles['email'].get()
            dia = str(self.titles['dia'].get())
            mes = str(self.titles['mês'].get())
            ano = self.titles['ano'].get()
            hora = self.titles['hora'].get()
            minuto = self.titles['minuto'].get()
            ranking = self.titles['ranking'].get()

            self.criar_licenca(email, dia, mes, ano, hora, minuto, ranking)
        else:
            messagebox.showwarning("Licença", 
        "Você atingiu o máximo de licenças geradas. Compre mais licenças.")

    def criar_licenca(self, email, dia, mes, ano, hora, minuto, ranking): 
        '''
        Criptografa uma mensagem com todos os dados (email e data)
        E escreve em um arquivo.
        '''
        f = Fernet(USER_KEY)
        with open(email + ".key", "wb") as file:
            message = f"{email}|{dia}/{mes}/{ano}|{hora}:{minuto}|{ranking}"
            result = f.encrypt(message.encode())
            file.write(result)
        messagebox.showinfo("Informação", "Arquivo gerado.")
        self.atual += 1
        self.garantir_integridade()

    def garantir_integridade(self):
        '''
        Escreve na licença atual o número de licenças geradas
        Escreve no arquivo de integridade uma cópia disso.
        '''
        with open('license', 'wb') as file:
            message = f"{self.timestamp}|{self.atual}|{self.total}|{self.tests}|{self.total_tests}|{self.expiration}"
            result = f.encrypt(message.encode())
            file.write(result)
        with open(self.caminho, "r") as file:
            licenses = json.load(file)
            licenses[self.timestamp] = self.atual
        with open(self.caminho, "w") as file:
            json.dump(licenses, file)

path.expanduser('~user')
if __name__ == "__main__":
    f = Fernet(ADMIN_KEY)
    try:
        with open("license", 'rb') as file:
            message = f.decrypt(file.readline())
            message = message.decode()
            timestamp, atual, total, test, total_test, exp = message.split("|")
    except Exception as e:
        print(e)
        timestamp, atual, total, test, total_test, exp = 0, 0, 0, 0, 0, 0
    
    janela = Tk()
    janela.title("Licenciador")
    janela.geometry("+600+200")
    program = Gerador(janela, timestamp, int(atual), 
        int(total), int(test), int(total_test), float(exp))
    program.mainloop()