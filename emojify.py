import sys
import unicodedata
if len(sys.argv) < 2:
	print("USAGE: python3 emojify.py CHARACTER")
	print("Will output Markdown to render that character as an image.")
	sys.exit(1)

if str is bytes: char = sys.argv[1].decode("UTF-8")[0] # Py2
else: char = sys.argv[1][0] # Py3
try:
	print("U+%X %s" % (ord(char), unicodedata.name(char)))
	print("")
except ValueError:
	print("U+%X <unknown>" % ord(char))

print("*![%s](https://s.w.org/images/core/emoji/2.2.1/svg/%x.svg)*" %
	(char, ord(char)))

