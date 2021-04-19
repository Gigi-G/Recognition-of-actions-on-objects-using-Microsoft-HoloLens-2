from modules.state import State

class CreateJSON(State):

    def info(self) -> None:
        pass
    
    def select(self) -> any:
        return None
    
    def create_JSON(self, file:list) -> any:
        via_list:list = self.__file_to_list(file[1], [0, 1])
        return self.__file_to_json(file[0], via_list)
    
    def __file_to_list(self, file, not_to_read:list = []) -> list:
        l:list = []
        for position, line in enumerate(file):
            if position not in not_to_read:
                l.append(line)
        return l
    
    def __file_to_json(self, file, action_list:list) -> any:
        i:int = -1
        start:int = 1
        end:int = 1
        hours:int = 0
        minutes:int = 0
        seconds:int = 0
        other:int = 0
        time:int = 0
        hours_find:int = 0
        minutes_find:int = 0
        seconds_find:int = 0
        other_find:int = 0
        time_find:int = 0
        actions:list = []
        for line in file:
            if i == -1:
                hours, minutes, seconds, other = [(int(elem)) for elem in line.split("-")]
                time = (hours * 3600 + minutes * 60 + seconds)/1000 + other  
                #print(hours, minutes, seconds, other)
                i += 1
            else:
                if i < len(action_list):
                    if start and end:
                        actions = action_list[i].split(",")
                        #print(actions)
                        sec, oth = [(int(elem)) for elem in actions[2].split(".")]
                        hours_find = 0 + hours
                        other_find = oth + other
                        seconds_find = sec + seconds
                        minutes_find = minutes
                        #print("START", hours_find, minutes_find, seconds_find, other_find)
                        time_find = (hours_find * 3600 + minutes_find * 60 + seconds_find)*1000 + other_find
                        start = 0
                    if start == 0 and end == 1:
                        h, m, s, o = [(int(elem)) for elem in line.split()[0].split("-")]
                        t = (h * 3600 + m * 60 + s)*1000 + o
                        if t >= time_find + 1500:
                            print("START", action_list[i].split(",")[4])
                            end = 0
                    if start == 0 and end == 0:
                        actions = action_list[i].split(",")
                        sec, oth = [(int(elem)) for elem in actions[3].split(".")]
                        hours_find = 0 + hours
                        other_find = oth + other
                        seconds_find = sec + seconds
                        minutes_find = minutes
                        #print("END", hours_find, minutes_find, seconds_find, other_find)
                        time_find = (hours_find * 3600 + minutes_find * 60 + seconds_find)*1000 + other_find
                        start = 1
                    if start == 1 and end == 0:
                        h, m, s, o = [(int(elem)) for elem in line.split()[0].split("-")]
                        t = (h * 3600 + m * 60 + s)*1000 + o
                        if t >= time_find + 1500:
                            print("END", action_list[i].split(",")[4])
                            end = 1
                            i += 1
                print(line)
        return "OK"


