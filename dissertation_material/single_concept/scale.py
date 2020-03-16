import collections
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.optimize import curve_fit
import powerlaw

#seed = 1234

def gen_BA(n, m, seed=None):
    G = nx.barabasi_albert_graph(n, m, seed)
    return G
#n = 1000
m = 2
#test = gen_BA(n, m, )

def distribution(graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    return deg, cnt
#print(degree_sequence)

def plot_dist(graph):
    deg, cnt = distribution(graph)
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    
    plt.show()
    return 1


def fit(x, y, pinit=None, bounds=(-np.inf, np.inf)):
    bounds = ((170000,2), (np.inf,3))
    pinit = [200000, 2.5]
    def func(x, a, b):
        return a * (x**(-b))
    popt, pcov = curve_fit(func, x, y,bounds=bounds, p0=pinit, maxfev=20000, method='trf')
    return popt, pcov

def log_fit(x, y):
    t = np.log10(x)
    def func(t, a, b):
        return a + (b * t)
    popt, pcov = curve_fit(func, t, y)

    return popt, pcov

def powerlaw_fit(x, y):
    fit = powerlaw.Fit(y, discrete=True, verbose=False)
    gamma = fit.power_law.alpha + 1
    return gamma

#n = 1000
#m = 2
#test = gen_BA(n, m)
#degree, count = distribution(test)
#params = fit(degree, count)[0]
#print(params)
def gen_growth(mini, maxi, step):
    gamma = []
    size = []
    for i in range(mini, maxi, step):
        G = gen_BA(i, m)
        degree, count = distribution(G)
        params = fit(degree, count)[0]
        size.append(i)
        print(params[1])
        gamma.append(params[1])
    return gamma, size

#start = 1000
#fin = 20000
#step = 100
#gamma, size = gen_growth(start, fin, step)

#plt.ylim(0,3)
#plt.plot(size, gamma)
#plt.show()