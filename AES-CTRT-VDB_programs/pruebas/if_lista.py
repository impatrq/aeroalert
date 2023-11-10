import time


hora = time.localtime()
a = str("%02.0f:%02.0f:%02.0f" %(hora[3],hora[4],hora[5]))
print(a)