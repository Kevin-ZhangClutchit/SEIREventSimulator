import random
import matplotlib.pyplot as plt
import os

ir_rate_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
ei_rate_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6]
se_rate_list = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]


def plot_ir_rate(x_list, y_list, save=False,
                 show=True,
                 save_dir='parameters/'):
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x_list) + 0.05)
    ylim = max(y_list) * 1.1
    ylim_low = 0
    ax.set_ylim(ylim_low, ylim)
    plt.xlabel('ir_rate')
    plt.ylabel('Days to Recover')
    plt.plot(x_list, y_list, marker='o', label='ir_rate', color="#1f78b4")
    ax.hlines([6, 7], 0, max(x_list) + 0.05,
              linestyles='dashed', colors=['#1f78b4', '#1f78b4'])
    plt.legend()

    # save figure
    if save:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_fn = save_dir + 'ir_rate_simulation.png'
        plt.savefig(save_fn)

    if show:
        plt.show()
    else:
        plt.close()


def plot_ei_rate(x_list, y_list, save=False,
                 show=True,
                 save_dir='parameters/'):
    fig, ax = plt.subplots()
    ax.set_xlim(0, max(x_list) + 0.05)
    ylim = max(y_list) * 1.1
    ylim_low = 0
    ax.set_ylim(ylim_low, ylim)
    plt.xlabel('ei_rate')
    plt.ylabel('Days to have symptom (test positive) ')
    plt.plot(x_list, y_list, marker='o', label='ei_rate', color="#1f78b4")
    ax.hlines([2, 4], 0, max(x_list) + 0.05,
              linestyles='dashed', colors=['#1f78b4', '#1f78b4'])
    plt.legend()

    # save figure
    if save:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_fn = save_dir + 'ei_rate_simulation.png'
        plt.savefig(save_fn)

    if show:
        plt.show()
    else:
        plt.close()


def plot_se_rate(x_list, y_list, save=False,
                 show=True,
                 save_dir='parameters/'):
    fig, ax = plt.subplots()
    ax.set_xlim(min(x_list) - 0.05, max(x_list) + 0.05)
    ylim = max(y_list) * 1.1
    ylim_low = min(y_list) * 0.9
    ax.set_ylim(ylim_low, ylim)
    plt.xlabel('se_rate')
    plt.ylabel('Approximate r0 value')
    plt.plot(x_list, y_list, marker='o', label='ei_rate', color="#1f78b4")
    ax.hlines([17, 19], 0, max(x_list) + 0.05,
              linestyles='dashed', colors=['#1f78b4', '#1f78b4'])
    plt.legend()

    # save figure
    if save:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_fn = save_dir + 'se_rate_simulation.png'
        plt.savefig(save_fn)

    if show:
        plt.show()
    else:
        plt.close()


nodes_num = 50000

y_list = []
'''
#Follow are ir_rate parameter selection codes:

for ir_rate in ir_rate_list:
    recover_days_cnt = 0
    for i in range(0, nodes_num):
        current = 0
        while True:
            current += 1
            rn = random.randint(0, 100) / 100
            if rn < ir_rate:
                break
        recover_days_cnt += current
    y_list.append(recover_days_cnt/nodes_num)

print(y_list)
plot_ir_rate(ir_rate_list,y_list,show=False,save=True)

#Follow are ei_rate selection
for ei_rate in ei_rate_list:
    recover_days_cnt = 0
    for i in range(0, nodes_num):
        current = 0
        while True:
            current += 1
            rn = random.randint(0, 100) / 100
            if rn < ei_rate:
                break
        recover_days_cnt += current
    y_list.append(recover_days_cnt/nodes_num)

print(y_list)
plot_ei_rate(ei_rate_list,y_list,show=False,save=True)
'''
# Follow are for se_rate
for se_rate in se_rate_list:
    infected_cnt = 0
    for i in range(0, nodes_num):
        current = 0
        for j in range(0, 30):
            rn = random.randint(0, 100) / 100
            if current <= 10:
                if rn < se_rate:
                    current += 1
            else:
                if rn < se_rate * pow((10 / current), 2):
                    current += 1
        infected_cnt += current
    y_list.append(infected_cnt / nodes_num)

print(y_list)
plot_se_rate(se_rate_list, y_list, show=False, save=True)
