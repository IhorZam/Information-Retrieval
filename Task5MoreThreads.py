import os
import re
import threading
import queue
import time
start_time = time.time()


def sort_key(el):
    return int(el)


class ThreadForTenRead(threading.Thread):

    def __init__(self):
        self.all_words = []
        self.invertIndex = {}
        self.file_name = ""
        threading.Thread.__init__(self)

    def run(self):
        print("Thread " + self.getName() + " entered")
        while True:
            if clientPool.empty():
                if not len(self.all_words) == 0:
                    self.write_info()
                return
            self.file_name = clientPool.get()
            with open(self.file_name[0], 'r') as auxFile:
                text = auxFile.readline()
                while text:
                    text = pattern.findall(text.lower())
                    for word in text:
                        self.add_word(word, self.file_name[1])
                        if len(self.all_words) > 18000:
                            self.write_info()
                    text = auxFile.readline()
            print("File read. Thread: " + self.getName())

    def add_word(self, word, file_id):
        if word not in self.invertIndex.keys():
            self.invertIndex[word] = [1, file_id]
            self.all_words.append(word)
        else:
            self.invertIndex[word][0] += 1
            if file_id not in self.invertIndex[word]:
                self.invertIndex[word].append(file_id)

    def write_info(self):
        with open(direction + "/ResFiles/File_result" + str(hash(self.file_name[0])) + ".txt", 'w') as res:
            print(res.name)
            self.all_words = list(set(self.all_words))
            self.all_words.sort()
            for key in self.all_words:
                res_word = key + " " + str(self.invertIndex[key][0]) + "k"
                for fileId in self.invertIndex[key][1:]:
                    res_word += " " + str(fileId)
                res_word += "\n"
                res.write(res_word)
            self.all_words = []
            self.invertIndex = {}


