import win32gui
import win32api
from tkinter import *



def checkered(canvas, line_distance,width,height):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,width,line_distance):
      canvas.create_line(x, 0, x, height, fill="#476042")
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,height,line_distance):
      canvas.create_line(0, y, width, y, fill="#476042")






def main():
    hwnd = win32gui.FindWindow(None, "Path Of Exile")

    rect = win32gui.GetWindowRect(hwnd)

    win32api.SetCursorPos((rect[2],rect[0]))

    x = rect[0]
    y = rect[1]
    width = rect[2] - x
    height = rect[3] - y


    print(hwnd)
    print(rect)

    #########################################################################

    # declare the window
    root = Tk()
    root.title("Python GUI App")
    root.geometry("+{0}+{1}".format(x,y))
    # root.attributes("-alpha", 1)

    canvas = Canvas(root,width=width,height=height)




    
    canvas.pack()

    checkered(canvas,width,height,10)


    root.mainloop()
    # set root background color

    # root.wm_attributes("-disabled", True)



main()