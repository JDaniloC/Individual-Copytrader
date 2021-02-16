from cryptography.fernet import Fernet
import json

chave = Fernet(b'yqzmMSzGGdoYCfIu_OCE5VEQeDh5v5M6vqjDqhAGYk0=')

'''
            INSTRUÇÕES
titulo = Texto que fica na janela do bot
icone  = Link do ícone (deixe "" para manter o da IQ)
login  = Título que aparece no login
nome   = Nome do bot (se necessário)
'''

infos = json.dumps({
    "titulo": "Copytrader",
    "login": "CopyClient Controller",
    "nome": "CopyTrader",
    "icone": ""
}).encode()


with open('data.dll', 'w', encoding='utf-8') as file:
    file.write(chave.encrypt(infos).decode('utf-8'))

print("Arquivo gerado")
