import tornado.ioloop
import tornado.web
import asyncio
import json


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello this is a python command executed from backend")


class listRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class queryParamRequestHandler(tornado.web.RequestHandler):
    # http://localhost:8882/isEven?num=3
    def get(self):
        num = self.get_argument("num")

        if num.isdigit():
            r = "odd" if int(num) % 2  else "even"
            self.write(f"{num} is {r} number")
        else:
            self.write(f"{num} is not a valid integer")


class resourceParamRequestHandler(tornado.web.RequestHandler):
    def get(self, studentName, courseId):
        self.write(f"hello {studentName} your are visiting course {courseId} ")


class fruitLisRequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def get(self):
        fh = open("fruitList.txt", "r")
        fruits = fh.read().splitlines()
        fh.close()

        self.write(json.dumps(fruits))

    def post(self):
        fh = open("fruitList.txt", "a")
        fruit = self.get_argument("fruit")
        fh.write(f"{fruit}\n")
        fh.close()

        self.write(json.dumps({"message":"fruit hasbeen added to list successfully"}))

class mainRequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.render("main.html")

class uploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("imgindex.html")

    def post(self):
        fileList = self.request.files["imgFile"]
        for f in fileList:
            fh = open(f"img/{f.filename}","wb")
            fh.write(f.body)
            fh.close()
        self.write(f"http://localhost:8882/img/{f.filename}")
        


if __name__=="__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/animal", listRequestHandler),
        (r"/isEven", queryParamRequestHandler),
        (r"/students/([a-z]+)/([0-9])+", resourceParamRequestHandler),
        (r"/fruitLst", fruitLisRequestHandler),

        (r"/main", mainRequestHandler),

        (r"/img/(.*)", tornado.web.StaticFileHandler, {"path" : "img"}),
        (r"/uploadimg", uploadHandler),
    ])

    port = 8882
    app.listen(port)
    print(f"Application is ready and listening on port {port}")

    tornado.ioloop.IOLoop.current().start()
