from io import FileIO

class ExtractAction:
    
    _action_file:FileIO

    def __init__(self, path:str) -> None:
        try:
            self._action_file = open(path, "r")
        except ValueError:
            print("ERROR: file not found.")
            exit(-1)
        return None

    def get_time(self) -> int:
        hours, minutes, seconds, millis = [(int(elem)) for elem in self._action_file.readline().split("-")]
        return (hours * 60 + minutes * 60 + seconds)*1000 + millis
    
    def get_action_vector(self) -> list:
        return [(act) for act in self._action_file]