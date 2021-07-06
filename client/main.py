import re, traceback
def escreve_erros(erro):
    linhas = " -> ".join(re.findall(
        r'line \d+', str(traceback.extract_tb(erro.__traceback__))))
    with open("errors.log", "a") as file:
        file.write(f"{type(erro)} - {erro}:\n{linhas}\n")

try:
    from bot import *
    eel.start('index.html', port = 8015)
except Exception as e:
    escreve_erros(e)