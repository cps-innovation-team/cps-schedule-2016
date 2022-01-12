import json

def main():
    dir = "/Users/msa/Desktop/"
    with open(dir + "Corona.txt") as inFile, open(dir + "Corona data with manual override applied.txt", "w") as outFile:
        oldRaw = inFile.readlines()[0]
        old = json.loads(oldRaw)
        result = old

        mTemplate = result["27042020"]
        tTemplate = result["28042020"]
        wTemplate = result["29042020"]
        rTemplate = result["30042020"]
        fTemplate = result["01052020"]
        prefix = "052020"

        for x in ["04", "11", "18"]:
            result[x + prefix] = mTemplate
        for x in ["05", "12", "19"]:
            result[x + prefix] = tTemplate
        for x in ["06", "13", "20"]:
            result[x + prefix] = wTemplate
        for x in ["07", "14", "21"]:
            result[x + prefix] = rTemplate
        for x in ["08", "15", "22"]:
            result[x + prefix] = fTemplate
        outFile.write(json.dumps(result))


main()
        
