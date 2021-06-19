import glob

csv:list = []

for folder in glob.glob("../data/VIDEO/*"):
    for file in glob.glob(folder + "/*.csv"):
        csv.append(file)

columns:bool = True
with open("framing_action.csv", "w") as f:
    for fcsv in csv:
        with open(fcsv, "r") as fc:
            if columns:
                f.writelines(fc.readlines())
                columns = False
            fc.readline()
            f.writelines(fc.readlines())
        