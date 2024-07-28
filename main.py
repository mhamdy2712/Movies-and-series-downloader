from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as kiImage
from io import BytesIO
from kivymd.uix.dialog import MDDialog
from PIL import Image as PillowImage
import plyer
import requests
from kivy.clock import Clock
from android.permissions import request_permissions, Permission
from kivy.utils import platform
import json
from jnius import autoclass
from bs4 import BeautifulSoup
from kivymd.uix.button import MDRectangleFlatButton,MDRectangleFlatIconButton
from kivy.uix.label import Label
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextFieldRound
import arabic_reshaper
import os
import time
from kivy.clock import mainthread
from kivymd.uix.floatlayout import MDFloatLayout
from bidi.algorithm import get_display
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
global DownloadLinks,box,BOXES,its_me,LINKS,Downloaded_Boxes,Downloaded_Links,Buttons,Paused_Buttons,Downloads,Paused_Boxes,Paused_Links,Names,Paused_Names,loop
DownloadLinks = []
box = []
its_me=False
import kivy
import kivymd
Downloaded_Boxes = []
Buttons =[]
Paused_Buttons=[]
Downloaded_Links = []
Paused_Boxes = []
Paused_Links = []
Names = []
BOXES=[]
LINKS=[]
Paused_Names = []
loop = None
import bidi
import re
global ff
global path1,path2
path1 = '/storage/emulated/0/HM Cinema'
path2 = '/storage/emulated/0/HM Cinema/Downlaods'
global Downloading
Downloading = False
global Bseries
global searchword
global update 
update= False
Bseries = False
def on_pause(dt):
    if not update:
        Thread(target=lambda: Update_all()).start()
def Update_all():
    global update
    update = True
    global LINKS
    s1 = []
    s2 = []
    x = os.path.join(path1, 'data/k1.json')
    with open(x, 'w') as jsonfile:
        for i in range(len(BOXES)):
            data = {}
            data['Name'] = BOXES[i].ids.Download_Name.text
            data['TotalSize'] = BOXES[i].ids.Total_Size.text
            data['Percentage'] = BOXES[i].ids.Percentage.text
            data['Value'] = BOXES[i].ids.Bar.value
            s1.append(data)
        json.dump(s1, jsonfile)
    jsonfile.close()
    x = os.path.join(path1, 'data/k2.json')
    with open(x, 'w') as jsonfile:
        json.dump(LINKS, jsonfile)
    jsonfile.close()
    x = os.path.join(path1, 'data/k3.json')
    with open(x, 'w') as jsonfile:
        for i in range(len(Downloaded_Boxes)):
            data = {}
            data['Name'] = Downloaded_Boxes[i].ids.Download_Name.text
            s2.append(data)
        json.dump(s2, jsonfile)
    jsonfile.close()
    x = os.path.join(path1, 'data/k4.json')
    with open(x, 'w') as jsonfile:
        json.dump(Downloaded_Links, jsonfile)
    jsonfile.close()
    update = False

class LoadingLayout(MDFloatLayout):

    def on_touch_down(self, touch): #Deactivate touch_down event
        if self.collide_point(*touch.pos):
            return True
