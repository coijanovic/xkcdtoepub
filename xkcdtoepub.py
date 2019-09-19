'''
This script 
1. downloads **all** posts from xkcd.com
2. compiles them into a markdown document
3. converts that document to epub
'''

import json
import wget
import subprocess

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
mdfile = open("xkcd.md", "w")

metadata = (
        "---\n"
        "title: xkcd\n"
        "subtitle: A webcomic of romance, sarcasm, math, and language.\n"
        "author: Randall Munroe\n"
        "cover-image: cover.png\n"
        "---\n"
        )

mdfile.write(metadata)

intro = (
        "# Introduction\n\n"
        "xkcd is a webcomic by Randall Munroe, it can be found at [xkcd.com](https://xkcd.com)\n\n"
        "This book was created by the `xkcdtoepub` script, which can be found at [github](https://github.com/coijanovic/xkcdtoepub)\n\n"
        "have fun!\n"
        "\\newpage\n\n"
        )

mdfile.write(intro)


print("starting download")
for p in range(1,cpnum+1):
    # get data
    cpurl = "https://xkcd.com/" + str(p) + "/info.0.json"
    cf = wget.download(cpurl, "json")
    print(f" - post {p} of {cpnum}")
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

print("calling pandoc")
r = subprocess.call("pandoc xkcd.md -o xkcd.epub", shell=True)

print("finished")
