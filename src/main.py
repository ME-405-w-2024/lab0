import pyb
import utime
import micropython

global sample_en
global square_toggle

micropython.alloc_emergency_exception_buf(100)

sample_en = 0
square_toggle = 0
time_since_start = 0

pinC0_value = 0

REF_VOLT = 3.3
MAX_ADC = 4096

adc0 = pyb.ADC(pyb.Pin.board.PC1)
    

def sampling_timer(self):              
    global sample_en
    sample_en = 1

tim = pyb.Timer(4, freq=100)      
tim.callback(sampling_timer)    


def square_timer(self):              
    global square_toggle
    square_toggle = 1  

tim2 = pyb.Timer(2, freq=0.2)      
tim2.callback(square_timer)


#Setup Pin C0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

#Loop Forever
while 1:

    if square_toggle:
        square_toggle = 0
        pinC0_value = not pinC0_value
        pinC0.value(pinC0_value)
        time_since_start = 0
    
    if sample_en:
        sample_en = 0

        voltage = (adc0.read()/MAX_ADC) * REF_VOLT
        print(str(time_since_start) + "," + str(voltage))

        time_since_start += 10
        