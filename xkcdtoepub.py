'''
This script 
1. downloads **all** posts from xkcd.com
2. compiles them into a markdown document
3. converts that document to epub
'''

import json
import wget

# Step 0: Find out total number of posts
cpurl = "https://xkcd.com/info.0.json"
tmpf = wget.download(cpurl, "json")
cpnum = json.loads(open(tmpf).read())["num"]

print("\nCurrent number of posts: ", cpnum)
