"""! @file main.py
@brief Micropython code for LAB0

LAB0 has two main functions, generating a square wave and reading measured voltages.
The square wave is to occur at a frequency of 0.2Hz.
The sampling of the voltages is to be in mV and done every 10ms.
"""

import globals
import step_response


if __name__ == "__main__":

    globals.init()
    globals.square_toggle = 0

    #Setup adc timer as timer 4, 100 hz freq
    step_response.adc_timer_setup(4,100)

    #Setup square wave timer as timer 5, 1/5 hz freq
    step_response.square_timer_setup(5,1) # change back to 0.2hz

    #Begin main loop
    step_response.step_response(globals.pinB0, globals.pinC0)
