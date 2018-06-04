# Parse a CSV export of the giveaway spreadsheet and construct an import file
# for CutieCakeBot (DeepBot). Nothing to do with the web site, technically.
import csv
import sys

if len(sys.argv) < 2:
	print("Provide a CSV file to parse, please! You may be able to do this by")
	print("dragging and dropping the file onto me.")
	sys.exit(1)

# Override the columns so we get actual keywords
fieldnames = "timestamp,username,email,bio,social1,social2,title,description,need_shipping,destinations,reference,more_prizes,keyword".split(",")
with open(sys.argv[1]) as f:
	# Since we're overriding the columns, skip the first row (the human-readable column names)
	giveaways = list(csv.DictReader(f, fieldnames=fieldnames))[1:]

commands = []
def make(cmd, *messages):
	messages = [m for m in messages if m]
	print(cmd)
	for pos, msg in enumerate(messages):
		last = (pos == len(messages) - 1)
		commands.append({
			# All commands have these settings: enabled, mod-only, and invisible in DeepBot's web page.
			"status": True, "accessLevel": 8, "hideFromCmdList": True,
			"command": "%s%d" % (cmd, pos) if pos else cmd, "message": msg,
			"CommandChaningCmdName": "" if last else "%s%d" % (cmd, pos+1), # Trigger command "chaning" [sic]
		})
		print(msg)
		if len(msg) > 400:
			print("** Message exceeds 400 characters, probably won't work **", file=sys.stderr)
			sys.exit(1)

for info in giveaways:
	# Unless overridden, the keyword is the giver's username.
	# Should we strip out hyphens and underscores?
	kwd = info["keyword"] or info["username"].lower()
	sparkles = "\u2728 %s \u2728" % info["username"]
	# There are potentially two social media links, but either or both could be absent.
	if info["social1"] and info["social2"]:
		social = info["social1"] + " | " + info["social2"]
	else:
		social = info["social1"] or info["social2"] # or ""
	# Shipping isn't needed for everything. If it is, there may be restrictions.
	if info["need_shipping"] == "Yes":
		shipping = sparkles + " NOTE: This is a physical item; you will need to provide a shipping address."
		if "International" in info["destinations"]:
			shipping += " Can be shipped anywhere in the world!"
		else:
			shipping += " Ships to " + info["destinations"].replace(", ", " and ") + " only."
	else:
		shipping = ""
	# First command is !keyword and has the main details. It chains.
	make("!" + kwd, "%s %s! %s Wait for the raffle to begin and do a !ticket command to join!" % (
			sparkles, info["title"], info["description"]),
		sparkles + " Giveaway reference: " + info["reference"],
		shipping,
		sparkles + " " + info["bio"],
		social and sparkles + " " + social,
	)
	# Then we have the "!keywordwin" command for the mods to tag the winner with.
	make("!%swin" % kwd, "/w @target@ Congratulations! You won username's %s! To claim your gift, send a message to %s" % (
		info["title"], info["email"]))
	print()

import json
with open("giveaways.json", "w") as fp:
	json.dump(commands, fp=fp, indent=4)
print("%d commands created." % len(commands))
