from sys import platform
from pathlib import Path
from os import environ, pathsep

def srcPath():
    return Path(__file__).parent

def setSystemPath():
    environ['PATH'] += pathsep + str(srcPath().parent / 'ncbi-blast-2.13.0' / 'bin')

def getPlatform():
    if platform.startswith('linux'):
        return 'Linux'
    elif platform.startswith('win'):
        return 'Windows'
    elif platform == 'darwin':
        return 'MacOS'
    else:
        return 'Other'
    
def getPrompt():
    dic = {}
    with open(srcPath() / 'prompt.txt', 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i][0] == '@':
                j = i + 1
                while j < len(lines) and lines[j][0] != '@':
                    j += 1
                dic[lines[i].strip()[1:]] = ''.join(lines[i:j])
    
    return dic
                