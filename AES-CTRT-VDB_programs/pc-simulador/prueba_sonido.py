from playsound import playsound
import _thread
import time

# cambiar a directorio "pc-simulador"
global alarma_sonora_aes_activation, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_hypoxia, alarma_sonora_manual_activation, alarma_sonora_test_failed, alarma_sonora_test_pass


alarma_sonora_aes_activation = alarma_sonora_aes_alert = alarma_sonora_sleep = alarma_sonora_hypoxia = alarma_sonora_manual_activation = alarma_sonora_test_failed = alarma_sonora_test_pass = 1

def thread_sonidos():
    global alarma_sonora_aes_activation, alarma_sonora_aes_alert, alarma_sonora_sleep, alarma_sonora_hypoxia, alarma_sonora_manual_activation, alarma_sonora_test_failed, alarma_sonora_test_pass
    while True:
        time.sleep(1)
        if alarma_sonora_aes_activation:
            playsound("./imgs_alerts_GUI/alerta_aes_act.mp3")     
        if alarma_sonora_aes_alert:
            playsound("./imgs_alerts_GUI/alerta_aes_alert.mp3")
        if alarma_sonora_sleep:
            playsound("./imgs_alerts_GUI/alerta_get_up.mp3")
        if alarma_sonora_hypoxia:
            playsound("./imgs_alerts_GUI/alerta_hypoxia.mp3")
        if alarma_sonora_manual_activation:
            playsound("./imgs_alerts_GUI/alerta_manual_act.mp3")
        if alarma_sonora_test_failed:
            playsound("./imgs_alerts_GUI/alerta_test_failed.mp3")
            alarma_sonora_test_failed = 0
        if alarma_sonora_test_pass:
            playsound("./imgs_alerts_GUI/alerta_test_pass.mp3")
            alarma_sonora_test_pass = 0

_thread.start_new_thread(thread_sonidos, ())

time.sleep(5)
while True:
    print(".", end="", flush=True)
    time.sleep(.01)
alarma_sonora_hypoxia = 1