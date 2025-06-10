import requests

url = "https://api.sr.se/api/v2/programs/index"
params = {
    "format": "json",
    "filter": "program.haspod",  # filtrera på program med podd
    "filterValue": "true",
    "pagination": "false"  # hämta allt på en gång
}

response = requests.get(url, params=params)
data = response.json()

for program in data.get("programs", []):
    print(f"{program['name']}: {program.get('description', 'Ingen beskrivning.')}")
