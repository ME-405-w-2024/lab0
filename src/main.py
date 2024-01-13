# spacing




import pyb
import utime
import micropython
import cqueue

global square_toggle

micropython.alloc_emergency_exception_buf(100)

square_toggle = 0
time_since_start = 0

# set initial value of c0
pinC0_value = 0

REF_VOLT = 3.3
MAX_ADC = 4096

# seutp adc to be pin 1
adc0 = pyb.ADC(pyb.Pin.board.PC1)
# setup Pin C0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

# setup c-queue
global int_queue
int_queue = cqueue.IntQueue(10)

def sampling_timer(self):              
    int_queue.put(adc0.read())

# create a timer at 100hz freq to serve as interrupt for measurement
timer = pyb.Timer(4, freq=100)      
timer.callback(sampling_timer)    

def square_timer(self):              
    global square_toggle
    square_toggle = 1  

# create a timer at 0.2hz freq to serve as interrupt for square wave
timer2 = pyb.Timer(2, freq=0.2)      
timer2.callback(square_timer)


#Loop Forever
while 1:
    if square_toggle:
        square_toggle = 0
        pinC0_value = not pinC0_value
        pinC0.value(pinC0_value)
        time_since_start = 0

    while int_queue.any():
        print(str(time_since_start) + "," + str((int_queue.get()/MAX_ADC) * REF_VOLT))
        time_since_start += 10