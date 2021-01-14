import pendulum

def waktu():
   hari        = pendulum.now(pendulum.timezone('Asia/Jakarta')).day
   bulan       = pendulum.now(pendulum.timezone('Asia/Jakarta')).month
   tahun       = pendulum.now(pendulum.timezone('Asia/Jakarta')).year
   jam         = pendulum.now(pendulum.timezone('Asia/Jakarta')).hour
   menit       = pendulum.now(pendulum.timezone('Asia/Jakarta')).minute
   detik       = pendulum.now(pendulum.timezone('Asia/Jakarta')).second
   realwaktu   = "%s-%s-%s (%s:%s:%s)" % (hari,bulan,tahun,jam,menit,detik)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return timing["timming"][0]

def tanggal():
   hari        = pendulum.now(pendulum.timezone('Asia/Jakarta')).day
   bulan       = pendulum.now(pendulum.timezone('Asia/Jakarta')).month
   tahun       = pendulum.now(pendulum.timezone('Asia/Jakarta')).year
   realwaktu   = "%s-%s-%s" % (hari,bulan,tahun)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return timing["timming"][0]   

def tahun():
   tahun       = pendulum.now(pendulum.timezone('Asia/Jakarta')).year
   realwaktu   = "%s" % (tahun)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return int(timing["timming"][0])

def bulan():
   bulan       = pendulum.now(pendulum.timezone('Asia/Jakarta')).month
   realwaktu   = "%s" % (bulan)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return int(timing["timming"][0])

def hari():
   hari        = pendulum.now(pendulum.timezone('Asia/Jakarta')).day
   realwaktu   = "%s" % (hari)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return int(timing["timming"][0])

def jam():
   jam         = pendulum.now(pendulum.timezone('Asia/Jakarta')).hour
   realwaktu   = "%s" % (jam)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return int(timing["timming"][0])

def menit():
   menit       = pendulum.now(pendulum.timezone('Asia/Jakarta')).minute
   realwaktu   = "%s" % (menit)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return int(timing["timming"][0])

def detik():
   detik       = pendulum.now(pendulum.timezone('Asia/Jakarta')).second
   realwaktu   = "%s" % (detik)
   timing      = {}
   timing.update({"timming":[realwaktu]})
   return int(timing["timming"][0])

#https://pendulum.eustace.io/docs/
#eval(importlib.reload({}))
