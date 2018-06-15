import matplotlib.pyplot as plt
import sys

import yaml
import numpy as np
import glob

# Import settings
with open("experiment_settings.yaml", "r") as f:
    parameters = yaml.load(f)

dir = ""
def main():
    global dir
    plot_type = sys.argv[1]
    if plot_type == "plot":
        dir = sys.argv[2]
        if sys.argv[3] == "all":
            # Compare all files in data folder
            # Reference: https://stackoverflow.com/questions/2225564/get-a-filtered-list-of-files-in-a-directory
            csvs = glob.glob("{}/*.csv".format(dir))
            print(csvs)
            nums = [x.replace("{}/".format(dir), "").replace(".csv", "") for x in csvs]
        else:
            nums = []
            for i in range(3, len(sys.argv)):
                nums += [sys.argv[i]]
            #print(nums)
        plot_comparison(nums)
    # elif plot_type == "plot":
    #     i = sys.argv[2]
    #     plot_csv("data/{}.csv".format(i))
    else:
        print("Command '{}' not recognized".format(plot_type))



class Data:
    def __init__(self, filename):
        tokens = []

        with open(filename, "r") as f:
            for line in f:
                tokens += [[float(i) for i in line.strip().split(",")]]

        max_pr = 1 / (parameters["num_agents"] + parameters["pr_epsilon"])

        if "anneal" in dir:
            self.x = np.asarray([z[0] for z in tokens])
        else:
            self.x = np.asarray([max_pr * z[0] / parameters["num_splits"] for z in tokens])
        self.y = np.asarray([z[1] for z in tokens])
        self.min_cis = np.asarray([z[2] for z in tokens])
        self.max_cis = np.asarray([z[3] for z in tokens])
        self.times = np.asarray([z[4] for z in tokens])

    def max_ratio(self):
        # Finds the value of i where (y[i] - y[0]) / times[i] is maximized
        i = np.argmax((self.y - self.y[0]) / self.times)
        return self.x[i], (self.y[i] - self.y[0]) / self.times[i]

# def plot_csv(filename):
#     data = Data(filename)
#     fig, ax = plt.subplots(2, 2)
#
#     ax[0, 0].plot(data.x, data.y, 'k-')
#     ax[0, 0].fill_between(data.x, data.min_cis, data.max_cis)
#     ax[0, 1].plot(data.x, data.times, 'k-')
#     ax[1, 0].plot(data.x, (data.y - data.y[0]) / data.times, 'k-')
#
#     plt.show()

def plot_comparison(nums):
    fig, ax = plt.subplots(2, 2)

    ax[0, 0].set_xlabel("max_temp")
    ax[0, 0].set_ylabel("Pr(Success | max_temp)")

    ax[0, 1].set_xlabel("max_temp")
    ax[0, 1].set_ylabel("t_p (in s)")

    ax[1, 0].set_xlabel("max_temp")
    ax[1, 0].set_ylabel("Pr(Success | max_temp) / t_p")

    ax[1, 1].set_xlabel("Number of Tasks")
    ax[1, 1].set_ylabel("argmax for p: (P(Success | p) - P(Success | 0)) / time_p")


    max_x = []
    max_y = []

    for num in nums:
        fname = "{}/{}.csv".format(dir, num)
        data = Data(fname)

        n_tasks = int(num) * int(num)
        
        ax[0, 0].plot(data.x, data.y, label="N={}".format(n_tasks))
        ax[0, 1].plot(data.x, data.times, label="N={}".format(n_tasks))
        ax[1, 0].plot(data.x, (data.y - data.y[0]) / data.times, label="N={}".format(n_tasks))
        x, y = data.max_ratio()
        max_x += [x]
        max_y += [y]

    # https://stackoverflow.com/questions/19068862/how-to-overplot-a-line-on-a-scatter-plot-in-python
    x_float = np.asarray([float(x) for x in nums])
    n_tasks = x_float ** 2
    b, m = np.polynomial.polynomial.polyfit(n_tasks, max_x, 1)
    print(x_float)
    ax[1, 1].scatter(n_tasks, max_x)
    ax[1, 1].plot(n_tasks, b + m * n_tasks, '--')

    ax[0, 0].legend()
    ax[0, 1].legend()
    ax[1, 0].legend()
    plt.show()

if __name__ == "__main__": main()