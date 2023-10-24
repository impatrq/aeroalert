class Pulso():
    def __init__ (self):
        self.datos=0
        self.datos2=0
        self.datos3=0

    def muestra (self, pin_prendido):
        from machine import SoftI2C, Pin, I2C
        from utime import ticks_diff, ticks_us
        from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
        import utime

        utime.sleep(1)
        i2c = SoftI2C(sda=Pin(21),  
                      scl=Pin(22),  
                      freq=400000)  
        sensor = MAX30102(i2c=i2c)
        
        if sensor.i2c_address not in i2c.scan():
            print("Sensor no encontrado")
            return
        elif not (sensor.check_part_id()):
            print("ID de dispositivo I2C no correspondiente a MAX30102")
            return
        else:
            print("Sensor conectado y reconocido")
        
        print("Configurando el sensor", '\n')
        sensor.setup_sensor()
        sensor.set_sample_rate(400)
        sensor.set_fifo_average(8)
        sensor.set_pulse_width(411)
        #sensor.set_adc_range(16348)
        
        sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)
        utime.sleep(1)
        dato3 =(sensor.read_temperature()) # ("Leyendo temperatura en °C.", '\n')
        self.datos3 = dato3
        print("Iniciando la adquisición de datos de los registros RED e IR...", '\n')
        utime.sleep(1)
        t_start = ticks_us()  # Starting time of the acquisition
        
        MAX_HISTORY = 32
        history = []
        minima = 0
        maxima = 0
        threshold_on = 0
        threshold_off = 0
        
        beats_history = []
        beat = False
        beats = 0
        

        while True:
            #while pin_prendido.value():
            # The check() method has to be continuously polled, to check if
            # there are new readings into the sensor's FIFO queue. When new
            # readings are available, this function will put them into the storage.
            sensor.check()
            # Check if the storage contains available samples
            if sensor.available():
                # Access the storage FIFO and gather the readings (integers)
                valueir = sensor.pop_red_from_storage()
                valuered = sensor.pop_ir_from_storage()
                
                 
                
                Spo2 = valueir * 100/13000                                                     # valueir * 105/16500 para mediciones en el dedo, Spo2 = valueir * 105/11500 para la muñeca por arriba
                self.datos2 = Spo2
                if valuered < 30000:
                    history.append(valuered)
                    # Get the tail, up to MAX_HISTORY length
                    history = history[-MAX_HISTORY:]


                minima, maxima = min(history), max(history)

                threshold_on =(minima + maxima * 2) / 3   #(minima + maxima * 1.75) // 2.748       # (a+b*2)/3 dedo --------- (a+b*1.5)/2.5
                threshold_off =((minima + maxima) / 2) #(( 1.3 * minima + maxima) // 2.302)    # (a+b)/2 dedo------ (a+b)/2
                
                if valuered > 4000:
                    
                    if not beat and valuered > threshold_on:
                        beat = True                    
                        t_us = ticks_diff(ticks_us(), t_start)
                        t_s = t_us/1000000
                        f = 1/t_s
                        bpm = f * 60
                        
                        if bpm < 300:
                            t_start = ticks_us()
                            beats_history.append(bpm)                    
                            beats_history = beats_history[-MAX_HISTORY:]
                            beats = round(sum(beats_history)/len(beats_history) )
                            self.datos = beats

                    if beat and valuered< threshold_off:
                        beat = False

                else:
                    print('Not finger',beats_history)
                    beats_history.append(0)
                    beats_history = beats_history[-MAX_HISTORY:]
                    beats = round(sum(beats_history)/len(beats_history) )
                    self.datos = beats
                    utime.sleep(2)
                
