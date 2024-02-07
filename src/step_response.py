"""! 
@file step_response.py
@brief Step response code for LAB0

This file contains functions for setting up interrupt timers and running the 
step response functionality. 
"""

# Imports
import pyb
import utime
import micropython
import cqueue
import globals


#Setup constants for ADC conversion
REF_VOLT = 3.3
MAX_ADC = 4096


def adc_timer_setup(tim_num: int,frequency: float):
    """! 
    @brief Setup for the ADC sampling timer.
    This function takes in a timer number and frequency, and performs the necessary
    setup functions to generate a timer.
    This timer is used to run the ADC voltage sampling function at a given frequency.
    """
    adc_tim = pyb.Timer(tim_num, freq=frequency)      
    adc_tim.callback(adc_timer_irq)
    adc_tim.counter(0)


def square_timer_setup(tim_num:int,frequency:float):
    """! 
    @brief Setup for the square wave generation timer.
    This function takes in a timer number and frequency, and performs the necessary
    setup functions to generate a timer.
    This timer is used to run the square wave generation flag function at a given frequency.
    """
    sqr_tim = pyb.Timer(tim_num, freq=frequency)      
    sqr_tim.callback(square_timer_irq)
    sqr_tim.counter(0)


def adc_timer_irq(tim_num):
    """! 
    @brief Interrupt callback function for sampling voltages.
    This function is called by the ADC sampling timer and reads the ADC at a given time.
    This value is then added to the queue to be used outside of the callback function.
    """
    globals.int_queue.put(globals.pinC0.read())


def square_timer_irq(tim_num):
    """! 
    @brief Interrupt callback function for setting pin states for square wave generation.
    This function is called by the square wave generation timer sets a flag at a given rate.
    The flag is then used by the main loop to determine when it is time to toggle the
    pin that generates the square wave.
    """
    globals.square_toggle = 1  


def step_response (square_pin: pyb.Pin, ADC_pin: pyb.ADC):
    """! 
    @brief Loop to generate needed outputs.
    Reads flag from square wave timer to toggle pin state at the requested interval.
    Reads from adc data queue and converts to mV values to print over serial.
    Performs no functions between either of these tasks.
    Data is printed to be read over a serial connection.
    """

    time_since_start = 0

    square_pin.value(0)

    globals.square_toggle = 0

    while 1:

        if globals.square_toggle and not square_pin.value(): #If the square wave is low -> high
            globals.square_toggle = 0
            square_pin.value(not square_pin.value())
        
        elif globals.square_toggle:
            print("End")
            square_pin.value(0)
            break


        if globals.int_queue.any():
            voltage = (globals.int_queue.get()/MAX_ADC) * REF_VOLT
            print(str(time_since_start) + "," + str(voltage))
            time_since_start += 10
    
    return