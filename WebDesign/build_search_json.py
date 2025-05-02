import json
import os

from bs4 import BeautifulSoup

search_data = []

# Folder where your HTML files are stored
html_folder = "./"

# Loop through all HTML files
for filename in os.listdir(html_folder):
    if filename.endswith(".html") and filename != "index.html" and filename != "HomePage.html":
        with open(os.path.join(html_folder, filename), "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text(separator=' ', strip=True)
            search_data.append({
                "title": filename.replace(".html", "").capitalize(),
                "url": filename,
                "content": text
            })

# Save to search.json
with open("search.json", "w", encoding="utf-8") as f:
    json.dump(search_data, f, indent=2)

