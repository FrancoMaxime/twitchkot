import web
import subprocess
import os
import signal
import threading


render = web.template.render('templates/', base='layout')
nameplayer = "livestreamer"
omxplayer = "\"omxplayer --adev local --win '35 35 1885 1045'\""
#omxplayer = "vlc"
player = None

urls = (
    '/', 'Index',
    '/index', 'Index',
)


class Index:

    def GET(self):
        return render.index()

    def POST(self):
        global player
        data = web.input(placeImg={})
        method = data.get("method", "malformed")
        if 'channel' in data :
            channel = data['channel']
            if player == None :
                player = PlayerThread(channel)
            else:
                stop_watching()
                player.channel = channel
        render.index()
        return player.run()



class PlayerThread(threading.Thread):

    def __init__(self,channel):
        threading.Thread.__init__(self)
        self.channel = channel
        self.running = False


    def run(self):
        self.running = True
        command = "livestreamer -np " + omxplayer + " --twitch-oauth-token 9g056yigicng5hgsonbakyl0ede3fd twitch.tv/"
        command = command + self.channel + " best"
        os.system(command)


def stop_watching():
    if player.running :
        player.running = False
        pids= map(int, subprocess.check_output(["pidof", omxplayer.split(' ')[0]]).split())
        for pid in pids:
            os.kill(pid, signal.SIGKILL)




if __name__ == "__main__":
    app = web.application(urls, globals())
    web.config.debug = False
    app.run()
