import os

pips = ["pillow", "python-dotenv", "tinify"]

for pip in pips:
    os.system("pip install " + pip)
