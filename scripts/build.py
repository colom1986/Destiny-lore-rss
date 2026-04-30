import feedparser
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Verified lore-heavy creators
FEEDS = [
     "https://www.youtube.com/feeds/videos.xml?channel_id=UCQZFAQPTQtrFrTu6Hb4vwsw",
     "https://www.youtube.com/feeds/videos.xml?channel_id=UCc5nW05ZkYg_B9H7Yk9vP3Q",
     "https://www.youtube.com/feeds/videos.xml?channel_id=UCd7o8K6yq7V2bZp7FvH8s7w",
     "https://www.youtube.com/feeds/videos.xml?channel_id=UCJr7kCqV0E6uJ9QpY9sJp6Q",
     "https://www.youtube.com/feeds/videos.xml?channel_id=UCQ0t0K0x7y6yD6Z7X8v9w0Q",
]

# Lore filter keywords
KEYWORDS = ["lore", "story", "history", "explained", "timeline"]

# Junk filters
BLOCK = ["shorts", "clip", "live", "stream"]

items = []

for url in FEEDS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        title = entry.title.lower()

        if not any(k in title for k in KEYWORDS):
            continue
        if any(b in title for b in BLOCK):
            continue

        items.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published_parsed
        })

# Deduplicate
seen = set()
unique = []
for item in items:
    if item["link"] not in seen:
        seen.add(item["link"])
        unique.append(item)

# ⏱ Sort newest first
unique.sort(key=lambda x: x["published"], reverse=True)

# Build RSS
rss = Element('rss', version='2.0')
channel = SubElement(rss, 'channel')

SubElement(channel, 'title').text = "Destiny 2 Lore Feed"
SubElement(channel, 'link').text = "https://youtube.com"
SubElement(channel, 'description').text = "Filtered Destiny Lore Videos"

for item in unique[:30]:
    i = SubElement(channel, 'item')
    SubElement(i, 'title').text = item["title"]
    SubElement(i, 'link').text = item["link"]

xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="  ")

with open("docs/feed.xml", "w", encoding="utf-8") as f:
    f.write(xml_str)
