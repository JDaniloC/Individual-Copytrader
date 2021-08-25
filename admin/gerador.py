from cryptography.fernet import Fernet
from datetime import timedelta
import time

ADMIN_KEY = b'mQsZgZwr59aCrmk6yY5vPkig1jSEybEv7wu0p6FQPsg='
licenses = int(input("Digite o valor de licenças: "))
tests = int(input("Digite o valor de testes: "))
days = int(input("Digite os dias de validade: "))
days = time.time() + timedelta(days = int(days)).total_seconds()

f = Fernet(ADMIN_KEY)
with open('license', 'wb') as file:
    message = f"{time.time()}|0|{licenses}|0|{tests}|{days}"
    result = f.encrypt(message.encode())
    file.write(result)