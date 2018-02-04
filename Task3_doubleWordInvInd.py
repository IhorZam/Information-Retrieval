import os
import re


def sort_key(word1):
    return word1.double_word


class DoubleWord:
    def __init__(self, double_word, file_id, intens):
        self.double_word = double_word
        self.file_id = file_id
        self.intens = intens


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        file_id = 0
        result_list = os.listdir(direction)
        all_words = []
        self.invertIndex = {}
        pattern = re.compile(r'\w+[\'\-]?\w+')
        for fileInfo in result_list:
            with open(direction + "/" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                res_text = pattern.findall(text)
                for i in range(len(res_text)):
                    if i + 1 < len(res_text):
                        updated_word = res_text[i] + " " + res_text[i+1]
                        all_words.append(DoubleWord(updated_word, file_id, 1))
                    else:
                        all_words.append(DoubleWord(res_text[i], file_id, 1))
            file_id += 1
            all_words.sort(key=sort_key)
            self.add_to_invert(all_words)
            all_words = []

    def add_to_invert(self, all_words):
        for r_word in all_words:
            if r_word.double_word not in self.invertIndex.keys():
                self.wordsNumber += 1
                self.invertIndex[r_word.double_word] = [r_word.intens, r_word.file_id]
            else:
                self.invertIndex[r_word.double_word][0] += 1
                if r_word.file_id in self.invertIndex[r_word.double_word]:
                    continue
                else:
                    self.invertIndex[r_word.double_word].append(r_word.file_id)


myDict = Dictionary("/home/ihorzam/Dropbox/PythonWorkspace/Information-Retrieval/Files")
print(myDict.wordsNumber)
