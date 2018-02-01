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
        answer_res = answer.split(" ")
        if len(answer_res) == 1:
            try:
                return self.invertIndex[answer_res[0]]
            except KeyError:
                return ['No such word. Maybe, you wrote an uppercase letter']
        for word in answer_res:
            if word not in self.invertIndex.keys():
                return ['No such word. Maybe, you wrote an uppercase letter']
        for i in range(len(answer_res)):
            if answer_res[i] == 'AND':
                if answer_res[i + 1] == 'NOT':
                    list_aux = self.NOT(answer_res[i - 1].strip(), answer_res[i + 1].strip())
                    for z in range(3):
                        answer_res.remove(answer_res[i - 1])
                    answer_res.insert(i - 1, list_aux)
                else:
                    list_aux = self.AND(answer_res[i - 1].strip(), answer_res[i + 1].strip())
                    for z in range(3):
                        answer_res.remove(answer_res[i - 1])
                    answer_res.insert(i - 1, list_aux)
            elif answer_res[i] == 'OR':
                list_aux = self.OR(answer_res[i - 1].strip(), answer_res[i + 1].strip())
                for z in range(3):
                    answer_res.remove(answer_res[i - 1])
                answer_res.insert(i - 1, list_aux)
            if i + 1 > len(answer_res):
                break
        return answer_res[0]

    def AND(self, files1, files2):
        res_list = []
        i = 0
        j = 0
        if type(files1) is not 'list':
            i = 1
        if type(files2) is not 'list':
            files2 = self.invertIndex[files2]
            j = 1
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

    def OR(self, files1, files2):
        if type(files1) is not 'list':
            files1 = self.invertIndex[files1]
            files1.remove(0)
        if type(files2) is not 'list':
            files2 = self.invertIndex[files2]
            files2.remove(0)
        res_list = files1 + files2
        return res_list

    def NOT(self, files1, files2):
        res_list = []
        if type(files1) is not 'list':
            files1 = self.invertIndex[files1]
            files1.remove(0)
        if type(files2) is not 'list':
            files2 = self.invertIndex[files2]
            files2.remove(0)
        for id in files1:
            if id not in files2:
                res_list.append(id)
        return res_list


myDict = Dictionary("D:\codd\PythonWorkspace\Information-Retrieval\Files")
print("Enter your answer. To stop this session enter \"stop\"")
text_input = input()
while text_input != "stop":
    print(myDict.search(text_input))
    text_input = input()
