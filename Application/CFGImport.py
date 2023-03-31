import PySimpleGUI as sg
import os.path
import urllib.request
import os
import re
import win32api
import requests
import webbrowser
from enum import Enum

sg.theme('DarkGrey15')

class user_id(Enum):
    CURRUSER = 0
    OTHERUSER = 1

steamProfiles = []
steamImages = []
steamid64ident = 76561197960265728
user = user_id.CURRUSER

def getUser(using_id):
    user = []
    if (using_id == user_id.CURRUSER):
        file = open("Assets/Text/current_user.txt")   
        for line in file:
            fields = line.split(";")
            user.append(fields[0])
            user.append(fields[1])
            user.append(fields[2])
    elif (using_id == user_id.OTHERUSER):
        file = open("Assets/Text/using_user.txt")
        for line in file:
            fields = line.split(";")
            user.append(fields[0])
            user.append(fields[1])
            user.append(fields[2])
    return user

def find_files(filename, search_path):
   result = []
   # Walking top-down from the root
   for root, subdirs, files in os.walk(search_path):
      if filename in files:
         result.append(os.path.join(root, filename))
   return result

def find_file(root_folder, rex):
    for root,dirs,subdirs in os.walk(root_folder):
        for f in dirs:
            result = rex.search(f)
            if result:
                if (os.path.basename(os.path.dirname(os.path.join(root, f))) == "Steam"):
                    return os.path.join(root, f)

def find_file_in_all_drives(file_name):
    #create a regular expression for the file
    rex = re.compile(file_name)
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        return find_file( drive, rex )

def getFolder(file_list):
    steamProfiles = file_list
    # Create a photoimage object of the image in the path
    for profile in steamProfiles:
        steam64 = int(profile) + int(steamid64ident)
        steamBanner = "https://www.steamidfinder.com/signature/"+str(steam64)+".png"
        img_data = requests.get(steamBanner).content
        with open('Assets/Images/'+str(profile)+'.png', 'wb') as handler:
            handler.write(img_data)
        steamImages.append(str(profile)+'.png')

def getUsers():
    url = "http://cfgimport.com/all_users/users.txt"
    try:
        urllib.request.urlretrieve(url, "Assets/Text/users.txt")
    except:
        print("Unable to download users")

def getConfig(userID):
    url1 = "http://cfgimport.com/uploads/"+userID+"/config.cfg"
    url2 = "http://cfgimport.com/uploads/"+userID+"/autoexec.cfg"
    url3 = "http://cfgimport.com/uploads/"+userID+"/video.txt"
    boolArr = [True, True, True]
    if (userID == getUser(user_id.CURRUSER)[1]):
        try:
            urllib.request.urlretrieve(url1, "Assets/CFG/User_CFG/config.cfg")
        except:
            boolArr[0] = False

        try:
            urllib.request.urlretrieve(url2, "Assets/CFG/User_CFG/autoexec.cfg")
        except:
            boolArr[1] = False

        try:
            urllib.request.urlretrieve(url3, "Assets/CFG/User_CFG/video.txt")
        except:
            boolArr[2] = False
    elif (userID == getUser(user_id.OTHERUSER)[1]):
        try:
            urllib.request.urlretrieve(url1, "Assets/CFG/Using_CFG/config.cfg")
        except:
            boolArr[0] = False

        try:
            urllib.request.urlretrieve(url2, "Assets/CFG/Using_CFG/autoexec.cfg")
        except:
            boolArr[1] = False

        try:
            urllib.request.urlretrieve(url3, "Assets/CFG/Using_CFG/video.txt")
        except:
            boolArr[2] = False
    return boolArr


file_list_column = [
    [
        sg.Text("Your userdata folder:", key="-USERDATA-")
    ],
    [
        sg.In(size=(35,1), enable_events=True, key="-FOLDER-")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20),
            key="-FILE LIST-"
        )
    ],
]

