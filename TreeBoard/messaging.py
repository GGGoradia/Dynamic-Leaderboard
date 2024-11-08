import json
import threading
import socket
import os
from random import randint
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosed
from time import sleep

from websockets.asyncio.client import connect as aconnect
from werkzeug.serving import get_interface_ip

def read_peers():
    with open("Peerfile", "r") as fp:
        return list(map(str.strip, fp.readlines()))

# class ConnectionManager:
#     def __init__(self, peers, notifs):
#         self.peers = peers
#         self.notifs = notifs
#         self.ws = None
#         self.target = None
#         self.send_queue = 

#     def connection_loop(self):
#         self.

class MessagingTask(threading.Thread):
    def __init__(self, notifs):
        super().__init__()
        self.notifs = notifs
        self.conn = None

    def run(self):
        notifs = self.notifs
        peers = read_peers()
        add = get_interface_ip(socket.AF_INET)
        print(f"[*] Detected self as {add}", flush=True)

        selfpr = (os.cpu_count() or 0) * 512 + randint(0, 512)
        print(f"[*] Score of {add} is {selfpr}", flush=True)
        notifs.tm_update([(selfpr, add)])

        self.conn = None
        tmout = 0
        target_parent = None
        while self.conn is None:
            if target_parent is None:
                for p in peers:
                    if p.split(":")[0] == add: continue
                    try:
                        self.conn = connect(f"ws://{p}/connect")
                    except:
                        pass
            elif target_parent.add != add:
                if tmout > 3:
                    notifs.tm.remove(target_parent.add)
                    target_parent = notifs.tm.parent_of(add)
                    tmout = 0
                else:
                    try:
                        self.conn = connect(f"ws://{target_parent}/connect")
                    except:
                        pass

            if self.conn is None:
                time = min(randint(0, 1 << tmout), 900)
                print(f"{add} is idling for {time}")
                sleep(time)
                tmout += 1
            else:
                remote = self.conn.remote_address[0] + ":" + str(self.conn.remote_address[1])
                print(f"{add} is connected to {remote}", flush=True)
                tmout = 0
                print("Syncing, topology data", flush=True)
                self.conn.send(json.dumps({"op": "tm_sync", "d": notifs.tm.serialize()}))
                while True:
                    try:
                        msg = self.conn.recv(timeout=30)
                    except TimeoutError:
                        pass
                    except ConnectionClosed:
                        self.conn = None
                        break

                    notifs.handle(json.loads(msg))
                    target_parent = notifs.tm.parent_of(add)
                    cond = self.conn.remote_address[0] != target_parent.add
                    if cond:
                        self.conn.close()
                        print(f"{add} is disconnect from {remote}", flush=True)
                        self.conn = None
                        break