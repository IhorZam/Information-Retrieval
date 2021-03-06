import os
import re


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        file_id = 0
        result_list = os.listdir(direction)
        self.resultMatrix = []
        self.filesDict = {}
        self.wordsDict = {}
        pattern = re.compile(r'\w+')
        for fileInfo in result_list:
            with open(direction + "\\" + fileInfo, 'r') as auxFile:
                self.filesDict[file_id] = fileInfo
                text = auxFile.read().lower()
                res_text = pattern.findall(text)
                for word in res_text:
                    if word in self.wordsDict.keys():
                        small_id = self.wordsDict[word]
                        self.resultMatrix[small_id][file_id] = 1
                        continue
                    self.wordsDict[word] = self.wordsNumber
                    aux_list = [0 for i in range(len(result_list))]
                    aux_list[file_id] = 1
                    self.wordsNumber += 1
                    self.resultMatrix.append(aux_list)
            file_id += 1


myDict = Dictionary("D:\codd\PythonWorkspace\Information-Retrieval\Files")
print(myDict.wordsNumber)
