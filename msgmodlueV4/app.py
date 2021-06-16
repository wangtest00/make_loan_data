import json
import tornado.web
import tornado.ioloop

LOGIN = False  # 是否登录


def fib(n):
    """计算斐波那契数列的第n项"""
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        body = self.request.body
        body = json.loads(body)
        username = body.get("username")
        password = body.get("password")
        if username == "foo" and password == "bar":
            global LOGIN
            LOGIN = True
            self.write("Welcome!")
        else:
            self.set_status(400)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        if LOGIN:
            self.write("Hello World!")
        else:
            self.set_status(400)


class ItemHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument("id")
        id = int(id)
        self.write(str(fib(id)))


if __name__ == "__main__":
    print("http://localhost:8888")
    app = tornado.web.Application([
        (r"/login", LoginHandler),
        (r"/hello", IndexHandler),
        (r"/world", IndexHandler),
        (r"/item", ItemHandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()