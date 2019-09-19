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

    title = cjson["safe_title"]
    alt = cjson["alt"]
    img = cjson["img"]

    mdentry = (
            f"# {title}\n\n"
            f"![{alt}]({img})\n\n"
            "\\newpage\n\n"
            )
    # wirte data to markdown file
    mdfile.write(mdentry)

mdfile.close()
