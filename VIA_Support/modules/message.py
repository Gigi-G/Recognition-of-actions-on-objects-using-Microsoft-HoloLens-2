from tkinter import Tk
from tkinter import messagebox

class Message:

    @staticmethod
    def Mbox(title:str, text:str) -> any:
        """
        Returns a message box

        Parameters:
            title (str): title of the message
            text (str): text of the message
        """
        Tk().withdraw()
        messagebox.showinfo(title, text)