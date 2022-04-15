# Lab 7

# Lab Exercise 7: Uniprocessor Scheduling Simulator copyright (c) Emmanuel Theodore

"""
ELEC4075 Engineering Operating Systems Electrical and Computer Engineering Wentworth Institute of Technology
• To create a simulator for the FCFS, SPN, and SRT scheduling algorithms. o Understand the operation of FCFS, SPN, and SRT.
o Create a visual representation (Gantt chart)
Note: You are allowed to work with one other student for this lab, you may also choose to work alone.
Instructions:
Create a simulator in C1 that simulates First-Come-First Serve (FCFC), Shortest Process Next (SPN), and Shortest- Remaining Time (SRT).
• The simulator will need to accept the following inputs for each process: Process Name, Arrival Time, and Service Time – you can create input files or have the user input each time.
• The simulator would need to calculate and display the following outputs (in a table) for each process: Process Name, Arrival Time, Service Time, Start Time, Finish Time, Wait Time, Turnaround Time.
• Similar to the examples we did in the lecture, you can ignore I/O i.e., in non-preemptive algorithms, the processes run straight through to the end once started, and in preemptive algorithms, only the OS can preempt a process.
"""

# input file Structure (one process per line)
# Process Name: A, Arrival Time: 0,, Service Time: 3

# import the necessary packages
import sys, os, time, random, math, datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# choose the algo to run
global Algo
if len(sys.argv) == 2:
    Algo = str(sys.argv[1])
    Algo.upper()

    print("Running " + str(Algo) + " Algorithm....")
else:
    print("Default values are used")
    print("Running FCFS Algorithm....")
    Algo = "FCFS"


# Class Definitions
class process:

    def __init__(self, name, arrival, service):
        self.name = name
        self.arrival = arrival
        self.service = service
        self.start = 0
        self.finish = 0
        self.wait = 0
        self.turnaround = 0
        self.remaining = service
        self.next = None
        self.executed = False
        self.tick = 0
        self.s = 's'

    def __str__(self):
        return print_table(self)


# Algo = "FCFS"
def fcfs(program):
    # Create a Queue
    # Sort the programs by arrival time and export it to a list
    queue = sorted(program.values(), key=lambda x: x.arrival)

    # Start time
    start = 0

    # Loop through the queue
    for i in queue:
        # Set the start time of the proces
        i.start = start
        # Set the finish time of the process
        i.finish = i.start + i.service
        # Set the wait time of the process
        i.wait = i.start - i.arrival
        # Set the turnaround time of the process
        i.turnaround = i.finish - i.arrival
        # increment the start time
        start += i.service


# Algo = "SPN"
def spn(program):
    # sort by lowest arrival time
    queue = sorted(program.values(), key=lambda x: x.arrival)

    q = []
    st = 0
    buffer = []

    # total time = all the service times
    total_time = sum(i.service for i in queue)

    # loop through each time slice
    for i in range(total_time):
        # when a process arrives, add it to the queue
        for j in queue:
            if j.arrival == i:
                q.append(j)
        # if the current process has not started yet or has finished
        if st == 0:
            # sort the queue by service time
            q = sorted(q, key=lambda x: x.service)
            # set the start time of the process
            st = q[0].service

        # end of time slice
        st -= 1
        # if the process has finished
        if st == 0:
            # set the finish time of the process
            q[0].finish = i + 1
            # set the wait time of the process
            q[0].wait = i - q[0].arrival
            # set the turnaround time of the process
            q[0].turnaround = q[0].finish - q[0].arrival
            # add the process to the buffer
            buffer.append(q[0])
            # remove the process from the queue
            q.pop(0)

    start = 0
    # Loop through the queue
    for i in buffer:
        # Set the start time of the proces
        i.start = start
        # increment the start time
        start += i.service


# Algo = "SRT"
def srt(program):
    # sort by lowest arrival time
    queue = sorted(program.values(), key=lambda x: x.arrival)

    q = []
    buffer = []

    # total time = all the service times
    total_time = sum(i.service for i in queue)

    # loop through each time slice
    for i in range(total_time):

        # when a process arrives, add it to the queue
        for j in queue:
            if j.arrival == i:
                q.append(j)

        # if the queue has 2 or more processes
        if len(q) >= 2:
            # if remaining service time of the first process is greater than the second process
            if q[0].remaining <= q[1].service:
                # sort the queue by service time
                q = sorted(q, key=lambda x: x.remaining)
        else:
            # sort the queue by service time
            q = sorted(q, key=lambda x: x.service)

        # if the current process has not started yet
        if q[0].s == 's':
            # set the start time of the process
            q[0].finish = q[0].service
            # set start flag
            q[0].s = i
            # set the start time of the process
            q[0].start = i

        # add the process to the buffer
        buffer.append(q[0])

        # remove the process from the queue
        # if the process has finished
        if q[0].remaining == 1:
            q[0].executed = True
            q[0].finish = i + 1
            q.pop(0)
        else:
            q[0].remaining -= 1

        # end of time slice

    for i in buffer:
        i.wait = i.start - i.arrival
        i.turnaround = i.finish - i.arrival

    # Debug: print(buffer.name)
    str_ = ""
    for i in buffer:
        str_ += (i.name + " ")
    print(str_)


