import tornado.ioloop
import tornado.web
import json
import os
import requests

staticpath = os.path.join("dist", 'static')
htmlpath = os.path.join("dist", 'index.html')
sessions = {}


def getToken(self):
    return self.xsrf_token.split(b"|")[-1]

def newSession(self):
    token = getToken(self)
    sessions[token]=requests.session()
    s = sessions.get(token)
    return s
def getSessions(self):
    token = getToken(self)
    sessions.setdefault(token, requests.session())
    s = sessions.get(token)
    return s


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(htmlpath)


from main import rushInto, getOrderInfo, quit


class ApiHandler(tornado.web.RequestHandler):
    def post(self):
        js = json.loads(self.request.body)
        session = getSessions(self)
        if js.get("op") == 'rush':
            res = rushInto(session, js.get("link"))
            self.write(res)
        elif js.get("op") == 'list':
            res = getOrderInfo(session)
            self.write("")
        elif js.get("op") == 'quit':
            res = quit(session, js.get("link"))
            self.write(res)
        pass
        # self.write("就这?")


from main import getCanUseTime


class BookListHandler(tornado.web.RequestHandler):
    def get(self):
        js = getCanUseTime()
        # print(js)
        self.write(json.dumps(js))


from main import getLT, loginCas


class LTHandler(tornado.web.RequestHandler):
    loginHtml = {}

    def get(self):
        print("getLt")
        session = newSession(self)
        lt, html = getLT(session)
        self.loginHtml[getToken(self)] = html
        self.write(lt)

    def post(self):
        print("postLt")
        session = getSessions(self)

        js = json.loads(self.request.body)
        # print(js)
        res = loginCas(session, js, self.loginHtml.get(getToken(self)))
        if "auto_user_check" in res.url:
            self.write("success")
        else:
            self.write("false")



setting = dict(
    static_path=staticpath,
)
if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api", ApiHandler),
        (r"/api/list", BookListHandler),
        (r"/api/lt", LTHandler)
    ], **setting)
    application.listen(10279)
    tornado.ioloop.IOLoop.current().start()
