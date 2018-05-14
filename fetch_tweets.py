import base64
import requests
import datetime

# Fetch up Twitter credentials from Mustard Mine if available
# If not, create a config.py with the necessary IDs.
import sys
sys.path.append("../mustard-mine")
try: import config
except ImportError: import config_sample as config

# TODO: URL-encode as needed
credentials = config.TWITTER_CLIENT_ID + ":" + config.TWITTER_CLIENT_SECRET
credentials = base64.b64encode(credentials.encode("ascii")).decode("ascii")

# Load up the most recent entries on the web site
grab_next = False
last_id = None
with open("gratitudeboard.md") as f:
	data = f.read()
	grats_header, grats_lines = data.split("Twitch Gratitude Board", 1)
	grats_lines = [line for line in grats_lines.split("\n") if line]
	# sscanf(line, "%*shttps://twitter.com/DeviCatOutlet/status/%s)", last_id)
	last_id = grats_lines[0].split("https://twitter.com/DeviCatOutlet/status/")[1].split(")")[0]
print("Starting from:", last_id)
r = requests.post("https://api.twitter.com/oauth2/token",
	data={"grant_type": "client_credentials"},
	headers={"Authorization": "Basic "+credentials})
r.raise_for_status()
credentials = r.json()
if credentials["token_type"] != "bearer":
	raise ValueError("Shouldn't happen")
credentials = credentials["access_token"]
r = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json",
	params={"screen_name": "devicatoutlet", "count": 200, "trim_user": 1,
	"since_id": last_id, "include_rts": 0, "exclude_replies": 1, "tweet_mode": "extended"},
	headers={"Authorization": "Bearer "+credentials})
if r.status_code != 200:
	print(r.json())
	r.raise_for_status()

new_grats = ""

for tweet in r.json():
	if "Gratitude Board" in tweet["full_text"]:
		print(tweet["created_at"] + " " + "https://twitter.com/DeviCatOutlet/status/" + tweet["id_str"])
		print(tweet["full_text"].replace("\n", r"\n"))
		print()
		date = datetime.datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S %z %Y")
		suffix = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd"}.get(date.day, "th")
		new_grats += "* [%s %d%s, %d](https://twitter.com/DeviCatOutlet/status/%s)\n" % (
			date.strftime("%B"), date.day, suffix, date.year, tweet["id_str"])

with open("gratitudeboard.md", "w") as f:
	f.write(grats_header + "Twitch Gratitude Board\n\n" + new_grats + "\n".join(grats_lines) + "\n")
