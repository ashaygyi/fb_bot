from fbchat.models import *
from google_images_download import google_images_download
from fbchat import log, Client
import apiai, json
import json
import random
import shutil


class EchoBot(Client):

    def apiaiConnect(self):
        self.CLIENT_ACCESS_TOKEN = 'e326aa6d12394afc8240df77deb9c637'
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = 'de'
        self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def findWholeWord(self, word, string):
        return word in string

    def onMessage(self, mid=None, author_id=None, message=None, message_object=None, thread_id=None,
                  thread_type=ThreadType.USER, ts=None, metadata=None, msg=None):

        self.markAsDelivered(thread_id, message_object.uid)
        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))
        mesg = message_object.text

        if author_id != self.uid:

            if self.findWholeWord('blackpink', mesg) or self.findWholeWord('Blackpink', mesg) or self.findWholeWord(
                    'BLACKPINK', mesg) or self.findWholeWord('BlackPink', mesg):
                client.reactToMessage(message_object.uid, MessageReaction.LOVE)

            if self.findWholeWord('twice', mesg) or self.findWholeWord('Twice', mesg) or self.findWholeWord('TWICE',mesg) or self.findWholeWord('TWICE',
                                                                                                            mesg):
                client.reactToMessage(message_object.uid, MessageReaction.LOVE)

            if self.findWholeWord('momoland', mesg) or self.findWholeWord('Momoland', mesg) or self.findWholeWord('MOMOLAND',
                                                                                                            mesg):
                client.reactToMessage(message_object.uid, MessageReaction.LOVE)

            if self.findWholeWord('bigbang', mesg) or self.findWholeWord('Bigbang', mesg) or self.findWholeWord('BigBang', mesg) or self.findWholeWord('BIGBANG',
                                                                                                            mesg):
                client.reactToMessage(message_object.uid, MessageReaction.LOVE)

            if (mesg[0:10] == 'luffy help' or mesg[0:10] == 'Luffy help') and len(mesg) == 10:
                self.send(Message(text='Hello'
                                       '\nYou can ask me to do things with luffy commands'
                                       '\neg.luffy send nudes'
                                       '\nYou can also chat with me using luffy in font of the sentence'
                                       '\neg.luffy hello, luffy how are you'), thread_id=thread_id,
                          thread_type=thread_type)
                elif mesg[0:5] == 'luffy' and len(mesg) > 6:
                if self.findWholeWord('send me ', mesg) or self.findWholeWord('SEND ME ', mesg) or self.findWholeWord(
                        'Send me ', mesg) or self.findWholeWord('Send Me ', mesg):
                    imglist = []
                    response = google_images_download.googleimagesdownload()
                    arguments = {"keywords": mesg[14:], "limit": 10, "no_download": True,
                                 "no_directory": True, "extract_metadata": True}
                    response.download(arguments)
                    json_data = open('./logs/' + mesg[14:] + '.json').read()
                    data = json.loads(json_data)
                    shutil.rmtree('./logs')
                    for a in range(0, 5):
                        imglist.append(data[a]['image_link'])
                        a += 1
                    random.shuffle(imglist)
                    self.sendRemoteImage(image_url=random.choice(imglist), thread_id=thread_id,
                                         thread_type=thread_type)
                elif self.findWholeWord('send ', mesg) or self.findWholeWord('SEND ', mesg):
                    imglist = []
                    response = google_images_download.googleimagesdownload()
                    arguments = {"keywords": mesg[11:], "limit": 10, "no_download": True,
                                 "no_directory": True, "extract_metadata": True}
                    response.download(arguments)
                    json_data = open('./logs/' + mesg[11:] + '.json').read()
                    data = json.loads(json_data)
                    shutil.rmtree('./logs')
                    for a in range(0, 5):
                        imglist.append(data[a]['image_link'])
                        a += 1
                    random.shuffle(imglist)
                    self.sendRemoteImage(image_url=random.choice(imglist), thread_id=thread_id,
                                         thread_type=thread_type)
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
client.listen()
