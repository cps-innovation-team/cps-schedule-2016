import json



def main():
    with open("/Users/msa/Desktop/Normal.txt") as oldFile, open("/Users/msa/Desktop/Corona.txt") as newFile, open("/Users/msa/Desktop/Output.txt", "w") as outFile:
        oldRaw = oldFile.readlines()[0]
        newRaw = newFile.readlines()[0]
        old = json.loads(oldRaw)
        new = json.loads(newRaw)
        result = old
        for (key, value) in new.iteritems():
            result[key] = value
        outFile.write(json.dumps(result))

main()
