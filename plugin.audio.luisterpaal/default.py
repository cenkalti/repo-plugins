#/*
# *      Copyright (C) 2010 Mart, Raymond
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import urllib,urllib2,re,xbmc,xbmcplugin,xbmcgui,httplib,htmllib,md5,time

PLUGIN              ='plugin.audio.luisterpaal'
VERSION             ='1.1.3'
TRACK_SEPERATOR     ='~'
DEFAULT_LUISTERPAAL ='10617791'
USER_AGENT          ='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
URL_LUISTERPALEN    ='http://3voor12.vpro.nl/luisterpaal/'
URL_ALBUM           ='http://3voor12.vpro.nl/feeds/luisterpaal/%s'
URL_COVER           ="http://images.vpro.nl/images/%s+s(200).jpg"

def LUISTERPALEN():
	#Luisterpalen, exluding default luisterpaal
	req = urllib2.Request(URL_LUISTERPALEN)
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	matchLuisterpalen = re.compile('<div class="list-text">\s*?<a href="/luisterpaal/(\d*?)">(.*?)</a>\s*?</div>').findall(link)
	for luisterpaalId, name in matchLuisterpalen:
		if luisterpaalId <> DEFAULT_LUISTERPAAL:
			name = ireplace(name, 'luisterpaal', '') + ' ...'
			addLuisterpaal(name, luisterpaalId)

def addLuisterpaal(name,luisterpaalId):
		u = sys.argv[0] + "?luisterpaalid=" + luisterpaalId
		ok = True
		name = unescape(name)
		liz = xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage='DefaultFolder.png')
		liz.setInfo(type="video", infoLabels={ "title": name } )
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

		
def ALBUMS(luisterpaalId):
	req = urllib2.Request(URL_ALBUM % (luisterpaalId, ))
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	link = response.read()
	response.close()
	matchAlbums = re.compile('<item>\s*?<title>(.*?)</title>\s*?<link>http://3voor12.vpro.nl/speler/luisterpaal/(\d*?)</link>\s*?<description>([\s\S]*?)</description>\s*?<enclosure length="\d*?" type="image/jpeg" url="http://images\.vpro\.nl/images/(\d*).*?"/>').findall(link)
	for title, albumId, description, coverId in matchAlbums:
		matchTracks = re.compile(r"\[\d*\] (.*?)&lt;br /&gt;").findall(description)
		matchTags = re.compile(r"&lt;br /&gt;Tags: (.*?)&lt;br /&gt;").findall(description)
		trackList = TRACK_SEPERATOR.join([name for name in matchTracks])
		addAlbum(title, albumId, coverId, trackList)

def addAlbum(name, albumId, coverId, tracks):
		u = sys.argv[0] + "?name=" + urllib.quote_plus(name) + "&albumid=" + albumId + "&coverid=" + coverId + "&tracks=" + urllib.quote_plus(tracks)
		cover = URL_COVER % (coverId, )
		ok = True
		name = unescape(name)
		liz = xbmcgui.ListItem(name, iconImage=cover, thumbnailImage=cover)
		liz.setInfo(type="video", infoLabels={ "title": name } )
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok

def TRACKS(name, albumId, coverId, tracks):
	tracklist = tracks.split(TRACK_SEPERATOR)
	nr = 0
	for track in tracklist:
		nr = nr + 1
		addTrack(nr, track, albumId, coverId)

def addTrack(nr,name,albumId,coverId):
		nrstr = str(nr).zfill(2)
		u = t(albumId, nrstr)
		cover = URL_COVER % (coverId, )
		ok = True
		name = unescape(name)
		liz = xbmcgui.ListItem(nrstr+'. '+name, iconImage=cover, thumbnailImage=cover)
		liz.setInfo(type="music", infoLabels={ "title": name } )
		ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
		return ok

def t(t1,t2):
	t3=[37226867320992396975461566531315574317608967475879418125453821259747188101936512193078231364454782224571989975483386379566565433493292521466557964159688068720865786131751038557861542124590128043512178306529896,25,66,78,83,0]
	t4=time.time()
	t5=(lambda t1,v:t1(v[t3[5]]))(v,t3)
	t6,t7=(lambda t1,t2,t3:t1%(t2,t3))(t5[t3[1]:t3[2]],t1,t2),(lambda t3,t4:t3%(t4,))(t5[t3[3]:t3[4]],t4)
	t8=md5.md5()
	t8.update((lambda t3,t4,t6:t3+t4+t6)(t5[t3[4]:],t6,t7))
	return (lambda t3,t4,t6,t7,t8:t3+t4+t6%(t7,t8))(t5[:t3[1]],t6,t5[t3[2]:t3[3]],t8.hexdigest(),t7)
	
def v(v1):
	v2 = []
	while v1:
		v2.append(chr(v1 % 128))
		v1 >>= 7
	return ''.join(v2)
	
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]

	return param
	
def ireplace(str, old, new):
	#case insensitive replace
	return re.sub('(?i)' + old, new, str)

def unescape(s):
	#from http://wiki.python.org/moin/EscapingHtml
	p = htmllib.HTMLParser(None)
	p.save_bgn()
	p.feed(s)
	return p.save_end()

params = get_params()
luisterpaalid = None
name = None
albumid = None
coverid = None
tracks = None
try:
		luisterpaalid = urllib.unquote_plus(params["luisterpaalid"])
except:
		pass
try:
		name = urllib.unquote_plus(params["name"])
except:
		pass
try:
		albumid = urllib.unquote_plus(params["albumid"])
except:
		pass
try:
		coverid = urllib.unquote_plus(params["coverid"])
except:
		pass
try:
		tracks = urllib.unquote_plus(params["tracks"])
except:
		pass

if not luisterpaalid and not name and not albumid and not coverid and not tracks:
		LUISTERPALEN()
		ALBUMS(DEFAULT_LUISTERPAAL)
elif luisterpaalid:
		ALBUMS(luisterpaalid)
else:
		TRACKS(name, albumid, coverid, tracks)

xbmcplugin.endOfDirectory(int(sys.argv[1]))