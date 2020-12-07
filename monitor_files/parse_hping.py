from time import sleep
import sys
def parse(hping_output):
    """
    This method will parse the output of hping
     and reformat it according to the assignment


    Args:
        hping_output (file): File containing plain text
    """ 
    with open(hping_output, 'r') as f:
        ping_values = []
        raw = f.read()
        raw_lines = raw.splitlines()
        for line in raw_lines:
            index_begin = line.find('rtt=')
            index_end = line[index_begin:].find('ms')
            if index_begin != -1 and index_end != -1:
                rtt_val = line[index_begin+4:index_begin + index_end]
                ping_values.append(rtt_val)
                
    return ping_values
                
def create_report(hping_output):
    pings_list = parse(hping_output)
    
    sum_of_pings = 0
    for ping in pings_list:
        sum_of_pings+= float(ping)
    try:
        avg_ping = sum_of_pings/len(pings_list)
    except ZeroDivisionError:
        print("No pings captured!\n")
        exit(1)
    code_lang = input("Which programming language was it? Type c or p\n").strip()
    if code_lang != 'c' and code_lang != 'p':
        print("Wrong input of programming language")
        print('You gave ' + code_lang + ', Length is '+ str(len(code_lang)))
        exit(1)
    output_file = 'pings_results_'+code_lang+'.txt'    
    with open(output_file, 'w') as f:
        for x in range(len(pings_list)):
            f.write(f'{x},{pings_list[x]}\n')
        f.write(f'Average ping RTT: {avg_ping}')


create_report(sys.argv[1])