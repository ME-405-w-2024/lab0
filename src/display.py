"""!
@file display.py

Run real and simulated dynamic response tests and plot the results. It uses Tkinter, an
old-fashioned and ugly but useful GUI library which is included in Python by default.
This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
Original program, based on example from above listed source and from reference code
distributed as part of the ME405 curriculum "lab0example.py". 
"""

# Imports
import math
import time
import tkinter
from random import random
import serial
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.backends._backend_tk import (NavigationToolbar2Tk)

# Constants
# CHANGE THIS DEVICE DEPENDING ON SYSTEM TYPE
#DEV_NAME = "COM6"
DEV_NAME = "/dev/cu.usbmodem2052339C57522"


def plot_RC_data(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    @brief Plot data from a real-world RC response.
    This function reads data from a serial port, then strips lines of strings,
    converting them to floating point numbers. Successfully gathered data is appended
    to arrays of time and voltage.
    To simplify code, plotting of the simulated response is called at the end of this function.
    @param plot_axes The set of axes to plot data onto, from Matplotlib
    @param plot_canvas The canvas to plot data onto, from Matplotlib
    @param xlabel The label for the horizontal axis
    @param ylabel The label for the vertical axis
    """

    times = []
    voltages = []   

    ser = serial.Serial(DEV_NAME, 115200, timeout=5) 

    try:
        ser.write("\n".encode())
        while True:
            line = ser.readline().decode()
            
            line = line.strip('\r\n')

            split_line = line.split(",")

            if len(split_line) > 1:

                times.append(float(split_line[0]))
                voltages.append(float(split_line[1]))

            if not line:
                print("Failed to get data")
                break
    finally:
        print("Closing serial port")
        ser.close()

    # Draw the plot
    plot_axes.plot(times, voltages,marker=".")
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()

    # Plot the simulated response
    plot_RC_response(plot_axes,plot_canvas,xlabel,ylabel)


def plot_RC_response(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    @brief Plot a simulated RC response.
    This function generates a data set of times and corresponding voltages.
    Generated data is intended to align with the real-world data gathered from the
    step response of an RC circuit occuring at time = 5s, and data arrays are offset to accomplish this. 
    @param plot_axes The set of axes to plot data onto, from Matplotlib
    @param plot_canvas The canvas to plot data onto, from Matplotlib
    @param xlabel The label for the horizontal axis
    @param ylabel The label for the vertical axis
    """

    # define constants
    R = 100000
    C = 0.0000033
    V_REF = 3.3

    # set up empty voltage array 
    voltages = [0] * 500
    
    # set up times array up to 5000ms
    times = [t for t in range(0, 5000, 10)]

    # generate data after rising edge
    voltages += [V_REF*(1-math.exp(-(t/1000)/(R*C))) for t in times]

    # append a new set of data to the end of times to make array lengths match
    times += [t for t in range(5000, 10000, 10)]

    # Draw the plot
    plot_axes.plot(times, voltages)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    @brief Create a TK windows with embedded Matplotlib data.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot.
    @param plot_function The function passed that plots data
    @param xlabel The label for the horizontal axis
    @param ylabel The label for the vertical axis
    @param title The title for the window opened
    """

    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # create a matplotlib figure
    fig = Figure()
    axes = fig.add_subplot()

    # create the drawing canvas and a navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas, xlabel, ylabel))
    
    # arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # this function runs until the user quits
    tkinter.mainloop()


if __name__ == "__main__":

    tk_matplot(plot_RC_data,
               xlabel="Time [ms]",
               ylabel="Voltage [V]",
               title="Step Response")