import re

a = "/path/to/file.flac"
x = re.sub("[^\.]+$", "mp3", a)

print(x)