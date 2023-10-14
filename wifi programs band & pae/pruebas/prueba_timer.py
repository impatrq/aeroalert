from threading import Timer
import time
class test_timer():
    def __init__(self):
        self.awesum="hh"
        self.timer = Timer(1,self.say_hello,args=["WOW"])
        self.timer.start()

    def say_hello(self,message):
        self.awesum=message
        while True:
            try:
                print ('HIHIHIIHIH')
                print (message)
                time.sleep(1)
                

            except KeyboardInterrupt:
                print("Keyboard interrupt")


if __name__ == '__main__':
    print ('Got to main')
    
    x=test_timer()

    print("a ver")
    time.sleep(10)
    print("funciono owo")