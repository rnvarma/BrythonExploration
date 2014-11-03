# basicServer.py | Carnegie Mellon University 15-112
# Author: Rohan Varma 11/3/14
# 
# Simple HTTP Server to relay messages back and forth between clients
# 
# This code is intended to be used as a server framwork for 15-112 
# students to send messages between different brython based clients. 
# In order to use the framwork, the students must inherit the
# ServerFramework class and then override the onPostRequest(data)
# and onGetRequest() methods. Run the server by calling the 
# run method on the ServerFramework instance 

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import urlparse, json


PORT_NUMBER = 8080

class ServerFramework(BaseHTTPRequestHandler):

  def do_GET(self):
    # basing get handler - overrides BaseHTTPRequestHandler
    returnData = self.onGetRequest(self)
    returnData = returnData if returnData else "hello world"
    # executing protocol to allow CORS (cross-origin resource sharing)
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
    self.send_header("Access-Control-Allow-Headers", "Content-Type");
    self.end_headers()
    # send data back to client
    self.wfile.write(returnData)
    return

  def do_POST(self):
    # basic post handler - overrides BaseHTTPRequestHandler
    # next two lines adapted from stackoverflow to convert post data to dictionary
    length = int(self.headers['Content-Length'])
    postData = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
    returnData = self.onPostRequest(postData)
    # executing protocol to allow CORS (cross-origin resource sharing)
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS");
    self.send_header("Access-Control-Allow-Headers", "Content-Type");
    self.end_headers()
    # send response back to client
    self.wfile.write(returnData)
    retun

  def initServer(self):
    # used to initialize things like persistent variables for storage purposes
    pass

  def onPostRequest(self, data): 
    # called on post requests
    # data : dictionary representing dictionary object sent from client
    # returns : a string message to be sent back as a result of the post request
    return ""

  def onGetRequest(self):
    # called on get requests to server
    # returns : a string message to be sent back to the client

  def run(self, PORT_NUMBER = 8080):
    self.initServer()
    self.server = HTTPServer(("", PORT_NUMBER), ServerFramework)
    self.server.serve_forever()
