from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from fighters_db import FightersDB
from http import cookies
from passlib.hash import bcrypt
from session_store import SessionStore

gSessionStore = SessionStore()


class MyRequestHandler(BaseHTTPRequestHandler):

    def end_headers(self):
        self.send_cookie()
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        BaseHTTPRequestHandler.end_headers(self)

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())

    def load_session_data(self):
        self.load_cookie()
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            self.sessionData = gSessionStore.getSessionData(sessionId)
            if self.sessionData == None:
                sessionId = gSessionStore.createSession()
                self.sessionData = gSessionStore.getSessionData(sessionId)
                self.cookie["sessionId"] = sessionId
        else:
            sessionId = gSessionStore.createSession()
            self.sessionData = gSessionStore.getSessionData(sessionId)
            self.cookie["sessionId"] = sessionId
            

    def handleNotFound(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(bytes("Not Found", "utf-8"))

    def handleFighterRetrieveMember(self, fighter_id):
        if "userID" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return

        db = FightersDB()
        fighter = db.getOneFighter(fighter_id)
        if fighter:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(fighter),"utf-8"))
        else:
            self.handleNotFound()

    def handleFighterRetrieveCollection(self):
        if "userID" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            print("userID is not GET")
            return

        db = FightersDB()
        fighter = db.getAllFighters()

        if fighter:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(fighter), "utf-8"))
        else:
            self.handleNotFound()


        # self.send_response(200)
        # self.send_header("Content-Type", "application/json")
        # self.end_headers()
        # db = FightersDB()
        # self.wfile.write(bytes(json.dumps(db.getAllFighters()), "utf-8"))

    def handleFighterCreate(self):
        if "userID" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            print("userID is non-existing in fighterCreate")
            return

        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the RAW body:", body)
        parsed_body = parse_qs(body)
        print("the PARSED body:", parsed_body)

        name = parsed_body["name"][0]
        color = parsed_body["color"][0]
        style = parsed_body["style"] [0]
        stock = parsed_body["stock"] [0]
        hp = parsed_body["hp"] [0]

        db = FightersDB()
        db.insertFighter(name, color, style, stock, hp)

        self.send_response(201)
        self.end_headers()
        
    def handleFighterDeleteMember(self, fighter_id):
        if "userID" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return

        db = FightersDB()
        db.deleteFighter(fighter_id)

        self.send_response(200)
        self.end_headers()


    def handleFighterUpdateMember(self, fighter_id):
        if "userID" not in self.sessionData:
            self.send_response(401)
            self.end_headers()
            return

        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        print("the RAW body:", body)

        parsed_body = parse_qs(body)
        print("the PARSED body:", parsed_body)

        name = parsed_body["name"][0]
        color = parsed_body["color"][0]
        style = parsed_body["style"] [0]
        stock = parsed_body["stock"] [0]
        hp = parsed_body["hp"] [0]

        db = FightersDB()
        db.updateFighter(name, color, style, stock, hp, fighter_id )


        self.send_response(200)
        self.end_headers()

    def handleUserCreate(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode("utf-8")
        pars_body = parse_qs(body)
        print("Parsed body:", pars_body)

        first_name = pars_body["first_name"] [0]
        last_name = pars_body["last_name"] [0]
        email = pars_body["email"] [0]   
        password = pars_body["password"] [0]

        db = FightersDB()
        user = db.getUserEmail(email)

        if user == None:
            hash_pass = bcrypt.hash(password)
            db = FightersDB()
            db.registerUser(first_name, last_name, email, hash_pass)
            user = db.getUserEmail(email)
            
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(422)
            self.end_headers()

    def handleSessionCreate(self):
        length = self.headers["Content-Length"]
        body = self.rfile.read(int(length)).decode('utf-8')

        pars_body = parse_qs(body)
        email = pars_body['email'][0]
        user_password = pars_body['password'][0]

        db = FightersDB()
        user = db.getUserEmail(email)
        print(user)
       

        if user != None:
            if bcrypt.verify(user_password, user['password']):
                self.sessionData['userID'] = user['id']
                self.send_response(201)
                self.end_headers()
            else:
                self.send_response(401)
                self.end_headers()
        else:
            self.send_response(401)
            self.end_headers()

    def do_OPTIONS(self):
        self.load_session_data()
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "OPTIONS, GET, POST, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.load_session_data()
        path_parts = self.path.split("/")
        resource = path_parts[1]
        if len(path_parts) > 2:
            identifier = path_parts[2]
        else:
            identifier = None

        if resource == "fighters" and identifier == None:
            self.handleFighterRetrieveCollection()
        elif resource == "fighters" and identifier != None:
            self.handleFighterRetrieveMember(identifier)
        else:
            self.handleNotFound()
    
    def do_POST(self):
        self.load_session_data()
        if self.path == "/fighters":
            self.handleFighterCreate()
        elif self.path == "/users":
            self.handleUserCreate()
        elif self.path == "/sessions":
            self.handleSessionCreate()
        else:
            self.handleNotFound()

    def do_DELETE(self):
        self.load_session_data()
        path_parts = self.path.split("/")
        resource = path_parts[1]
        if len(path_parts) > 2:
            identifier = path_parts[2]
        else:
            identifier = None

        if resource == "fighters" and identifier != None:
            self.handleFighterDeleteMember(identifier)
        else:
            self.handleNotFound()

    def do_PUT(self):
        self.load_session_data()
        path_parts = self.path.split("/")
        resource = path_parts[1]
        if len(path_parts) > 2:
            identifier = path_parts[2]
        else:
            identifier = None

        if resource == "fighters" and identifier != None:
            self.handleFighterUpdateMember(identifier)
        else:
            self.handleNotFound()
        
        
def run():
    listen = ("127.0.0.1", 8080)
    server = HTTPServer(listen, MyRequestHandler)

    print("Listening...")
    server.serve_forever()

run()

