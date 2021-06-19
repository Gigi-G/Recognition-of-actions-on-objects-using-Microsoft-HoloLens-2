from modules.joints_dataframe import JointsDataFrame

def main() -> None:
    dataframe:JointsDataFrame = JointsDataFrame()
    dataframe.get_dataframe()

if __name__ == "__main__":
    main()