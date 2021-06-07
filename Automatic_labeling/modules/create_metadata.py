class CreateMetadata:
    
    @staticmethod
    def create(action_vector:list, time:int, left_size:int = 0, right_size:int = 0) -> dict:
        met:dict = {}
        start_index:int = 10000000
        for elem in action_vector:
            key:str = "1_" + str(start_index)
            t, a = elem.split()
            hours, minutes, seconds, millis = [(int(el)) for el in t.split("-")]
            tim = ((hours * 60 + minutes * 60 + seconds)*1000 + millis) - time - left_size
            tim_f = tim + right_size
            met[key] = {
                "vid": 1,
                "flg": 0,
                "z": [tim/1000, tim_f/1000],
                "xy": [],
                "av": {
                    "1": a
                }
            }
            start_index += 1
        return met