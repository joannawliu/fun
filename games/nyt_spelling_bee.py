import requests

# download Scrabble words with 4+ letters
def get_words():
    r = requests.get("https://raw.githubusercontent.com/redbo/scrabble/master/dictionary.txt")
    return [w.strip().lower() for w in r.text.split() if len(w) >= 4]

# get string of the day from user
while True:
    letters = input("7-letter string (1st character is center): ").lower().strip()
    if len(letters) == 7 and len(set(letters)) == 7:
        break
    print("Enter exactly 7 unique letters: ")
center = letters[0]
allowed = set(letters)

# filter words that:
# contain the center letter
# only use letters from the string
words = get_words()
valid = [w for w in words 
         if center in w and set(w).issubset(allowed)]

# display results
print(f"\n{len(valid)} words:")
for w in sorted(valid):
    print(w)
