import matplotlib.pyplot as plt
import numpy as np

def create_syn_graph(data_file):
    # X axis should be the time passed 
    # Y axis should be the number of packets sent until that point in time
    raw_string = ''
    with open (data_file, 'r') as f:
        raw_string = f.read()

    x_axis = []
    y_axis = []

    lines_raw_string = raw_string.splitlines()
    x_axis.append(float(lines_raw_string[0].split(',')[1]))
    y_axis.append(int(lines_raw_string[0].split(',')[0]))
    for x in range(1,len(lines_raw_string)):
        data_from_line = lines_raw_string[x].split(',')
        if len(data_from_line) == 2:
            time = data_from_line[1]
            packet_counter = data_from_line[0]
            x_axis.append(float(time) + x_axis[x-1] )
            y_axis.append(int(packet_counter) + y_axis[x-1] )
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.set_yscale('log')
    ax.set_title(data_file)
    ax.set_xlabel('Time passed in seconds')
    ax.set_ylabel('Number of packets sent')
    if '_c' in data_file:
        fig.savefig('Syn_pkts_c.png')
    else:
        fig.savefig('Syn_pkts_p.png')
    
def get_std(filename):
    time_values = []
    with open(filename, 'r') as f:
        raw = f.read()
        lines = raw.splitlines()
        for line in lines:
            data_list = line.split(',')
            if len(data_list) == 2:
                time_values.append(float(data_list[1]))


    return np.std(time_values)


# print('STD for Python - ' + str(get_std('syns_results_p.txt')))
# print('STD for C - ' + str(get_std('syns_results_c.txt')))
# create_syn_graph('syns_results_p.txt')

###########################
# Ping part of the file   #
###########################

def create_ping_graph(data_file):
    # X axis should be RTT in milliseconds
    # Y axis should number of pings.
    raw_string = ''
    with open (data_file, 'r') as f:
        raw_string = f.read()

    x_axis = []
    y_axis = []

    lines_raw_string = raw_string.splitlines()
    x_axis.append(float(lines_raw_string[0].split(',')[1]))
    y_axis.append(int(lines_raw_string[0].split(',')[0]))
    for x in range(1,len(lines_raw_string)):
        data_from_line = lines_raw_string[x].split(',')
        if len(data_from_line) == 2:
            time = data_from_line[1]
            packet_counter = data_from_line[0]
            x_axis.append(float(time) + x_axis[x-1] )
            y_axis.append(int(packet_counter) + y_axis[x-1] )
    fig, ax = plt.subplots()
    ax.plot(x_axis, y_axis)
    ax.set_yscale('log')
    ax.set_title(data_file)
    ax.set_xlabel('RTT in milliseconds')
    ax.set_ylabel('Packets by order of sending')
    if '_c' in data_file:
        fig.savefig('Pings_c.png')
    else:
        fig.savefig('Pings_p.png')

# create_ping_graph('pings_results_c.txt')
# create_ping_graph('pings_results_p.txt')
print('STD for Python - ' + str(get_std('pings_results_p.txt')))
print('STD for C - ' + str(get_std('pings_results_c.txt')))