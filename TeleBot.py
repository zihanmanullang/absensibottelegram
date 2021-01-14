import sys
import time
import calendar
import datetime
import telepot
import urllib3
import json
import math
import requests
import os
import re
import telegram
import pendulum
import importlib
import traceback
import waktu
import random
import xlsxwriter
#
from random import randint
#
import mysql
from mysql import connector
#
from geopy.geocoders import Nominatim
#
import urllib.request
import urllib.parse
#
from pymysql import*
import xlwt
import pandas.io.sql as zql


bot_time    = time.time()
HTML        = parse_mode= 'Markdown' #*text-here* << BOLD, _text-here_ << italic, [www.facebook.com] << LINK

developers  = {} # Isi chat_id / user_id khusus developer untuk mengakses command eval
staff       = {}
generaluser = {}
TOKEN       = '' # Isi token bot kedalam tanda '' , dapatkan dari @botfather
trackking   = {} # Gunanya untuk trackking data absensi
tracklunch  = {}
trackwaktu  = {}
trackreason = []

submit      = {}
activity    = {} # Gunanya untuk trackking aktivitas absensi

rangeday    = calendar.monthrange(waktu.tahun(),waktu.bulan())
countday    = calendar.monthrange(waktu.tahun(),waktu.bulan())[1]

if "Absensi %s-%s.xlsx"% (waktu.bulan(),waktu.tahun()) not in "EXCEL/":
   xlsxwriter.Workbook("EXCEL/Absensi %s-%s.xlsx" % (waktu.bulan(),waktu.tahun())).add_worksheet()
   #open("EXCEL/Absensi %s-%s.xlsx"% (waktu.bulan(),waktu.tahun()), "a")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="absensionline"
    )

lastmonth = countday+1
con       = connect(user="root",password="",host="localhost",database="absensionline")
df        = zql.read_sql("SELECT * FROM user_lokasi WHERE waktu BETWEEN '%s-%s-%s' AND '%s-%s-%s'" % (1,waktu.bulan(),waktu.tahun(),lastmonth,waktu.bulan(),waktu.tahun()),con)
df.to_excel('EXCEL/Absensi %s-%s.xls' % (waktu.bulan(),waktu.tahun()))

#Auto save DB ke excel setiap akhir bulan dan jam 7 malam
if waktu.tanggal() == countday and waktu.jam() == 19:
   lastmonth = countday+1
   con       = connect(user="root",password="",host="localhost",database="absensionline")
   df        = zql.read_sql("SELECT * FROM user_lokasi WHERE waktu BETWEEN '%s-%s-%s' AND '%s-%s-%s'" % (1,waktu.bulan(),waktu.tahun(),lastmonth,waktu.bulan(),waktu.tahun()),con)
   df.to_excel('EXCEL/Absensi %s-%s.xls' % (waktu.bulan(),waktu.tahun()))

#User level untuk akses command
def urank(chat_id):   
   if chat_id in generaluser  :return 1
   if chat_id in staff        :return 2
   if chat_id in developers   :return 3
   else                       :return 0

#Mengubah timestamp menjadi string
def strtime(total_seconds):
   MINUTE  = 60
   HOUR    = MINUTE * 60
   DAY     = HOUR * 24
   days    = int(total_seconds / DAY )
   hours   = int((total_seconds % DAY) / HOUR)
   minutes = int((total_seconds % HOUR) / MINUTE)
   seconds = int(total_seconds % MINUTE)
   string = list()
   if days > 0:string.append(days == 1 and "1 hari" or "%s" % (days) + " hari")
   if hours > 0:string.append(hours == 1 and "1 jam" or "%s" % (hours) + " jam" )
   if minutes > 0:string.append(minutes == 1 and "1 menit" or "%s" % (minutes) + " menit")
   if seconds > 0:string.append(seconds == 1 and "1 detik" or "%s" % (seconds) + " detik")
   else:
     if len(string) == 0:string.append("0 detik")
   return ", ".join(string)

#Auto delay absen
def delayabsenpagi(x):
   tomorrow    = int(x+1)
   if tomorrow <= countday:      
      extract  = datetime.datetime.now().replace(day=tomorrow, hour=7, minute=25, second=0).timestamp()
      pureit   = int(extract-datetime.datetime.now().timestamp())
   return strtime(pureit) 

