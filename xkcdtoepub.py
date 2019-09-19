'''
This script
1. downloads **all** posts from xkcd.com
2. compiles them into a markdown document
3. converts that document to epub
'''

import subprocess
import json
import wget

# Step 0: Find out total number of posts
CP_URL = "https://xkcd.com/info.0.json"
try:
    TMPF = wget.download(CP_URL, "json")
except Exception as ex:
    print(f"post could not be downloaded: {ex}\n")
    exit()

CP_NUM = json.loads(open(TMPF).read())["num"]

print("\nCurrent number of posts: ", CP_NUM)

# step 1: find out number of VOLUMES needed

############################
PPV = 333 # posts per volume
############################

VOLUMES = (CP_NUM // PPV) + 1

for v in range(VOLUMES):
    print(f"starting volume {v}/{VOLUMES}")
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
        "This book was created by the `xkcdtoepub` script, which"
        "can be found at [github](https://github.com/coijanovic/xkcdtoepub)\n\n"
        f"This is volume {v} of {VOLUMES} containing posts {v*PPV} to {v*PPV+PPV-1}\n"
        "\\newpage\n\n"
        )

    mdfile.write(intro)


    print("starting download")
    notfound = 0
    for p in range(1, PPV+1):
        # get data
        CP_URL = "https://xkcd.com/" + str(v*PPV + p) + "/info.0.json"
        try:
            cf = wget.download(CP_URL, "json")
        except Exception as ex:
            print(f"post {v*PPV + p} could not be downloaded: {ex}\n")
            notfound += 1
            continue
        print(f" - post {v*PPV + p} of {CP_NUM}")
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

    print(f"downloaded {PPV-notfound} of {PPV}")
    print("calling pandoc")
    r = subprocess.call(f"pandoc xkcd_v{v}.md -o xkcd_v{v}.epub", shell=True)

print("finished")
