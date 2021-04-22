#! /usr/bin/python3
import json
from sys import path
from modules.select_file import SelectFile
from modules.extract_json import ExtractJSON
from modules.extract_action import ExtractAction
from modules.create_metadata import CreateMetadata

def save_json_file(path:str, js:dict) -> None:
    with open(path, "w") as f:
        f.write(json.dumps(js))
        f.close()
    print("JSON file has just been saved!")

def main() -> None:
    via_json = SelectFile.get_path("Insert the absolute path of the VIA JSON file:")
    js = json.loads(
        ExtractJSON.get_json(
            via_json
        )
    )
    ex_action:ExtractAction = ExtractAction(
        SelectFile.get_path("Insert the absolute path of the action file:")
    )
    time:int = ex_action.get_time()
    action:list = ex_action.get_action_vector()
    js["metadata"] = CreateMetadata.create(action, time, left_size = 2000, right_size = 1000)
    js["file"]["1"]["src"] = js["file"]["1"]["fname"] = SelectFile.get_path("Insert the absolute path of the video:")
    save_json_file(via_json, js)


if __name__ == "__main__":
    main()