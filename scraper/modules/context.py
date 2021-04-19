from typing import List
from modules.state import State
from modules.select_coordinates import SelectCoordinates
from modules.select_via_file import SelectViaFile
from modules.create_json import CreateJSON

class Context:
    _state:State
    _i:int = 0

    def __init__(self) -> None:
        self._state = SelectCoordinates()
    
    def info(self) -> None:
        self._state.info()
    
    def select(self) -> any:
        f = self._state.select()
        self.__change_state()
        return f
    
    def create_JSON(self, file:list) -> any:
        return self._state.create_JSON(file)

    def __change_state(self) -> None:
        if self._i == 0:
            self._state = SelectViaFile()
        elif self._i == 1:
            self._state = CreateJSON()
        self._i += 1