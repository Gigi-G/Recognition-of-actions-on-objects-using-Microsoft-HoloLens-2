from modules.state import State
from modules.select_file import SelectFile
from modules.message import Message

class SelectCoordinates(State):

    def info(self) -> None:
        Message.Mbox("Informazione", "Seleziona il file contenente le coordinate della mano.")

    def select(self) -> any:
        return open(SelectFile.get_path(), "r")
    
    def create_JSON(self, file:list) -> any:
        return None