# functions
def initProcess(input_):
    # creating a program dictionary
    programsDict = {}

    inputArray = input_.split(",")
    inputArray = [x.strip() for x in inputArray]
    tempArray = []

    for s in inputArray:
        v = s.split(":")
        v = [x.replace(" ", "") for x in v]
        tempArray.append(v[1])  # grab the value of the array
        # [' A', ' 0', ' 3.']
    programsDict[tempArray[0]] = process(tempArray[0], int(tempArray[1]), int(tempArray[2]))

    return programsDict


# function to remove a space from a string if the string is more than one character
rm = "        |"


def removeSpace(string):
    x = str(string)
    if len(x) > 1:
        global rm
        rm = "       |"
    else:
        rm = "        |"

    return string


# output Data in a table format
def print_table(process_dict):
    print("Printing Table.....")
    print("____________________________________________________________________________________________________")
    print("| Process Name | Arrival Time | Service Time | Start Time | Finish Time | Wait Time | Turnaround Time |")
    print("____________________________________________________________________________________________________")
    for key in process_dict:
        print("|", removeSpace(process_dict[key].name), rm, removeSpace(process_dict[key].arrival), rm,
              removeSpace(process_dict[key].service), rm,
              removeSpace(process_dict[key].start), rm, removeSpace(process_dict[key].finish), rm,
              removeSpace(process_dict[key].wait),
              "      |",
              removeSpace(process_dict[key].turnaround), rm)
    print("____________________________________________________________________________________________________")
    print("\n")


# output Data in a table format
def output_table(process_dict):
    # open the output file
    output = open("output_part_1.txt", "a")
    output.write("Pass @ " + str(datetime.datetime.now()) + " with " + Algo + " ----> \n")
    output.write("input.txt______________________________________\n")
    output.write("| Process Name | Arrival Time | Service Time |\n")
    for key in process_dict:
        output.write(
            "| " + process_dict[key].name + "         | " + str(process_dict[key].arrival) + "         | " + str(
                process_dict[key].service) + "         |\n")
    output.write("____________________________________________\n")
    output.write("\n")
    output.write(
        "output.txt_____________________________________________________________________________________________\n")
    output.write(
        "| Process Name | Arrival Time | Service Time | Start Time | Finish Time | Wait Time | Turnaround Time |\n")
    output.write(
        "____________________________________________________________________________________________________\n")
    for key in process_dict:
        output.write(
            "| " + process_dict[key].name + "         | " + str(process_dict[key].arrival) + "         | " + str(
                process_dict[key].service) + "         | " +
            str(process_dict[key].start) + "        | " + str(process_dict[key].finish) + "        | " + str(
                process_dict[key].wait) + "       | " +
            str(process_dict[key].turnaround) + "            |\n")
    output.write(
        "____________________________________________________________________________________________________\n")
    output.write("\n")


def printChart(process_dict, algo):
    # print("Gantt chart")
    # print("____________________________________________________________________________________________________")

    data = []
    for key in process_dict:
        data.append(dict(Task=process_dict[key].name, Start=process_dict[key].start, Finish=process_dict[key].finish))
    df = pd.DataFrame(data)
    # days between start and end of each task
    df['service_Time'] = df.Finish - df.Start
    # sort in ascending order of start date
    df = df.sort_values(by='Task', ascending=False)
    fig, ax = plt.subplots(1, figsize=(16, 3))
    ax.barh(df.Task, df.service_Time, left=df.Start)
    plt.title('Gantt Chart: ' + algo, size=18)
    total_time = sum(i.service for i in process_dict.values())
    x_ticks = [i for i in range(total_time+1)]
    x_labels = [i for i in range(total_time+1)]
    plt.xticks(x_ticks, x_labels)
    plt.show()


def picker(algo, process_dict):
    if algo == "FCFS":
        fcfs(process_dict)
    elif algo == "SPN":
        spn(process_dict)
    elif algo == "SRT":
        srt(process_dict)


def main():
    # create an empty array to store the input
    LineInFile = []
    # open the input file
    fp1 = open("inp.txt", "r")

    line = fp1.readline()

    # if the file is empty, exit the program
    if line == "":
        print("Empty File")
        sys.exit()

    # read fp1 line by line into LineInFile
    while line != "":
        line = fp1.readline()
        if line != "":
            LineInFile.append(line)

    programDict = {}
    # create a dictionary of processes
    for key in LineInFile:
        programDict.update(initProcess(key))

    picker(Algo, programDict)
    output_table(programDict)
    print_table(programDict)
    printChart(programDict, Algo)


if __name__ == "__main__":
    main()

# Changelog
# - V 0.1 Basic UI, Input and output functionality
# - V 0.2 implements 2/3 algorithms
# - V 0.3 implement 3/3 algorithms
