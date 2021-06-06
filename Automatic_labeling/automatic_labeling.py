#! /usr/bin/python3
import json
from modules.extract_json import ExtractJSON
from modules.extract_action import ExtractAction
from modules.create_metadata import CreateMetadata
import glob

def create_filename(path:str) -> str:
    return "../data/Annotation/" + path.split("/")[-1][:-3] + "json"

def save_json_file(path:str, js:dict) -> None:
    with open(create_filename(path), "w") as f:
        f.write(json.dumps(js))
        f.close()
    print("JSON file has just been saved!")

def metadata_list(js:dict) -> list:
    annotations:list = []
    for key, value in js["metadata"].items():
        annotations.append([key, value["z"]])
    return annotations

def print_metadata_element(annotations:list) -> None:
    print("Select the line that you want to modify:")
    index:int = 0
    for val in annotations:
        print(str(index) + ": " + str(val))
        index += 1

def modify_specific_part(via_json:str, js:dict) -> None:
    annotations:list = metadata_list(js)
    inp:str = ""
    while True:
        print_metadata_element(annotations)
        print("Write 'quit' or 'q' to exit.")
        inp = input()
        if inp == "quit" or inp == "q":
            save_json_file(via_json, js)
            break
        print("Insert left window value:")
        left:float = float(input())
        print("Insert right window value:")
        right:float = float(input())
        CreateMetadata.modify_specific_key(js["metadata"], annotations[int(inp)][0], left, right)

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
        #modify_specific_part(via_json, js)


if __name__ == "__main__":
    main()