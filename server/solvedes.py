import execjs

with open("des.js")as f:
    js = f.read()
js = execjs.compile(js)
userid = "201705130120"
passwd = "Wangzixi1108"
lt="LT-2736599-cEhQhV61SopddODFug5wBgWuVgrdlu-cas"
rsa = js.call("strEnc", userid + passwd + lt, "1", "2", "3")
print(rsa)