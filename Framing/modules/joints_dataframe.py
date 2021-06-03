from modules.extract_video_duration import ExtractVideoDuration
from modules.hand_pose import HandPose
import glob
import json
import pandas as pd

class JointsDataFrame():

    def __init__(self) -> None:
        self.__hand_joints:dict = []
        self.__hand_joint_names:list = []
        self.__load_data()
        self.__load_hand_joints()

    def __load_data(self) -> None:
        self.__videos:list = glob.glob("../data/Video/*.mp4")
        self.__annotations:list = glob.glob("../data/Annotation/*.json")
        self.__hand_poses:list = glob.glob("../data/HandPoses/*.txt")
        self.__actions:list = glob.glob("../data/Actions/*.txt")

    def __load_hand_joints(self) -> None:
        with open("./hand_joints.json") as f:
            self.__hand_joints = json.load(f)
            self.__hand_joint_names = self.__hand_joints.keys()
            f.close()  

    def __win_size(self) -> float:
        frame_rate:int = 30
        return 1000/frame_rate

    def __create_records(self, video_duration:int, start_tim:int, hand_pose_dict:dict, data:dict) -> None:
        index_data:int = 0
        while video_duration > 0:
            index:int = 0
            for key in data:
                data[key].append(0)
            video_duration -= self.__win_size()
            while index < (self.__win_size() if video_duration >=0 else self.__win_size() + video_duration):
                if str(start_tim) in hand_pose_dict:
                    for key, val in hand_pose_dict[str(start_tim)].items():
                        data[key][index_data] = val
                start_tim += 1
                index += 1
            index_data += 1

    def get_dataframe(self) -> pd.DataFrame:
        for video in self.__videos:
            video_duration:int = ExtractVideoDuration.get_duration(video)
            hand_pose:HandPose = HandPose(self.__hand_poses[self.__videos.index(video)])
            data = self.__hand_joints.copy()
            self.__create_records(
                video_duration,
                hand_pose.get_start_time(),
                hand_pose.get_hand_pose_dict(),
                data
            )
            return pd.DataFrame(data, columns=self.__hand_joint_names)