import tornado.ioloop
import tornado.web
import json
import os
import requests

staticpath = os.path.join("dist", 'static')
htmlpath = os.path.join("dist", 'index.html')
from SduCasLogin import sessions, getSessions, LTHandler,BaseHandle




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("token")
        self.render(htmlpath)


from main import rushInto, getOrderInfo, quit


class ApiHandler(BaseHandle):
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


setting = dict(
    static_path=staticpath,
    cookie_secret='sducasssssssssss',
    login_url="/",
)
def clean():
    for key in sessions.items():
        del sessions[key]
if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/api", ApiHandler),
        (r"/api/list", BookListHandler),
        (r"/api/lt", LTHandler)
    ], **setting)
    application.listen(10279)
    tornado.ioloop.PeriodicCallback(clean, 1000*60*60).start()
    tornado.ioloop.IOLoop.current().start()
