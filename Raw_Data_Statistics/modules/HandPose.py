from io import FileIO

class HandPose:

    _hand_pose:list = []
    _start_time:int = 0

    def __init__(self, path:str) -> None:
        try:
            self.__extract_hand_pose(open(path, "r"))
        except ValueError:
            print("ERROR: file not found.")
            exit(-1)
    
    def _get_millis(self, timestamp:str) -> int:
        hours, minutes, seconds, millis = [(int(elem)) for elem in timestamp.split("-")]
        return (hours * 3600 + minutes * 60 + seconds) * 1000 + millis
    
    def __extract_hand_pose(self, file_pose:FileIO) -> None:
        self._start_time = self._get_millis(file_pose.readline())
        self._hand_pose = [(pose) for pose in file_pose]
    
    def print_hand_pose(self, num:int) -> None:
        index:int = 0
        while index < num:
            print(self._hand_pose[num])
            index += 1
            
    def get_start_time(self) -> int:
        return self._start_time
    
    def get_hand_pose_dict(self) -> dict:
        d = {}
        for pose in self._hand_pose:
            timestamp, hand, other = pose.replace(",", ".").split()
            key:str = str(self._get_millis(timestamp) - self._start_time)
            joint_info:list = other.split("_")
            if key not in d:
                d[key] = {
                    hand + "_" + joint_info[0]: [
                        float(joint_info[2]),
                        float(joint_info[4]),
                        float(joint_info[6])
                    ]
                }
            else:
                d[key][hand + "_" + joint_info[0]] = [
                    float(joint_info[2]),
                    float(joint_info[4]),
                    float(joint_info[6])
                ]
        return d