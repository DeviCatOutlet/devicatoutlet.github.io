# Run this after updating emote data to see if any emotes got lost
# It'll show a noisy diff for any emote that used to be an image and
# is now text, but tries to avoid being too noisy if it's just that
# the emote IDs are a digit longer.
import subprocess

block = []
for line in subprocess.run(["git", "diff"], capture_output=True, check=True, encoding="utf-8").stdout.split("\n"):
	if line.startswith("diff --git"):
		# Header line
		print(line)
	if line.startswith("-"):
		block.append(line)
	elif line.startswith("+"):
		if not block:
			print(line) # Added line
			continue
		changedfrom = block.pop(0)
		delta = len(line) - len(changedfrom)
		if 0 <= delta <= 5: continue # Accept small lengthenings, eg when emote IDs change
		print(changedfrom)
		print(line)
	else:
		# End of a block
		for removed in block:
			print(removed)
		block = []
