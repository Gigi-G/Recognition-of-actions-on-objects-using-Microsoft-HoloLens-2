#! /usr/bin/python3
from modules.context import Context

def main() -> None:
    context:Context = Context()
    i:int = 0
    file:list = []
    while(i < 2):
        context.info()
        file.append(context.select())
        i += 1
    context.create_JSON(file)

if __name__ == "__main__":
    main()