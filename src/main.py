"""! @file main.py
Doxygen style docstring for the file 
"""

import pyb
import utime
import micropython
import cqueue

micropython.alloc_emergency_exception_buf(100)

global square_toggle
global int_queue

square_toggle = 0
time_since_start = 0
pinC0_value = 0

REF_VOLT = 3.3
MAX_ADC = 4096

QUEUE_SIZE = 10

int_queue = cqueue.IntQueue(QUEUE_SIZE)


def adc_timer_setup(tim_num,frequency):
    """!
    Doxygen style docstring for interrupt setup function
    """
    adc_tim = pyb.Timer(tim_num, freq=frequency)      
    adc_tim.callback(adc_timer_irq)


def square_timer_setup(tim_num,frequency):
    """!
    Doxygen style docstring for interrupt setup function
    """
    sqr_tim = pyb.Timer(tim_num, freq=frequency)      
    sqr_tim.callback(square_timer_irq)


def adc_timer_irq(tim_num):
    """!
    Doxygen style docstring for interrupt callback function
    """
    int_queue.put(adc0.read())


def square_timer_irq(tim_num):
    """!
    Doxygen style docstring for interrupt callback function
    """
    global square_toggle
    square_toggle = 1  


def step_response (square_pin: pyb.Pin, ADC_pin: pyb.ADC):
    """!
    Doxygen style docstring for this function 
    """
    global square_toggle
    global sample_en

    time_since_start = 0
    while 1:

        if square_toggle:
            square_toggle = 0
            square_pin.value(not square_pin.value())
            time_since_start = 0

        if int_queue.any():
            voltage = (int_queue.get()/MAX_ADC) * REF_VOLT
            print(str(time_since_start) + "," + str(voltage))
            time_since_start += 10


if __name__ == "__main__":

    adc0 = pyb.ADC(pyb.Pin.board.PC1)

    #Setup Pin C0
    pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)

    adc_timer_setup(4,100)

    square_timer_setup(5,0.2)

    step_response(pinC0, adc0)