import math
import time
import tkinter
from random import random
import serial
import io
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.backends._backend_tk import (NavigationToolbar2Tk)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    boilerplate text
    @param plot_axes
    @param plot_canvas
    @param xlabel
    @param ylabel
    """

    times = [t / 7 for t in range(200)]
    rando = random() * 2 * math.pi - math.pi
    boing = [-math.sin(t + rando) * math.exp(-(t + rando) / 11) for t in times]

    # Draw the plot
    plot_axes.plot(times, boing)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def plot_RC_data(plot_axes, plot_canvas, xlabel, ylabel):

    times = []
    voltages = []   

    ser = serial.Serial('COM6', 115200, timeout=1) # this will not work on unix

    try:
        while True:
            line = ser.readline()
            
            if not line:
                break
    finally:
        ser.close()


    # Draw the plot
    plot_axes.plot(times, voltages)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def plot_RC_response(plot_axes, plot_canvas, xlabel, ylabel):

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
    text
    @param plot_function
    @param xlabel
    @param ylabel
    @param title
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
    
    tk_matplot(plot_RC_response,
               xlabel="Time [ms]",
               ylabel="Voltage [V]",
               title="title")