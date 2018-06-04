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
def make(kwd, tag, next, message):
	commands.append({
		# All commands have these settings: enabled, mod-only, and invisible in DeepBot's web page.
		"status": True, "accessLevel": 8, "hideFromCmdList": True,
		"command": "!" + kwd + tag, "message": message,
		"CommandChaningCmdName": next and ("!" + kwd + next), # Trigger command "chaning" [sic]
	})
	print(message)

for info in giveaways:
	# Unless overridden, the keyword is the giver's username.
	# Should we strip out hyphens and underscores?
	kwd = info["keyword"] or info["username"].lower()
	print("\n!" + kwd)
	sparkles = "\u2728 %s \u2728" % info["username"]
	# There are potentially two social media links, but either or both could be absent.
	if info["social1"] and info["social2"]:
		social = info["social1"] + " | " + info["social2"]
	else:
		social = info["social1"] or info["social2"] # or ""
	# First command is !keyword and has the main details.
	make(kwd, "", "ref", "%s %s! %s Wait for the raffle to begin and do a !ticket command to join!" % (
			sparkles, info["title"], info["description"]))
	make(kwd, "ref", "bio", "%s Giveaway reference: %s" % (sparkles, info["reference"]))
	# Second command is the biography. No chaining if no social.
	make(kwd, "bio", social and "social", sparkles + " " + info["bio"])
	# Finally, the social media link(s), if any.
	if social: make(kwd, "social", "", sparkles + " " + social)
	print("!" + kwd + "win")
	make(kwd, "win", "", "/w @target@ Congratulations! You won username's %s! To claim your gift, send a message to %s" % (
		info["title"], info["email"]))

import json
with open("giveaways.json", "w") as fp:
	json.dump(commands, fp=fp, indent=4)
print("%d commands created." % len(commands))
