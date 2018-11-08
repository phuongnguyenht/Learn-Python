# Viettalk Files Migration

import json
import MySQLdb
import PIL 
from PIL import Image
import os
from shutil import copyfile
import threading
import time

class functionThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

def loadJson(fileName):
    f = open(fileName, 'r')
    return json.load(f)

avatarDb = MySQLdb.connect('localhost', 'upload', '123456a@hehe', 'avatars', 3307)
avatarCur = avatarDb.cursor()
coverDb = MySQLdb.connect('localhost', 'upload', '123456a@hehe', 'covers', 3307)
coverCur = coverDb.cursor()
photoDb = MySQLdb.connect('localhost', 'upload', '123456a@hehe', 'images_upload', 3307)
photoCur = photoDb.cursor()

def getAvatar(id):
    try:
        avatarCur.execute('SELECT path FROM images WHERE id=%d' % id)
        return 'avatars/' + avatarCur.fetchone()[0]
    except TypeError:
        return None

def getCover(id):
    try:
        coverCur.execute('SELECT path FROM images WHERE id=%d' % id)
        return 'covers/' + coverCur.fetchone()[0]
    except TypeError:
        return None

def getPhoto(id):
    try:
        val = os.path.splitext(os.path.basename(id))[0]
        photoCur.execute("SELECT path FROM images WHERE imagekey='%s'" % val)
        return 'images/' + photoCur.fetchone()[0]
    except TypeError:
        return None

def getSticker(id):
    return 'sticker/' + id

def getVoice(id):
    try:
        val = os.path.splitext(os.path.basename(id))[0]
        photoCur.execute("SELECT path FROM images WHERE imagekey='%s'" % val)
        return 'images/' + photoCur.fetchone()[0]
    except TypeError:
        return None

def resize(image, base, ratio, name):
    try:
        image = '/data/nginx-www/data/' + image
        img = Image.open(image)
        width, height = img.size
        w = 0
        h = 0
        if (width > height):
            w = 200
            h = 200 * height/width
        else:
            h = 200
            w = 200 * width/height

        w *= ratio
        h *= ratio

        size = w, h
        img.thumbnail(size, Image.ANTIALIAS)
    
        outFile = 'old_viettalk_images/' + os.path.splitext(os.path.basename(str(name)))[0] + '_t' + str(base) + '.png'
        img.save(outFile, "PNG")
    except IOError:
        print 'File error: ' + image

def copyImage(image, name):
    try:
        image = '/data/nginx-www/data/' + image
        img = Image.open(image)
        img.thumbnail(img.size, Image.ANTIALIAS)
    
        outFile = 'old_viettalk_images/' + os.path.splitext(os.path.basename(str(name)))[0] + '.png'
        img.save(outFile, "PNG")
    except IOError:
        print 'File error: ' + image

def migrateAvatars():
    print 'Migrating avatars'
    avatars = loadJson('avatars.json')

    for a in avatars:
        avatar = getAvatar(a)
        if avatar is not None:
            threads = []
            threads.append(functionThread(copyImage, avatar, a))
            threads.append(functionThread(resize, avatar, 200, 1, a))
            threads.append(functionThread(resize, avatar, 300, 3/2, a))
            threads.append(functionThread(resize, avatar, 400, 2, a))
            threads.append(functionThread(resize, avatar, 500, 5/2, a))
            for t in threads:
                t.start()
            for t in threads:
                t.join()

def migrateCovers():
    print 'Migrating covers'
    covers = loadJson('covers.json')

    for c in covers:
        cover = getCover(c)
        if cover is not None:
            threads = []
            threads.append(functionThread(copyImage, cover, c))
            threads.append(functionThread(resize, cover, 200, 1, c))
            threads.append(functionThread(resize, cover, 300, 3/2, c))
            threads.append(functionThread(resize, cover, 400, 2, c))
            threads.append(functionThread(resize, cover, 500, 5/2, c))
            for t in threads:
                t.start()
            for t in threads:
                t.join()

def migratePhotos():
    photos = loadJson('photos.json')
    timePoint = int(time.time())
    print 'Migrating photos using time point: ' + str(timePoint)

    for p in photos:
        # 6 months from now
        if (timePoint - p["time"]) > 15552000:
            break

        photo = getPhoto(p["url"])
        if photo is not None:
            copyImage(photo, p["url"])
            resize(photo, 200, 1, p["url"])
            resize(photo, 300, 3/2, p["url"])
            resize(photo, 400, 2, p["url"])
            resize(photo, 500, 5/2, p["url"])

def migrateVoices():
    print 'Migrating voices'
    voices = loadJson('voices.json')

    for v in voices:
        voice = getVoice(v)
        if voice is not None:
            try: 
                voice = '/data/nginx-www/data/' + voice 
                copyfile(voice, 'old_viettalk_voices/' + os.path.splitext(os.path.basename(v))[0])
                print '1 voice file copied'
            except IOError:
                print 'Voice file error: ' + v

def migrateStickers():
    print 'Migrating stickers'
    stickers = loadJson('stickers.json')

    for s in stickers:
        sticker = getSticker(s)
        if sticker is not None:
            try:
                sticker = '/data/nginx-www/data/' + sticker 
                copyfile(sticker, 'old_viettalk_images/' + os.path.basename(sticker))
                print '1 sticker copied'
            except IOError:
                print 'Sticker file error: ' + s 
                
migrateAvatars()
migrateCovers()
#migrateVoices()
#migrateStickers()
migratePhotos()

