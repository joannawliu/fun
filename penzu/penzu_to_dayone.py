import json
import uuid
import zipfile
import re
from markdownify import markdownify as md, MarkdownConverter

# ── CONFIG ───────────────────────────────────────────────────────────────────
INPUT    = "penzu_journal_clean.json"   # output from penzu_export.py
OUTPUT   = "Journal.zip"               # import this file into Day One
TIMEZONE = "America/New_York"          # change to your timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# ─────────────────────────────────────────────────────────────────────────────

# pre-compile regex patterns for link conversion
HEADER_LINK = re.compile(r'^#{1,6} (\[.+?\]\(.+?\))$', re.MULTILINE)
INLINE_LINK = re.compile(r'\[(.+?)\]\((https?://[^\)]+)\)')

class DayOneConverter(MarkdownConverter):
    def convert_li(self, el, text, **kwargs):
        # count how many ul/ol ancestors this <li> has to determine indent depth
        depth = 0
        parent = el.parent
        while parent:
            if parent.name in ['ul', 'ol']:
                depth += 1
            parent = parent.parent
        indent = '  ' * (depth - 1)  # 2 spaces per level
        return f"{indent}- {text.strip()}\n"

def convert(html):
    # convert Penzu's HTML richtext to Markdown for Day One; some formatting issues remain
    result = DayOneConverter(bullets='-', newline_style='backslash').convert(html or "")
    result = HEADER_LINK.sub(r'\1', result)
    result = INLINE_LINK.sub(r'\1: <\2>', result)
    return result

# load entries and filter out junk entries created by a Penzu bug
# (hundreds of blank entries with title "Untitled" and body "Test", all created at the same timestamp)
# remove or adjust this filter if it doesn't apply to your account
data = json.load(open(INPUT))
clean = [e for e in data if not (e.get("title") == "Untitled" and (e.get("plaintext_body") or "").strip() == "Test")]
print(f"Loaded {len(data)} entries, {len(clean)} after filtering junk entries")

# convert each entry to Day One's expected JSON format
entries = []
for e in clean:
    entry = {
        "uuid":         uuid.uuid4().hex.upper(),  # Day One requires a unique ID per entry
        "creationDate": e.get("created_at", ""),
        "modifiedDate": e.get("modified_at", ""),
        "timeZone":     TIMEZONE,
        "text":         convert(e.get("richtext_body") or e.get("plaintext_body") or ""),
        "tags":         [],
        "photos":       [],
        "starred":      False,
    }
    entries.append(entry)

dayone = {
    "metadata": {"version": "1.0"},
    "entries": entries
}

# Day One expects a zip file containing a single Journal.json file
json_bytes = json.dumps(dayone, ensure_ascii=False, indent=2).encode("utf-8")
with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("Journal.json", json_bytes)

print(f"✅ Done! {len(entries)} entries written to {OUTPUT}")
print("Import via: Day One -> File -> Import -> Day One JSON")
