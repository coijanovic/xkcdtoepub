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

# step 1: find out number of volumes needed

############################
ppv = 333 # posts per volume
############################

volumes = (cpnum // ppv) + 1

for v in range(volumes):
    print(f"starting volume {v}/{volumes}")
    # Step 1: build the markdown file
    mdfile = open(f"xkcd_v{v}.md", "w")

    metadata = (
            "---\n"
            f"title: xkcd - volume {v}\n"
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
            f"This is volume {v} of {volumes} containing posts {v*ppv} to {v*ppv+ppv-1}\n"
            "\\newpage\n\n"
            )

    mdfile.write(intro)


    print("starting download")
    notfound = 0
    for p in range(1,ppv+1):
        # get data
        cpurl = "https://xkcd.com/" + str(v*ppv + p) + "/info.0.json"
        try: 
            cf = wget.download(cpurl, "json")
        except: 
            print(f"post {v*ppv + p} could not be downloaded")
            notfound += 1
            continue
        print(f" - post {v*ppv + p} of {cpnum}")
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

    print(f"downloaded {ppv-notfound} of {ppv}")
    print("calling pandoc")
    r = subprocess.call(f"pandoc xkcd_v{v}.md -o xkcd_v{v}.epub", shell=True)

print("finished")
