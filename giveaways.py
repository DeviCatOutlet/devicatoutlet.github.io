# Parse a CSV export of the giveaway spreadsheet and construct an import file
# for CutieCakeBot (DeepBot). Nothing to do with the web site, technically.
import csv
import json
import sys

if len(sys.argv) < 2:
	print("Provide a CSV file to parse, please! You may be able to do this by")
	print("dragging and dropping the file onto me.")
	sys.exit(1)

# Override the columns so we get actual keywords
# This needs to correspond, column by column, to the spreadsheet Google Forms creates.
fieldnames = "timestamp,username,email,bio,social1,social2,title,description,need_shipping,destinations,reference,more_prizes,keyword".split(",")
with open(sys.argv[1]) as f:
	# Since we're overriding the columns, skip the first row (the human-readable column names)
	giveaways = list(csv.DictReader(f, fieldnames=fieldnames))[1:]

commands = []
# Helper function to create a command that produces one or more messages.
# If it produces more than one, they are automatically chained in the bot.
def make(cmd, *messages):
	messages = [m for m in messages if m] # Remove blanks
	print(cmd)
	for pos, msg in enumerate(messages):
		if pos == len(messages) - 1:
			# It's the last (or only) one.
			chain = ""
		else:
			# There are more after this, so chain. The chained command has
			# the number of the *next* command, so for !foo2, the chained
			# command will be !foo3.
			chain = "%s%d" % (cmd, pos+1)
		if pos == 0:
			# It's the first one (and possibly the only one).
			command = cmd # Just use the command name as-is.
		else:
			# It's a chained command. Add a number onto the command so it
			# can be referenced for chaining (!foo1, !foo2, etc).
			command = "%s%d" % (cmd, pos)
		commands.append({
			# All commands have these settings: enabled, mod-only, and invisible in DeepBot's web page.
			"status": True, "accessLevel": 8, "hideFromCmdList": True,
			"command": command, "message": msg,
			"CommandChaningCmdName": chain # Trigger command "chaning" [sic]
		})
		print(msg)
		if len(msg) > 400:
			# It's possible to go a little bit over 400, but not safe.
			print("** Message exceeds 400 characters, probably won't work **", file=sys.stderr)
			sys.exit(1)

modinfo = []

for info in giveaways:
	# Unless overridden, the keyword is the giver's username.
	# Should we strip out hyphens and underscores?
	kwd = info["keyword"] or info["username"].lower()
	sparkles = "\u2728 %s \u2728" % info["username"] # This prefix goes on all the commands' messages.
	# There are potentially two social media links, but either or both could be absent.
	if info["social1"] and info["social2"]:
		social = info["social1"] + " | " + info["social2"]
	else:
		social = info["social1"] or info["social2"] # or ""
	# Shipping isn't needed for everything. If it is, there may be restrictions.
	if info["need_shipping"] == "Yes":
		shipping = " \u2728 NOTE: This is a physical item; you will need to provide a shipping address."
		if "International" in info["destinations"]:
			shipping += " Can be shipped anywhere in the world!"
		else:
			shipping += " Ships to " + info["destinations"].replace(", ", " and ") + " only."
	else:
		shipping = ""
	# First command is !keyword and has the main details. It chains.
	make("!" + kwd, "%s %s! %s Wait for the raffle to begin and do a !ticket command to join!" % (
			sparkles, info["title"], info["description"]),
		sparkles + " Giveaway reference: " + info["reference"] + shipping,
		sparkles + " " + info["bio"],
		social and sparkles + " " + social, # We skip this one if there's nothing in it
	)
	# Then we have the "!keywordwin" command for the mods to tag the winner with.
	win = "/w @target@ Congratulations! You won %s's %s! To claim your gift, send a message to %s" % (
		info["username"], info["title"], info["email"])
	make("!%swin" % kwd, win)
	print()

	modinfo.append([info["username"], info["title"], "!" + kwd, "!%swin" % kwd, win])

# Save the commands for import into DeepBot. It might be a biggish file, but it should all fit on the
# clipboard. Paste it into DeepBot as per this: http://wiki.deepbot.tv/import_and_export_commands
with open("giveaways.json", "w") as fp:
	json.dump(commands, fp=fp, indent=4)
# Save the mods' info into a CSV file. This can be laid out onto the schedule.
with open("giveaways.csv", "w") as fp:
	csv.writer(fp).writerows(modinfo)
print("%d commands created." % len(commands))
