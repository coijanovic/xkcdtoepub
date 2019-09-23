# XKCD to .epub

This python script compliles all posts from [xkcd.com](https://xkcd.com) into a number of .epub files

## How to

1. Make sure you have [pandoc](https://pandoc.org) installed. It is used for the conversion from markdown to epub.
2. modify the `ppv` ("posts per volume") variable in `xkcdtoepub.py` to your liking. 
3. run the script (`python3 [path to script]/xkcdtoepub.py`)

**Note**: I had problems with ``pandoc`` not being able to handle to many post at once, ``333 ppv`` seems to work fine, but I would not go over ``1000 ppv``.
