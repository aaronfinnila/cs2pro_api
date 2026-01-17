# CS2 Pro Player Data Fetcher

A Python tool for fetching Counter-Strike 2 professional player data from Liquipedia, including nationality, birth date, current team, team history, and team logos.

## Features

- Fetch player information from Liquipedia
- Extract player details (country, birth date, current team)
- Retrieve complete team history
- Download team logo images
- Export data to JSON format
- Respects Liquipedia API Terms of Service (30s delay between requests)

## Prerequisites

- Python 3.6 or higher
- Internet connection

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 2. Activate the Virtual Environment

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```cmd
.venv\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install requests mwparserfromhell
```

## Configuration

Open [get_playerdata.py](get_playerdata.py) and modify the `players` array at the top of the file with the player names you want to fetch:

```python
players = ["XANTARES", "karrigan", "frozen"]
```

**Note:** Player names should match their Liquipedia page names exactly (case-sensitive).

### Example Player Names:
- `s1mple`
- `ZywOo`
- `NiKo`
- `device`
- `m0NESY`

## Usage

1. Make sure your virtual environment is activated
2. Run the script:

```bash
python get_playerdata.py
```

3. The script will:
   - Fetch data for each player in the list
   - Display progress in the terminal
   - Wait 30 seconds between API requests (Liquipedia ToS requirement)
   - Save all data to `player_data.json`

### Expected Output:
```
Fetched FaZe Clan image
Waiting 30s...
Fetched Mousesports image
Waiting 30s...
Fetched XANTARES
Waiting 30s...
...
Saved data for 3 players to player_data.json
```

## Output Format

The script generates a `player_data.json` file with the following structure:

```json
[
  {
    "name": "XANTARES",
    "country": "Turkey",
    "birth_date": "1995-08-07",
    "team": "Eternal Fire",
    "team_history": ["FaZe Clan", "Mousesports", "..."],
    "team_images": ["https://...", "https://..."]
  }
]
```

## Important Notes

- **Rate Limiting:** The script enforces a 30-second delay between API requests to comply with Liquipedia's Terms of Service
- **Execution Time:** Fetching data for multiple players can take several minutes
- **API Compliance:** Data is retrieved according to [Liquipedia API Terms of Service](https://liquipedia.net/api-terms-of-use)

## Deactivating Virtual Environment

When you're done, deactivate the virtual environment:

```bash
deactivate
```

## Data Source

All data is sourced from [Liquipedia Counter-Strike](https://liquipedia.net/counterstrike/) and is used in compliance with their API Terms of Service.

## Troubleshooting

**Player not found error:**
- Verify the player name matches their Liquipedia page exactly
- Check the player's Liquipedia page exists

**Connection errors:**
- Ensure you have a stable internet connection
- Check if Liquipedia is accessible

**Module not found:**
- Make sure your virtual environment is activated
- Reinstall dependencies with `pip install requests mwparserfromhell`
