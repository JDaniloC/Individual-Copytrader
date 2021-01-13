from cryptography.fernet import Fernet
import time

ADMINKEY = b'mQsZgZwr59aCrmk6yY5vPkig1jSEybEv7wu0p6FQPsg='
total = int(input("Digite o valor de licenças: "))

f = Fernet(ADMINKEY)
with open('license', 'wb') as file:
    message = f"{time.time()}|0|{total}"
    result = f.encrypt(message.encode())
    file.write(result)