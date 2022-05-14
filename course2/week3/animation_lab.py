import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14,20, 10000)

raw = [x1, x2, x3, x4]

trials = [random.randint(100, 1000) for _ in range(4)]
trial_max = max(trials)
buckets = [[] for _ in range(4)]
print(trial_max)

def update(curr):
    if trial_max == curr:
        a.event_source.stop()
    plt.cla()
    plt.suptitle('Sample Frequency')
    plt.title('Sample Frequency')
    ax1 = plt.subplot(1, 4, 1)
    ax1.set_title('Normal')
    ax2 = plt.subplot(1, 4, 2)
    ax2.set_title('Gamma')
    ax3 = plt.subplot(1, 4, 3)
    ax3.set_title('Exponential')
    ax4 = plt.subplot(1, 4, 4)
    ax4.set_title('Uniform')
    for index, val in enumerate(trials):
        if trials[index] > 0:
            trials[index] = trials[index] - 1
            buckets[index].append(raw[index][random.randrange(10000)])

    for i in range(4):
        plt.subplot(1, 4, i+1)
        plt.hist(buckets[i], bins=20, alpha=0.5)

fig = plt.figure()
a = animation.FuncAnimation(fig, update, interval=1)
plt.show()

