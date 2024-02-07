# spacing




import pyb
import utime
import micropython
import cqueue
import config

<<<<<<< Updated upstream
global square_toggle

micropython.alloc_emergency_exception_buf(100)

=======
#Allocate memory for debug dump
micropython.alloc_emergency_exception_buf(100)

#Define local variables
>>>>>>> Stashed changes
square_toggle = 0
time_since_start = 0

# set initial value of c0
pinC0_value = 0

REF_VOLT = 3.3
MAX_ADC = 4096

<<<<<<< Updated upstream
# seutp adc to be pin 1
adc0 = pyb.ADC(pyb.Pin.board.PC1)
# setup Pin C0
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

# setup c-queue
global int_queue
int_queue = cqueue.IntQueue(10)

def sampling_timer(self):              
    int_queue.put(adc0.read())
=======

def adc_timer_setup(tim_num,frequency):
    """! @brief Setup for the ADC sampling timer

    This function takes in a timer number and frequency, and performs the necessary
    setup functions to generate a timer.
    This timer is used to run the ADC voltage sampling function at a given frequency.
    """
    adc_tim = pyb.Timer(tim_num, freq=frequency)      
    adc_tim.callback(adc_timer_irq)


def square_timer_setup(tim_num,frequency):
    """! @brief Setup for the square wave generation timer

    This function takes in a timer number and frequency, and performs the necessary
    setup functions to generate a timer.
    This timer is used to run the square wave generation flag function at a given frequency.
    """
    sqr_tim = pyb.Timer(tim_num, freq=frequency)      
    sqr_tim.callback(square_timer_irq)


def adc_timer_irq(tim_num):
    """! @brief Interrupt callback function for sampling voltages

    This function is called by the ADC sampling timer and reads the ADC at a given time.
    This value is then added to the queue to be used outside of the callback function.
    """
    config.int_queue.put(adc0.read())
>>>>>>> Stashed changes

# create a timer at 100hz freq to serve as interrupt for measurement
timer = pyb.Timer(4, freq=100)      
timer.callback(sampling_timer)    

<<<<<<< Updated upstream
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
=======
def square_timer_irq(tim_num):
    """! @brief Interrupt callback function for setting pin states for square wave generation

    This function is called by the square wave generation timer sets a flag at a given rate.
    The flag is then used by the main loop to determine when it is time to toggle the
    pin that generates the square wave.
    """
    config.square_toggle = 1  


def step_response (square_pin: pyb.Pin, ADC_pin: pyb.ADC):
    """! @brief Loop to generate needed outputs

    Reads flag from square wave timer to toggle pin state at the requested interval.
    Reads from adc data queue and converts to mV values to print over serial.
    Performs no functions between either of these tasks.
    """
    time_since_start = 0

    square_pin.value(0)

    while 1:

        if config.square_toggle and not square_pin.value(): #If the square wave is low -> high
            square_toggle = 0
            square_pin.value(not square_pin.value())
            time_since_start = 0
        
        elif config.square_toggle:
            print("End")
            break


        if config.int_queue.any():
            voltage = (config.int_queue.get()/MAX_ADC) * REF_VOLT
            print(str(time_since_start) + "," + str(voltage))
            time_since_start += 10



if __name__ == "__main__":

    config.init()

    #Setup pin to read voltages from
    adc0 = pyb.ADC(pyb.Pin.board.PC1)

    #Setup Pin C0
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

    #Setup adc timer
    adc_timer_setup(4,100)

    #Setup square wave timer
    square_timer_setup(5,0.2)

    #Begin main loop
    step_response(pinC0, adc0)
>>>>>>> Stashed changes
