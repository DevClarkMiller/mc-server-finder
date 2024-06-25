import zipfile
import os
from termcolor import colored
import atexit

target_file = 'server.jar'
serverJars = []
fileCount = 0

def exit_handler():
    #Finally output the found server jar files to the txt file
        f = open("foundJars.txt", "w")
        f.write("FOUND SERVER JARS\n")
        for file in serverJars:
            print(file)
            f.write(file + '\n')
        f.close()

def checkFile(f):
    global serverJars
    if os.path.basename(f) == target_file:
        print(colored(f"Target Found: {f}", 'green'))
        serverJars.append(f)
        return True
    return False    

def scanZip(f):
    print(colored("Found zip", "yellow"))

    with zipfile.ZipFile(f, 'r') as zip_file:   #Giving it r, makes it a recursive scan!
       for file_info in zip_file.infolist():
           #print(colored(file_info.filename, "yellow"))
           if checkFile(file_info.filename):
               return
    print("target not found")

def scan(dir):
    global fileCount
    global serverJars
    try:
        for filename in os.listdir(dir):
            f = os.path.join(dir, filename)

            if os.path.isdir(f):    # If folder, use recursion to scan the files
                scan(f)
            elif os.path.isfile(f): # If file
                fileCount += 1
                print(f"Files parsed: {fileCount}")
                if checkFile(f) != True:
                    #print(colored(os.path.basename(f), "red"))
                    pass
                name, ext = os.path.splitext(f)
                if ext == '.zip':
                    scanZip(f)
    except PermissionError:
        pass
    except RecursionError:
        pass
    except Exception:
        pass

atexit.register(exit_handler)

directory = input("Enter directory to scan for minecraft servers: ")

scan(directory)

