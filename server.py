from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import hashlib
import sqlite3

PORT = 12345


def request_parse(request):
    res = dict()
    res["type"] = request.split(":")[0]
    res["name"] = request.split(":")[1].split("&")[0]
    res["password"] = request.split(":")[1].split("&")[1]
    return res


def to_md5(password):
    return hashlib.md5(password.encode("utf-8")).hexdigest()


class ProcessClient(WebSocketServerProtocol):

    client_count = 0

    def __init__(self):
        super().__init__()
        self.is_admin = False

    def onConnect(self, request):
        self.client_count += 1
        print("Client connecting: {0}".format(request.peer))
        print(str(self.client_count) + " concurrent clients are connected")

    def onClose(self, was_clean, code, reason):
        self.client_count -= 1
        print("WebSocket connection closed: {0}".format(reason))

    def onMessage(self, data, is_binary):
        if is_binary:
            print("Can't answer to binary message")
            return
        data = data.decode("utf8")
        request = request_parse(data)
        answer = ""
        if request["type"] == "check":
            conn = sqlite3.connect("users")
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE name = ? and password = ?",
                        (request["name"], to_md5(request["password"])))
            if cur.fetchall():
                answer = "Yes!"
            else:
                answer = "No!"
            conn.close()

        elif request["type"] == "login":
            conn = sqlite3.connect("users")
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE name = ? and password = ?",
                        (request["name"], to_md5(request["password"])))
            try:
                res = cur.fetchall()[0]
                if res[1] == "Admin" and res[2] == to_md5("qwerty"):
                    self.is_admin = True
                    answer = "You are successfully logged in!"
                else:
                    answer = "Fail, name or password is incorrect!"
            except IndexError:
                answer = "Error in name or password!"
            conn.close()

        elif request["type"] == "add":
            if not self.is_admin:
                answer = "Permission denied!"
            else:
                conn = sqlite3.connect("users")
                cur = conn.cursor()
                cur.execute("SELECT * FROM users WHERE name = ? and password = ?",
                            (request["name"], to_md5(request["password"])))
                if cur.fetchall():
                    answer = "Such user already exists!"
                else:
                    cur.execute("INSERT INTO users(name, password) VALUES (?, ?)",
                                (request["name"], to_md5(request["password"])))
                    conn.commit()
                    answer = "User " + request["name"] + " added to database!"
                conn.close()

        elif request["type"] == "logout":
            if self.is_admin:
                self.is_admin = False
                answer = "You are successfully logged out!"
            else:
                answer = "Fail, you are not an admin(:"
        self.sendMessage(answer.encode('utf8'), False)
        print("Answer: ", answer)


def start():
    factory = WebSocketServerFactory(u"ws://0.0.0.0:" + str(PORT))
    factory.protocol = ProcessClient
    reactor.listenTCP(PORT, factory)
    reactor.run()

start()