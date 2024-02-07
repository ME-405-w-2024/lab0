"""! 
@file globals.py
@brief Global variable declaration for LAB0

This file declares global variables for use across multiple files. 
This is the "canonical" method of sharing variables between files, see the following:
https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules
"""

import cqueue
import pyb

def init():
    """! 
    @brief Initialization for global variables across files.
    Pins are declared to be ADC or inputs, and a queue 
    is generated to read data written during interrupts.
    """

    global square_toggle
    global int_queue
    global pinC0
    global pinB0

    square_toggle = 0

    #Define queue maximum size
    QUEUE_SIZE = 10
    #Setup queue
    int_queue = cqueue.IntQueue(QUEUE_SIZE)

    #Setup Pin C0 as an ADC to read voltages from
    pinC0 = pyb.ADC(pyb.Pin.board.PC0)

    #Setup Pin B0 as an output to change
    pinB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.OUT_PP)