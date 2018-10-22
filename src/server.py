import socketserver as SocketServer
import hashlib
import base64

WS_MAGIC_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
BUF_LEN = 1024
OP_TEXT = 129  # \x81
OP_CLOSE = 136  # \x88


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(BUF_LEN).strip().decode('utf-8')
        headers = self.data.split("\r\n")

        # is it a websocket request?
        if "Connection: Upgrade" in self.data and "Upgrade: websocket" in self.data:
            # getting the websocket key out
            for h in headers:
                if "Sec-WebSocket-Key" in h:
                    key = h.split(" ")[1]
            # let's shake hands shall we?
            self.shake_hand(key)

            while True:
                frame = ''
                payload = bytearray()
                decoded_payload = ''
                try:
                    frame = self.request.recv(BUF_LEN).strip()
                    # print("in_data : %s" % frame)
                    # print("FIN : %s" % frame[0])

                    if len(frame) < 1:
                        print("Empty data error. Close connection")
                        return

                    if frame[0] == OP_CLOSE:
                        print("Connection closed by client")
                        return

                    if frame[0] != OP_TEXT:
                        print("Wrong packet opcode: %s. Close connection" % frame[0])
                        return

                    payload = self.decode_frame(bytearray(frame))
                    if len(payload) < 1:
                        continue

                    decoded_payload = payload.decode('utf-8').strip()
                    b = "{0:08b}".format(int(decoded_payload))

                    self.send_frame(bytearray(b.encode()))  # response to message
                    if "bye" == decoded_payload.lower():
                        "Bidding goodbye to our client..."
                        return
                except Exception as exp:
                    print("Error: %s\r\n%s\r\n%s" % (exp, frame, payload))
                    return

        else:
            self.request.sendall("HTTP/1.1 400 Bad Request\r\n" + \
                                 "Content-Type: text/plain\r\n" + \
                                 "Connection: close\r\n" + \
                                 "\r\n" + \
                                 "Incorrect request")

    def shake_hand(self, key):
        # calculating response as per protocol RFC
        key = key + WS_MAGIC_STRING
        resp_key = base64.standard_b64encode(hashlib.sha1(key.encode('utf-8')).digest())

        resp = "HTTP/1.1 101 Switching Protocols\r\n" + \
               "Upgrade: websocket\r\n" + \
               "Connection: Upgrade\r\n" + \
               "Sec-WebSocket-Accept: %s\r\n\r\n" % resp_key.decode('utf-8')

        self.request.sendall(resp.encode('utf-8'))

    def decode_frame(self, frame):
        length = frame[1] & 127  # may not be the  actual length in the two special cases

        index_first_mask = 2  # if not a  special case

        if length == 126:  # if a special case, change indexFirstMask
            index_first_mask = 4

        elif length == 127:  # ditto
            index_first_mask = 10

        masks = frame[index_first_mask: 4 + index_first_mask]  # four bytes starting from indexFirstMask

        index_first_data_byte = index_first_mask + 4  # four bytes further

        real_length = len(frame) - index_first_data_byte  # length of real data
        encrypted_payload = frame[index_first_data_byte: index_first_data_byte + real_length]

        decoded = bytearray([encrypted_payload[i] ^ masks[i % 4] for i in range(real_length)])

        return decoded

    def send_frame(self, payload):
        # setting fin to 1 and opcpde to 0x1
        frame = [129]
        # adding len. no masking hence not doing +128
        frame += [len(payload)]
        # adding payload
        frame_to_send = bytearray(frame) + payload

        self.request.sendall(frame_to_send)


if __name__ == "__main__":
    server_address = ("0.0.0.0", 46464)
    server = SocketServer.TCPServer(server_address, MyTCPHandler)
    try:
        server.serve_forever(5)
    except KeyboardInterrupt:
        pass
        server.server_close()