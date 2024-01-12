
import pyb
import time
#import step_response as sr

#Setup Pin C0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

#Loop Forever
while 1:
    #Set value to 1
    pinC0.value(1)
    #Wait 5 sec
    time.sleep(1)
    #sr.step_response()
    #Set value to 0
    pinC0.value(0)
    #Wait 5 sec
    time.sleep(1)