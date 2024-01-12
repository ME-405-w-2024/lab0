
import pyb
import time

#Setup Pin C0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

#Loop Forever
while 1:
    #Set value to 1
    pinC0.value(1)
    #Wait 5 sec
    time.sleep(5)
    #Set value to 0
    pinC0.value(0)
    #Wait 5 sec
    time.sleep(5)