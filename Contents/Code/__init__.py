# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

####################################################################################################

FANART = { 'Filmz TV' : 'art-filmztv.jpg', 'Filmz Exclusive' : 'art-filmzexclusive.jpg', 'Railgun TV' : 'art-railgun.jpg' }

SHOWS_FEED = "http://videovideo.dk/shows/json"

VIDEO_PREFIX = "/video/videovideodk"

NAME = L('Title')

ART           = 'art-default.jpg'
ICON          = 'icon-default.png'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("Coverflow", viewMode="Coverflow", mediaType="items")
    Plugin.AddViewGroup("PanelStream", viewMode="PanelStream", mediaType="items")
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def MainMenu():
    dir = MediaContainer(viewGroup="Coverflow")
    shows = JSON.ObjectFromURL(SHOWS_FEED)
    for show in shows:
        dir.Append(
            Function(
                DirectoryItem(Episodes,
                              show['title'],
                              summary=show['description'],
                              thumb=show['imagefull'],
                              art=GetArt(show['title'])
                ),
                title=show['title'],
                url=show['url']
            )
        )
    return dir

def Episodes(sender, title="", url=""):
    dir = MediaContainer(title2=title,viewGroup="PanelStream",art=GetArt(title))
    episodes = JSON.ObjectFromURL(url)
    for episode in episodes:
        dir.Append(Function(VideoItem(PlayEpisode,episode['title'],summary=episode['shownotes'],thumb=episode['imagefull'],subtitle=episode['timetamp']), url=episode['distributions']['720']))
    return dir

def PlayEpisode(sender,url):
    return Redirect(url)

def GetArt(key):
    if key in FANART:
        return R(FANART[key])
    else:
        return R(ART)