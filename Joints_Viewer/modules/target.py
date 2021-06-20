from modules.extract_json import ExtractJSON
import json

class Target():

    @staticmethod
    def get(filename:str, start_tim:int) -> dict:
        js:dict = json.loads(
            ExtractJSON.get_json(
                filename
            )
        )
        metadata:dict = js["metadata"]
        result:dict = {}
        for key, value in metadata.items():
            result[key] = {
                "action": value["av"]["1"],#[:-2],
                "time": [int(value["z"][0] * 1000 + start_tim), int(value["z"][1] * 1000 + start_tim)] 
            }
        return result