from growth import write_to_file
import numpy as np
import matplotlib.pyplot as plt
import sys

def read_file(filename):
    data = np.genfromtxt(filename,delimiter=",")
    return data



def parse_data(data):
    axis1 = [line[0] for line in data]
    axis2 = [line[1] for line in data]
    return axis1, axis2

def parse_data2(data):
    axis1 = [line[0] for line in data]
    axis2 = [line[1] for line in data]
    return axis1, axis2

def plot_power(X, Y, ylimlow=2,ylimhigh=3):
    plt.ylim(ylimlow,ylimhigh)
    plt.scatter(X,Y)
    plt.title("Scale Free Nature of Preferential Attatchment Degree Distribution")
    plt.ylabel("Power of Distribution")
    plt.xlabel("Ratio of Network Growth")
    plt.show()

def plot_deviation(X, Y, ylimlow=-2,ylimhigh=3):
    plt.ylim(ylimlow,ylimhigh)
    plt.scatter(X,Y, alpha=0.5)
    plt.title("Random Attatchment Growth of 0.1 Deviation from Inital Power - 2")
    plt.ylabel("Proportional Network Size Change")
    plt.xlabel("Component attatchment")
    plt.show()

def avg_diff(values):
    start = values[0]
    end = values[-1]
    others = values[1:]
    avg = np.mean(others)
    diff = start - avg
    pcnt = (diff / start) * 100
    diff2 = start - end
    pcnt2 = (diff2 / start)*100
    return str(pcnt) + "%", str(pcnt2) + "%"



if __name__ == "__main__":
    f = str(sys.argv[1]) + ".txt"
    dat = read_file(f)
    a, b = parse_data2(dat)
    plot_deviation(a,b)