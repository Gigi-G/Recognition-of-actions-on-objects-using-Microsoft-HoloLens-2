from tkinter import Tk
from tkinter.filedialog import askopenfilename

class SelectFile:

    @staticmethod
    def get_path() -> str:
        """
        Returns the path of the selected file
        """
        Tk().withdraw()
        return askopenfilename()
        