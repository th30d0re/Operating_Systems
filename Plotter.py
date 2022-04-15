# plots runs and agrgates data from runs
import matplotlib.pyplot as plt


def main():
    # open the log file
    fp1 = open("Runtime.txt", "r")
    line = fp1.readline()



    # testing plots
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]
    plt.plot(x, y)

    # naming the x axis
    plt.xlabel('Runtime')
    # naming the y axis
    plt.ylabel('Time')

    # giving a title to my graph
    plt.title('Runtime Vs Time')

    # function to show the plot
    plt.show()

if __name__ == '__main__':
    main()