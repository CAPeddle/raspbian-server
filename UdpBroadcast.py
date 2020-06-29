import socket
import time
import fcntl
import struct
import threading

class UdpBroadcast(threading.Thread):
    def __init__(self, name, debug=False): 
        threading.Thread.__init__(self)
        self._debug = debug
        self._running = True    
        self._localIp = self.get_local_ip_address()
        if (self._debug):
            print("Local Address %s" % (self._localIp))

    def stop(self):
        if (self._debug):
            print ("Received stop")
        self._running = False

    def get_local_ip_address(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(2)
            try:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
            except socket.timeout:
                return "0.0.0.0"

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as server:
            # self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

            # Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
            # Do not use socket.SO_REUSEADDR except you using linux(kernel<3.9): goto https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ for more information.
            # For linux hosts all sockets that want to share the same address and port combination must belong to processes that share the same effective user ID!
            # So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
            # Thanks to @stevenreddie
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

            # Enable broadcasting mode
            server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

            # Set a timeout so the socket does not block
            # indefinitely when trying to receive data.
            server.settimeout(0.2)
            message = bytes(self._localIp, 'utf-8')
            try:
                if (self._debug):
                    print("Starting broadcast")
                while self._running:                      
                    server.sendto(message, ("<broadcast>", 37020))
                    if (self._debug):
                        print("message sent {}".format(message))
                    time.sleep(1)
                print("Broadcast Stopped Running")                
                exit()

            except KeyboardInterrupt:
                print("Broadcast received Keyboardinterupt")
                self.stop()
                pass

            except Exception as e:
                print ("\nProgram end")

                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)

                exit()


if __name__ == '__main__':
    udpbroadcast = UdpBroadcast(True)
    try:
        print ("Starting Thread")
        udpbroadcast.start()
        while True:
            time.sleep(0.02)
            pass

    except KeyboardInterrupt:        
        print("Outter Keyboardinterupt to exit")
        udpbroadcast.stop()        
        pass
    
    print("exit main")
    udpbroadcast.join()