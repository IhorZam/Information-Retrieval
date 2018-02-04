import os
import re


def sort_key(word1):
    return word1.word


class Word:
    def __init__(self, word, file_id, intens,index):
        self.word = word
        self.file_index = index
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
            word_counter = 0
            with open(direction + "/" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                text = pattern.findall(text)
                for word in text:
                    all_words.append(Word(word, file_id, 1, word_counter))
                    word_counter += 1
            file_id += 1
        all_words.sort(key=sort_key)
        is_in = False
        for r_word in all_words:
            if r_word.word not in self.invertIndex.keys():
                self.invertIndex[r_word.word] = [r_word.intens, [r_word.file_id, r_word.file_index]]
            else:
                self.invertIndex[r_word.word][0] += 1
                for i in range(len(self.invertIndex[r_word.word])):
                    if i == 0:
                        continue
                    else:
                        if self.invertIndex[r_word.word][i][0] == r_word.file_id:
                            self.invertIndex[r_word.word][i].append(r_word.file_index)
                            is_in = True
                            break
            if not is_in:
                self.invertIndex[r_word.word].append([r_word.file_id, r_word.file_index])


myDict = Dictionary("/home/ihorzam/Dropbox/PythonWorkspace/Information-Retrieval/Files")
print(myDict.wordsNumber)
