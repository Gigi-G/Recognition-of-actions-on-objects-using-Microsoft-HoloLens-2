import moviepy.editor

class ExtractVideoDuration:

    @staticmethod
    def get_duration(path:str) -> int:
        try:
            return int(moviepy.editor.VideoFileClip(path).duration*1000)
        except ValueError:
            print("ERROR: file not found.")
            exit(-1)
        return None