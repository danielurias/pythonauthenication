import base64
import os


class SessionStore:

    def __init__(self):
        self.sessions = {}

    def getSessionData(self, sessionId):
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None

    def createSession(self):
        sessionId = self.generateSessionId()
        self.sessions[sessionId] = {}
        return sessionId
        

    def generateSessionId(self):
        rnum = os.urandom(32)
        rstr = base64.b64encode(rnum).decode("utf-8")
        return rstr