from modules.extract_video_duration import ExtractVideoDuration
from modules.hand_pose import HandPose
import glob
import json
import pandas as pd
from modules.target import Target
import copy

class JointsDataFrame():

    def __init__(self) -> None:
        self.__index_data:int = 0
        self.__hand_joints:dict = []
        self.__hand_joint_names:list = []
        self.__load_data()
        self.__load_hand_joints()

    def __load_data(self) -> None:
        folders:list = glob.glob("../data/VIDEO/*")
        self.__video_in_folder:list = []
        self.__annotations:list = []
        self.__hand_poses:list = []
        for folder in folders:
            self.__video_in_folder.append(glob.glob(folder + "/*.mp4"))
            self.__annotations.append(glob.glob(folder + "/*.json"))
            self.__hand_poses.append(glob.glob(folder + "/*_handPose3D.txt"))
        #for folder in folders:
        #    for annotation in glob.glob(folder + "/*.json"):
        #        self.__annotations.append(annotation)
        #    for action in glob.glob(folder + "/*_action.txt"):
        #        self.__hand_poses.append(action)
        #    for hand_poses in glob.glob(folder + "/*_handPose3D.txt"):
        #        self.__hand_poses.append(hand_poses)

    def __load_hand_joints(self) -> None:
        with open("./hand_joints.json") as f:
            self.__hand_joints = json.load(f)
            self.__hand_joint_names = self.__hand_joints.keys()
            f.close()  

    def __win_size(self) -> float:
        frame_rate:int = 30
        return 1000/frame_rate

    def __create_records(self, video_duration:int, start_tim:int, hand_pose_dict:dict, data:dict, target:dict) -> None:
        while video_duration > 0:
            index:int = 0
            for key in data:
                if key == "TARGET":
                    data[key].append("No_action")
                else:
                    data[key].append(0)
            video_duration -= self.__win_size()
            find_time:bool = False
            while index < (self.__win_size() if video_duration >=0 else self.__win_size() + video_duration):
                if str(start_tim) in hand_pose_dict:
                    find_time = True
                    for key, val in hand_pose_dict[str(start_tim)].items():
                        data[key][self.__index_data] = val
                        #data["TIME"][self.__index_data] = start_tim
                start_tim += 1
                index += 1
            for _, val in target.items():
                if val["time"][0] <= start_tim <= val["time"][1]:
                    if find_time:
                        data["TARGET"][self.__index_data] = val["action"]
                    else:
                        for key in data:
                            data[key] = data[key][:-1]
                        self.__index_data -= 1
                        break
            self.__index_data += 1

    def get_dataframe(self) -> pd.DataFrame:
        records = copy.deepcopy(self.__hand_joints)
        for videos in self.__video_in_folder:
            for video in videos:
                print(video[:-10] + "_handPose3D.txt")
                print(video[:-10] + "_action.json")
                video_duration:int = ExtractVideoDuration.get_duration(video)
                hand_pose:HandPose = HandPose(video[:-10] + "_handPose3D.txt")
                self.__create_records(
                    video_duration,
                    hand_pose.get_start_time(),
                    hand_pose.get_hand_pose_dict(),
                    records,
                    Target.get(video[:-10] + "_action.json", hand_pose.get_start_time())
                )
        return pd.DataFrame(records, columns=self.__hand_joint_names)