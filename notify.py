import pynotify
import feedparser
import hashlib
import os,inspect
import html2text

####################### EDIT THIS #######################

# URL of you cachet RSS
cachet = "http://cachet.herokuapp.com/rss"

#########################################################

# Define Current Path
currentpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

# File to save notified items
showed = "%s/notified.cache"%currentpath

# Function to show message on Gnome3
def sendmessage(title, message):
	pynotify.init("image")
	notice = pynotify.Notification(title,message,"%s/cachet.png"%currentpath).show()
	return notice

# Create the cache file if this not exist
if not os.path.exists(showed):
	open(showed, 'w').close()

feed = feedparser.parse(cachet)
for item in feed.entries:
	itemhash = hashlib.md5(item.title + item.updated_at).hexdigest()
	if not itemhash in open(showed).read():
		with open(showed, "ab") as myfile:
			myfile.write(itemhash + "\n")
		sendmessage("New Issue: %s (%s)"%(item.title,item.status),"%s - %s"%(html2text.html2text(item.message).replace("\n", " "), item.updated_at))
