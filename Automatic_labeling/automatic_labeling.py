#! /usr/bin/python3
import json
import glob
from modules.extract_json import ExtractJSON
from modules.extract_action import ExtractAction
from modules.create_metadata import CreateMetadata

def create_filename(path:str) -> str:
    return "../data/Annotation/" + path.split("/")[-1][:-3] + "json"

def save_json_file(path:str, js:dict) -> None:
    with open(create_filename(path), "w") as f:
        f.write(json.dumps(js))
        f.close()
    print("JSON file has just been saved!")

def main() -> None:
    via_json:str = "./via.json"
    js = json.loads(
        ExtractJSON.get_json(
            via_json
        )
    )
    action_files:list = glob.glob("../data/Actions/*.txt")
    for file in action_files:
        ex_action:ExtractAction = ExtractAction(
            file
        )
        time:int = ex_action.get_time()
        action:list = ex_action.get_action_vector()
        js["metadata"] = CreateMetadata.create(action, time, left_size = 2000, right_size = 2000)
        save_json_file(file, js)

if __name__ == "__main__":
    main()