# OS Parser

# Importing the necessary modules
import time
start = time.time()
import re, sys
from os.path import exists
from datetime import datetime

""""""

# Lab 6 Changes:
# - adding percentage threshold and number of processes and taking this input from the commandline
# - adding default values for the percentage threshold and number of processes
if len(sys.argv) == 3:

    Threshold = int(sys.argv[1])
    numberOfProcesses = int(sys.argv[2])

    print("Threshold: " + str(Threshold))
    print("Number of processes: " + str(numberOfProcesses))
else:
    print("Default values are used")
    Threshold = 80
    numberOfProcesses = 2


# defining classs
class process():

    def __init__(self, pid, state, io, newOrNot):
        self.pid = pid
        self.state = state
        self.io = io
        self.new = newOrNot

    def __str__(self):
        print("pid: " + self.pid + " state: " + self.state + " io: " + self.io +
              " new: " + self.new)


class io():

    def __init__(self, disk, printer, keyboard):
        self.disk = disk
        self.printer = printer
        self.keyboard = keyboard


# functions


def initProcess(input):
    # creating a program dictionary
    programsDict = {}

    inputArray = input.split(" ")

    # splitting inputArray into an array of pairs of strings
    n = 2
    splitPairs = [inputArray[i:i + n] for i in range(0, len(inputArray), n)]

    # creating a process object
    # for each pair in splitPairs create a process object where the first string is the pid and the second string is the state
    for pair in splitPairs:

        # if the first string in the pair is "end" then break
        if pair[0] == "end\n":
            break
        # Note: some systoms use 'end\n' and some use 'end\r\n'
        programsDict[pair[0]] = process(pair[0], pair[1], "", "")
    return programsDict


def outputRuntime(runtime):
    output = open("Runtime.txt", "a")
    runtime = str(runtime)
    output.write(runtime + "\n")


def outputSlice(line, programs):
    output = open("inp2_parsed.txt", "a")
    processView = ""
    ioView = io("Disk queue: ", "Printer queue: ", "Keyboard queue: ")

    # building strings to print
    for key in programs:
        if line.find(key) != -1:
            processView += key + " " + programs[key].state + "* "
        else:
            processView += key + " " + programs[key].state + " "

        if programs[key].io == "":
            pass
        elif programs[key].io == "disk":
            ioView.disk += key + " "
        elif programs[key].io == "printer":
            ioView.printer += key + " "
        elif programs[key].io == "keyboard":
            ioView.keyboard += key + " "
        else:
            pass

    # Outputing the strings
    output.write(line + "\n" + processView + "\n" + ioView.disk + "\n")
    output.write(ioView.printer + "\n")
    output.write(ioView.keyboard + "\n")


# prints the line being prossessed, the state of the prossess
def printSlice(line, programs):
    print("__________________________")
    prossessView = ""
    ioView = io("Disk queue: ", "Printer queue: ", "Keyboard queue: ")

    # building strings to print
    for key in programs:
        if line.find(key) != -1:
            prossessView += key + " " + programs[key].state + "* "
        else:
            prossessView += key + " " + programs[key].state + " "

        if programs[key].io == "":
            pass
        elif programs[key].io == "disk":
            ioView.disk += key + " "
        elif programs[key].io == "printer":
            ioView.printer += key + " "
        elif programs[key].io == "keyboard":
            ioView.keyboard += key + " "
        else:
            pass

    # printing the strings
    print(line + "\n" + prossessView)
    print(ioView.disk)
    print(ioView.printer)
    print(ioView.keyboard)
    print("__________________________")


def main():
    # vars
    LineInFile = []
    # open the input file
    fp1 = open("input_files/100thresh2.txt", "r")
    # open the output file
    fp2 = open("inp2_parsed.txt", "w")

    # open analitics
    path_exists = exists("Runtime.txt")
    if path_exists:
        fp3 = open("Runtime.txt", "a")
    else:
        fp3 = open("Runtime.txt", "w")


    line = fp1.readline()
    if line != "":
        # fp2.write(line)
        program = initProcess(line)

    # read fp1 line by line into LineInFile
    while line != "":
        line = fp1.readline()
        if line != "":
            LineInFile.append(line)

    # parse the each line in LineInFile by ":", ";", "."
    for line in LineInFile:
        rch = re.split(": |; |\.", line)
        if "Time" in rch[1]:
            pid = rch[1][16]
            id = "P" + pid
            program[id].state = "Ready"
        if "request" in rch[1]:
            pid = rch[1][1]
            state = "Blocked"
            io = rch[1][16:]
            id = "P" + pid
            program[id].state = state
            program[id].io = io
        if "dispatched" in rch[2]:
            pid = rch[2][1]
            state = "Running"
            io = ""
            id = "P" + pid
            program[id].state = state
            program[id].io = io
        if "interrupt" in rch[1]:
            pid = rch[1][len(rch[1]) - 1]
            id = "P" + pid
            if program[id].state == "Blocked":
                program[id].state = "Ready"
            elif program[id].state == "Blocked/Suspend":
                program[id].state = "Ready/Suspend"
        if "terminated" in rch[1]:
            program[id].io = ""
            program[id].state = "Exit"
            program[id].io = ""

        printSlice(line, program)
        outputSlice(line, program)

        # get number blocked state
        pBlocked = 0
        pExit = 0
        pNumber = 0
        pbArray = []
        for p in program:
            state = program[p].state
            if state == "Blocked":
                pBlocked += 1
            pbArray.append(p + ":" + state)
            if state == "Exit":
                pExit += 1
                for q in program:
                    if program[q].state == "Blocked/Suspend":
                        program[q].state = "Blocked"
                    if state == "Ready/Suspend":
                        program[q].state = "Ready"

        print("Blcoked Prosses: " + str(pBlocked))
        print("Exited Prosses: " + str(pExit))
        pNumber = len(program) - pExit
        print("Number of Active proseses: " + str(pNumber))

        # % prosses blocked
        ppb = (pBlocked / len(program)) * 100
        print("% of Prosses blcoked: " + str(ppb))
        # pprint.pprint(pbArray)

        # if Threshold is reached, suspend the [numberOfProcesses] presses with the lowest p number
        if ppb == Threshold:
            print("Threshold reached <--------------------")
            pbArray.sort(key=lambda x: x.split(":")[1])
            for i in range(0, numberOfProcesses):
                pbArray[i] = pbArray[i].split(":")[0]
            for p in range(numberOfProcesses):
                x = pbArray[p]
                x = x.split(":")
                if program[x[0]].state == "Blocked":
                    program[x[0]].state = "Blocked/Suspend"

        # print the presses
        print("__________________________")
        for p in program:
            print(p + ":" + program[p].state)
        print("__________________________")

    end = time.time()
    runtime = str(end - start)
    print("Runtime: " + runtime)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    miliseconds = str((end - start) * 1000)
    out = ("Runtime: " + miliseconds + "ms Time: " + current_time)
    outputRuntime(out)


if __name__ == '__main__':
    main()