import os


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        self.resultDictionary = []
        result_list = os.listdir(direction)
        with open(direction + "\\ResultDictionary.txt", 'w') as resultFile:
            for fileInfo in result_list:
                with open(direction + "\\" + fileInfo, 'r') as auxFile:
                    text = auxFile.readline()
                    while text != "":
                        res_text = text.split(" ")
                        for word in res_text:
                            word = word.strip()
                            if word in self.resultDictionary:
                                continue
                            self.resultDictionary.append(word)
                            self.wordsNumber += 1
                            resultFile.write(word + "\n")
                        text = auxFile.readline()


myDict = Dictionary("D:\codd\PythonWorkspace\Information Retrieval\Files")
print(myDict.wordsNumber)
