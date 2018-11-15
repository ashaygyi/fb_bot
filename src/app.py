import os
import requests
from fbchat.models import *
from fbchat import log, Client
import apiai, json
import random
import threading
from flask import Flask, render_template

nudes = ['https://drive.google.com/uc?id=1w_EpBtt1MgDFv7rJ3QPDqGfESX2UOKBh',
         'https://drive.google.com/uc?id=1stxfNUdOsmojZ7spSGdGahJ0wU_L6bka',
         'https://drive.google.com/uc?id=1aBFXHSMlxLQdIwSRvaFhUtK812RfhilM',
         'https://drive.google.com/uc?id=1bmqkfHqD3N4NPmv8zY296tXm2lma2lCF']
blackpink = ['https://drive.google.com/uc?id=1j6-5QgbctEJtXmZ7UWlayDBYDiqFj0Iz',
             'https://drive.google.com/uc?id=1q3-mQvEvtCnlXLQ0XZTRda6qiq81jB2B',
             'https://drive.google.com/uc?id=1p8garPN9FcD6VU0vbH50L435N336ow2r',
             'https://drive.google.com/uc?id=1z0KPrv8IJagQAifAtYcq08eaGAAxvR7U']
twice = ['https://drive.google.com/uc?id=1QTRSCjxSY50kwpoWy67I78sQFb1JJymx',
         'https://drive.google.com/uc?id=1C8BSNoW9E6wlhIqDsFVBDYY3db10b3Tx',
         'https://drive.google.com/uc?id=1rEsUHAR9OkMk5tXJU7dB1q8kzoX6HYJZ',
         'https://drive.google.com/uc?id=1uj8WFHWNCwUk7Tm9_CJKh69ysTm4JyDt']


class EchoBot(Client):

    def apiaiConnect(self):
        self.CLIENT_ACCESS_TOKEN = 'e326aa6d12394afc8240df77deb9c637'
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def findWholeWord(self, word, string):
        return word in string

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):

        global a
        a = False
        self.markAsDelivered(thread_id, message_object.uid)
        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        mesg = message_object.text

        if author_id != self.uid:
            if self.findWholeWord('blackpink', mesg) or self.findWholeWord('Blackpink', mesg) or self.findWholeWord('BLACKPINK', mesg) or self.findWholeWord('BlackPink', mesg):
                a = True
                client.reactToMessage(message_object.uid, MessageReaction.LOVE)
                self.sendRemoteImage(image_url=random.choice(blackpink), thread_id=thread_id, thread_type=thread_type)
            if self.findWholeWord('twice', mesg) or self.findWholeWord('Twice', mesg) or self.findWholeWord('TWICE', mesg):
                a = True
                client.reactToMessage(message_object.uid, MessageReaction.LOVE)
                self.sendRemoteImage(image_url=random.choice(twice), thread_id=thread_id, thread_type=thread_type)
            if a is False:
                if (mesg[0:10] == 'luffy help' or mesg[0:10] == 'Luffy help') and len(mesg) == 10:
                    self.send(Message(text='Hello'
                                           '\nYou can ask me to do things with luffy commands'
                                           '\neg.luffy send nudes'
                                           '\nYou can also chat with me using luffy in font of the sentence'
                                           '\neg.luffy hello, luffy how are you'), thread_id=thread_id, thread_type=thread_type)
                elif (mesg[0:5] == 'luffy' or mesg[0:5] == 'Luffy') and len(mesg) > 6:
                    if self.findWholeWord('send nudes', mesg):
                        self.sendRemoteImage(image_url=random.choice(nudes), thread_id=thread_id, thread_type=thread_type)
                    else:
                        self.apiaiConnect()
                        self.request.query = mesg[5:]
                        response = self.request.getresponse()
                        obj = json.load(response)
                        reply = obj['result']['fulfillment']['speech']
                        self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                else:
                    self.send(Message(text="Please put the word 'luffy' in the beginning of the line"
                                           "\nOr type luffy help"), thread_id=thread_id, thread_type=thread_type)
        self.markAsRead(thread_id)

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key')


client = EchoBot(os.environ.get('email'), os.environ.get('password'),
                 session_cookies={'c_user': os.environ.get('c_user'),
                                 'datr': os.environ.get('datr'),
                                 'fr': os.environ.get('fr'),
                                 'noscript': os.environ.get('noscript'),
                                 'pl': os.environ.get('pl'),
                                 'sb': os.environ.get('sb'),
                                 'spin': os.environ.get('spin'),
                                 'xs': os.environ.get('xs')})
# client = EchoBot(os.environ.get('email'), os.environ.get('password'))
# session = client.getSession()
# client.setSession(session)

@app.route('/')
def home():
    return render_template('welcome.html')


if __name__ == '__main__':
        app.run(debug=False)
        client.listen()

