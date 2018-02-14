import os
import re


def sort_key(word1):
    return word1.word


class Word:
    def __init__(self, word, file_id, index):
        self.word = word
        self.file_index = index
        self.file_id = file_id


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.insert(0, item)

    def pop(self):
        return self.items.pop(0)

    def peek(self):
        return self.items[0]

    def size(self):
        return len(self.items)


class Node:
    def __init__(self):
        self.alph = {}


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        file_id = 0
        result_list = os.listdir(direction)
        self.files_dict = {}
        all_words = []
        self.root = Node()
        self.root_per = Node()
        self.three_gram = {}
        self.per = {}
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
                    self.add_to_tree(word, False)
                    self.add_to_gram(word)
                    self.add_to_per(word)
                    word_counter += 1
            file_id += 1
            all_words.sort(key=sort_key)
            self.add_to_invert(all_words)
            all_words = []

    def add_to_invert(self, all_words):
        for r_word in all_words:
            is_in = False
            if r_word.word not in self.invertIndex:
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

    def add_to_tree(self, word, per):
        if per:
            aux = self.root_per
        else:
            aux = self.root
        for i in range(len(word)):
            char_ind = ord(word[i])
            if char_ind not in aux.alph.keys():
                aux.alph[char_ind] = Node()
            aux = aux.alph[char_ind]

    def add_to_per(self, word):
        self.per[word] = []
        aux_word = word + '$'
        self.per[word].append(aux_word)
        for i in range(len(word)):
            aux_word = aux_word[1:] + aux_word[0]
            self.add_to_tree(aux_word, True)
            self.per[word].append(aux_word)

    def add_to_gram(self, word):
        if len(word) > 3:
            aux_word = '$' + word + '$'
        else:
            aux_word = '$' + word
        for key in self.make_three_gram(aux_word):
            if key in self.three_gram.keys():
                if word not in self.three_gram[key]:
                    self.three_gram[key].append(word)
            else:
                self.three_gram[key] = [word]

    @staticmethod
    def make_three_gram(word):
        res_list = []
        for i in range(len(word)):
            if i + 2 > len(word) - 1:
                break
            else:
                key = word[i:i + 3]
                res_list.append(key)
        return res_list

    def get_words_from_gram(self, gram_list):
        res_list = []
        for gram in gram_list:
            for word in self.make_three_gram(gram):
                res_list.append(self.three_gram[word])
        for i in range(len(res_list)):
            if i + 1 > len(res_list) - 1:
                break
            aux_list = list(set(res_list[i]) & set(res_list[i + 1]))
            res_list.pop(i)
            res_list.pop(i)
            res_list.insert(i, aux_list)
        return res_list[0]

    def joker_search(self, search):
        if not search:
            print("No word entered!")
            return
        elif search[len(search) - 1] == '*' and search[0] == '*':
            search = search[1:len(search) - 1]
            answer = search
            return self.get_words_from_gram([answer])
        if search[len(search) - 1] == '*':
            search = search[:len(search) - 1]
            answer = '$' + search
            return self.get_words_from_gram([answer])
        elif search[0] == '*':
            search = search[1:]
            answer = search + '$'
            return self.get_words_from_gram([answer])
        else:
            answer = '$' + search + '$'
            answer = answer.split("*")
            return self.get_words_from_gram(answer)


myDict = Dictionary("/home/ihorzam/Dropbox/PythonWorkspace/Information-Retrieval/Files")
print("Enter your question. To stop this session enter \"stop\"")
text_input = input()
while text_input != "stop":
    print(myDict.joker_search(text_input))
    text_input = input()
print("Ready")