class ThreadMerging(threading.Thread):

    def __init__(self):
        self.file_names = []
        threading.Thread.__init__(self)

    def run(self):
        print("Thread " + self.getName() + " entered")
        while True:
            if mergePool.empty():
                return
            self.file_names = mergePool.get()
            self.merge(self.file_names[0], self.file_names[1], self.file_names[2], self.file_names[3])

    def merge(self, file1, file2, fileRes, last):
        with open(direction + "/ResFiles/" + file1, 'r') as file_one:
            with open(direction + "/ResFiles/" + file2, 'r') as file_two:
                if last:
                    res = open(direction + "/Ready/LastResult", 'wb')
                    word_counter = 0
                else:
                    res = open(direction + "/ResFiles/" + fileRes, 'w')
                if last:
                    self.last_dict(file1, file2)
                aux_line1 = file_one.readline()
                aux_line2 = file_two.readline()
                while aux_line1 and aux_line2:
                    res_line = ""
                    if type(aux_line1) is not list:
                        aux_line1 = aux_line1.split(" ")
                    if type(aux_line2) is not list:
                        aux_line2 = aux_line2.split(" ")
                    if aux_line1[0] == aux_line2[0]:
                        cap = int(aux_line1[1][:-1]) + int(aux_line2[1][:-1])
                        positions = list(set(aux_line1[2:]) | set(aux_line2[2:]))
                        for i in range(len(positions)):
                            positions[i] = int(positions[i].strip())
                        positions.sort()
                        if last:
                            word_counter += 1
                            if word_counter == 1:
                                res_line = "1" + self.getGcode(word_counter)
                            else:
                                res_line = self.getGcode(word_counter)
                            for i in range(len(positions)):
                                if i == 0:
                                    res_line += self.getGcode(positions[i])
                                else:
                                    range1 = self.getGcode(positions[i] - positions[i - 1])
                                    res_line += range1
                            res.write(self.convertToBytes(res_line))
                        else:
                            res_line = aux_line1[0] + " " + str(cap) + "k"
                            for i in range(len(positions)):
                                res_line += " " + str(positions[i])
                            res_line += "\n"
                            res.write(res_line)
                        aux_line1 = file_one.readline()
                        aux_line2 = file_two.readline()
                    elif aux_line1[0] < aux_line2[0]:
                        positions = aux_line1[2:]
                        for i in range(len(positions)):
                            positions[i] = int(positions[i].strip())
                        positions.sort()
                        if last:
                            word_counter += 1
                            if word_counter == 1:
                                res_line = "1" + self.getGcode(word_counter)
                            else:
                                res_line = self.getGcode(word_counter)
                            for i in range(len(positions)):
                                if i == 0:
                                    res_line += self.getGcode(positions[i])
                                else:
                                    range1 = self.getGcode(positions[i] - positions[i - 1])
                                    res_line += range1
                            res.write(self.convertToBytes(res_line))
                        else:
                            res_line = aux_line1[0] + " " + aux_line1[1]
                            for i in range(len(positions)):
                                res_line += " " + str(positions[i])
                            res_line += "\n"
                            res.write(res_line)
                        aux_line1 = file_one.readline()
                    else:
                        positions = aux_line2[2:]
                        for i in range(len(positions)):
                            positions[i] = int(positions[i].strip())
                        positions.sort()
                        if last:
                            word_counter += 1
                            if word_counter == 1:
                                res_line = "1" + self.getGcode(word_counter)
                            else:
                                res_line = self.getGcode(word_counter)
                            for i in range(len(positions)):
                                if i == 0:
                                    res_line += self.getGcode(positions[i])
                                else:
                                    range1 = self.getGcode(positions[i] - positions[i - 1])
                                    res_line += range1
                            res.write(self.convertToBytes(res_line))
                        else:
                            res_line = aux_line2[0] + " " + aux_line2[1]
                            for i in range(len(positions)):
                                res_line += " " + str(positions[i])
                            res_line += "\n"
                            res.write(res_line)
                        aux_line2 = file_two.readline()
                if aux_line1:
                    while aux_line1:
                        res_line = ""
                        if type(aux_line1) is not list:
                            aux_line1 = aux_line1.split(" ")
                        positions = aux_line1[2:]
                        for i in range(len(positions)):
                            positions[i] = int(positions[i].strip())
                        positions.sort()
                        if last:
                            word_counter += 1
                            if word_counter == 1:
                                res_line = "1" + self.getGcode(word_counter)
                            else:
                                res_line = self.getGcode(word_counter)
                            for i in range(len(positions)):
                                if i == 0:
                                    res_line += self.getGcode(positions[i])
                                else:
                                    range1 = self.getGcode(positions[i] - positions[i - 1])
                                    res_line += range1
                            res.write(self.convertToBytes(res_line))
                        else:
                            res_line = aux_line1[0] + " " + aux_line1[1]
                            for i in range(len(positions)):
                                res_line += " " + str(positions[i])
                            res_line += "\n"
                            res.write(res_line)
                        aux_line1 = file_one.readline()
                if aux_line2:
                    while aux_line2:
                        res_line = ""
                        if type(aux_line2) is not list:
                            aux_line2 = aux_line2.split(" ")
                        positions = aux_line2[2:]
                        for i in range(len(positions)):
                            positions[i] = int(positions[i].strip())
                        positions.sort()
                        if last:
                            word_counter += 1
                            if word_counter == 1:
                                res_line = "1" + self.getGcode(word_counter)
                            else:
                                res_line = self.getGcode(word_counter)
                            for i in range(len(positions)):
                                if i == 0:
                                    res_line += self.getGcode(positions[i])
                                else:
                                    range1 = self.getGcode(positions[i] - positions[i - 1])
                                    res_line += range1
                            res.write(self.convertToBytes(res_line))
                        else:
                            res_line = aux_line2[0] + " " + aux_line2[1]
                            for i in range(len(positions)):
                                res_line += " " + str(positions[i])
                            res_line += "\n"
                            res.write(res_line)
                        aux_line2 = file_two.readline()
        res.close()
        os.remove(direction + "/ResFiles/" + file1)
        os.remove(direction + "/ResFiles/" + file2)

    def convertToBytes(self, line):
        n = int(line, 2)
        n = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        return n

    def convertToBitString(self, received):
        return "{0:b}".format(int.from_bytes(received, byteorder='big'))

    def getGcode(self, number):
        if number == 1:
            return "0"
        binar = "{0:b}".format(number)[1:]
        length = ""
        for i in range(len(binar)):
            length += "1"
        length += "0"
        return length + binar

    def invert_decoder(self, dir):
        with open(dir, 'rb') as byteTestRead:
            line = "{0:b}".format(int.from_bytes(byteTestRead.readline(), byteorder='big'))
            zsuv_length = 0
            result_line = ""
            aux_byte = "1"
            i = 0
            line = line[1:]
            while i < len(line):
                if line[i] == '0' and zsuv_length == 0:
                    result_line += aux_byte + " "
                    i += 1
                elif line[i] == '1':
                    zsuv_length += 1
                    i += 1
                elif line[i] == '0':
                    if i + zsuv_length > len(line):
                        continue
                    i += 1
                    for j in range(i, zsuv_length + i):
                        aux_byte += line[j]
                    result_line += str(int(aux_byte, 2)) + " "
                    aux_byte = "1"
                    i = i + zsuv_length
                    zsuv_length = 0
            return result_line

    def last_dict(self, first, second):
        with open(direction + "/ResFiles/" + first, 'r') as file_one:
            with open(direction + "/ResFiles/" + second, 'r') as file_two:
                dicti = open(direction + "/Ready/Dictionary.txt", 'w')
                table = open(direction + "/Ready/Table.txt", 'w')
                word_counter = 0
                glob_counter = 1
                root_word = ""
                root_end = 0
                aux_words = []
                aux_line1 = file_one.readline()
                aux_line2 = file_two.readline()
                while aux_line1 and aux_line2:
                    if type(aux_line1) is not list:
                        aux_line1 = aux_line1.split(" ")
                    if type(aux_line2) is not list:
                        aux_line2 = aux_line2.split(" ")
                    res_line = ""
                    if aux_line1[0] == aux_line2[0]:
                        word_counter += 1
                        cap = int(aux_line1[1][:-1]) + int(aux_line2[1][:-1])
                        if root_word != "":
                            for i in range(len(root_word)):
                                if root_word[i] != aux_line1[0][i]:
                                    if i > 3:
                                        aux_words.append(aux_line1[0])
                                        table.write(str(word_counter) + " " + str(cap) + "\n")
                                        if i < root_end:
                                            root_word = aux_line1[0]
                                            root_end = i
                                        break
                                    else:
                                        if len(aux_words) > 1:
                                            res_line = self.make_word(root_word, root_end, aux_words)
                                        else:
                                            res_line = str(len(root_word)) + root_word
                                        dicti.write(res_line)
                                        table.write(str(word_counter) + " " + str(cap) + "\n")
                                        glob_counter += len(res_line)
                                        root_word = ""
                                        aux_words = []
                                        root_end = 0
                                        break
                        else:
                            root_word = aux_line1[0]
                            root_end = len(root_word)
                            aux_words.append(aux_line1[0])
                            table.write(str(word_counter) + " " + str(cap) + " " + str(glob_counter) + "\n")
                        aux_line1 = file_one.readline()
                        aux_line2 = file_two.readline()
                    elif aux_line1[0] < aux_line2[0]:
                        word_counter += 1
                        if root_word != "":
                            for i in range(len(root_word)):
                                if root_word[i] != aux_line1[0][i]:
                                    if i > 3:
                                        aux_words.append(aux_line1[0])
                                        table.write(str(word_counter) + " " + aux_line1[1] + "\n")
                                        if i < root_end:
                                            root_word = aux_line1[0]
                                            root_end = i
                                        break
                                    else:
                                        if len(aux_words) > 1:
                                            res_line = self.make_word(root_word, root_end, aux_words)
                                        else:
                                            res_line = str(len(root_word)) + root_word
                                        dicti.write(res_line)
                                        table.write(str(word_counter) + " " + aux_line1[1] + "\n")
                                        glob_counter += len(res_line)
                                        root_word = ""
                                        aux_words = []
                                        root_end = 0
                                        break
                        else:
                            root_word = aux_line1[0]
                            root_end = len(root_word)
                            aux_words.append(aux_line1[0])
                            table.write(str(word_counter) + " " + aux_line1[1] + " " + str(glob_counter) + "\n")
                        aux_line1 = file_one.readline()
                    else:
                        word_counter += 1
                        if root_word != "":
                            for i in range(len(root_word)):
                                if root_word[i] != aux_line2[0][i]:
                                    if i > 3:
                                        aux_words.append(aux_line2[0])
                                        table.write(str(word_counter) + " " + aux_line2[1] + "\n")
                                        if i < root_end:
                                            root_word = aux_line2[0]
                                            root_end = i
                                        break
                                    else:
                                        if len(aux_words) > 1:
                                            res_line = self.make_word(root_word, root_end, aux_words)
                                        else:
                                            res_line = str(len(root_word)) + root_word
                                        dicti.write(res_line)
                                        table.write(str(word_counter) + " " + aux_line2[1] + "\n")
                                        glob_counter += len(res_line)
                                        root_word = ""
                                        aux_words = []
                                        root_end = 0
                                        break
                        else:
                            root_word = aux_line2[0]
                            root_end = len(root_word)
                            aux_words.append(aux_line2[0])
                            table.write(str(word_counter) + " " + aux_line2[1] + " " + str(glob_counter) + "\n")
                        aux_line2 = file_two.readline()
                if aux_line1:
                    while aux_line1:
                        word_counter += 1
                        if root_word != "":
                            for i in range(len(root_word)):
                                if root_word[i] != aux_line1[0][i]:
                                    if i > 3:
                                        aux_words.append(aux_line1[0])
                                        table.write(str(word_counter) + " " + aux_line1[1] + "\n")
                                        if i < root_end:
                                            root_word = aux_line1[0]
                                            root_end = i
                                        break
                                    else:
                                        if len(aux_words) > 1:
                                            res_line = self.make_word(root_word, root_end, aux_words)
                                        else:
                                            res_line = str(len(root_word)) + root_word
                                        dicti.write(res_line)
                                        table.write(str(word_counter) + " " + aux_line1[1] + "\n")
                                        glob_counter += len(res_line)
                                        root_word = ""
                                        aux_words = []
                                        root_end = 0
                                        break
                        else:
                            root_word = aux_line1[0]
                            root_end = len(root_word)
                            aux_words.append(aux_line1[0])
                            table.write(str(word_counter) + " " + aux_line1[1] + " " + str(glob_counter) + "\n")
                        aux_line1 = file_one.readline()
                if aux_line2:
                    while aux_line2:
                        word_counter += 1
                        if root_word != "":
                            for i in range(len(root_word)):
                                if root_word[i] != aux_line2[0][i]:
                                    if i > 3:
                                        aux_words.append(aux_line2[0])
                                        table.write(str(word_counter) + " " + aux_line1[1] + "\n")
                                        if i < root_end:
                                            root_word = aux_line2[0]
                                            root_end = i
                                        break
                                    else:
                                        if len(aux_words) > 1:
                                            res_line = self.make_word(root_word, root_end, aux_words)
                                        else:
                                            res_line = str(len(root_word)) + root_word
                                        dicti.write(res_line)
                                        table.write(str(word_counter) + " " + aux_line2[1] + "\n")
                                        glob_counter += len(res_line)
                                        root_word = ""
                                        aux_words = []
                                        root_end = 0
                                        break
                        else:
                            root_word = aux_line2[0]
                            root_end = len(root_word)
                            aux_words.append(aux_line2[0])
                            table.write(str(word_counter) + " " + aux_line2[1] + " " + str(glob_counter) + "\n")
                        aux_line2 = file_two.readline()
                dicti.close()
                table.close()

    def make_word(self, root, end, aux):
        res_word = str(len(root)) + root[:end] + "*" + root[end:]
        ends = []
        for el in aux:
            if el == root:
                continue
            ends.append(el[end:])
        for ending in ends:
            res_word += str(len(ending)) + ending
        return res_word


