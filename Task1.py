import os
import re


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        self.resultDictionary = []
        result_list = os.listdir(direction)
        pattern = re.compile(r'\w+')
        with open(direction + "\\ResultDictionary.txt", 'w') as resultFile:
            for fileInfo in result_list:
                with open(direction + "\\" + fileInfo, 'r') as auxFile:
                    text = auxFile.read().lower()
                    res_text = pattern.findall(text)
                    for word in res_text:
                        if len(word) < 2:
                            continue
                        if word in self.resultDictionary:
                            continue
                        self.resultDictionary.append(word)
                        self.wordsNumber += 1
                        resultFile.write(word + "\n")
                print("done")


myDict = Dictionary("D:\codd\PythonWorkspace\Information-Retrieval\Files")
print(myDict.wordsNumber)
