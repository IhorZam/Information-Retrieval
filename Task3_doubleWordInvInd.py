import os


def sort_key(word1):
    return word1.double_word


class DoubleWord:
    def __init__(self, double_word, file_id, intens):
        self.double_word = double_word
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
        for fileInfo in result_list:
            with open(direction + "\\" + fileInfo, 'r') as auxFile:
                text = auxFile.read().lower()
                res_text = text.split(" ")
                for i in range(len(res_text)):
                    if i + 1 < len(res_text):
                        updated_word = res_text[i].lstrip('\'\".,!?\n').rstrip('\n\'\".,!?') + " " + res_text[i+1].lstrip('\'\".,!?\n').rstrip('\n\'\".,!?')
                        all_words.append(DoubleWord(updated_word, file_id, 1))
                    else:
                        all_words.append(DoubleWord(res_text[i], file_id, 1))
            file_id += 1
        all_words.sort(key=sort_key)
        for r_word in all_words:
            if r_word.double_word not in self.invertIndex.keys():
                self.invertIndex[r_word.double_word] = [r_word.intens, r_word.file_id]
            else:
                self.invertIndex[r_word.double_word][0] += 1
                if r_word.file_id in self.invertIndex[r_word.double_word]:
                    continue
                else:
                    self.invertIndex[r_word.double_word].append(r_word.file_id)


myDict = Dictionary("D:\Dropbox\PythonWorkspace\Information-Retrieval\Files")
print(myDict.wordsNumber)
