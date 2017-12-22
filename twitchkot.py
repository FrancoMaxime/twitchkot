import web
import subprocess
import os
import signal
import threading


render = web.template.render('templates/', base='layout')
nameplayer = "livestreamer"


urls = (
    '/', 'Index',
    '/index', 'Index',
)

player = None

class Index:

    def GET(self):
        name = 'bob'
        return render.index(name)

    def POST(self):
        data = web.input(placeImg={})
        method = data.get("method", "malformed")
        if 'channel' in data :
            channel = data['channel']
            if player == None :
                player = PlayerThread(channel)
            else:
                player.stop()
                player.channel = channel
            player.run()



class PlayerThread(threading.Thread):

    def __init__(self,channel):
        threading.Thread.__init__(self)
        self.channel = channel


    def run(self):
        command = "livestreamer -np \"omxplayer --adev local --win '35 35 1885 1045'\" --twitch-oauth-token 9g056yigicng5hgsonbakyl0ede3fd twitch.tv/"
        command = command + self.channel + " best"
        os.system(command)

    def stop(self):
        pids= map(int, subprocess.check_output(["pidof", nameplayer]).split())
        for pid in pids:
            os.kill(pid, signal.SIGKILL)




if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.debug = False
    app.run()
