import requests
import json
import bs4



def startUp(session=None) -> str:
    if session is None:
        session =requests.session()
    url = "http://seat.lib.sdu.edu.cn/home/book/index"
    r = session.get(url)

    url = "http://seat.lib.sdu.edu.cn/cas/index.php?callback=http://seat.lib.sdu.edu.cn/home/book/index"
    headers = {
        "Referer": "http://seat.lib.sdu.edu.cn/home/book/index"
    }
    r = session.get(url=url, headers=headers)
    ## 302重定向的url
    url = r.url
    #预计是下面这个链接
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


def getCanUseTime():
    url = "http://seat.lib.sdu.edu.cn/home/book/more/lib/17/type/4"
    r = requests.get(url=url)
    html = r.text
    html = bs4.BeautifulSoup(html, "html.parser")
    panels = html.find_all(name="div", attrs={"class": "x_panel visible-xs visible-sm"})
    urls = []
    baseurl = "http://seat.lib.sdu.edu.cn"
    for div in panels:
        herf = div.find(name="a")
        if herf:
            times = div.find_all(name="span", attrs={"style": "font-size:16px; color:#000;"})
            urls.append({
                "link": baseurl + herf.attrs["href"],
                "timeStart": times[0].string,
                "timeEnd": times[1].string
            })
    return urls


def loginCas(session, data, loginhtml):
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
    print(headers)
    print(url)
    print(data)
    print(r.url)
    url = r.url
    r = session.get(url=url, headers=headers)
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


def rushInto(session, url):
    oldurl = url
    timeid = url.split("act_id/")[1].split("/type")[0]
    url = f"http://seat.lib.sdu.edu.cn/api.php/activities/{timeid}/application2"
    params = {
        "mobile": 13130245131,
        "id": timeid
    }
    headers = {
        "Referer": oldurl,
        "Host": "seat.lib.sdu.edu.cn",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6",
    }
    r = session.get(url=url, params=params, headers=headers)
    return r.text


def quit(session, url):
    oldurl = url
    timeid = url.split("act_id/")[1].split("/type")[0]
    url = f"http://seat.lib.sdu.edu.cn/api.php/activities/{timeid}/quit"
    params = {
        "id": timeid
    }
    headers = {
        "Referer": oldurl,
        "Host": "seat.lib.sdu.edu.cn",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6",
    }
    r = session.get(url=url, params=params, headers=headers)
    return r.text


def getOrderInfo(session):
    url = "http://seat.lib.sdu.edu.cn/user/index/activity2"
    headers = {
        "Referer": "http://seat.lib.sdu.edu.cn/book/notice/act_id/6794/type/4/lib/17"
    }
    r = s.get(url=url, headers=headers)
    # print(r.text)
    return r.text


def getAllBook(session):
    url = "http://seat.lib.sdu.edu.cn/user/index/book"
    headers = {
        "Referer": "http://seat.lib.sdu.edu.cn/home/web/index"
    }
    r = s.get(url=url, headers=headers)
    print(r.text)


if __name__ == '__main__':
    # res = login(123, "***")
    s = requests.session()

    html = startUp(s)
    # print(html)
    html = bs4.BeautifulSoup(html, "html.parser")
    ans = html.find(id="lt")
    lt = ans.attrs["value"]
    import execjs

    with open("des.js")as f:
        js = f.read()
    js = execjs.compile(js)
    ####!!!!!!!!!!!!用户名和密码!!!!!!!!
    userid = ""
    passwd = ""
    rsa = js.call("strEnc", userid + passwd + lt, "1", "2", "3")
    headers = {
        "Referer":     "http://pass.sdu.edu.cn/cas/login?service=http%3A%2F%2Fseat.lib.sdu.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Fseat.lib.sdu.edu.cn%2Fbook%2Fnotice%2Fact_id%2F6668%2Ftype%2F4%2Flib%2F17&skipWechat=true"

    }
    data = {
        "rsa": rsa,
        "ul": len(userid),
        "pl": len(passwd),
        "lt": lt,
        "execution": "e1s1",
        "_eventId": "submit",
    }

    form = html.find(id="loginForm")
    formurl = form.attrs['action']

    baseurl = "http://pass.sdu.edu.cn"
    url = baseurl + formurl
    r = s.post(url=url, headers=headers, data=data)
    print(headers)
    print(url)
    print(data)
    print(r.url)
    url = r.url
    r = s.get(url=url, headers=headers)
    set_cookie = r.headers["Set-Cookie"]
    # print(set_cookie)
    cookies = list(map(lambda x: x.split(";")[0].split("="), set_cookie.split(",")))

    # 登录结束
    exit(0)

    url = "http://seat.lib.sdu.edu.cn/home/book/more/lib/17/type/4"
    r = s.get(url=url)
    html = r.text
    html = bs4.BeautifulSoup(html, "html.parser")
    panels = html.find_all(name="div", attrs={"class": "x_panel visible-xs visible-sm"})
    urls = []
    baseurl = "http://seat.lib.sdu.edu.cn"
    for div in panels:
        herf = div.find(name="a")
        if herf:
            times = div.find_all(name="span", attrs={"style": "font-size:16px; color:#000;"})
            urls.append({
                "link": baseurl + herf.attrs["href"],
                "timeStart": times[0].string,
                "timeEnd": times[1].string
            })
    # print(panels)
    print(urls)
    url = urls[0]["link"]
    timeid = url.split("act_id/")[1].split("/type")[0]
    print(timeid)
    url = f"http://seat.lib.sdu.edu.cn/api.php/activities/{timeid}/application2"
    url2 = f"http://seat.lib.sdu.edu.cn/api.php/activities/{timeid}/quit"

    params = {
        "mobile": 13130245131,
        "id": timeid
    }
    headers = {
        "Referer": urls[0]["link"],
        "Host": "seat.lib.sdu.edu.cn",
        "Proxy-Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8,zh-TW;q=0.7,en-US;q=0.6",
    }
    r = s.get(url=url, params=params, headers=headers)
    print(r.text)
