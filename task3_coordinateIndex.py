import os
import re


def sort_key(word1):
    return word1.word


class Word:
    def __init__(self, word, file_id, index):
        self.word = word
        self.file_index = index
        self.file_id = file_id


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        file_id = 0
        result_list = os.listdir(direction)
        self.files_dict = {}
        all_words = []
        self.invertIndex = {}
        pattern = re.compile(r'\w+[\'\-]?\w+')
        for fileInfo in result_list:
            word_counter = 0
            self.files_dict[file_id] = fileInfo
            with open(direction + "/" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                text = pattern.findall(text)
                for word in text:
                    all_words.append(Word(word, file_id, word_counter))
                    word_counter += 1
            file_id += 1
            all_words.sort(key=sort_key)
            self.add_to_invert(all_words)
            all_words = []

    def add_to_invert(self, all_words):
        for r_word in all_words:
            is_in = False
            if r_word.word not in self.invertIndex.keys():
                self.wordsNumber += 1
                self.invertIndex[r_word.word] = [1, [r_word.file_id, r_word.file_index]]
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