class Ar_text(MDTextFieldRound):
    max_chars = NumericProperty(20)  # maximum character allowed
    str = StringProperty()

    def _init_(self, **kwargs):
        super(Ar_text, self)._init_(**kwargs)
        self.text = bidi.algorithm.get_display(arabic_reshaper.reshape("اطبع شيئاً"))

    def insert_text(self, substring, from_undo=False):
        if not from_undo and (len(self.text) + len(substring) > self.max_chars):
            return

        self.str = self.str+substring
        self.text = bidi.algorithm.get_display(arabic_reshaper.reshape(self.str))
        substring = ""
        super(Ar_text, self).insert_text(substring, from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        self.str = self.str[0:len(self.str)-1]
        self.text = bidi.algorithm.get_display(arabic_reshaper.reshape(self.str))
class WindowManager(ScreenManager):
    pass
class FResults(Screen):
    def closepopup(self,dt):
        self.popup.dismiss()
    def get_buttons(self):
        global names
        names=[]
        button = MDRectangleFlatIconButton(text='[b]Go Back[/b]',theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial"
                                           ,icon='arrow-up',
                                               pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                               ,on_release=self.go_back)
        self.ids.bl_main.add_widget(button)
        if ff:
            for i in range(len(ff)):
                x = ff[i].text.rstrip()
                x = x.rstrip()
                x = x.rstrip()
                x = x.strip('\n')
                reshaped_text = arabic_reshaper.reshape(x)
                x = bidi.algorithm.get_display(reshaped_text)
                x= azbot_alasm(x)
                names.append(x)
                if(Bseries):
                    button = MDRectangleFlatButton(text=x,theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                                   pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                                   ,on_release=self.manager.get_screen('seasons').aperta)
                    self.ids.bl_main.add_widget(button)
                else:
                    button = MDRectangleFlatButton(text=x,    theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                                   pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                                   ,on_release=self.manager.get_screen('fresolution').aperta)
                    self.ids.bl_main.add_widget(button)
        else:
            label = Label(text="Your search didn't return any results",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                            pos_hint={'center_x': 0.5,'center_y':0.5}, size_hint=(1, None),
                                            )
            self.ids.bl_main.add_widget(label)
    def go_back(self,button):
        self.manager.transition.direction = 'down'
        self.manager.current ='fsearch'
    @mainthread
    def popupopen(self):
        self.popup = MDDialog(size_hint=(0.9,None),text="Connection error, Check your network", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.popup.open()
        Clock.schedule_once(self.closepopup,1.2)

def s0rt(u):
    new_list = []
    i=0
    s0rt.b= False
    s0rt.er = []
    while u:
            minimum =  int(re.search(r'\d+', u[0]).group())
            g=u[0]
            for i in u:
                if  int(re.search(r'\d+', i).group()) < minimum:
                    minimum = int(re.search(r'\d+',i ).group())
                    g=i
            new_list.append(g)
            u.remove(g)
    return new_list

def azbot_alasm(s):
    if s[0]=='(':
        try:
            int(s[1])
        except:
            s=s[1:]
            s = s+')'
    return s
class Seasons(Screen):
    loading_layout = None
    def aperta(self,button):
        self.manager.transition.direction = 'up'
        self.manager.current='seasons'
        self.ids.bl_main.clear_widgets()
        self.loading_layout = LoadingLayout()
        self.launch_thread(button.text)
    def launch_thread(self, name):
        self.add_widget(self.loading_layout)
        Thread(target=self.get_season, args=(name,), daemon=True).start()

    def put_buttons(self):
        try:
            self.box = BoxLayout(size_hint_y=None)
            memory_saved_image = BytesIO()
            pil_edited_image = PillowImage.open(BytesIO(ses_img_data))
            pil_edited_image.save(memory_saved_image, 'png')
            memory_saved_image.seek(0)
            image_from_memory = CoreImage(memory_saved_image, ext='png')
            image = kiImage(source='',texture=image_from_memory.texture,size_hint_y=None)
            button = MDRectangleFlatIconButton(text='Go Back',font_name="/storage/emulated/0/HM Cinema/font/arial",icon='arrow-up',
                                                   pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                                   ,on_release=self.go_back)
            self.ids.bl_main.add_widget(button)
            labelspace1 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelspace2 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            label = Label(text=name,font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            self.ids.bl_main.add_widget(self.box)
            self.box.add_widget(image)
            self.ids.bl_main.add_widget(labelspace1)
            self.ids.bl_main.add_widget(label)
            self.ids.bl_main.add_widget(labelspace2)
            for k in range(len(r)):
                x=r[k]
                button = MDRectangleFlatButton(text=x,    theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                               pos_hint={'center_x':0.5},size_hint=(1,None)
                                               ,on_release=self.manager.get_screen('episodes').aperta)
                self.ids.bl_main.add_widget(button)
                self.manager.transition.direction = 'up'
                self.manager.current='seasons'
        except:
            pass
    def closepopup(self,dt):
        self.popup.dismiss()
    def get_season(self,namee):
        global OneSeason
        global selectedurl
        OneSeason=False
        global names
        global ses_img_data
        global name
        global seasonss
        name = namee
        global foundses
        index = names.index(name)
        i = 1
        while index > 43:
            i = i + 1
            index -= 44
        try:
            result_new = requests.get("https://mycima.run:2096/search/" + searchword + "/list/series/?page_number=" + str(i))
        except:
            self.go_back(12)
            self.manager.get_screen('fresults').popupopen()
            self.my_thread()
            return
        srcm = result_new.content
        soup = BeautifulSoup(srcm, "lxml")
        ff = soup.find_all("div", {"class": "Thumb--GridItem"})
        selectedurl = ff[index].find("a").attrs['href']
        result_new = requests.get(selectedurl)
        srcm = result_new.content
        sp = BeautifulSoup(srcm, "lxml")
        found = sp.find_all("div", {"class": "List--Seasons--Episodes"}, )
        try:
            ph= sp.find('singlecontainerright').find("mycima").attrs['style']
            seasonphoto = ph[10:-2]
        except:
            try:
                ph = sp.find('singlecontainerright').find("mycima").attrs['data-lazy-style']
                seasonphoto = ph[10:-2]
            except:
                self.go_back(12)
                self.popupopen2()
                return
        try:
            response = requests.get(seasonphoto)
            ses_img_data = response.content
        except:
            response = requests.get('https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=20&m=922962354&s=612x612&w=0&h=f-9tPXlFXtz9vg_-WonCXKCdBuPUevOBkp3DQ-i0xqo=')
            ses_img_data = response.content

        if found:
            foundses = found[0].find_all("a")
            seasonss = []
            m = []
            for i in range(len(foundses)):
                x = foundses[i].text.rstrip()
                x = x.strip('\n')
                x = x.replace('\n', ' ')
                seasonss.append(x)
            for x in seasonss:
                m.append(x)
            global r
            r = s0rt(m)
            x=r
            r=[]
            for m in x:
                reshaped_text = arabic_reshaper.reshape(m)
                x = bidi.algorithm.get_display(reshaped_text)
                x=azbot_alasm(x)
                r.append(x)
            x=seasonss
            seasonss =[]
            for m in x:
                reshaped_text = arabic_reshaper.reshape(m)
                x = bidi.algorithm.get_display(reshaped_text)
                x=azbot_alasm(x)
                seasonss.append(x)

        else:
            OneSeason=True
        self.my_thread()
    @mainthread
    def go_back(self,button):
        self.manager.transition.direction = 'down'
        self.manager.current = 'fresults'
    @mainthread
    def my_thread(self):
        if not OneSeason:
            self.put_buttons()
        self.remove_widget(self.loading_layout)
        if OneSeason:
            self.manager.get_screen('episodes').aperta(1)
    @mainthread
    def popupopen(self):
        self.popup = MDDialog(size_hint=(0.9,None),text="Connection error, Check your network", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.popup.open()
        Clock.schedule_once(self.closepopup,1.2)
    @mainthread
    def popupopen2(self):
        global popup8
        popup8 = MDDialog(text="Can't access page", radius=[20, 7, 20, 7],
                         size_hint=(0.9,None),pos_hint={'center_x': 0.5, 'center_y': 0.2})
        popup8.open()
        Clock.schedule_once(self.closepopup8,1.2)
    def closepopup8(self,dt):
        popup8.dismiss()


class DownloadBox(BoxLayout):
    pass


class Heart(Screen):
    def gohere(self,button):
        self.manager.transition.direction = 'up'
        self.manager.current = 'heart'
        Clock.schedule_once(self.leave,0.8)
    def leave(self,dt):
        self.manager.transition.direction = 'down'
        self.manager.current = 'fsearch'


class FSearch(Screen):
    loading_layout = None
    DownloadLinks = []
    BoxY=0.1
    box =[]
    Downloaded_Boxes =[]
    Downloaded_Links=[]
    Dowanloads =0
    Paused_Boxes=[]
    Paused_Links=[]
    Names = []
    Paused_Names = []
    LabelY = 0.05
    Buttons=[]
    loop = None
    Start=0
    def Show_Arabic(self,x):
        textnew = bidi.algorithm.get_display(arabic_reshaper.reshape(x))
        return textnew

    def started(self,dt):
        global Paused_Boxes,Paused_Links,Downloaded_Boxes,Downloaded_Links,BOXES,LINKS,DownloadLinks,box
        try:
            if self.Start==0:
                x = os.path.join(path1, 'data/k1.json')
                with open(x) as jsonfile:
                    Data1 = json.load(jsonfile)
                x = os.path.join(path1, 'data/k2.json')
                with open(x) as jsonfile:
                    Paused_Links = json.load(jsonfile)
                x = os.path.join(path1, 'data/k3.json')
                with open(x) as jsonfile:
                    Data2 = json.load(jsonfile)
                x = os.path.join(path1, 'data/k4.json')
                with open(x) as jsonfile:
                    Downloaded_Links = json.load(jsonfile)
                for i in range(len(Data1)):
                    x = Data1[i]
                    Paused_Boxes.append(DownloadBox())
                    Paused_Boxes[-1].ids.PauseButton.icon='play-circle-outline'
                    Paused_Boxes[-1].ids.PauseButton.bind(on_release=self.lol1)
                    Paused_Boxes[-1].ids.PauseButton.id = Paused_Links[i]
                    Paused_Boxes[-1].ids.Close.icon = 'close-circle-outline'
                    Paused_Boxes[-1].ids.Close.bind(on_release=self.Close)
                    Paused_Boxes[-1].ids.Close.id = Paused_Links[i]
                    Paused_Boxes[-1].ids.Downloaded_Size.text = 'Download Paused'
                    Paused_Boxes[-1].ids.Download_Name.text = x['Name']
                    Paused_Boxes[-1].ids.Total_Size.text = x['TotalSize']
                    Paused_Boxes[-1].ids.Percentage.text = x['Percentage']
                    Paused_Boxes[-1].ids.Bar.value = x['Value']
                    self.ids.bl_main.add_widget(Paused_Boxes[-1])
                for i in Paused_Boxes:
                    BOXES.append(i)
                for i in Paused_Links:
                    LINKS.append(i)
                for i in range(len(Data2)):
                    x = Data2[i]
                    Downloaded_Boxes.append(DownloadBox())
                    Downloaded_Boxes[-1].ids.Download_Name.text = x['Name']
                    Downloaded_Boxes[-1].ids.Close.icon= 'minus-circle-outline'
                    Downloaded_Boxes[-1].ids.Close.bind(on_release=self.Close)
                    Downloaded_Boxes[-1].ids.Close.id = Downloaded_Links[i]
                    Downloaded_Boxes[-1].ids.Total_Size.text = ' '
                    Downloaded_Boxes[-1].ids.Downloaded_Size.text = 'Download Done'
                    Downloaded_Boxes[-1].ids.Percentage.text = '100 %'
                    Downloaded_Boxes[-1].ids.shrta.text = ''
                    Downloaded_Boxes[-1].ids.fadi.text = '         '
                    Downloaded_Boxes[-1].ids.PauseButton.icon = 'heart'
                    Downloaded_Boxes[-1].ids.PauseButton.bind(on_release=self.manager.get_screen('heart').gohere)
                    Downloaded_Boxes[-1].ids.Bar.value = 100
                    self.ids.bl_main2.add_widget(Downloaded_Boxes[-1])
                self.Start=231
        except:
            pass
    def on_enter(self,*args):
        Clock.schedule_once(self.started, 0.1)
    def aperta(self,s,what):
        self.manager.get_screen('fresults').ids.bl_main.clear_widgets()
        self.manager.transition.direction = 'up'
        self.manager.current='fresults'
        self.loading_layout = LoadingLayout()
        self.launch_thread(s,what)
    def launch_thread(self, name,what):
        self.manager.get_screen('fresults').add_widget(self.loading_layout)
        if what=='f':
            Thread(target=self.i_clickedf, args=(name,), daemon=True).start()
        else:
            Thread(target=self.i_clickeds, args=(name,), daemon=True).start()
    def i_clickedf(self,s):
        global Bseries
        Bseries = False
        global ff
        global searchword
        searchword = s
        ff = []
        i=1
        while True:
            fbool = ff
            try:
                result_new = requests.get("https://mycima.world/search/" + searchword + "/page/" + str(i))
            except:
                self.popupopen()
                break
            srcm = result_new.content
            soup = BeautifulSoup(srcm, "lxml")
            Found = soup.find_all("strong", {"dir": "auto"})
            ff = ff + Found
            if fbool == ff:
                break
            i = i + 1
        self.my_thread()
    def closepopup(self,dt):
        fspopup.dismiss()

    def i_clickeds(self,s):
        global ff
        global searchword
        global Bseries
        Bseries = True
        searchword = s
        ff = []
        i=1

        while True:
            fbool = ff
            try:
                result_new = requests.get("https://mycima.run:2096/search/" + searchword + "/list/series/?page_number=" + str(i))
            except:
                self.popupopen()
                break
            srcm = result_new.content
            soup = BeautifulSoup(srcm, "lxml")
            Found = soup.find_all("strong", {"dir": "auto"})
            ff = ff + Found
            if fbool == ff:
                break
            i = i + 1
        self.my_thread()
    def MDownload(self,button):
        global DownloadLinks,BOXES,LINKS, box,Buttons,Paused_Buttons, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        index = MoviesRes.index(button.text)
        try:
            DownloadLinks.index(Movies_DLinks[index])
            self.popupopen4()
            return
        except:
            try:
                Paused_Links.index(Movies_DLinks[index])
                self.popupopen4()
                return
            except:
                try:
                    Downloaded_Links.index(Movies_DLinks[index])
                    self.popupopen5()
                    return
                except:
                    pass
        DownloadLinks.append(Movies_DLinks[index])
        box.append(DownloadBox())
        Name = MovieName[:41]
        box[-1].ids.PauseButton.bind(on_release=self.lol2)
        box[-1].ids.Close.bind(on_release=self.Close)
        box[-1].ids.Close.id = Movies_DLinks[index]
        box[-1].ids.PauseButton.id = Movies_DLinks[index]
        box[-1].ids.Download_Name.text = Name
        box[-1].ids.Downloaded_Size.text = 'Wait For Download'
        try:
            box[-1].ids.Total_Size.text= getsize(Movies_DLinks[index])
        except:
            box[-1].ids.Total_Size.text= "None"
        box[-1].ids.Percentage.text= '0 %'
        box[-1].ids.Bar.value = 0
        BOXES.append(box[-1])
        LINKS.append(DownloadLinks[-1])
        self.ids.bl_main.add_widget(box[-1])
        self.manager.transition.direction = 'down'
        self.manager.current = 'fresults'
        self.ids.navigation.switch_tab('downloadqueue')
        self.openpopup2()
        self.DownloadQueue()
    def SDownload(self,button):
        global DownloadLinks,BOXES,LINKS,box,Buttons,Paused_Buttons, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        global Episode_DLinks
        index = Episode_Ress.index(button.text)
        try:
            DownloadLinks.index(Episode_DLinks[index])
            self.popupopen4()
            return
        except:
            try:
                Paused_Links.index(Episode_DLinks[index])
                self.popupopen4()
                return
            except:
                try:
                    Downloaded_Links.index(Episode_DLinks[index])
                    self.popupopen5()
                    return
                except:
                    pass

        DownloadLinks.append(Episode_DLinks[index])
        box.append(DownloadBox())
        Name = name[:25]
        try:
            Nom = Name+'  '+season+'  '+epis
        except:
            Name = name[:33]
            Nom = Name+'  '+epis
        box[-1].ids.PauseButton.bind(on_release=self.lol2)
        box[-1].ids.Close.bind(on_release=self.Close)
        box[-1].ids.Close.id = Episode_DLinks[index]
        box[-1].ids.Download_Name.text = Nom
        try:
            box[-1].ids.Total_Size.text= getsize(Episode_DLinks[index])
        except:
            box[-1].ids.Total_Size.text= "None"
        box[-1].ids.Downloaded_Size.text = 'Wait For Download'
        box[-1].ids.Percentage.text= '0%'
        box[-1].ids.PauseButton.id = Episode_DLinks[index]
        box[-1].ids.Bar.value = 0
        BOXES.append(box[-1])
        LINKS.append(DownloadLinks[-1])
        self.ids.bl_main.add_widget(box[-1])
        self.manager.transition.direction = 'down'
        self.manager.current = 'episodes'
        self.ids.navigation.switch_tab('downloadqueue')
        self.openpopup2()
        self.DownloadQueue()
    def DownloadQueue(self):
        global DownloadLinks, box, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        if box==[]:
            return False
            pass
        else:
            if Downloading:
                return True
            else:
                self.PrepareDownload()
                return True
    def lol1(self,button):
        Resumeing = Thread(target=lambda: self.ResumeDownload(button))
        Resumeing.start()
    def lol2(self,button):
        global event
        Clock.unschedule(event)
        Pausing = Thread(target=lambda: self.PauseDownload(button))
        Pausing.start()
    def ResumeDownload(self,button):
        global DownloadLinks,box,Buttons,Paused_Buttons, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        Link = button.id
        index=Paused_Links.index(Link)
        button.icon= 'pause-circle-outline'
        button.unbind(on_release=self.lol1)
        button.bind(on_release= self.lol2)
        Paused_Boxes[index].ids.Downloaded_Size.text = 'Wait For Download'
        DownloadLinks.append(Paused_Links[index])
        box.append(Paused_Boxes[index])
        Paused_Links.remove(Paused_Links[index])
        Paused_Boxes.remove(Paused_Boxes[index])
        self.DownloadQueue()
    def PrepareDownload(self):
        box[0].ids.Downloaded_Size.text = 'Collecting Data'
        downloadThread = Thread(target=lambda: self.Download(DownloadLinks[0]))
        downloadThread.start()
    def Download(self,link):
        global DownloadLinks, box, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        global Downloading
        global loop
        global event
        global prevSize
        Downloading = True
        global downloading_link
        downloading_link = link
        loop = 1
        try:
            r = requests.get(link, stream=True)
        except:
            self.popupopen()
            Downloading = False
            loop = 0
            return
        fileSize= int(r.headers['Content-Length'])
        name = link.split('/')[-1].split('?')[0]
        name = name[:-5]
        dlFile = name
        existSize = 0
        x = os.path.join(path2, dlFile)
        dlFile = x
        if os.path.exists(dlFile):
            outputFile = open(dlFile, "ab")
            existSize = os.path.getsize(dlFile)
            range = 'bytes='+ str(existSize) + '-' + str(fileSize)
            try:
                r = requests.get(link, stream=True, headers={"Range": range})
            except:
                Downloading = False
                loop = 0
                self.popupopen()
                return
        else:
            outputFile = open(dlFile, "wb")
            try:
                r = requests.get(link, stream=True)
            except:
                Downloading = False
                loop = 0
                self.popupopen()
                return
        numBytes = 0
        downloadedSize = existSize
        # If the file exists, but we already have the whole thing, don't download again
        #if fileSize == existSize:
        #    loop = 0
        brox= box[0]
        prevSize=0
        numBytes=0
        event = Clock.schedule_interval(lambda dt: self.Speed(numBytes,),1)
        for chunk in r.iter_content(chunk_size=1024):
            if loop==0:
                break
            if chunk:
                print('lsa 48al')
                try:
                    brox.ids.Bar.value = downloadedPercentage
                except:
                    pass
                outputFile.write(chunk)
                numBytes = numBytes + len(chunk)
                downloadedSize+= len(chunk)
                downloadedPercentage= round((downloadedSize/fileSize)*100)
                brox.ids.Downloaded_Size.text = getStandardSize(downloadedSize)
                brox.ids.Percentage.text = str(downloadedPercentage) + ' %'
                brox.ids.Bar.value = downloadedPercentage
            else:
                self.DownloadDone()
                Downloading = False
                outputFile.close()
                Clock.unschedule(event)
                brox.ids.Speed.text = ''
                return
            if downloadedSize == fileSize:
                loop=0
                brox.ids.Downloaded_Size.text = getStandardSize(fileSize)
                brox.ids.Percentage.text = '100 %'
                brox.ids.Bar.value = 100
                brox.ids.Speed.text = ''
                Clock.unschedule(event)
                self.DownloadDone()
                return
        Downloading=False
        Clock.unschedule(event)
        brox.ids.Speed.text = ''
        outputFile.close()
    def Speed(self,nowSize):
        global prevSize
        x = getStandardSize(nowSize-prevSize)
        box[0].ids.Speed.text = x + '/S'
        prevSize = nowSize
    def PauseDownload(self,button):
        global DownloadLinks,box,Buttons,Paused_Buttons, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        global loop
        global Downloading
        Link = button.id
        index=DownloadLinks.index(Link)
        button.icon =  'play-circle-outline'
        button.unbind(on_release=self.lol2)
        button.bind(on_release= self.lol1)
        box[index].ids.Downloaded_Size.text = 'Download paused'
        Paused_Links.append(DownloadLinks[index])
        Paused_Boxes.append(box[index])
        box.remove(box[index])
        DownloadLinks.remove(DownloadLinks[index])
        if Downloading:
            if downloading_link==Link:
                loop=0
                time.sleep(0.25)
        self.DownloadQueue()
        return

    @mainthread
    def my_thread(self):
        self.manager.get_screen('fresults').get_buttons()
        self.manager.get_screen('fresults').remove_widget(self.loading_layout)
    @mainthread
    def DownloadDone(self):
        global DownloadLinks,its_me,BOXES,LINKS,Paused_Buttons, box, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        Downloaded_Boxes.append(DownloadBox())
        Downloaded_Boxes[-1].ids.Download_Name.text = box[0].ids.Download_Name.text
        Downloaded_Boxes[-1].ids.Total_Size.text= ' '
        Downloaded_Boxes[-1].ids.Close.bind(on_release=self.Close)
        Downloaded_Boxes[-1].ids.Close.icon = 'minus-circle-outline'
        Downloaded_Boxes[-1].ids.Close.id = DownloadLinks[0]
        Downloaded_Boxes[-1].ids.Downloaded_Size.text = 'Download Done'
        Downloaded_Boxes[-1].ids.Percentage.text= '100 %'
        Downloaded_Boxes[-1].ids.shrta.text= ''
        Downloaded_Boxes[-1].ids.fadi.text= '         '
        Downloaded_Boxes[-1].ids.PauseButton.icon = 'heart'
        Downloaded_Boxes[-1].ids.PauseButton.bind(on_release=self.manager.get_screen('heart').gohere)
        Downloaded_Boxes[-1].ids.Bar.value = 100
        self.ids.bl_main2.add_widget(Downloaded_Boxes[-1])
        self.ids.bl_main.remove_widget(box[0])
        BOXES.remove(box[0])
        LINKS.remove(DownloadLinks[0])
        box.remove(box[0])
        Downloaded_Links.append(DownloadLinks[0])
        DownloadLinks.remove(DownloadLinks[0])
        name = Downloaded_Links[-1].split('/')[-1].split('?')[0]
        name = name[:-5]
        plyer.notification.notify(title='Enjoy :)', message="Downloaded: " + name)
        self.openpopup3()
        loop = 0
        x = self.DownloadQueue()
    @mainthread
    def Close(self,button):
        global DownloadLinks,BOXES,LINKS, box, Downloaded_Boxes, Downloaded_Links, Downloads, Paused_Boxes, Paused_Links, Names, Paused_Names, loop
        global loop
        global Downloading
        Link = button.id
        try:
            index= DownloadLinks.index(Link)
            if Downloading:
                if downloading_link==Link:
                    loop=0
                    time.sleep(0.25)
            name = DownloadLinks[index].split('/')[-1].split('?')[0]
            name = name[:-5]
            file_path = os.path.join(path2, name)
            if os.path.exists(file_path):
                os.remove(file_path)
            LINKS.remove(DownloadLinks[index])
            DownloadLinks.remove(DownloadLinks[index])
            self.ids.bl_main.remove_widget(box[index])
            BOXES.remove(box[index])
            box.remove(box[index])
        except:
            try:
                print(Paused_Links)
                print(Link)
                index = Paused_Links.index(Link)
                name = Paused_Links[index].split('/')[-1].split('?')[0]
                name = name[:-5]
                file_path = os.path.join(path2, name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                LINKS.remove(Paused_Links[index])
                Paused_Links.remove(Paused_Links[index])
                self.ids.bl_main.remove_widget(Paused_Boxes[index])
                BOXES.remove(Paused_Boxes[index])
                Paused_Boxes.remove(Paused_Boxes[index])
            except:
                index = Downloaded_Links.index(Link)
                Downloaded_Links.remove(Downloaded_Links[index])
                self.ids.bl_main2.remove_widget(Downloaded_Boxes[index])
                Downloaded_Boxes.remove(Downloaded_Boxes[index])
    @mainthread
    def popupopen(self):
        global  fspopup
        fspopup = MDDialog(size_hint=(0.9,None),text="Connection error, Check your network", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.manager.get_screen('fresults').go_back(2)
        fspopup.open()
        Clock.schedule_once(self.closepopup,1.2)
    @mainthread
    def openpopup2(self):
        global  fspopup3
        fspopup3 = MDDialog(size_hint=(0.9,None),text="Download successfully added to queue", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        fspopup3.open()
        Clock.schedule_once(self.closepopup2,1.2)
    @mainthread
    def openpopup3(self):
        global  fspopup2
        fspopup2 = MDDialog(size_hint=(0.9,None),text="Download Done, Enjoy :)", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        fspopup2.open()
        Clock.schedule_once(self.closepopup3,1.2)
    @mainthread
    def openpopup4(self):
        global  fspopup4
        fspopup4 = MDDialog(size_hint=(0.9,None),text="Download already exist in queue", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        fspopup4.open()
        Clock.schedule_once(self.closepopup4,1.2)
    def openpopup5(self):
        global  fspopup5
        fspopup5 = MDDialog(size_hint=(0.9,None),text="Download already done", radius=[20, 7, 20, 7],
                         pos_hint={'center_x': 0.5, 'center_y': 0.2})
        fspopup5.open()
        Clock.schedule_once(self.closepopup5,1.2)


    def closepopup2(self,dt):
        fspopup3.dismiss()
    def closepopup3(self,dt):
        fspopup2.dismiss()
    def closepopup4(self,dt):
        fspopup4.dismiss()
    def closepopup5(self,dt):
        fspopup5.dismiss()



class Episodes(Screen):
    loading_layout = None
    def aperta(self,button):
        self.manager.transition.direction = 'up'
        self.manager.current='episodes'
        self.ids.bl_main.clear_widgets()
        self.loading_layout = LoadingLayout()
        if not OneSeason:
            self.launch_thread(button.text)
        else:
            self.launch_thread("m4 mohm")

    def launch_thread(self, name):
        self.add_widget(self.loading_layout)
        Thread(target=self.get_epis, args=(name,), daemon=True).start()
    def go_back(self,button):
        self.manager.transition.direction = 'down'
        self.manager.current = 'fresults' if OneSeason else 'seasons'
    def get_epis(self,sea):
        self.ids.bl_main.clear_widgets()
        global seasonlink
        global season
        global ss
        global u
        global seasonss
        if not OneSeason:
            global r
            season=sea
            index = seasonss.index(sea)
            seasonlink = foundses[index].attrs['href']
        else:
            seasonlink = selectedurl
        try:
            result_new = requests.get(seasonlink)
        except:
            self.go_back(12)
            if not OneSeason:
                self.manager.get_screen('seasons').popupopen()
                self.my_thread()
            else:
                self.manager.get_screen('fresults').popupopen()
                self.my_thread()
            return
        srcm = result_new.content
        sp = BeautifulSoup(srcm, "lxml")
        found = sp.find_all("episodetitle")
        ss = []
        g = []
        j = 1000
        for i in range(len(found)):
            b = found[i].text
            try:
                minimum = int(re.search(r'\d+', b).group())
            except:
                b = b + str(j)
                j = j + 1000
            x = b.rstrip()
            x = x.rstrip()
            x = x.strip('\n')
            x = x.replace('\n', ' ')
            ss.append(x)
        for x in ss:
            g.append(x)
        u = s0rt(g)
        #ss.append('جزء من الموسم')
        #u.append('جزء من الموسم')
        x = u
        u = []
        for m in x:
            reshaped_text = arabic_reshaper.reshape(m)
            x = bidi.algorithm.get_display(reshaped_text)
            x=azbot_alasm(x)
            u.append(x)
        x=ss
        ss=[]
        for m in x:
            reshaped_text = arabic_reshaper.reshape(m)
            x = bidi.algorithm.get_display(reshaped_text)
            x=azbot_alasm(x)
            ss.append(x)
        self.my_thread()
    def put_buttons(self):
        try:
            self.box = BoxLayout(size_hint_y=None)
            memory_saved_image = BytesIO()
            pil_edited_image = PillowImage.open(BytesIO(ses_img_data))
            pil_edited_image.save(memory_saved_image, 'png')
            memory_saved_image.seek(0)
            image_from_memory = CoreImage(memory_saved_image, ext='png')
            image = kiImage(source='',texture=image_from_memory.texture,size_hint_y=None)
            button = MDRectangleFlatIconButton(text='[b]Go Back[/b]',font_name="/storage/emulated/0/HM Cinema/font/arial",icon='arrow-up',
                                                   pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                                   ,on_release=self.go_back)
            self.ids.bl_main.add_widget(button)
            labelspace1 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelspace2 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelname = Label(text=name,font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            if not OneSeason:
                labelseason = Label(text=season,font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
                labelspace3 = Label(text='     ', font_name='/storage/emulated/0/HM Cinema/font/arial', padding_y=20, size=(100, 70))
                labelspace4 = Label(text='     ', font_name='/storage/emulated/0/HM Cinema/font/arial', padding_y=20, size=(100, 70))
            self.ids.bl_main.add_widget(self.box)
            self.box.add_widget(image)
            self.ids.bl_main.add_widget(labelspace1)
            self.ids.bl_main.add_widget(labelname)
            if not OneSeason:
                self.ids.bl_main.add_widget(labelspace4)
                self.ids.bl_main.add_widget(labelspace3)
                self.ids.bl_main.add_widget(labelseason)
            self.ids.bl_main.add_widget(labelspace2)
            for k in range(len(u)):
                x=u[k]
                button = MDRectangleFlatButton(text=x,theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                pos_hint={'center_x':0.5},size_hint=(1,None)
                                ,on_release= self.manager.get_screen('episresolution').aperta)
                self.ids.bl_main.add_widget(button)
        except:
            pass
    def closepopup(self,dt):
        self.popup.dismiss()
    @mainthread
    def my_thread(self):
        self.put_buttons()
        self.remove_widget(self.loading_layout)
    @mainthread
    def popupopen(self):
        self.popup = MDDialog(text="Connection error, Check your network", radius=[20, 7, 20, 7],
                         size_hint=(0.9,None),pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.popup.open()
        Clock.schedule_once(self.closepopup,1.2)
class FResolution(Screen):
    loading_layout = None
    def aperta(self,button):
        self.manager.transition.direction = 'up'
        self.manager.current='fresolution'
        self.ids.bl_main.clear_widgets()
        self.loading_layout = LoadingLayout()
        self.launch_thread(button.text)

    def launch_thread(self, name):
        self.add_widget(self.loading_layout)
        Thread(target=self.get_res, args=(name,), daemon=True).start()

    def get_res(self,name):
        global Movies_DLinks
        global MoviesRes
        global MovieName
        self.namee = name
        index = names.index(name)
        global soup
        i=1
        while index > 43:
            i = i + 1
            index -= 44
        try:
            result_new = requests.get("https://mycima.world/search/" + searchword + "/page/" + str(i))
        except:
            self.go_back(12)
            self.manager.get_screen('fresults').popupopen()
            self.my_thread([])
            return
        srcm = result_new.content
        soup = BeautifulSoup(srcm, "lxml")
        found = soup.find_all("div", {"class": "Thumb--GridItem"})
        selectedurl = found[index].find("a").attrs['href']
        try:
            result_new = requests.get(selectedurl)
        except:
            self.go_back(12)
            self.manager.get_screen('fresults').popupopen()
            self.my_thread([])
            return
        srcm = result_new.content
        soup = BeautifulSoup(srcm, "lxml")
        try:
            ph= soup.find('singlecontainerright').find("mycima").attrs['style']
        except:
            ph= soup.find('singlecontainerright').find("mycima").attrs['data-lazy-style']
        ph = ph[10:-2]
        foundres = soup.find_all("resolution")
        foundqu = soup.find_all("quality")
        foundlink = soup.find_all("a", {"class": "hoverable activable"})
        foundsize = []
        self.res = []
        for i in range(len(foundlink)):
            foundsize.append(foundlink[i].attrs['href'])
        for i in range(len(foundres)):
            try:
                x = foundqu[i].text.replace(' ','') + "        " + foundres[i].text.replace(' ','') + "        "+ str(getsize(foundsize[i]).replace(' ',''))
            except:
                self.go_back(12)
                self.manager.get_screen('fresults').popupopen()
                self.my_thread([])
                return
            x = x.replace('\n', ' ')
            self.res.append(x)
        Movies_DLinks = foundsize
        MoviesRes = self.res
        self.my_thread(ph)

    def put_buttons(self,ph):
        try:
            global MovieName
            self.box = BoxLayout(size_hint_y=None,size_hint=(0.2,0.3))
            try:
                try:
                    response = requests.get(ph)
                    img_data = response.content
                except:
                    response = requests.get('https://media.istockphoto.com/vectors/no-image-available-sign-vector-id922962354?k=20&m=922962354&s=612x612&w=0&h=f-9tPXlFXtz9vg_-WonCXKCdBuPUevOBkp3DQ-i0xqo=')
                    img_data = response.content
            except:
                self.go_back(12)
                self.manager.get_screen('fresults').popupopen()
                self.remove_widget(self.loading_layout)
                return

            memory_saved_image = BytesIO()
            pil_edited_image = PillowImage.open(BytesIO(img_data))
            pil_edited_image.save(memory_saved_image, 'png')
            memory_saved_image.seek(0)
            image_from_memory = CoreImage(memory_saved_image, ext='png')
            image = kiImage(source='',texture=image_from_memory.texture,size_hint_y=None,size_hint=(0.2,0.3))
            button = MDRectangleFlatIconButton(text='[b]Go Back[/b]',font_name="/storage/emulated/0/HM Cinema/font/arial",icon='arrow-up',
                                                   pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                                   ,on_release=self.go_back)
            self.ids.bl_main.add_widget(button)
            labelspace1 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelspace2 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelname = Label(text=self.namee,font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            MovieName = self.namee
            self.ids.bl_main.add_widget(self.box)
            self.box.add_widget(image)
            self.ids.bl_main.add_widget(labelspace1)
            self.ids.bl_main.add_widget(labelname)
            self.ids.bl_main.add_widget(labelspace2)
            for k in range(len(self.res)):
                x=self.res[k]
                button = MDRectangleFlatButton(text=x,theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                               pos_hint={'center_x':0.5},size_hint=(1,None),
                                               on_release=self.manager.get_screen('fsearch').MDownload)
                self.ids.bl_main.add_widget(button)
        except:
            pass
    def go_back(self,button):
        self.manager.transition.direction = 'down'
        self.manager.current = 'fresults'
    @mainthread
    def my_thread(self,ph):
        self.put_buttons(ph)
        self.remove_widget(self.loading_layout)

class EpisResolution(Screen):
    loading_layout = None
    def aperta(self,button):
        self.manager.transition.direction = 'up'
        self.manager.current='episresolution'
        self.ids.bl_main.clear_widgets()
        self.loading_layout = LoadingLayout()
        self.launch_thread(button.text)

    def launch_thread(self, epis):
        self.add_widget(self.loading_layout)
        Thread(target=self.get_res, args=(epis,), daemon=True).start()

    def get_res(self,episs):
        global epis
        global Episode_DLinks
        global Episode_Ress
        global ss
        epis = episs
        index= ss.index(epis)
        try:
            result_new = requests.get(seasonlink)
        except:
            self.go_back(12)
            self.manager.get_screen('episodes').popupopen()
            self.my_thread([])
            return
        srcm = result_new.content
        sp = BeautifulSoup(srcm, "lxml")
        found = sp.find_all("div", {"class": "Episodes--Seasons--Episodes"}, )
        found = found[0].find_all("a")
        epislink = found[index].attrs['href']
        try:
            result_new = requests.get(epislink)
        except:
            self.go_back(12)
            self.manager.get_screen('episodes').popupopen()
            self.my_thread([])
            return
        srcm = result_new.content
        soup = BeautifulSoup(srcm, "lxml")
        found = soup.find('ul',{"class": "List--Download--Mycima--Single"})
        foundres = found.find_all("resolution")
        foundqu = found.find_all("quality")
        foundlink = found.find_all("a", {"class": "hoverable activable"})
        foundsize = []
        for i in range(len(foundlink)):
            foundsize.append(foundlink[i].attrs['href'])
        rss=[]
        for i in range(len(foundres)):
            try:
                x = foundqu[i].text + "        " + foundres[i].text + "        " + str(getsize(foundsize[i])).rstrip()
            except:
                self.go_back(12)
                self.manager.get_screen('episodes').popupopen()
                self.remove_widget(self.loading_layout)
                return
            x = x.rstrip()
            x = x.rstrip()
            x = x.strip('\n')
            x = x.strip('\n')
            x = x.replace('\n', ' ')
            rss.append(x)
        Episode_DLinks = foundsize


        Episode_Ress = rss
        self.my_thread(rss)
    def put_buttons(self,ss):
        try:
            self.box = BoxLayout(size=(200,200),size_hint_y=None)
            memory_saved_image = BytesIO()
            pil_edited_image = PillowImage.open(BytesIO(ses_img_data))
            pil_edited_image.save(memory_saved_image, 'png')
            memory_saved_image.seek(0)
            image_from_memory = CoreImage(memory_saved_image, ext='png')
            image = kiImage(source='',texture=image_from_memory.texture,size=(200,200),size_hint_y=None)
            button = MDRectangleFlatIconButton(text='[b]Go Back[/b]',font_name="/storage/emulated/0/HM Cinema/font/arial",icon='arrow-up',
                                                   pos_hint={'center_x': 0.5}, size_hint=(1, None)
                                                   ,on_release=self.go_back)
            self.ids.bl_main.add_widget(button)
            labelname = Label(text=name,font_name='/storage/emulated/0/HM Cinema/font/arial')
            labelspace1 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelspace2 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelspace3 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            labelspace4 =Label(text='     ',font_name='/storage/emulated/0/HM Cinema/font/arial',padding_y=20,size=(100,70))
            if not OneSeason:
                labelseason = Label(text=epis + ' - '+season,font_name='/storage/emulated/0/HM Cinema/font/arial')
            else:
                labelseason = Label(text=epis,font_name='/storage/emulated/0/HM Cinema/font/arial')
            self.ids.bl_main.add_widget(self.box)
            self.box.add_widget(image)
            self.ids.bl_main.add_widget(labelspace1)
            self.ids.bl_main.add_widget(labelname)
            self.ids.bl_main.add_widget(labelspace2)
            self.ids.bl_main.add_widget(labelspace4)
            self.ids.bl_main.add_widget(labelseason)
            self.ids.bl_main.add_widget(labelspace3)
            for k in range(len(ss)):
                x=ss[k]
                button = MDRectangleFlatButton(text=x,theme_text_color="Primary",font_name="/storage/emulated/0/HM Cinema/font/arial",
                                               pos_hint={'center_x':0.5},size_hint=(1,None),
                                               on_release=self.manager.get_screen('fsearch').SDownload)
                self.ids.bl_main.add_widget(button)
        except:
            pass
    def go_back(self,button):
        self.manager.transition.direction = 'down'
        self.manager.current = 'episodes'
    @mainthread
    def my_thread(self,ss):
        self.put_buttons(ss)
        self.remove_widget(self.loading_layout)



def getsize(url):
    r = requests.get(url, stream=True)
    if "Content-Length" in r.headers:
        total_size = r.headers['Content-Length']
    else:
        total_size = None
    return getStandardSize(int(total_size))

def getStandardSize(size):
    itme = ['bytes', 'KB', 'MB', 'GB', 'TB']
    for x in itme:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
        size /= 1024.0
    return size


hm_cinema = """
WindowManager:
    id:smanager
    FSearch:
        name: 'fsearch'
    FResults:
    Seasons:
    Episodes:
    FResolution:
    EpisResolution:
    Heart:

<Heart>:
    name:'heart'
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
        Rectangle:
            size: self.size  
    Image:
        source: '/storage/emulated/0/HM Cinema/img/heart.svg.png'
<LoadingLayout>
    canvas.before:
        Color:
            rgba: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
        Rectangle:
            pos: self.pos
            size: self.size
    MDSpinner:
        size_hint: .1, .1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
<FSearch>:
    name: "fsearch"
    MDBottomNavigation:
        id: navigation
        panel_color: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0,1
        MDBottomNavigationItem:
            name: 'fsearch'
            text: 'Movies'
            icon: 'alpha-m-circle'
            canvas:
                Color:
                    rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
                Rectangle:
                    size: self.size  
            Image:
                source: '/storage/emulated/0/HM Cinema/img/head.jpeg'
                size: 100,50
                pos: (0,0.01)
                pos_hint: { 'center_x' :0.5,'y':0.4}
            Label:
                text: 'Welcome to HM Cinema Movies section'
                pos_hint: { 'center_x' :0.5,'y':0.15}
            MDTextFieldRound:
                icon_left: "magnify"
                hint_text: "Search"
                id: input
                multiline: False
                size: 100,50
                pos_hint: { 'center_x' :0.5,'y':0.57}
                size_hint:  0.85,0.05
                font_name: '/storage/emulated/0/HM Cinema/font/arial'
            MDRectangleFlatButton:
                text: "[b]Search[/b]"
                on_release: root.aperta(input.text,'f')
                pos_hint: { 'center_x' :0.5,'y':0.43}
            MDRectangleFlatButton:
                text: "Show arabic text"
                on_press: input.text = root.Show_Arabic(input.text)
                on_release: input.text = root.Show_Arabic(input.text)
                pos_hint: { 'center_x' :0.87,'y':0.5}

        MDBottomNavigationItem:
            name: "ssearch"
            icon: 'alpha-s-circle'
            text: 'Series'
            canvas:
                Color:
                    rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
                Rectangle:
                    size: self.size  
            Image:
                source: '/storage/emulated/0/HM Cinema/img/head.jpeg'
                size: 100,50
                pos: (0,0.01)
                pos_hint: { 'center_x' :0.5,'y':0.4}
            Label:
                text: 'Welcome to HM Cinema Series section'
                pos_hint: { 'center_x' :0.5,'y':0.15}
            MDTextFieldRound:
                icon_left: "magnify"
                hint_text: "Search"
                id: finput
                multiline: False
                size: 100,50
                pos_hint: { 'center_x' :0.5,'y':0.57}
                size_hint:  0.85,0.05
                font_name: '/storage/emulated/0/HM Cinema/font/arial'
            MDRectangleFlatButton:
                text: "[b]Search[/b]"
                on_release: root.aperta(finput.text,'s')
                pos_hint: { 'center_x' :0.5,'y':0.43}
            MDRectangleFlatButton:
                text: "Show arabic text"
                on_press: input.text = root.Show_Arabic(input.text)
                on_release: input.text = root.Show_Arabic(input.text)
                pos_hint: { 'center_x' :0.87,'y':0.5}

        MDBottomNavigationItem:
            icon: 'arrow-down-bold'
            text: 'Downloads'
            canvas:
                Color:
                    rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
        
                Rectangle:
                    size: self.size     
            name: 'downloadqueue'
            ScrollView:
                id: scroll
                size_hint: (1, 1)
                width: 390  # Button width plus BoxLayout padding
                pos_hint: {'right':1}
                BoxLayout:
                    id: bl_main
                    orientation: 'vertical'
                    size : self.size
                    size_hint_y: None
                    padding: [20, 20, 20, 20]
                    height: self.minimum_height
                    spacing: 15
        MDBottomNavigationItem:
            name: 'downloaded'
            text: 'Downloaded'
            icon: 'heart'
            canvas:
                Color:
                    rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
                Rectangle:
                    size: self.size 
            ScrollView:
                id: scroll2
                size_hint: (1, 0.95)
                width: 390  # Button width plus BoxLayout padding
                pos_hint: {'right':1}
                BoxLayout:
                    id: bl_main2
                    orientation: 'vertical'
                    size : self.size
                    size_hint_y: None
                    padding: [20, 20, 20, 20]
                    height: self.minimum_height
                    spacing: 15
  

 



<FResults>:
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0

        Rectangle:
            size: self.size     
    name: 'fresults'
    ScrollView:
        id: results_scroll
        size_hint: (1, 1)
        width: 390  # Button width plus BoxLayout padding
        pos_hint: {'right':1}
        BoxLayout:
            id: bl_main
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [20, 20, 20, 20]
            spacing: 15
<Seasons>:
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0

        Rectangle:
            size: self.size     
    name: 'seasons'
    ScrollView:
        size_hint: (1, 1)
        width: 390  # Button width plus BoxLayout padding
        pos_hint: {'right':1}
        BoxLayout:
            id: bl_main
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [20, 20, 20, 20]
            spacing: 15
<Episodes>:
    name: 'episodes'
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0
    
        Rectangle:
            size: self.size     
    ScrollView:
        size_hint: (1, 1)
        width: 390  # Button width plus BoxLayout padding
        pos_hint: {'right':1}
        BoxLayout:
            id: bl_main
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [20, 20, 20, 20]
            spacing: 15
    MDSpinner:
        id: load
        active: False
        size: dp(64), dp(64)
        size_hint: None, None
        pos_hint: {'center_x': 0.5, "center_y": .5}

<EpisResolution>:
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0

        Rectangle:
            size: self.size     
    name: 'episresolution'
    ScrollView:
        id: scroll
        size_hint: (1, 1)
        width: 390  # Button width plus BoxLayout padding
        pos_hint: {'right':1}
        BoxLayout:
            id: bl_main
            orientation: 'vertical'
            size_hint_y: None
            padding: [20, 20, 20, 20]
            height: self.minimum_height
            spacing: 15
<FResolution>:
    canvas:
        Color:
            rgb: 0x26 / 255.0, 0x32 / 255.0, 0x38 / 255.0

        Rectangle:
            size: self.size     
    name: 'fresolution'
    ScrollView:
        id: scroll
        size_hint: (1, 1)
        width: 390  # Button width plus BoxLayout padding
        pos_hint: {'right':1}
        BoxLayout:
            id: bl_main
            orientation: 'vertical'
            size : self.size
            size_hint_y: None
            padding: [20, 20, 20, 20]
            height: self.minimum_height
            spacing: 15            

<DownloadBox>
    id: downloadbox
    orientation: 'vertical'
    size : (800,200)
    size_hint_y: None
    padding: [3, 10, 3, 10]
    spacing:8
    canvas.before:
        Color:
            rgba: 1,1,1,0.25
        Rectangle:
            pos: self.pos
            size: self.size
    Label:
        id: Download_Name
        size: (110,8)
        pos_hint: {'center_x':0.5}
        font_name: '/storage/emulated/0/HM Cinema/font/arial'
        size_hint_x: None
        size_hint_y: None
    BoxLayout:
        orientation: 'horizontal'
        size : (400,8)
        size_hint_y: None
        size_hint_x: None
        spacing: 3
        id: BP

        MDIconButton:
            size_hint_y: None
            size_hint_x: None
            user_font_size: "15sp"
            pos_hint:{'center_y':0.2}
            id: PauseButton
            icon: "pause-circle-outline"
            theme_text_color: "Custom"
            text_color: 1,1,1,1
        MDProgressBar:
            id: Bar
            size_hint_y: None
            size_hint_x: None
            size:(650,6)
            min: 0
            pos_hint:{'center_x':0.07}
            max: 100
            value: 100
        MDIconButton:
            size_hint_y: None
            size_hint_x: None
            user_font_size: "15sp"
            pos_hint:{'center_y':0.2}
            id: Close
            icon: "close-circle-outline"
            theme_text_color: "Custom"
            text_color: 0.7,0,0,1

    BoxLayout:
        orientation: 'horizontal'
        size : (400,12)
        size_hint_y: None
        size_hint_x: None
        spacing: 13
        Label:
            id: fadi
            size: (300,12)
            text: '   '
            size_hint_x: None
            font_size: 13.5
        Label:
            size: (400,12)
            id: Downloaded_Size
            size_hint_x: None
        Label:
            id: shrta
            size: (8,12)
            text: ' / '
            size_hint_x: None
        Label:
            size: (200,12)
            id: Total_Size
            size_hint_x: None
        Label:
            size: (200,12)
            id: Percentage
            size_hint_x: None
        Label:
            size: (200,12)
            id: Speed
            size_hint_x: None


"""
class MyMainApp(MDApp):
    def build(self):
        self.root_widget= Builder.load_string(hm_cinema)
        self.theme_cls.primary_palette = "Blue"  # "Purple", "Red"
        self.theme_cls.primary_hue = "200"
        self.title = 'HM Cinema'
        request_permissions([Permission.INTERNET,Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        if os.path.exists(path1):
            pass
        else:
            os.mkdir(path1)
        if os.path.exists(path2):
            pass
        else:
            os.mkdir(path2)

        Clock.schedule_interval(on_pause,3)
        return self.root_widget


if __name__ == "__main__":
    MyMainApp().run()

