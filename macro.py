import os
import urllib.request
import sys
import random
import time

try:
    import pydirectinput
    import pygetwindow as gw
    pydirectinput.PAUSE = 0.001
except ImportError:
    print("[ERR]: Missing libraries.")
    print("Pls run: pip install pydirectinput pygetwindow")
    input("Press Enter to exit...")
    sys.exit()

file = "words_alpha.txt"
url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
twindow = "Roblox"
typochance = 0.05

cyan_c = "\033[96m"
green_c = "\033[92m"
yellow_c = "\033[93m"
red_c = "\033[91m"
reset_c = "\033[0m"
bold_c = "\033[1m"

neightypo = {
    'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfc', 'e': 'wsdr',
    'f': 'drtg', 'g': 'ftyhb', 'h': 'gyujn', 'i': 'ujko', 'j': 'huikm',
    'k': 'jiolm', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx'
}


def loadword():
    if not os.path.exists(file):
        print("Downloading dictionary...")
        urllib.request.urlretrieve(url, file)
    with open(file, "r") as f:
        return [w for w in f.read().splitlines() if len(w) >= 2]

def humdel(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def ftypingdel():
    if random.random() < 0.10:
        humdel(0.3, 0.7)
    else:
        humdel(0.08, 0.15)


def getypochar(correctchar):
    if correctchar in neightypo:
        return random.choice(neightypo[correctchar])
    return None

def focustype(fullword, query, utypo=False):
    suffix = fullword[len(query):]

    try:
        scriptwind = gw.getActiveWindow()
    except:
        scriptwind = None

    try:
        windows = gw.getWindowsWithTitle("Roblox")
        if not windows:
            return "[ERR]: Roblox not found"

        twindow = windows[0]
        if twindow.isMinimized:
            twindow.restore()

        twindow.activate()
         
        humdel(0.04, 0.08)

        if suffix:
            for char in suffix:

                if utypo and random.random() < typochance:
                    wrongchars = getypochar(char)
                    if wrongchars:
                        pydirectinput.write(wrongchars)
                        humdel(0.08, 0.18)
                        pydirectinput.press('backspace')
                        humdel(0.06, 0.12)

                pydirectinput.write(char)
                ftypingdel()

        humdel(0.08, 0.15)
        pydirectinput.press('enter')

        if scriptwind:
            humdel(0.08, 0.15)
            try:
                scriptwind.activate()
            except:
                pass

        return f"SENT: {fullword}"

    except Exception as e:
        return f"[ERR]: {e}"

def clearview():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clearview()
    print(f"{cyan_c}Loading Words...{reset_c}")
    words = loadword()

    clearview()
    print(f"{bold_c}=== [SEARCH] LAST LETTER MACRO by cxent==={reset_c}")
    apick = input("Enable AUTO-PICK? (y/n): ").strip().lower() == "y"

    usedword = set()
    status = "Ready"

    while True:
        clearview()
        print(f"{cyan_c}=== [AUTO] LAST LETTER MACRO by cxent ==={reset_c}")
        print(f" Mode: {yellow_c}{'AUTO-PICK' if apick else 'LIST SELECT'}{reset_c}")
        print(f" Words Used: {yellow_c}{len(usedword)}{reset_c}")
        print(f" Last Action: {green_c}{status}{reset_c}")
        print(" -----------------------------")
        print(f" {yellow_c}-i{reset_c} (Ism) | {yellow_c}-s{reset_c} (Short) | {yellow_c}-b{reset_c} (Long) | {yellow_c}-t{reset_c} (Typo)")
        print(f" {red_c}re;{reset_c} (Reset) | {red_c}ex;{reset_c} (Exit)")
        print(" -----------------------------")

        try:
            rawint = input(f"{bold_c}>> {reset_c}").strip().lower()
        except KeyboardInterrupt:
            break

        if not rawint:
            continue

        if rawint == "re;":
            usedword.clear()
            status = "Memory Cleared"
            continue

        if rawint == "ex;":
            break

        parts = rawint.split()
        query = parts[0]

        f_ism = "-i" in parts
        f_sht = "-s" in parts
        f_bst = "-b" in parts
        f_typo = "-t" in parts

        matches = [w for w in words if w.startswith(query) and w not in usedword]

        if not matches:
            status = f"No matches for '{query}'"
            continue

        selected = None
        mode_txt = ""

        if f_ism:
            ism = [w for w in matches if w.endswith("ism")]
            selected = min(ism, key=len) if ism else random.choice(matches)
            mode_txt = "(Ism)"
        elif f_sht:
            selected = min(matches, key=len)
            mode_txt = "(Short)"
        elif f_bst:
            selected = max(matches, key=len)
            mode_txt = "(Long)"
        elif apick:
            selected = random.choice(matches)
            mode_txt = "(Auto)"

        if f_typo:
            mode_txt += " [TYPO]"

        if selected:
            usedword.add(selected)
            result = focustype(selected, query, utypo=f_typo)
            status = f"{result} {mode_txt}"
            continue

if __name__ == "__main__":
    main()
