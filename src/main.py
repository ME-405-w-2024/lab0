import pyb
import utime

def tick(timer):                # we will receive the timer object when being called
    print('Tick')      # show current timer's counter value
tim = pyb.Timer(4, freq=2)      # create a timer object using timer 4 - trigger at 1Hz
tim.callback(tick)              # set the callback to our tick function

#Setup Pin C0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

#Loop Forever
while 1:
    #Set value to 1
    pinC0.value(1)
    #Wait 5 sec
    utime.sleep(5)
    #Set value to 0
    pinC0.value(0)
    #Wait 5 sec
    utime.sleep(5)