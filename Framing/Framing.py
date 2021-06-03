from modules.joints_dataframe import JointsDataFrame

def main() -> None:
    dataframe:JointsDataFrame = JointsDataFrame()
    dataframe.get_dataframe().to_csv("./framing_action.csv", index=False)

if __name__ == "__main__":
    main()