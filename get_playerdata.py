import requests
import mwparserfromhell
import json
import re
import time

players = ["Magnojez"]

API_URL = "https://liquipedia.net/counterstrike/api.php"

# User-Agent for ToS of the API
HEADERS = {
    "User-Agent": "CS2Stats testing (aaronfinnilaa@gmail.com) Python requests"
}

def fetch_player_wikitext(player_name):
    params = {
        "action": "parse",
        "page": player_name,
        "format": "json",
        "prop": "wikitext"
    }
    response = requests.get(API_URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("parse", {}).get("wikitext", {}).get("*", "")

def parse_infobox(wikitext):
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    
    info = {
        "country": None,
        "birth_date": None,
        "team": None,
        "team_history": []
    }
    
    for t in templates:
        if t.name.matches("Infobox player") or t.name.matches("Infobox Player"):
            for field in ["country", "birth_date", "team"]:
                if t.has(field):
                    info[field] = str(t.get(field).value).strip()
                if t.has("team_history"):
                    teams_text = str(t.get("team_history").value)
                    teams = re.split(r",|\n", teams_text)
                    info["team_history"] = [t.split("|")[-1].strip('}') for t in teams if t.strip()
                                            and all(x not in t for x in ["Counter-Strike", "Substitute", "Inactive"])]
            break
    return info

def fetch_team_image(team_name):
    params = {
        "action": "parse",
        "page": team_name,
        "format": "json",
        "prop": "wikitext"
    }
    response = requests.get(API_URL, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    wikitext = data.get("parse", {}).get("wikitext", {}).get("*", "")
    
    wikicode = mwparserfromhell.parse(wikitext)
    templates = wikicode.filter_templates()
    
    for t in templates:
        if t.name.matches("Infobox team") or t.name.matches("Infobox Team"):
            if t.has("image"):
                image_filename = str(t.get("image").value).strip()
                
                image_filename = image_filename.replace("File:", "").strip()
                params = {
                    "action": "query",
                    "titles": f"File:{image_filename}",
                    "prop": "imageinfo",
                    "iiprop": "url",
                    "format": "json"
                }
                response = requests.get(API_URL, params=params, headers=HEADERS)
                response.raise_for_status()
                data = response.json()
                
                pages = data.get("query", {}).get("pages", {})
                page_data = next(iter(pages.values()), {})
                if "imageinfo" in page_data:
                    return page_data["imageinfo"][0].get("url")
            break
    
    return None

def clean_teams(teams):
    for i, t in enumerate(teams):
        if "}" in t:
            teams[i] = t.split("}", 1)[0].strip()
    return teams

def fetch_player_data(player_name):
    wikitext = fetch_player_wikitext(player_name)
    info = parse_infobox(wikitext)
    team_images = []
    team_history = clean_teams(info["team_history"])
    for team in team_history:
        team_images.append(fetch_team_image(team))
        print(f"Fetched {team} image")
        if team_history and team_history[-1] != team:
            print(f"Waiting 30s...")
            time.sleep(30) # Liquipedia ToS: 30s between parse requests
    
    player_data = {
        "name": player_name,
        "country": info["country"],
        "birth_date": info["birth_date"],
        "team": info["team"],
        "team_history": team_history,
        "team_images": team_images
    }
    return player_data

all_players_data = []

for player in players:
    try:
        data = fetch_player_data(player)
        all_players_data.append(data)
        print(f"Fetched {player}")
        if len(all_players_data) < len(players):
            print(f"Waiting 30s...")
            time.sleep(30)  # Liquipedia ToS: 30s between parse requests
    except Exception as e:
        print(f"Error fetching {player}: {e}")

with open("player_data.json", "w") as f:
    json.dump(all_players_data, f, indent=2)

print(f"Saved data for {len(all_players_data)} players to player_data.json")