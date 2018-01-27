import os
import re


def sort_key(word1):
            return word1.word


class Word:
    def __init__(self, word, file_id, intens):
        self.word = word
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
        pattern = re.compile(r'\w+')
        for fileInfo in result_list:
            with open(direction + "\\" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                res_text = pattern.findall(text)
                for word in res_text:
                    if len(word) < 2:
                        continue
                    all_words.append(Word(word, file_id, 1))
            file_id += 1
        all_words.sort(key=sort_key)
        for r_word in all_words:
            if r_word.word not in self.invertIndex.keys():
                self.invertIndex[r_word.word] = [r_word.intens, r_word.file_id]
            else:
                self.invertIndex[r_word.word][0] += 1
                if r_word.file_id in self.invertIndex[r_word.word]:
                    continue
                else:
                    self.invertIndex[r_word.word].append(r_word.file_id)

    def search(self, answer):
        pattern = re.compile(r'\w+')
        answer_splited = pattern.findall(answer)
        


myDict = Dictionary("D:\codd\PythonWorkspace\Information-Retrieval\Files")
print("Enter your answer. To stop this session enter \"stop\"")
text_input = input()
while text_input != "stop":
    myDict.search(text_input)
    text_input = input()
