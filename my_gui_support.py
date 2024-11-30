#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#    Nov 29, 2024 11:27:36 PM +07  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import my_gui

_debug = True # False to eliminate debug printing from callback functions.

def main(*args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = my_gui.Toplevel1(_top1)
    root.mainloop()

if __name__ == '__main__':
    my_gui.start_up()




