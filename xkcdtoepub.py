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
try:
    tmpf = wget.download(cpurl, "json")
except:
    printf("post could not be downloaded. exiting.")
    exit()

cpnum = json.loads(open(tmpf).read())["num"]

print("\nCurrent number of posts: ", cpnum)

# Step 1: build the markdown file
mdfile = open("allposts.md", "w")

for p in range(1,20):
    # get data
    cpurl = "https://xkcd.com/" + str(p) + "/info.0.json"
    print("getting ", cpurl)
    cf = wget.download(cpurl, "json")
    cjson = json.loads(open(cf).read())

    # wirte data to markdown file
    mdfile.write("# " + cjson["safe_title"] + "\n\n")
    mdfile.write("![" + cjson["alt"] + "](" + cjson["img"] + ")\n\n")
    mdfile.write("\\newpage\n\n")

mdfile.close()
