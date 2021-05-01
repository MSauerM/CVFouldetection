from InputGUI.GUIMain import start_GUI
import struct

if __name__ == '__main__':
    print("Start dialog")
    print (struct.calcsize("P")*8)
    start_GUI()