image_viewer_column = [
    [sg.Text("You are using your own("+getUser(user_id.CURRUSER)[0]+"'s) config for import", key="-USEDCONFIG-", visible=True), 
     sg.Button("Use your own config", visible=False, key="-OWNCONFIG-")],
    [sg.Text("Choose a profile from the list on the left", key="-SHOW1-", visible=False)],
    [sg.Image(key="-IMAGE-", visible=False)],
    [sg.Text("If the image is blank, you can check this link to see the profile:", visible=False, key="-SHOW2-")],
    [sg.Text(key="-LINK-", enable_events=True, visible=False)],
    [sg.Text("If there are no profiles, or an expected profile is not here, log in to the \naccount you need, start CS:GO, close CS:GO and relaunch the application", visible=False, key="-SHOW3-")],
    [sg.Button("Import current cfg to this profile", visible=False, key="-IMPORT BUTTON-")],
    [sg.Text("This user hasn't uploaded config.cfg", visible=False, key="-CONF-", text_color="red")],
    [sg.Text("This user hasn't uploaded autoexec.cfg", visible=False, key="-AUTO-", text_color="red")],
    [sg.Text("This user hasn't uploaded video.txt", visible=False, key="-VIDEO-", text_color="red")],
    [sg.Text("---------------------------------------------------------------------------------------------------", visible=False, key="-SHOW5-")],
    [sg.Text("If you want to search for other people's configs - Search with \nname(Case sensitive), Steam3(only last 8 digits) or community ID. \nProfiles has to be registered at cfgimport.com to show up", visible=False, key="-SHOW6-")],
    [sg.In(size=(20,1), enable_events=True, key="-SEARCH-", visible=False), sg.Button("Search", key="-SEARCH BUTTON-", visible=False)],
    [sg.Text(visible=False, key="-USER-")],
    [sg.Button(visible=False, key="-USER BUTTON-")]
]

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column)
    ]
]

folder = find_file_in_all_drives("userdata")
started = False

window = sg.Window("CFG Import Tool", layout, finalize=True)
window.SetIcon("Assets/Images/favicon.ico")

window["-FOLDER-"].update(folder)
if (os.path.basename(folder) == "userdata"):
    try: 
        file_list = os.listdir(folder)
        getFolder(file_list)
    except:
        file_list = []

    fnames = [
        "SteamID: "+
        f
        for f in file_list           
    ]
    window["-SHOW1-"].update(visible=True)
    window["-FILE LIST-"].update(fnames)

