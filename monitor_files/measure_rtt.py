import sys
import shlex  
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from datetime import datetime
def get_simple_cmd_output(cmd, stderr=STDOUT):
    """
    Execute a simple external command and get its output.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr,text=True).communicate()[0]

def get_ping_time(host):
    host = host.split(':')[0]
    cmd = "fping {host} -C 3 -q".format(host=host)
    res = [float(x) for x in get_simple_cmd_output(cmd).strip().split(':')[-1].split() if x != '-']
    if len(res) > 0:
        return sum(res) / len(res)
    else:
        return 999999


def main(dest, program_type):
    f = None
    if program_type== 'c':
        f = open('pings_results_c.txt', 'a')
    else:
        f = open('pings_results_p.txt', 'a')        
    pings_checks = 0
    avg = 0
    try:
        while(True):
            pings_checks +=1
            rtt_seconds = get_ping_time(dest)
            f.write(f'{pings_checks}, {rtt_seconds}\n')
            avg += rtt_seconds
            sleep(5)
    except KeyboardInterrupt:
        avg /= pings_checks
        f.write(f'Average: {avg}')
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write(f'\nFinishing time: {current_time}')
        f.close()

# usage : python3.8 measure_rtt.py <IP> <c/p>
if len(sys.argv) != 3:
    print('usage : python3.8 measure_rtt.py <IP> <c/p>\nc/p - p for python, c for C\n')
else:
    main(sys.argv[1], sys.argv[2])
    



