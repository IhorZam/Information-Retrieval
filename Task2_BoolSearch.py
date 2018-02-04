import os
import re


def sort_key(word1):
            return word1.word


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


class Word:
    def __init__(self, word, file_id, intens):
        self.word = word
        self.file_id = file_id
        self.intens = intens


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        self.wordsNumber = 0
        self.files_dict = {}
        file_id = 0
        result_list = os.listdir(direction)
        all_words = []
        self.invertIndex = {}
        pattern = re.compile(r'\w+')
        for fileInfo in result_list:
            self.files_dict[file_id] = fileInfo
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
        polish_write = []
        operator_stack = Stack()
        answer = answer.split(" ")
        for word in answer:
            if word == "AND":
                operator_stack.push("AND")
            elif word == "OR":
                if not operator_stack.is_empty():
                    if operator_stack.peek() == "AND":
                        polish_write.append("AND")
                        operator_stack.pop()
                operator_stack.push("OR")
            elif word == "AND" and answer.next() == "NOT":
                operator_stack.push("AND NOT")
            elif word == '(':
                operator_stack.push('(')
            elif word == ')':
                operator = operator_stack.pop()
                polish_write.append(operator)
                operator_stack.pop()
            else:
                polish_write.append(word)
        while not operator_stack.is_empty():
            operator = operator_stack.pop()
            polish_write.append(operator)

        result_lists = {}
        z = 0
        name = ""
        for i in range(len(polish_write) + 1):
            i = z
            if polish_write[i] == "OR":
                try:
                    first_list = self.invertIndex[polish_write[i - 2]]
                    first_list.pop(0)
                except KeyError:
                    try:
                        first_list = result_lists[polish_write[i-2]]
                        result_lists.pop(polish_write[i-2])
                    except KeyError:
                        print("No such word: " + polish_write[i-2])
                        return
                try:
                    second_list = self.invertIndex[polish_write[i - 1]]
                    second_list.pop(0)
                except KeyError:
                    try:
                        second_list = result_lists[polish_write[i-1]]
                        result_lists.pop(polish_write[i-1])
                    except KeyError:
                        print("No such word: " + polish_write[i-1])
                        return
                name = polish_write[i - 2] + "OR" + polish_write[i - 1]
                polish_write.remove(polish_write[i-2])
                polish_write.remove(polish_write[i-2])
                polish_write.remove(polish_write[i-2])
                result_lists[name] = self.OR(first_list, second_list)
                polish_write.insert(i-2, name)
                z = i - 2
            elif polish_write[i] == "AND":
                try:
                    first_list = self.invertIndex[polish_write[i - 2]]
                    first_list.pop(0)
                except KeyError:
                    try:
                        first_list = result_lists[polish_write[i-2]]
                        result_lists.pop(polish_write[i-2])
                    except KeyError:
                        print("No such word: " + polish_write[i-2])
                        return
                try:
                    second_list = self.invertIndex[polish_write[i - 1]]
                    second_list.pop(0)
                except KeyError:
                    try:
                        second_list = result_lists[polish_write[i-1]]
                        result_lists.pop(polish_write[i-1])
                    except KeyError:
                        print("No such word: " + polish_write[i-1])
                        return
                name = polish_write[i - 2] + "AND" + polish_write[i - 1]
                polish_write.remove(polish_write[i-2])
                polish_write.remove(polish_write[i-2])
                polish_write.remove(polish_write[i-2])
                result_lists[name] = self.AND(first_list, second_list)
                polish_write.insert(i-2, name)
                z = i - 2
            elif polish_write[i] == "AND NOT":
                try:
                    first_list = self.invertIndex[polish_write[i - 2]]
                    first_list.pop(0)
                except KeyError:
                    try:
                        first_list = result_lists[polish_write[i-2]]
                        result_lists.pop(polish_write[i-2])
                    except KeyError:
                        print("No such word: " + polish_write[i-2])
                        return
                try:
                    second_list = self.invertIndex[polish_write[i - 1]]
                    second_list.pop(0)
                except KeyError:
                    try:
                        second_list = result_lists[polish_write[i-1]]
                        result_lists.pop(polish_write[i-1])
                    except KeyError:
                        print("No such word: " + polish_write[i-1])
                        return
                name = polish_write[i - 2] + "ANDNOT" + polish_write[i - 1]
                polish_write.remove(polish_write[i-2])
                polish_write.remove(polish_write[i-2])
                polish_write.remove(polish_write[i-2])
                result_lists[name] = self.ANDNOT(first_list, second_list)
                polish_write.insert(i-2, name)
                z = i - 2
            else:
                z = i + 1
        files_res = []
        for nm in result_lists[name]:
            files_res.append(self.files_dict[nm])
        return files_res

    def AND(self, files1, files2):
        res_list = []
        i = 0
        j = 0
        while i < len(files1) and j < len(files2):
            if files1[i] == files2[i]:
                res_list.append(files1[i])
                i += 1
                j += 1
            elif files1[i] < files2[i]:
                i += 1
            else:
                j += 2
        return res_list

    def OR(self, first_list, second_list):
        res_list = []
        for el in first_list:
            res_list.append(el)
        for el in second_list:
            if el not in res_list:
                res_list.append(el)
        return res_list

    def ANDNOT(self, first_list, second_list):
        for el in second_list:
            if el in first_list:
                first_list.remove(el)
        return first_list


myDict = Dictionary("D:\codd\PythonWorkspace\Information-Retrieval\Files")
print("Enter your question. To stop this session enter \"stop\"")
text_input = input()
while text_input != "stop":
    print(myDict.search(text_input))
    text_input = input()
