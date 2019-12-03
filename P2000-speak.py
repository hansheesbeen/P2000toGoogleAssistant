import sys
import pychromecast
import os
import os.path
from gtts import gTTS
import time
import hashlib
import http.server
import socketserver
from configparser import ConfigParser

parser = ConfigParser()
parser.read('settings.config')

ip           = parser.get("SETTINGS","IPDEVICE")
local_server = parser.get("SETTINGS","LOCALSERVER")
langu        = parser.get("SETTINGS","LANGUAGE")
say          = sys.argv[1];

#********* retrieve local ip
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip=s.getsockname()[0]
s.close()
#**********************

fname=hashlib.md5(say.encode()).hexdigest()+".mp3"; #create md5 filename for caching

castdevice = pychromecast.Chromecast(ip)
castdevice.wait()
vol_prec=castdevice.status.volume_level
castdevice.set_volume(0.5) #set volume 0 for not hear the BEEEP

try:
   os.mkdir(local_server)
except:
   pass

if not os.path.isfile(local_server+fname):
   tts = gTTS(say,lang=langu) #Choose language
   tts.save(local_server+fname)

mc = castdevice.media_controller
mc.play_media(local_server+fname, "audio/mp3")

mc.block_until_active()

mc.pause() #prepare audio and pause...

time.sleep(1)
castdevice.set_volume(vol_prec) #setting volume to precedent value
time.sleep(0.2)

mc.play() #play the mp3

while not mc.status.player_is_idle:
   time.sleep(0.5)

mc.stop()

castdevice.quit_app()