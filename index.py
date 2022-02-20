import http.server
import socketserver
import os
import urllib
import textwrap

my_port = 80


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    index_of = ('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n'
    '<html><head>\n'
    '<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n'
    '<title>Index of {abs_path}</title>\n'
    '</head>\n'
    '<body class="vsc-initialized">\n'
    '<h1>Index of {abs_path}</h1>\n'
    '<table>\n'
    '<tbody><tr><th valign="top"><img src="/icon/blank.gif" alt="[ICO]"></th><th><a href="http://event.sato-mami.com{path}?C=N;O=D">Name</a></th><th><a href="http://event.sato-mami.com{path}?C=M;O=A">Last modified</a></th><th><a href="http://event.sato-mami.com{path}?C=S;O=A">Size</a></th><th><a href="http://event.sato-mami.com{path}?C=D;O=A">Description</a></th></tr>\n'
    '<tr><th colspan="5"><hr></th></tr>\n'
    '<tr><td valign="top"><img src="/icon/back.gif" alt="[PARENTDIR]"></td><td><a href="http://event.sato-mami.com{path}../">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>\n'
    '{content}\n'
    '<tr><th colspan="5"><hr></th></tr>\n'
    '</tbody></table>\n'
    '<address>Apache/2.4.41 (Ubuntu) Server at event.sato-mami.com Port 80</address>\n\n'

    '</body></html>\n')

    index_data = {"/home/mami/valentine/":[["unknown.gif","congratulations.php","2022-02-11 21:45","84"],["unknown.gif","login.php","2022-02-11 21:45","1.8K"]],"/home/mami/":[["folder.gif","valentine/","2022-02-11 21:45","- "]],"/home/":[["folder.gif","mami/","2022-02-11 21:44","- "]],"/":[["folder.gif","bin/","2022-02-11 20:02","- "],["folder.gif","dev/","2022-02-11 01:01","- "],["folder.gif","etc/","2022-02-11 21:35","- "],["folder.gif","home/","2022-02-11 19:35","- "],["folder.gif","lib/","2022-02-11 21:11","- "],["folder.gif","lib64/","2022-02-11 00:58","- "],["folder.gif","proc/","2022-02-11 00:41","- "],["folder.gif","root/","2022-02-11 19:52","- "],["folder.gif","sbin/","2022-02-11 19:40","- "],["folder.gif","tmp/","2022-02-11 21:12","- "],["folder.gif","usr/","2022-02-11 19:40","- "]],"/etc/":[["unknown.gif","group","2022-02-11 19:53","10"],["unknown.gif","hosts","2022-02-11 21:29","251"],["unknown.gif","ld.so.cache","2022-02-11 19:53","26K"],["script.gif","ld.so.conf","2022-02-11 19:53","34"],["unknown.gif","localtime","2022-02-11 19:53","2.2K"],["unknown.gif","passwd","2022-02-11 20:04","71"],["unknown.gif","passwd-","2022-02-11 19:53","32"],["script.gif","resolv.conf","2022-02-11 19:53","738"],["unknown.gif","shadow","2022-02-11 21:35","150"],["unknown.gif","shadow-","2022-02-11 21:35","19"]]}

    index_of_dirs = ["/home/mami/valentine", "/home/mami", "/home", "/", "/etc"]
    file_tmp = """<tr><td valign="top"><img src="http://event.sato-mami.com/icon/{img}" alt="[   ]"></td><td><a href="http://event.sato-mami.com{path}{filename}">{filename}</a></td><td align="right">{date}  </td><td align="right">{size}</td><td>&nbsp;</td></tr>"""

    forbidden = ('<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">\n'
    '<html><head>\n'
    '<meta http-equiv="content-type" content="text/html; charset=windows-1252">\n'
    '<title>403 Forbidden</title>\n'
    '</head><body class="vsc-initialized">\n'
    '<h1>Forbidden</h1>\n'
    '<p>You don\'t have permission to access this resource.</p>\n'
    '<hr>\n'
    '<address>Apache/2.4.41 (Ubuntu) Server at 192.168.11.246 Port 80</address>\n'
    '\n'
    '</body></html>\n')

    notfound = ('<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">\n'
    '<html><head>\n'
    '<meta http-equiv="content-type" content="text/html; charset=windows-1252">\n'
    '<title>404 Not Found</title>\n'
    '</head><body class="vsc-initialized">\n'
    '<h1>Not Found</h1>\n'
    '<p>The requested URL was not found on this server.</p>\n'
    '<hr>\n'
    '<address>Apache/2.4.41 (Ubuntu) Server at 192.168.11.246 Port 80</address>\n'
    '\n'
    '</body></html>\n')

    login = ('<!DOCTYPE html>\n'
    '<html lang="ja">\n'
    '\n'
    '<head>\n'
    '<meta charset="UTF-8">\n'
    '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
    '<title>認証</title>\n'
    '</head>\n'
    '\n'
    '<body>\n'
    '<div style="text-align: center;">\n'
    '{message}\n'
    '<form method="post">\n'
    '<h1>パスワードを入力して認証してください。</h1>\n'
    'ユーザー名　<input type="text" placeholder="your name?" name="user"><br>\n'
    'パスワード　<input type="password" placeholder="Password" name="password"><br>\n'
    '<button style="margin-top: 12px;">Login</button>\n'
    '</form>\n'
    '</div>\n'
    '</body>\n'
    '\n'
    '</html>')

    def getContent(self):
        spath = self.path.split("?")[0]
        print(spath)
        path = os.path.normpath("/home/"+spath)
        print(path)
        if path in self.index_of_dirs:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            p = path.rstrip("/") + "/"
            print(p)
            content = ""
            for i in self.index_data[p]:
                print(i)
                content += self.file_tmp.format(img=i[0], path=spath, filename=i[1], date=i[2], size=i[3])
            
            html = self.index_of.format(path=spath.rstrip("/") + "/", abs_path=p, content=content)
            if path == "/":
                html = html.replace('<tr><td valign="top"><img src="/icon/back.gif" alt="[PARENTDIR]"></td><td><a href="http://event.sato-mami.com/../../">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>\n', '')
            return bytes(html, "utf-8")

        if path.split("/")[1] in ["/bin", "/dev", "/lib", "/lib64", "/proc", "/root", "/sbin", "/tmp", "/usr"]:
            self.send_response(403)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            return bytes(self.forbidden, "utf-8")

        if path == "/home/mami/valentine/login.php":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            return bytes(self.login.format(message=""), "utf-8")
        
        if path == "/home/mami/valentine/congratulations.php":
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            return bytes("", "utf-8")
        
        if path == "/etc/group":
            return b"root:x:0:\n"
        if path == "/etc/hosts":
            return ("127.0.0.1 localhost\n"
            "127.0.1.1 ubuntu\n"
            "\n"
            "160.251.23.81 admintool.mami\n"
            "\n"
            "# The following lines are desirable for IPv6 capable hosts\n"
            "::1     ip6-localhost ip6-loopback\n"
            "fe00::0 ip6-localnet\n"
            "ff00::0 ip6-mcastprefix\n"
            "ff02::1 ip6-allnodes\n"
            "ff02::2 ip6-allrouters\n").encode()
        if path == "/etc/ld.so.conf":
            return b"include /etc/ld.so.conf.d/*.conf\n"
        if path == "/etc/passwd":
            return ("root:x:0:0:root:/root:/bin/bash\n"
            "mami:x:1000:1000::/home/mami:/bin/bash\n").encode()
        if path == "/etc/passwd-":
            return b"root:x:0:0:root:/root:/bin/bash\n"
        if path == "/etc/resolv.conf":
            return ("# # This file is managed by man:systemd-resolved(8). Do not edit.\n"
            "#\n"
            "# This is a dynamic resolv.conf file for connecting local clients to the\n"
            "# internal DNS stub resolver of systemd-resolved. This file lists all\n"
            "# configured search domains.\n"
            "#\n"
            '# Run "resolvectl status" to see details about the uplink DNS servers\n'
            "# currently in use.\n"
            "#\n"
            "# Third party programs must not access this file directly, but only through the\n"
            "# symlink at /etc/resolv.conf. To manage man:resolv.conf(5) in a different way,\n"
            "# replace this symlink by a static file or a different symlink.\n"
            "#\n"
            "# See man:systemd-resolved.service(8) for details about the supported modes of\n"
            "# operation for /etc/resolv.conf.\n\n"

            "options edns0\n"
            "nameserver 80.208.227.143\n"
            "nameserver 80.208.228.143\n").encode()
        if path == "/etc/shadow":
            return ("root:x:19033::::::\n"
            "mami:$6$Lsc6t8iJfxQRnWG5$sVGmKbyIQzez3DHjlZaUVrZVrpcdl/HQMm5I5mPBL53vNEMr1Y3xYZ9hdVtDfiFLK3dS.SRKglfPChFXZOPra/:19034:0:99999:7:::\n").encode()
        if path == "/etc/shadow-":
            return b"""root:x:19033::::::\n"""
        if path == "/etc/ld.so.cache":
            self.send_response(200)
            self.send_header('Content-Type', 'chemical/x-cache')
            self.end_headers()
            with open("/home/mami/etc/ld.so.cache", mode="rb") as f:
                return f.read()
        if path == "/etc/localtime":
            with open("/home/mami/etc/localtime", mode="rb") as f:
                return f.read()
        
        if spath == "/icon/folder.gif":
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            with open("icon/folder.gif", mode="rb") as f:
                return f.read()
        if spath == "/icon/script.gif":
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            with open("icon/script.gif", mode="rb") as f:
                return f.read()
        if spath == "/icon/unknown.gif":
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            with open("icon/unknown.gif", mode="rb") as f:
                return f.read()
        if spath == "/icon/back.gif":
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            with open("icon/back.gif", mode="rb") as f:
                return f.read()
        if spath == "/icon/blank.gif":
            self.send_response(200)
            self.send_header('Content-Type', 'image/gif')
            self.end_headers()
            with open("icon/blank.gif", mode="rb") as f:
                return f.read()

        self.send_response(404)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        return bytes(self.notfound, "utf-8")

    def do_GET(self):
        self.wfile.write(self.getContent())

    def do_POST(self):
        spath = self.path.split("?")[0]
        path = os.path.normpath("/home/"+spath)
        if path == "/home/mami/valentine/login.php":
            data = urllib.parse.parse_qs(self.rfile.read(int(self.headers['Content-Length'])).decode())
            print(data.get("user", "") == ["mamitantokucho"] and data.get("password", "") == ["kawaee"])
            print(data)
            if data["user"] == ["mamitantokucho"] and data["password"] == ["kawaee"]:
                self.send_response(301)
                self.send_header('Location','http://admintool.mami/')
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(self.login.format(message="<p style='color: red;font-size: 1.2rem;'>データベース上のパスワードと合致しませんでした。</p>"), "utf-8"))
        else:
            self.wfile.write(self.getContent())


my_handler = MyHttpRequestHandler
socketserver.ThreadingTCPServer.allow_reuse_address = True

with socketserver.ThreadingTCPServer(("", my_port), my_handler) as httpd:
    print("Http Server Serving at port", my_port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.socket.close()