#Fungsi Bot
def handle(msg):

    chat_id     = msg['chat']['id']
    realwaktu   = waktu.waktu()

    submit.update({chat_id:[waktu.jam(),waktu.menit(),waktu.detik()]})
    trackwaktu.update({chat_id:[waktu.jam(),waktu.menit(),waktu.detik()]})
    print(msg)

    if 'location' in msg.keys():
       if chat_id in trackreason:bot.sendMessage(chat_id,"[WARNING] Anda terlambat, isi alasan dahulu kemudian kirim lokasi (/telat<spasi>alasan).")
       elif chat_id in trackking:
          if activity[chat_id] == "MASUK KANTOR":
             if len(msg['location']) > 0:
                latitude        = msg['location']['latitude']
                longitude       = msg['location']['longitude']
                geolocator      = Nominatim(user_agent="Google")
                placename       = geolocator.reverse("%s, %s"%(latitude,longitude))

                if chat_id in trackking.keys():
                   names    = trackking[chat_id]["nama"]
                   waktus   = trackking[chat_id]["waktu"]
                   durasis  = trackking[chat_id]["durasi"]
                   status1  = trackking[chat_id]["status1"]
                   status2  = trackking[chat_id]["status2"]

                   #Titik lokasi penentuan dimana harus absen, silahkan gunakan google maps web untuk menentukan titik nya,
                   #library bot akan membaca berdasarkan latitude dan longitude yang didapat dari GPS yang dikirim user
                   if "Medan" in str(placename) or "" in str(placename):
                      bot.sendMessage(chat_id,"*Nama*:%s, *Status*:%s (%s), *Tanggal & Waktu*:%s, *Durasi Terlambat*: %s" % (names,status1,status2,waktus,durasis),HTML)
                      bot.sendMessage(chat_id,"[BERHASIL] Data telah tersimpan, selamat bekerja!")
                      cursor   = db.cursor()
                      sql      = "INSERT INTO user_lokasi (nama, lokasi, waktu, status) VALUES (%s, %s, %s, %s)"
                      cursor.execute(sql, (names, str(placename), waktus, status1))
                      db.commit()
                      trackking.pop(chat_id)
                      #print("trackking history telah dihapus")               
                   else:
                      bot.sendMessage(chat_id,"Titik lokasi absen salah! Ulangi lagi")

          if activity[chat_id] == "MASUK ISTIRAHAT":
             if len(msg['location']) > 0:
                latitude        = msg['location']['latitude']
                longitude       = msg['location']['longitude']
                geolocator      = Nominatim(user_agent="Google")
                placename       = geolocator.reverse("%s, %s"%(latitude,longitude))

                if chat_id in trackking.keys():
                   names    = trackking[chat_id]["nama"]
                   waktus   = trackking[chat_id]["waktu"]
                   durasis  = trackking[chat_id]["durasi"]
                   status1  = trackking[chat_id]["status1"]
                   status2  = trackking[chat_id]["status2"]

                   if "Medan" in str(placename) or "" in str(placename):
                      bot.sendMessage(chat_id,"*Nama*:%s, *Status*:%s, *Tanggal & Waktu*:%s" % (names,status1,waktus),HTML)
                      bot.sendMessage(chat_id,"[BERHASIL] Data telah tersimpan, selamat bekerja!")
                      cursor   = db.cursor()
                      sql      = "INSERT INTO user_lokasi (nama, lokasi, waktu, status) VALUES (%s, %s, %s, %s)"
                      cursor.execute(sql, (names, str(placename), waktus, status1))
                      db.commit()
                      trackking.pop(chat_id)
                      print("trackking history telah dihapus")               
                   else:
                      bot.sendMessage(chat_id,"Titik lokasi absen salah! Ulangi lagi")
       else:bot.sendMessage(chat_id,"Ketik /absen<spasi>masuk<spasi>nama , setelah itu kirim lokasi!")

    if 'caption' in msg.keys():
       if msg['caption'][0] == "/":

             command     = msg['caption'][1:].split(" ", 1)
             if len(command) > 1:
                command, args = command[0], command[1]
             else:
                command, args = command[0], ""

             if command == "absen" or command == "a":
                
                kind, field = args.split(" ", 1)

                ################################### MASUK KANTOR SECTION ###################################
                if kind == "in" or kind == "masuk":
                  jam             = submit[chat_id][0]
                  menit           = submit[chat_id][1]
                  detik           = submit[chat_id][2]
                  jams            = "%s (%s:%s:%s)" % (waktu.tanggal(),jam,menit,detik)
                  
                  todayat         = datetime.datetime.now()
                  worktime        = todayat.replace(hour=21, minute=25, second=0)
                  usertime        = todayat.replace(hour=jam, minute=menit, second=detik)
                  if usertime > worktime:
                     bot.sendMessage(chat_id,"[[WARNING]] Absensi *MASUK KANTOR* via bot dibuka mulai jam 07.25, harap tunggu %s lagi" % (delayabsenpagi(waktu.hari())),HTML)
                  elif usertime <= worktime:
                     activitys       = "MASUK KANTOR"
                     activity.update({chat_id:activitys})

                     jam             = trackwaktu[chat_id][0]
                     menit           = trackwaktu[chat_id][1]
                     detik           = trackwaktu[chat_id][2]
                     jams            = "%s (%s:%s:%s)" % (waktu.tanggal(),jam,menit,detik)
                     
                     todayat         = datetime.datetime.now()
                     worktime        = todayat.replace(hour=7, minute=45, second=0)
                     usertime        = todayat.replace(hour=jam, minute=menit, second=detik)
                     
                     cursor          = db.cursor()
                     sql             = "INSERT INTO absensi (nama, masuk) VALUES ('%s', '%s')" % (field,jams)
                     cursor.execute(sql)
                     db.commit()

                     if usertime > worktime:
                        if 'photo' in msg.keys():
                           if len(msg['photo']) > 0:
                              durationlate    = int(usertime.timestamp())-int(worktime.timestamp())
                              url             = urllib.request.urlopen("https://api.telegram.org/bot%s/getFile?file_id=%s" % (TOKEN, msg['photo'][0]["file_id"]))
                              udict           = url.read().decode('utf-8')
                              data            = json.loads(udict)
                              foto_path       = data['result']['file_path']
                              foto_url        = "https://api.telegram.org/file/bot%s/%s" % (TOKEN, foto_path)

                              foto            = urllib.request.urlopen(foto_url).read()
                              status          = "MASUK KANTOR"
                              status2         = "TELAT MASUK KANTOR"
                              sql             = "INSERT INTO upload_foto (nama, foto, waktu, status) VALUES (%s, %s, %s, %s)"
                              cursor.execute(sql, (field, foto, jams, status))
                              db.commit()
                              trackreason.append(chat_id)
                              trackking.update({chat_id:{"nama":str(field),"waktu":jams,"durasi":strtime(durationlate),"status1":"%s"%(status),"status2":"%s"%(status2)}})                                     
                              bot.sendMessage(chat_id,"[BERHASIL] Anda telat %s, jelaskan alasannya! (/telat<spasi>alasan)" % (strtime(durationlate)))

                     elif usertime <= worktime:
                        if 'photo' in msg.keys():
                           if len(msg['photo']) > 0:
                              url             = urllib.request.urlopen("https://api.telegram.org/bot%s/getFile?file_id=%s" % (TOKEN, msg['photo'][0]["file_id"]))
                              udict           = url.read().decode('utf-8')
                              data            = json.loads(udict)
                              foto_path       = data['result']['file_path']
                              foto_url        = "https://api.telegram.org/file/bot%s/%s" % (TOKEN, foto_path)

                              foto            = urllib.request.urlopen(foto_url).read()
                              status          = "MASUK KANTOR"
                              status2         = "TEPAT WAKTU"
                              sql             = "INSERT INTO upload_foto (nama, foto, waktu, status) VALUES (%s, %s, %s, %s)"
                              cursor.execute(sql, (field, foto, jams, status))                         
                              db.commit()
                              trackking.update({chat_id:{"nama":str(field),"waktu":jams,"durasi":"-","status1":"%s"%(status),"status2":"%s"%(status2)}})
                              bot.sendMessage(chat_id,"[BERHASIL] Sekarang, kirimkan lokasi!")
               
                ################################### ISTIRAHAT SECTION ###################################
                if kind == "inrest" or kind == "Inrest" or kind == "masukistirahat":
                  jam             = submit[chat_id][0]
                  menit           = submit[chat_id][1]
                  detik           = submit[chat_id][2]
                  jams            = "%s (%s:%s:%s)" % (waktu.tanggal(),jam,menit,detik)
                  
                  todayat         = datetime.datetime.now()
                  worktime        = todayat.replace(hour=9, minute=25, second=0)
                  usertime        = todayat.replace(hour=jam, minute=menit, second=detik)
                  if usertime > worktime:
                     bot.sendMessage(chat_id,"[[WARNING]] Absensi *MASUK KANTOR* via bot dibuka mulai jam 07.25, harap tunggu %s lagi" % (delayabsenpagi(waktu.hari())),HTML)
                  elif usertime <= worktime:
                     activitys       = "MASUK KANTOR"
                     activity.update({chat_id:activitys})

                     jam             = trackwaktu[chat_id][0]
                     menit           = trackwaktu[chat_id][1]
                     detik           = trackwaktu[chat_id][2]
                     jams            = "%s (%s:%s:%s)" % (waktu.tanggal(),jam,menit,detik)
                     
                     todayat         = datetime.datetime.now()
                     worktime        = todayat.replace(hour=7, minute=45, second=0)
                     usertime        = todayat.replace(hour=jam, minute=menit, second=detik)
                     
                     cursor          = db.cursor()
                     sql             = "INSERT INTO absensi (nama, masuk) VALUES ('%s', '%s')" % (field,jams)
                     cursor.execute(sql)
                     db.commit()

                     if usertime > worktime:
                        if 'photo' in msg.keys():
                           if len(msg['photo']) > 0:
                              durationlate    = int(usertime.timestamp())-int(worktime.timestamp())
                              url             = urllib.request.urlopen("https://api.telegram.org/bot%s/getFile?file_id=%s" % (TOKEN, msg['photo'][0]["file_id"]))
                              udict           = url.read().decode('utf-8')
                              data            = json.loads(udict)
                              foto_path       = data['result']['file_path']
                              foto_url        = "https://api.telegram.org/file/bot%s/%s" % (TOKEN, foto_path)

                              foto            = urllib.request.urlopen(foto_url).read()
                              status          = "MASUK KANTOR"
                              status2         = "TELAT MASUK KANTOR"
                              sql             = "INSERT INTO upload_foto (nama, foto, waktu, status) VALUES (%s, %s, %s, %s)"
                              cursor.execute(sql, (field, foto, jams, status))
                              db.commit()
                              trackreason.append(chat_id)
                              trackking.update({chat_id:{"nama":str(field),"waktu":jams,"durasi":strtime(durationlate),"status1":"%s"%(status),"status2":"%s"%(status2)}})                                     
                              bot.sendMessage(chat_id,"[BERHASIL] Anda telat %s, jelaskan alasannya! (/telat<spasi>alasan)" % (strtime(durationlate)))


    elif "text" in msg.keys():
      if msg["text"] == "Dave" or msg["text"] == "dave" or msg["text"] == "Bot" or msg["text"] == "bot":
         rancho = random.choice(["Hi "+msg['from']['first_name']+"","Haloo :)"])
         bot.sendMessage(chat_id,str(rancho))

      elif msg['text'][0] == "/":
         command     = msg['text'][1:].split(" ", 1)
         if len(command) > 1:
               command, args = command[0], command[1]
         else:
               command, args = command[0], ""

         if command == "eval" or command == "e":
            if urank(chat_id) >=3:
               ret = eval(args)
               bot.sendMessage(chat_id,str(ret))
            else:bot.sendMessage(chat_id,"Done")

         if command == "Telat" or command == "telat":
            if chat_id in trackking:
               args        = str(args)            
               namas       = trackking[chat_id]["nama"]
               waktus      = trackking[chat_id]["waktu"]
               durasis     = trackking[chat_id]["durasi"]
               status1s    = trackking[chat_id]["status1"]
               status2s    = trackking[chat_id]["status2"]
               if chat_id in trackreason:
                  cursor   = db.cursor()
                  sql      = "INSERT INTO terlambat (nama, waktu, durasi, status, alasan) VALUES (%s, %s, %s, %s, %s)"
                  cursor.execute(sql, (namas, waktus, durasis, status2s, args))
                  trackreason.remove(chat_id)
                  bot.sendMessage(chat_id,"[BERHASIL] Telah menyimpan data alasan, sekarang kirim lokasi!")
                  db.commit()
               else:bot.sendMessage(chat_id,"Anda sedang tidak terlambat, tidak perlu menggunakan perintah ini")   
            else:bot.sendMessage(chat_id,"Ketik /absen<spasi>masuk<spasi>nama , jika anda terlambat maka gunakan /late<spasi>alasan")

         if command == "uptime":
            uptime = strtime(time.time() - bot_time)
            bot.sendMessage(chat_id,"%s" % (uptime))


bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('I am Listening ...')

while 1:
    time.sleep(10)
