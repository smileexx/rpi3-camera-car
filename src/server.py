from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json


class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        print(self.data)
        data = json.loads(self.data)
        newData = {}
        for k, v in data.items():
            if v:
                newData[k] = v

        print(newData)
        self.sendMessage(json.dumps(newData))

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, SimpleEcho)
server.serveforever()
