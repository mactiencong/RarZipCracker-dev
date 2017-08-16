import zipfile
import rarfile
import os
import argparse
from itertools import product
import time
import sys

CHARACTER ='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&()'

parser = argparse.ArgumentParser(description="ZipRarCracker", epilog="Use -h for help")
parser.add_argument("-i", "--input", help="Zip or Rar path", required=True)
parser.add_argument("rules", nargs="*", help="<min_pass_length> <max_pass_length> <characters>")
rarfile.UNRAR_TOOL = "./unrarw32.exe"
class Cracker:
    def __init__(self, argv):
        self.argv = argv
    def getFileType(self, path):
        ext = os.path.splitext(path)[1].upper()
        if ext == ".ZIP":
            return "ZIP"
        if ext == ".RAR":
            return "RAR"
        return None
    def getFileFromPath(self, file_type, path):
        if self.isFileExist(path) == False:
            return False
        if file_type=="ZIP":
            return zipfile.ZipFile(path)
        return rarfile.RarFile(path)
    def isFileExist(self, path):
        return os.path.isfile(path)
    def parseArgv(self):
        print(self.argv)
        number_argv = len(self.argv)
        if number_argv<2 or number_argv>5 or number_argv==3:
            return False
        self.file_path = self.argv[1]
        self.hasRule = False
        if number_argv >= 4:
            self.hasRule = True
            self.min_character = int(self.argv[2])
            self.max_character = int(self.argv[3])
        if number_argv == 5:
            self.characters = self.argv[4]
        else:
            self.characters = CHARACTER
        return True
    def encodePasswordWithFileType(file_type, password):
        if file_type=="ZIP":
            return password.encode()
        return password
    def end(self, message):
        print(message)
        parser.exit()
    def tryExtractFile(self, file, password):
        try:
            file.extractall(pwd=password)
            return True
        except:
            return False
    def bruteWithPassLength(self, file, pass_length):
        listPass = product(self.characters, repeat=pass_length)
        for pass_chars in listPass:
            password = "".join(pass_chars)
            if self.tryExtractFile(file, password)==True:
                return password
        return False
    def bruteNoRule(self, file):  
        pass_length = 1
        while True:
            found_pass = self.bruteWithPassLength(file, pass_length)
            if  found_pass!= False:
                return found_pass
            pass_length +=1
        return False
    def bruteWithRule(self, file):
        for pass_length in range(self.min_character, self.max_character):
            found_pass = self.bruteWithPassLength(file, pass_length)
            if  found_pass!= False:
                return found_pass
        return False
    def run(self):
        if self.parseArgv()==False:
            parser.print_help()
            parser.exit()
        file_type = self.getFileType(self.file_path)
        if file_type==None:
            self.end("File type invalid")
        compressed_file = self.getFileFromPath(file_type, self.file_path)
        if compressed_file==None:
            self.end("File invalid")
        found_pass = False
        if self.hasRule==True:
            found_pass = self.bruteWithRule(compressed_file)
        else:
            found_pass = self.bruteNoRule(compressed_file)
        if found_pass != False:
            print("Pass="+found_pass)
        else:
            print("Not found pass")
        parser.exit()
cracker = Cracker(sys.argv[1:])
cracker.run()