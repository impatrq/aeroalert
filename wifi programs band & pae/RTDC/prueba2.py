import json

msg = "aterriza"



data = {'mensage': msg}
message = json.dumps(data).encode('utf-8')
mensage = json.loads(message.decode('utf-8'))
print(mensage['mensage'])