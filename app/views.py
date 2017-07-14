from flask import render_template,jsonify,request
from app import app
import pandas as pd

master_sheet = pd.read_csv('master_sheet.tsv',sep='\t')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/getSuggestions")
def suggestions():
	userinput = dict(request.args)
	userinput = cleanInput(userinput)
	print userinput
	return jsonify(results=generateSuggestions(userinput))

userinput = {'gaming': [u'gaming_light'],\
 'laptop_brand': [u'brand_lenovo', u'brand_hp',\
  u'brand_dell', u'brand_acer'], \
  'usages': [u'usage_coding', u'usage_photo', u'usage_cds', u'usage_office', u'usage_internet'],\
   'touch_screen': [u'tc_no'], 'other_usages': [u''], 'screen_size': [u'screen_med'],\
    'budget': [u'50000'], 'contact_no': [u''], 'windows': [u'windows_no'],\
     'photo_editing': [u'photo_editing_adv'], 'video_editing': [u'video_editing_basic'],\
      'email_address': [u''], 'buying': [u'buying_off']}

def cleanInput(userinput):
	userinput = {k.replace("[]", "") : v for k,v in userinput.iteritems()}
	if 'gaming' not in userinput.keys():
		userinput['gaming'] = []
	userinput['budget'] = int(userinput['budget'][0])
	if 'tc_no' in userinput['touch_screen']:
		userinput['touch_screen'] = False
	else:
		userinput['touch_screen'] = True
	if 'windows_no' in userinput['windows']:
		userinput['windows'] = False
	else:
		userinput['windows'] = True
	userinput['screen_size'] = screenSize(userinput['screen_size'])
	userinput['laptop_brand'] = brand(userinput['laptop_brand'])
	print userinput['laptop_brand']
	return userinput

def screenSize(screen):
	size = []
	for s in screen:
		if s == 'screen_tiny':
			size.extend([0,12.5])
		if s == 'screen_small':
			size.extend([12.5,15])
		if s == 'screen_med':
			size.extend([15,16])
		if s == 'screen_large':
			size.extend([16,18])
	return (min(size),max(size))

def brand(brands):	
	return [str(x[6:]) for x in brands]

def gamingtype(gaming):
	for x in gaming:
		if 'demanding' in x:
			return True
	return False

def videotype(video_editing):
	for x in video_editing:
		if 'adv' in x:
			return True
	return False

def phototype(photo_editing):
	for x in photo_editing:
		if 'adv' in x:
			return True
	return False

def usagetype(usage):
	for x in usage:
		if 'usage_coding' in x or 'usage_eng' in x:
			return True
	return False


def bucketSelection(uc):
	if gamingtype(uc['gaming']) or videotype(uc['video_editing']):
		return 'BV'
	elif usagetype(uc['usages']) or phototype(uc['photo_editing']):
		return 'BP'
	else:
		return 'B'

def generateSuggestions(uc):
	bucket = bucketSelection(uc)
	filteredLaptops = filterMaster(uc)
	return filteredLaptops

def filterMaster(uc):
	ms = master_sheet.copy()
	if uc['touch_screen']:
		ms = [ms['normal / touch / 360 / detachable'].isin(['360','detachable','touch'])]
	else:
		ms = ms[ms['normal / touch / 360 / detachable']=='normal']
	ms = ms[ms["Best Price"]>(uc['budget']+2000)]
	ms = ms[(ms["screen size in numbers"]<=uc['screen_size'][1]) & (ms["screen size in numbers"]>=uc['screen_size'][0])]
	ms["OS"] = ms["OS"].str.lower()
	if uc['windows']:
		ms = ms[ms["OS"].str.contains("win") | (ms["Best Price"]<(uc['budget']-6000))]
	ms = [ms['Brand'].isin(uc["laptop_brand"])]
	return ms.shape