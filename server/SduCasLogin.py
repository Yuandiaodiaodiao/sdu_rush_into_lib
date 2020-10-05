import tornado.web

import json
import requests

sessions = {}
import bs4


def startUp(session=None) -> str:
    if session is None:
        session = requests.session()
    # url = "http://seat.lib.sdu.edu.cn/home/book/index"
    # r = session.get(url)

    url = "http://seat.lib.sdu.edu.cn/cas/index.php?callback=http://seat.lib.sdu.edu.cn/home/book/index"
    headers = {
        "Referer": "http://seat.lib.sdu.edu.cn/home/book/index"
    }
    r = session.get(url=url, headers=headers)
    ## 302重定向的url
    url = r.url
    # 预计是下面这个链接
    # url = "http://pass.sdu.edu.cn/cas/login?service=http%3A%2F%2Fseat.lib.sdu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Fseat.lib.sdu.edu.cn%2Fbook%2Fnotice%2Fact_id%2F6668%2Ftype%2F4%2Flib%2F17&skipWechat=true"
    headers = {
        "Host": "pass.sdu.edu.cn",
    }
    r = session.get(
        url=url,
        headers=headers,
    )

    r = r.text
    return r


def getLT(session):
    ## 初始化拿到cas页面的html
    html = startUp(session)
    # print(html)
    # print(html)
    html = bs4.BeautifulSoup(html, "html.parser")
    ans = html.find(id="lt")
    # print(ans)
    lt = ans.attrs["value"]
    return lt, html


def loginCas(session, data, loginhtml):
    # 欺骗referer
    headers = {
        "Referer": 'http://pass.sdu.edu.cn:80/cas/login?service=http%3A%2F%2Fseat.lib.sdu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Fseat.lib.sdu.edu.cn%2Fhome%2Fbook%2Findex'
    }

    data["execution"] = "e1s1"
    data["_eventId"] = "submit"
    form = loginhtml.find(id="loginForm")
    formurl = form.attrs['action']
    baseurl = "http://pass.sdu.edu.cn"
    url = baseurl + formurl
    r = session.post(url=url, headers=headers, data=data)
    url = r.url
    r = session.get(url=url, headers=headers)
    return r


def getToken(self):
    return self.get_cookie("token")


def getTokenXSRF(self):
    return self.get_cookie("_xsrf")


def getSessions(self):
    token = getToken(self)
    s = sessions.setdefault(token, requests.session())
    return s


class LTHandler(tornado.web.RequestHandler):
    loginHtml = {}

    def get(self):
        print("getLt")
        self.clear_cookie("token")
        # 创建新的会话
        s = requests.session()
        # 访问cas认证网页拿到long token
        lt, html = getLT(s)
        # 保存session和html
        sessions[getTokenXSRF(self)] = s
        self.loginHtml[getTokenXSRF(self)] = html
        self.write(lt)

    def post(self):
        print("postLt")
        js = json.loads(self.request.body)
        session = sessions[getTokenXSRF(self)]
        # 拿到rsa之后走cas认证
        res = loginCas(session, js, self.loginHtml.get(getTokenXSRF(self)))
        if "auto_user_check" in res.url:
            # 304到这个url就成功了 做一个新的token表示登录进去了
            token = self.xsrf_token.decode()
            self.set_cookie("token", token)
            sessions[token] = session
            del sessions[getTokenXSRF(self)]
            print("loginsuccess")
            self.write("success")
        else:
            print("loginfalse")
            self.clear_cookie("token")
            self.write("false")


class BaseHandle(tornado.web.RequestHandler):
    # 覆盖这个函数用来确定当前用户
    def get_current_user(self):
        token = self.get_secure_cookie("token")
        if not token:
            return None
        if len(token) < 1:
            return None
        return dict(
            token=token
        )
