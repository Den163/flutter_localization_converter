import argparse
import os.path
import xml.dom.minidom as minidom
import json
import getopt
import re
from collections import OrderedDict

from typing import List, Dict, Tuple, AnyStr

def log(s) : 
    print(s)

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transforms android xml localization file to flutter arb")
    parser.add_argument(
        "fileNames", 
        help="Names of files that you want to convert from xml to json (Can be substrings of file names)",
        nargs="+")
    parser.add_argument(
        "-o",
        help="Optional output file name",
        dest='o'
    )
    parser.add_argument(
        "-v",
        action="store_true",
        help="Prints verbose info about parsing process",
        dest='v'
    )

    args = parser.parse_args()
    if not args.v: 
        global log 
        log = lambda f: None
    outputName: str = args.o or "strings.json"
    strings = {}

    filesToUse: List[str] = findFiles(args.fileNames)

    for name in filesToUse: 
        checkFilename(name)

    for name in filesToUse:
        log(f"Trying parse `{name}`")
        parsedStrings = parseXmlFile(name)
        
        if len(parsedStrings.keys()) == 0: continue
        fixCollisions(strings, parsedStrings)
        strings.update(parsedStrings)

    log("Parsing is successful. Convert to json")

    strings = OrderedDict(sorted(strings.items(), key=lambda t: t[0]))
    jsonString = json.dumps(strings, ensure_ascii=False, indent=4)

    fileToWrite = open(outputName, "w", encoding='utf-8')
    fileToWrite.write(jsonString)



def findFiles(fileNames: List[str]) -> List[str]:
    matchedFiles: List[str] = []
    walker = os.walk(os.getcwd())

    for (path, dir, file) in walker:
        for file in file:
            if ('.xml' in file) == False: continue

            for name in fileNames:
                if name in file:
                    matchedFiles.append(os.path.join(path, file))
                    break # go to next file

    return matchedFiles

def checkFilename(name: str) -> None: 
    if os.path.isfile(name) == False: 
        print(f"Exit with error. `{name}` doesn't exist")
        exit(1)
    if ("xml" in name) == False: 
        print(f"Exit with error. `{name}` is not a xml file")
        exit(1)

def parseXmlFile(fileName: str) -> Dict[str, str]:
    values: Dict[str, str] = {}

    try:
        dom = minidom.parse(fileName)
        stringsElements = dom.getElementsByTagName("string") 

        for element in stringsElements :
            key = element.getAttribute("name")
            value = element.firstChild.data
            values[key] = fixValue(value)

    except Exception:
        log(f"`{fileName}` is empty or format is incorrect. Skip it")
        
    return values

def fixValue(value: str) -> str:
    newValue: str = re.sub(r"%(([0-9]\$)?)s", r"$s\1", value).replace("//n", "/n")
    if value != newValue: log(f"Fixed value from `{value}` to `{newValue}`")
    return newValue

def fixCollisions(leftDict: Dict[str, str], rigthDict: Dict[str, str]):
    keyValuePair: Tuple[str, str] = leftDict.items()

    for (k, v) in keyValuePair:
        if rigthDict.__contains__(k):
            oldValue = rigthDict.pop(k)
            newKey = k + '_'
            rigthDict[newKey] = oldValue
            log(f"Collision with key `{k}`. Fixing it to `{newKey}`")

# Main program

main()