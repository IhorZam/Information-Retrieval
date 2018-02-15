import os
import re
import sys


def sort_key(word1):
    return word1.word


class Dictionary:

    def __init__(self, direction):
        self.direction = direction
        file_id = 0
        self.res_file_counter = 0
        self.files_dict = {}
        self.all_words = []
        self.invertIndex = {}
        pattern = re.compile(r'\w+[\'\-]?\w+')
        for fileInfo in os.listdir(direction + "/FilesToWork"):
            self.files_dict[file_id] = fileInfo
            with open(direction + "/FilesToWork/" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                text = pattern.findall(text)
                for word in text:
                    self.add_word(word, file_id)
                    if len(self.all_words) > 5000:
                        self.write_info()
                file_id += 1
        self.write_info()
        self.merge_files()

    def add_word(self, word, file_id):
        if word not in self.invertIndex.keys():
            self.invertIndex[word] = [0, file_id]
            self.all_words.append(word)
        else:
            self.invertIndex[word][0] += 1
            if file_id not in self.invertIndex[word]:
                self.invertIndex[word].append(file_id)

    def merge_files(self):
        result_list = os.listdir(self.direction + "/ResFiles")
        self.res_file_counter = 0
        while len(result_list) != 1:
            res_file = self.merge(result_list[0], result_list[1])
            self.res_file_counter += 1
            os.remove(self.direction + "/ResFiles/" + result_list[0])
            os.remove(self.direction + "/ResFiles/" + result_list[1])
            result_list.pop(0)
            result_list.pop(0)
            result_list.insert(0, res_file)
        print(result_list[0])

    def merge(self, file1, file2):
        with open(self.direction + "/ResFiles/" + file1, 'r') as file_one:
            with open(self.direction + "/ResFiles/" + file2, 'r') as file_two:
                with open(self.direction + "/ResFiles/Result" + str(self.res_file_counter) + ".txt", 'w') as res:
                    aux_line1 = file_one.readline()
                    aux_line2 = file_two.readline()
                    while aux_line1 and aux_line2:
                        if type(aux_line1) is not list:
                            aux_line1 = aux_line1.split(" ")
                        if type(aux_line2) is not list:
                            aux_line2 = aux_line2.split(" ")
                        res_line = ""
                        if aux_line1[0] == aux_line2[0]:
                            res_line += aux_line1[0]
                            for el in list(set(aux_line1[1:]) | set(aux_line2[1:])):
                                res_line += " " + el.strip()
                            res_line += "\n"
                            res.write(res_line)
                            aux_line1 = file_one.readline()
                            aux_line2 = file_two.readline()
                        elif aux_line1[0] < aux_line2[0]:
                            res_line += aux_line1[0]
                            for el in aux_line1[1:]:
                                res_line += " " + el.strip()
                            res_line += "\n"
                            res.write(res_line)
                            aux_line1 = file_one.readline()
                        else:
                            res_line += aux_line2[0]
                            for el in aux_line2[1:]:
                                res_line += " " + el.strip()
                            res_line += "\n"
                            res.write(res_line)
                            aux_line2 = file_two.readline()
                    if aux_line1:
                        while aux_line1:
                            res_line = ""
                            if type(aux_line1) is not list:
                                aux_line1 = aux_line1.split(" ")
                            res_line += aux_line1[0]
                            for el in aux_line1[1:]:
                                res_line += " " + el.strip()
                            res_line += "\n"
                            res.write(res_line)
                            aux_line1 = file_one.readline()
                    if aux_line2:
                        while aux_line2:
                            res_line = ""
                            if type(aux_line2) is not list:
                                aux_line2 = aux_line2.split(" ")
                            res_line += aux_line2[0]
                            for el in aux_line2[1:]:
                                res_line += " " + el.strip()
                            res_line += "\n"
                            res.write(res_line)
                            aux_line2 = file_two.readline()
        return "Result" + str(self.res_file_counter) + ".txt"

    def write_info(self):
        with open(self.direction + "/ResFiles/File_result" + str(self.res_file_counter) + ".txt", 'w') as res:
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
            self.invertIndex = {}
            self.res_file_counter += 1


myDict = Dictionary("/home/ihorzam/Work/PythonFiles/")
print("Ready")