class Dictionary:

    def __init__(self, direction):
        self.res_file_counter = 0
        self.file_id = 1
        self.direction = direction
        self.queueFill()
        threads = []
        for i in range(30):
            threads.append(ThreadForTenRead())
            threads[i].start()
        for i in range(30):
            threads[i].join()
        print("-----------------Merge---------------------")
        self.merge_files()

    def queueFill(self):
        for fileInfo in os.listdir(direction + "/FilesToTest/"):
            files_dict[self.file_id] = fileInfo
            clientPool.put([direction + "/FilesToTest/" + fileInfo, self.file_id])
            self.file_id += 1

    def checkDecode(self, path):
        encoding = [
            'utf-8',
            'GBK',
            'ASCII',
            'US-ASCII',
            'Big5',
            'windows-1251',
            'cp500'
        ]
        correct_encoding = ''

        for enc in encoding:
            try:
                open(path, encoding=enc).readline()
            except (UnicodeDecodeError, LookupError):
                pass
            else:
                correct_encoding = enc
                break
        return correct_encoding

    def merge_files(self):
        print("Start merging...")
        old_files_list = os.listdir(direction + "/ResFiles")
        new_files_list = []
        last_files = False
        while len(old_files_list) != 1:
            if len(old_files_list) == 2:
                last_files = True
            while len(old_files_list) != 0:
                if len(old_files_list) == 1:
                    new_files_list.insert(0, old_files_list[0])
                    old_files_list.pop(0)
                else:
                    new_name = "Result" + str(self.res_file_counter) + ".txt"
                    mergePool.put([old_files_list[0], old_files_list[1], new_name, last_files])
                    self.res_file_counter += 1
                    old_files_list.pop(0)
                    old_files_list.pop(0)
                    new_files_list.insert(0, new_name)
            threads = []
            for i in range(len(new_files_list)):
                threads.append(ThreadMerging())
                threads[i].start()
            for i in range(len(new_files_list)):
                threads[i].join()
            old_files_list = new_files_list
            new_files_list = []
        print(old_files_list[0])


res_file_counter = 0
file_id = 0
clientPool = queue.Queue(0)
mergePool = queue.Queue(0)
direction = "/home/ihorzam/Work/PythonFiles/"
pattern = re.compile(r'\w+[\'\-]?\w+')
files_dict = {}
myDict = Dictionary(direction)
print("--- %s seconds ---" % (time.time() - start_time))
print("Ready")

