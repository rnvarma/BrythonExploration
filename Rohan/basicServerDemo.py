from basicServer import BasicServer, ServerFramework

class myServer(ServerFramework):

  chatLog = []
	
  def onPostRequest(self, data):
    sender = str(data['sender'][0])
    msg = str(data['message'][0])
    myServer.chatLog.insert(0,(msg, sender))
    return "message recieved"

  def onGetRequest(self):
    final = ""
    for (msg, sender) in myServer.chatLog:
      final += sender + ":" + msg + "|"
    return final


BasicServer().run(myServer)