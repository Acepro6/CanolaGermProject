import tkinter as tk
from Views.MainView import MainView
from Model.Model import Model
from Controller.Controller import Controller

def main():
    # Initialize Tk Window
    root = tk.Tk()
    root.title("Canola Germ Project")
    root.geometry('800x600')
    model = Model()
    controller = Controller(model)
    app = MainView(root, controller)
    root.mainloop()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()