window["-LINK-"].set_cursor("hand2")
window["-LINK-"].Widget.bind("<Enter>", lambda _: window["-LINK-"].update(font=(None, 10, "underline")))
window["-LINK-"].Widget.bind("<Leave>", lambda _: window["-LINK-"].update(font=(None, 10)))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
        
    if event == "-FILE LIST-":
        try:
            file = values["-FILE LIST-"][0].split(" ")
            filename = os.path.join("Assets/Images/", file[1]+".png")
            window["-IMAGE-"].update(filename=filename, visible=True)
            steam64 = int(file[1]) + int(steamid64ident)
            link = os.path.join("https://www.steamidfinder.com/lookup/", str(steam64))
            window["-SHOW1-"].update(visible=False)
            window["-LINK-"].update(link, visible=True)
            window["-SHOW2-"].update(visible=True)
            window["-SHOW3-"].update(visible=True)
            window["-IMPORT BUTTON-"].update(visible=True)
            window["-SHOW5-"].update(visible=True)
            window["-SHOW6-"].update(visible=True)
            window["-SEARCH-"].update(visible=True)
            window["-SEARCH BUTTON-"].update(visible=True)
            window["-AUTO-"].update(visible=False)
            window["-CONF-"].update(visible=False)
            window["-VIDEO-"].update(visible=False)

        except:
            pass

    elif event == "-IMPORT BUTTON-":
        if (user == user_id.CURRUSER):
            getConfig(getUser(user_id.CURRUSER)[1])
            path = folder+"/"+file[1]+"/730/local/cfg/"
            try:
                os.replace("Assets/CFG/User_CFG/config.cfg", path+"config.cfg")
                window["-CONF-"].update("config.cfg imported", visible=True, text_color="green")
            except:
                window["-CONF-"].update("config.cfg not uploaded", visible=True, text_color="red")

            try:
                os.replace("Assets/CFG/User_CFG/autoexec.cfg", path+"autoexec.cfg")
                window["-AUTO-"].update("autoexec.cfg imported", visible=True, text_color="green")
            except:
                window["-AUTO-"].update("autoexec.cfg not uploaded", visible=True, text_color="red")
            
            try:
                os.replace("Assets/CFG/User_CFG/video.txt", path+"video.txt")
                window["-VIDEO-"].update("video.txt imported", visible=True, text_color="green")
            except:
                window["-VIDEO-"].update("video.txt not uploaded", visible=True, text_color="red")

        elif (user == user_id.OTHERUSER):
            getConfig(getUser(user_id.OTHERUSER)[1])
            path = folder+"/"+file[1]+"/730/local/cfg/"
            try:
                os.replace("Assets/CFG/Using_CFG/config.cfg", path+"config.cfg")
                window["-CONF-"].update("config.cfg imported", visible=True, text_color="green")
            except:
                window["-CONF-"].update("config.cfg not uploaded", visible=True, text_color="red")

            try:
                os.replace("Assets/CFG/Using_CFG/autoexec.cfg", path+"autoexec.cfg")
                window["-AUTO-"].update("autoexec.cfg imported", visible=True, text_color="green")
            except:
                window["-AUTO-"].update("autoexec.cfg not uploaded", visible=True, text_color="red")

            try:
                os.replace("Assets/CFG/Using_CFG/video.txt", path+"video.txt")
                window["-VIDEO-"].update("video.txt imported", visible=True, text_color="green")
            except:
                window["-VIDEO-"].update("video.txt not uploaded", visible=True, text_color="red")

    elif event == "-LINK-":
        webbrowser.open(link)

    elif event == "-SEARCH BUTTON-":
        getUsers()
        window["-AUTO-"].update(visible=False)
        window["-CONF-"].update(visible=False)
        window["-VIDEO-"].update(visible=False)
        word = values["-SEARCH-"]
        if (word != "" and word != " "):
            with open('Assets/Text/users.txt', 'r') as fp:
                # read all lines in a list
                lines = fp.readlines()
                for line in lines:
                    # check if string present on a current line
                    if line.find(word) != -1:
                        splitline = line.split(";")
                        window["-USER-"].update("Name: "+splitline[0]+", SteamID: "+splitline[1]+", CommunityID: "+splitline[2], visible=True)
                        window["-USER BUTTON-"].update("Use "+splitline[0]+"'s Config for import", visible=True)
                        break

    elif event == "-USER BUTTON-":
        window["-AUTO-"].update(visible=False)
        window["-CONF-"].update(visible=False)
        window["-VIDEO-"].update(visible=False)
        user = user_id.OTHERUSER
        window["-OWNCONFIG-"].update(visible=True)
        window["-USEDCONFIG-"].update("You are using "+splitline[0]+"'s config for import")
        with open('Assets/Text/using_user.txt', 'w') as f:
            f.write(line)
        getConfig(getUser(user_id.OTHERUSER)[1])
        print(getUser(user_id.OTHERUSER)[1])

    elif event == "-OWNCONFIG-":
        window["-AUTO-"].update(visible=False)
        window["-CONF-"].update(visible=False)
        window["-VIDEO-"].update(visible=False)
        user = user_id.CURRUSER
        window["-USEDCONFIG-"].update("You are using your own("+getUser(user_id.CURRUSER)[0]+"'s) config for import")

window.close()