import glob
from modules.extract_video_duration import ExtractVideoDuration

def main():
    videos:list = glob.glob("../data/Video/*.mp4")
    times:list = []
    for video in videos:
        video_duration:int = ExtractVideoDuration.get_duration(video)
        times.append(video_duration)
    print(times)
if __name__ == "__main__":
    main()
