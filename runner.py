# Used to run a program a set number of times and return the average time taken
import os, sys, time
from datetime import datetime


def main():
    # Get the number of times to run the program from argv
    if len(sys.argv) != 4:
        print("Usage: runner.py <number of times to run> <Threshold> <Number of processes>")
        sys.exit(1)

    num_times = int(sys.argv[1])
    # Get the program to run from argv
    program = ("python3 main.py " + sys.argv[2] + " " + sys.argv[3])

    # Run the program num_times times
    times = []
    for i in range(num_times):
        start = time.time()
        # Run the program
        os.system(program)
        end = time.time()
        # Add the time taken to the list
        times.append(end - start)

    # Calculate the average time
    avg = sum(times) / len(times)
    print("Average time: " + str(avg*1000) + "ms")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    # store Data in a file
    f = open("avgRun.txt", "a")
    f.write("Run (" + str(current_time) + "):")
    f.write("______________________________________\n")
    f.write("Run amount: " + sys.argv[1] + " Average Time: " + str(avg*1000) + "ms\n")
    f.write(" Parameters: [Threshold: " + sys.argv[2] + " Number of Processes: " + sys.argv[3] + "]\n")
    f.write("___________________________________________________\n")
    f.close()


if __name__ == '__main__':
    main()