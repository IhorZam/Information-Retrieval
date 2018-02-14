import os
import re
import sys


def sort_key(word1):
    return word1.word


class Word:
    def __init__(self, word, file_id):
        self.word = word
        self.file_id = file_id


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        file_id = 0
        self.res_file_counter = 0
        result_list = os.listdir(direction + "/Files")
        self.files_dict = {}
        self.all_words_obj = []
        self.all_words = []
        self.invertIndex = {}
        pattern = re.compile(r'\w+[\'\-]?\w+')
        for fileInfo in result_list:
            self.files_dict[file_id] = fileInfo
            with open(direction + "/Files/" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                text = pattern.findall(text)
                for word in text:
                    self.all_words_obj.append(Word(word, file_id))
                    self.all_words.append(word)
                    inv_size = sys.getsizeof(self.all_words_obj)
                    if inv_size > 2000000000:
                        self.write_info()
                file_id += 1
        self.write_info()

    def write_info(self):
        with open(self.direction + "/Files_res/File_result" + str(self.res_file_counter) + ".txt", 'w') as res:
            self.add_to_invert(self.all_words_obj)
            self.all_words = list(set(self.all_words))
            self.all_words.sort()
            for key in self.all_words:
                res_word = key
                for fileId in self.invertIndex[key]:
                    try:
                        res_word += " " + self.files_dict[fileId]
                    except KeyError:
                        continue
                res_word += "\n"
                res.write(res_word)
            self.all_words = []
            self.res_file_counter += 1

    def add_to_invert(self, all_words):
        for r_word in all_words:
            if r_word.word not in self.invertIndex.keys():
                self.invertIndex[r_word.word] = [0, r_word.file_id]
            else:
                self.invertIndex[r_word.word][0] += 1
                if r_word.file_id in self.invertIndex[r_word.word]:
                    continue
                else:
                    self.invertIndex[r_word.word].append(r_word.file_id)


myDict = Dictionary("/home/ihorzam/Dropbox/PythonWorkspace/Information-Retrieval")
print("Ready")
