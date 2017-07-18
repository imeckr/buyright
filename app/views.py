from flask import render_template,jsonify,request,session,redirect,url_for
from app import app
import pandas as pd

master_sheet = pd.read_csv('master_sheet.tsv',sep='\t')
suggestion_sheet = pd.read_csv('suggestions.tsv',sep='\t')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/validateInputs")
def validateInputs():
	if 'userInput' in session.keys():
		session.pop('userInput')
	userInput = dict(request.args)
	userInput = cleanInput(userInput)
	session['userInput'] = userInput
	return jsonify(data_validation=True)

@app.route("/suggestions")
def suggestions():
	if 'userInput' not in session.keys():
		return redirect(url_for('index'))
	userInput = session['userInput']
	print userInput
	suggestions = generateSuggestions(userInput)[:10]
	suggestions_light = generateSuggestions(userInput,light=True)[:10]
	text_suggestions = generateTextSuggestions(userInput)
	print text_suggestions
	return render_template('suggestions.html',suggestions=suggestions,suggestions_light=suggestions_light,text_suggestions=text_suggestions)

userInput = {'gaming': [u'gaming_light'],\
 'laptop_brand': [u'brand_lenovo', u'brand_hp',\
  u'brand_dell', u'brand_acer'], \
  'usages': [u'usage_coding', u'usage_photo', u'usage_cds', u'usage_office', u'usage_internet'],\
   'touch_screen': [u'tc_no'], 'other_usages': [u''], 'screen_size': [u'screen_med'],\
    'budget': [u'50000'], 'contact_no': [u''], 'windows': [u'windows_no'],\
     'photo_editing': [u'photo_editing_adv'], 'video_editing': [u'video_editing_basic'],\
      'email_address': [u''], 'buying': [u'buying_off']}

def cleanInput(userInput):
	userInput = {k.replace("[]", "") : v for k,v in userInput.iteritems()}
	if 'gaming' not in userInput.keys():
		userInput['gaming'] = []
	userInput['budget'] = int(userInput['budget'][0])
	if 'tc_no' in userInput['touch_screen']:
		userInput['touch_screen'] = False
	else:
		userInput['touch_screen'] = True
	if 'windows_no' in userInput['windows']:
		userInput['windows'] = False
	else:
		userInput['windows'] = True
	userInput['screen_size'] = screenSize(userInput['screen_size'])
	userInput['laptop_brand'] = brand(userInput['laptop_brand'])
	return userInput

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
	if len(size)==0:
		size=[0,18]
	return (min(size),max(size))

def brand(brands):
	brands = [str(x[6:]) for x in brands]	
	if len(brands)==0:
		brands = ["HP","Asus","Acer","Lenovo","Dell","MSI"]
	return brands

def gamingType(gaming):
	for x in gaming:
		if 'demanding' in x:
			return True
	return False

def videoType(video_editing):
	for x in video_editing:
		if 'adv' in x:
			return True
	return False

def photoType(photo_editing):
	for x in photo_editing:
		if 'adv' in x:
			return True
	return False

def usageType(usage):
	for x in usage:
		if 'usage_coding' in x or 'usage_eng' in x:
			return True
	return False


def bucketSelection(uc):
	if gamingType(uc['gaming']) or videoType(uc['video_editing']):
		return 'BV'
	elif usageType(uc['usages']) or photoType(uc['photo_editing']):
		return 'BP'
	else:
		return 'B'

def suggestionUIFormat(suggestions):
	for i in range(len(suggestions)):
		if(suggestions[i]["MS offc"]=="Yes"):
			suggestions[i]["Software"] = suggestions[i]["OS"].title() +" + MS Office"
		else:
			suggestions[i]["Software"] = suggestions[i]["OS"].title()
		if(suggestions[i]["VRAM"]=="Integrated"):
			suggestions[i]["VRAM"] = "Integrated Graphics"
		else:
			suggestions[i]["VRAM"] = suggestions[i]["VRAM"] + " " + suggestions[i]["GPU"]
	return suggestions

def generateSuggestions(uc,light=False):
	bucket = bucketSelection(uc)
	print bucket
	filteredLaptops = filterMaster(uc,light)
	sortedLaptops = sortLaptops(filteredLaptops,bucket)
	suggestionUI = suggestionUIFormat(sortedLaptops.to_dict(orient="records"))
	return suggestionUI

def filterMaster(uc,light=False):
	ms = master_sheet.copy()
	print ms.shape
	if uc['touch_screen']:
		ms = ms[ms['normal / touch / 360 / detachable'].isin(['360','detachable','touch'])]
	else:
		ms = ms[ms['normal / touch / 360 / detachable']=='normal']
	print ms.shape
	ms = ms[ms["Best Price"]<(uc['budget']+2000)]
	print ms.shape
	ms = ms[(ms["screen size in numbers"]<=uc['screen_size'][1]) & (ms["screen size in numbers"]>=uc['screen_size'][0])]
	print ms.shape
	ms["OS"] = ms["OS"].str.lower()
	if uc['windows']:
		ms = ms[ms["OS"].str.contains("win") | (ms["Best Price"]<(uc['budget']-6000))]
	print ms.shape
	ms = ms[ms['Brand'].isin(uc["laptop_brand"])]
	print ms.shape
	if light:
		ms = ms[ms["Weight"]<1.65]
	return ms

def sortLaptops(filteredLaptops,bucket):	
	if bucket == "BP":
		filteredLaptops.sort_values(["BP","processor score","RAM Memory","gpu score","VRAM Memory","MS offc"],ascending=[True,False,False,False,False,False],inplace=True)
	elif bucket == "BV":
		filteredLaptops.sort_values(["BV","gpu score","processor score","VRAM Memory","RAM Memory","MS offc"],ascending=[True,False,False,False,False,False],inplace=True)
	else:
		filteredLaptops.sort_values(["B","processor score","RAM Memory","gpu score","VRAM Memory","MS offc"],ascending=[True,False,False,False,False,False],inplace=True)
	return filteredLaptops

def generateTextSuggestions(uc):
	bucket = bucketSelection(uc)
	slabs = [0,25000,40000,60000,80000,1000000]
	for i in slabs:
		if i >= uc["budget"]:
			high = i
			break
	#Patch for budget higher than 80000
	if high>80000:
		high = 80000
	ss = suggestion_sheet.copy()
	return ss[(ss.Bucket==bucket) & (ss.Budget==high)].to_dict(orient="records")[0]

