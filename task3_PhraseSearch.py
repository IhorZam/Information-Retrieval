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

    def search(self, phrase):
        phrase = phrase.split(" ")
        operators = []
        files_lists = {}
        for word in phrase:
            if word[0] != '/':
                for i in range(len(self.invertIndex[word])):
                    if i == 0:
                        continue
                    aux_list = self.invertIndex[word][i]
                    key_ind = self.invertIndex[word][i][0]
                    aux_list.pop(0)
                    if key_ind not in files_lists.keys():
                        files_lists[key_ind] = [aux_list]
                    else:
                        files_lists[key_ind].append(aux_list)
            else:
                operators.append(int(word[1:]))
        files_result_list = []
        for key in files_lists.keys():
            if not len(files_lists[key]) < len(phrase) // 2 + 1:
                list_for_check = files_lists[key]
                normal_file = False
                for i in range(len(list_for_check)):
                    if i + 1 > len(list_for_check) - 1:
                        break
                    normal_file = self.check_lists(list_for_check[i], list_for_check[i + 1], operators[i])
                if normal_file:
                    files_result_list.append(self.files_dict[key])
        return files_result_list

    def check_lists(self, list1, list2, move):
        i = 0
        j = 0
        while i < len(list1) and j < len(list2):
            if list1[i] + 1 + move == list2[j]:
                return True
            elif list1[i] > list2[j]:
                j += 1
            else:
                i += 1




myDict = Dictionary("/home/ihorzam/Dropbox/PythonWorkspace/Information-Retrieval/Files")
print(myDict.search("voice /1 squeakily"))