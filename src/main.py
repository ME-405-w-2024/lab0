"""! 
@file main.py
@brief Micropython code for LAB0

This file runs as main on the NUCLEO board. 
The function generation portion of this lab has two main functions, 
generating a square wave and reading measured voltages.
The square wave is to occur at a frequency of 0.2Hz.
The sampling of the voltages is to be in mV and done every 10ms.
This file sets up the interrupt timers and begins the step response.
"""

# Imports
import globals
import step_response
import pyb
import micropython

# Allocate emergency memory for exceptions during interrupts
micropython.alloc_emergency_exception_buf(1000)


if __name__ == "__main__":

    # Call the "globals" file for use of globals across files
    globals.init()
    globals.square_toggle = 0

    # Begin main loop
    while 1:
        # write data over virtual serial port
        if pyb.USB_VCP().any():
            pyb.USB_VCP().read()

            # Setup adc timer as timer 4, 100 hz freq
            step_response.adc_timer_setup(4,100)

            # Setup square wave timer as timer 5, 1/5 hz freq
            step_response.square_timer_setup(5,0.2)

            # Generate the step function using pinC0 as the ADC and pinB0 as the output
            step_response.step_response(globals.pinB0, globals.pinC0)