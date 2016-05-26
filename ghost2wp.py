"""
Originally made by @tzangms https://gist.github.com/tzangms/a5b640e4368204426310
Edited for user simplicity. 
Edited to bypass errors with except: exit (this is really not right, but JSON seems to differ on different Ghost versions)
Tutorial is available at: http://www.eidmantas.com/how-to-migrate-from-ghost-to-wordpress/

Requirements:
* A Wordpress Blog
* Ghost export file (json).
* Python Packages: python-wordpress-xmlrpc

  >>> pip install python-wordpress-xmlrpc

!!!!! USE THIS AT YOUR OWN RISK. !!!!! 
"""

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, GetPosts

from dateutil.parser import parse
from time import sleep
import json

"""!!! EDIT THESE VALUES, MAKE SURE TO LEAVE /XMLRPC.PHP AT THE END !!!"""

xmlrpc_endpoint = 'http://eidmantas.com/xmlrpc.php'
username = 'Eidmantas'
password = 'password'

wp = Client(xmlrpc_endpoint, username, password)

"""!!! DONT FORGET  TO UPLOAD YOUR FILE AND CHANGE ITS NAME, OR THE VARIABLE HERE !!!"""
filename = 'your-ghost-export-file.json'

with open(filename) as f:
    text = f.read()

data = json.loads(text)
for p in data['db'][0]['data']['posts']:
    print p['title']
    date = p.get('published_at', None)
    if date is None:
        p.get('created_at')
    post = WordPressPost()
    post.slug = p['slug']
    post.content = p['html']
    post.title = p['title']
    post.post_status = 'publish'
    try:
        post.date = parse(date)

    except:
        exit
    wp.call(NewPost(post))
