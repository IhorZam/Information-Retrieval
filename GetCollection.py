import re
import requests


class GetCollection:
    def __init__(self, path):
        res_direction = "/home/ihorzam/Work/PythonFiles/FilesToWork/Wiki/"
        pattern = re.compile(r'<a.+href="(.+)"')
        collCounter = 0
        while True:
            with open(res_direction + "File" + str(collCounter) + ".txt", 'w') as ouf:
                res = requests.get(path)
                res1 = pattern.findall(res.content.decode())
                path = "https://en.wikipedia.org/" + res1[5]
                ouf.write(res.content.decode())
                collCounter += 1


start = GetCollection('https://en.wikipedia.org/wiki/Microsoft')