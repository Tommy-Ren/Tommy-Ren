"""Build self-contained profile SVGs. Python stdlib only; no rendering services."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime, timezone
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import random
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
USER = "Tommy-Ren"
BG, PANEL, LINE = "#080e1c", "#101a2e", "#23314c"
WHITE, MUTED = "#edf4ff", "#9eafc9"
CYAN, PURPLE, GREEN = "#65e5ff", "#b39aff", "#a6f4c5"
MONO = "'Cascadia Code','SFMono-Regular',Consolas,monospace"
SANS = "'Segoe UI',Arial,sans-serif"


def text(x, y, value, size=16, color=WHITE, weight=400, mono=False, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" font-size="{size}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def svg(width, height, title, body, css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title><style>{css}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>{body}</svg>\n'''


def frame(width, height):
    return f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="{BG}" stroke="{LINE}"/>'


def save(name, content):
    ET.fromstring(content)
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")


def hero():
    rng = random.Random(42)
    stars = "".join(f'<circle cx="{rng.randrange(30,1170)}" cy="{rng.randrange(24,420)}" r="{rng.choice([.7,1,1.5])}" fill="{CYAN}" opacity="{rng.choice([.18,.3,.5])}"/>' for _ in range(65))
    grid = "".join(f'<path d="M {x} 0 V 444" stroke="{LINE}" opacity=".22"/>' for x in range(0,1200,40))
    grid += "".join(f'<path d="M 0 {y} H 1200" stroke="{LINE}" opacity=".22"/>' for y in range(0,444,40))
    body = f'''<defs>
      <linearGradient id="accent"><stop stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
      <radialGradient id="haze"><stop stop-color="#6641bd" stop-opacity=".32"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></radialGradient>
      <radialGradient id="planet" cx=".28" cy=".2"><stop stop-color="#b4f3ff"/><stop offset=".25" stop-color="#43a4c5"/><stop offset=".65" stop-color="#3e3577"/><stop offset="1" stop-color="#10172b"/></radialGradient>
      <clipPath id="edge"><rect x="1" y="1" width="1198" height="442" rx="24"/></clipPath>
    </defs><g clip-path="url(#edge)">
    <rect width="1200" height="444" fill="{BG}"/>{grid}
    <ellipse cx="960" cy="160" rx="440" ry="330" fill="url(#haze)"/>{stars}
    <path d="M 40 52 H 1158" stroke="{LINE}"/>
    <circle cx="46" cy="30" r="5" fill="#ff7b8a"/><circle cx="64" cy="30" r="5" fill="#ffce78"/><circle cx="82" cy="30" r="5" fill="{GREEN}"/>
    {text(106,35,'tommy@github: ~ / profile',13,MUTED,mono=True)}
    {text(1048,35,'VOL. 01',12,MUTED,mono=True)}
    <rect x="46" y="83" width="222" height="28" rx="14" fill="#15283b" stroke="#2a4c65"/>
    <circle class="pulse" cx="63" cy="97" r="4" fill="{CYAN}"/>
    {text(77,102,'SOFTWARE / SYSTEMS / AI',11,CYAN,mono=True)}
    {text(42,195,'TOMMY',92,WHITE,800,extra='letter-spacing="-4"')}
    <text x="42" y="285" font-family="{SANS}" font-size="108" font-weight="800" letter-spacing="-4" fill="url(#accent)">REN<tspan class="cursor" fill="{CYAN}">_</tspan></text>
    {text(47,330,'Turning curiosity into things that work.',21,MUTED)}
    {text(47,377,'SFU COMPUTING SCIENCE',13,CYAN,600,True)}
    {text(47,402,'AI concentration  /  Statistics minor  /  Burnaby, BC',12,MUTED,mono=True)}
    <g transform="translate(925 171)">
      <ellipse rx="157" ry="69" fill="none" stroke="#7960bb" stroke-width="1" transform="rotate(-24)"/>
      <ellipse rx="122" ry="118" fill="none" stroke="#34546f" stroke-dasharray="3 9"/>
      <circle r="70" fill="url(#planet)" stroke="#6acbdf" stroke-opacity=".6"/>
      <path d="M -61 -33 Q -10 -66 60 -21 M -68 -12 Q -10 -44 68 1 M -68 12 Q 0 -17 62 27" fill="none" stroke="#91dce5" stroke-width="7" opacity=".19"/>
      <g class="orbit"><circle cx="122" cy="0" r="5" fill="{CYAN}"/><circle cx="-122" cy="0" r="3" fill="{PURPLE}"/></g>
    </g>
    <rect x="675" y="257" width="458" height="148" rx="13" fill="#0c1526" stroke="#34435f"/>
    <path d="M 675 290 H 1133" stroke="#273650"/>
    <circle cx="694" cy="275" r="3" fill="{GREEN}"/>{text(708,279,'developer.config',12,MUTED,mono=True)}
    {text(696,318,'const focus = [',14,PURPLE,mono=True)}
    {text(716,342,'"reliable systems",',14,CYAN,mono=True)}
    {text(716,366,'"intelligent tools", "playable ideas"',14,GREEN,mono=True)}
    {text(696,390,']; // always a work in progress',13,MUTED,mono=True)}
    <rect y="441" width="1200" height="3" fill="url(#accent)"/>
    </g><rect x="1" y="1" width="1198" height="442" rx="24" fill="none" stroke="{LINE}"/>'''
    css = '.orbit{animation:orbit 32s linear infinite;transform-origin:0px 0px}.cursor{animation:blink 1.3s steps(1) infinite}.pulse{animation:pulse 3s ease-in-out infinite}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes blink{50%{opacity:0}}@keyframes pulse{50%{opacity:.35}}'
    save("hero.svg", svg(1200,444,"Tommy Ren — Software / Systems / AI",body,css))


def buttons():
    for name,label,accent,width,icon in [("linkedin","LINKEDIN",CYAN,152,"in"),("email","SAY HELLO",PURPLE,160,"@")]:
        body = f'<rect x="1" y="1" width="{width-2}" height="42" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
        body += text(16,28,icon,16,accent,700,True) + text(52,27,label,12,WHITE,600,True)
        save(name+".svg",svg(width,44,label,body))


def mobile_art():
    body = frame(600,490)
    body += '<defs><linearGradient id="name"><stop stop-color="#65e5ff"/><stop offset="1" stop-color="#b39aff"/></linearGradient><radialGradient id="planet"><stop stop-color="#86ddeb"/><stop offset=".4" stop-color="#4c72a6"/><stop offset="1" stop-color="#211d42"/></radialGradient></defs>'
    body += text(28,35,'tommy@github: ~ / profile',15,MUTED,mono=True)
    body += f'<path d="M 28 53 H 572" stroke="{LINE}"/>'
    body += text(28,94,'SOFTWARE / SYSTEMS / AI',16,CYAN,600,True)
    body += text(25,191,'TOMMY',83,WHITE,800)
    body += f'<text x="25" y="282" fill="url(#name)" font-family="{SANS}" font-size="96" font-weight="800">REN<tspan class="cursor">_</tspan></text>'
    body += '<g transform="translate(468 220)"><ellipse rx="92" ry="38" fill="none" stroke="#8472ba" transform="rotate(-25)"/><circle r="52" fill="url(#planet)"/><g class="orbit"><circle cx="85" cy="0" r="4" fill="#65e5ff"/></g></g>'
    body += text(28,332,'Turning curiosity into',22,MUTED)
    body += text(28,363,'things that work.',22,MUTED)
    body += f'<path d="M 28 393 H 572" stroke="{LINE}"/>'
    body += text(28,425,'SFU COMPUTING SCIENCE',17,CYAN,600,True)
    body += text(28,457,'AI / Statistics / Burnaby, BC',17,MUTED,mono=True)
    css='.orbit{animation:orbit 32s linear infinite;transform-origin:0px 0px}.cursor{animation:blink 1.3s steps(1) infinite}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes blink{50%{opacity:0}}'
    save('hero-mobile.svg',svg(600,490,'Tommy Ren — Software / Systems / AI',body,css))
    rows=[('LANGUAGES',CYAN,['Python / TypeScript / JavaScript','C / C++ / C# / Java / SQL']),
          ('BACKEND + SYSTEMS',PURPLE,['FastAPI / Flask / Node.js','TCP/IP / Concurrency']),
          ('FRONTEND + GAMES',GREEN,['React / Next.js','HTML / CSS / Unity']),
          ('CLOUD + DATA','#ffbc93',['AWS EC2 / ECS / Docker','PostgreSQL / Firebase'])]
    body=frame(600,544)
    for i,(label,color,lines) in enumerate(rows):
        y=38+i*132
        body+=text(28,y,label,16,color,600,True)
        body+=text(28,y+36,lines[0],21,WHITE)
        body+=text(28,y+66,lines[1],21,WHITE)
        if i<3:
            body+=f'<path d="M 28 {y+92} H 572" stroke="{LINE}"/>'
    save('stack-mobile.svg',svg(600,544,'Tools in my orbit',body))


def divider():
    body = f'<defs><linearGradient id="line"><stop stop-color="{BG}" stop-opacity="0"/><stop offset=".3" stop-color="{CYAN}"/><stop offset=".7" stop-color="{PURPLE}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient></defs><path d="M 0 12 H 1200" stroke="url(#line)" stroke-opacity=".5"/><path d="M 590 12 L 600 6 L 610 12 L 600 18 Z" fill="{CYAN}"/>'
    save("divider.svg",svg(1200,24,"",body))


def stack():
    rows = [
        ("LANGUAGES",CYAN,["Python","TypeScript","JavaScript","C / C++","C#","Java","SQL"]),
        ("BACKEND + SYSTEMS",PURPLE,["FastAPI","Flask","Node.js","TCP/IP","Concurrency"]),
        ("FRONTEND + GAMES",GREEN,["React","Next.js","HTML / CSS","Unity"]),
        ("CLOUD + DATA","#ffbc93",["AWS EC2 / ECS","Docker","PostgreSQL","Firebase"]),
    ]
    body = frame(1200,284)
    for idx,(label,color,items) in enumerate(rows):
        y = 37 + idx*65
        body += text(28,y+10,label,13,color,600,True)
        x = 245
        for item in items:
            w = len(item)*8.5 + 27
            body += f'<rect x="{x}" y="{y-12}" width="{w}" height="34" rx="8" fill="{PANEL}" stroke="{LINE}"/>' + text(x+13,y+10,item,14,WHITE,mono=True)
            x += w+10
        if idx != 3:
            body += f'<path d="M 28 {y+37} H 1172" stroke="{LINE}" opacity=".6"/>'
    save("stack.svg",svg(1200,284,"Tools in my orbit",body))


def fetch(url, api=False):
    headers = {"User-Agent":"Tommy-Ren-Profile", "Accept":"application/vnd.github+json" if api else "text/html"}
    if api and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as response:
        return response.read().decode("utf-8")


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []
        self.tooltips = {}
        self.tip_id = None

    def handle_starttag(self,tag,attrs):
        attrs = dict(attrs)
        if "data-date" in attrs and "data-level" in attrs:
            self.cells.append({"date":attrs["data-date"],"level":int(attrs["data-level"]),"id":attrs["id"]})
        if tag == "tool-tip":
            self.tip_id = attrs.get("for")
            if self.tip_id:
                self.tooltips[self.tip_id] = ""

    def handle_data(self,data):
        if self.tip_id:
            self.tooltips[self.tip_id] += data

    def handle_endtag(self,tag):
        if tag == "tool-tip":
            self.tip_id = None


def refresh():
    profile = json.loads(fetch(f"https://api.github.com/users/{USER}",True))
    repos = []
    page = 1
    while True:
        batch = json.loads(fetch(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}",True))
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    parser = CalendarParser()
    parser.feed(fetch(f"https://github.com/users/{USER}/contributions"))
    cells = sorted(parser.cells,key=lambda cell:cell["date"])
    if len(cells) < 350 or len({cell["date"] for cell in cells}) != len(cells):
        raise ValueError("GitHub contribution calendar format changed; keeping the last snapshot.")
    for cell in cells:
        label = parser.tooltips.get(cell.pop("id"),"")
        match = re.search(r"([\d,]+) contributions? on",label)
        if "No contributions on" in label:
            cell["count"] = 0
        elif match:
            cell["count"] = int(match[1].replace(",",""))
        else:
            raise ValueError(f"Missing contribution count for {cell['date']}; keeping the last snapshot.")
        if cell["level"] not in range(5):
            raise ValueError("Unexpected GitHub contribution level")
    originals = [r for r in repos if not r["fork"]]
    languages = Counter(r["language"] for r in originals if r["language"])
    return {"username":USER,"updated":datetime.now(timezone.utc).date().isoformat(),
            "public_repositories":len(repos),"original_repositories":len(originals),
            "created":profile["created_at"][:4],"languages":dict(sorted(languages.items(),key=lambda v:(-v[1],v[0]))),"contributions":cells}


def activity(data):
    counts = list(data["languages"].items())
    height = 230 + ((len(counts)+3)//4)*27
    body = frame(1200,height)
    body += text(28,35,"PUBLIC REPOSITORY TELEMETRY",12,CYAN,600,True)
    body += text(1170,35,"UPDATED " + data["updated"] + " UTC",11,MUTED,mono=True,extra='text-anchor="end"')
    for x,value,label in [(28,data["public_repositories"],"PUBLIC REPOS"),(260,data["original_repositories"],"ORIGINAL REPOS"),(510,len(data["languages"]),"PRIMARY LANGUAGES"),(830,data["created"],"ON GITHUB SINCE")]:
        body += text(x,108,value,47,WHITE,700)
        body += text(x,135,label,11,MUTED,mono=True)
    body += f'<path d="M 28 157 H 1172" stroke="{LINE}"/>'
    total = sum(data["languages"].values())
    colors = [CYAN,PURPLE,GREEN,"#ffbc93","#f48ec4","#83a8ff","#e8cf84","#75cebd"]
    x = 28
    for i,(language,count) in enumerate(counts):
        w = 1144 * count/total
        body += f'<rect x="{x:.2f}" y="183" width="{w:.2f}" height="10" fill="{colors[i%len(colors)]}"/>'
        x += w
        lx,ly = 28+(i%4)*292,224+(i//4)*27
        body += f'<circle cx="{lx+4}" cy="{ly-4}" r="4" fill="{colors[i%len(colors)]}"/>'
        body += text(lx+16,ly,f"{language}  {count}",12,MUTED,mono=True)
    save("activity.svg",svg(1200,height,"Public GitHub repository statistics for Tommy Ren",body))


def contributions(data):
    cells = data["contributions"]
    first = date.fromisoformat(cells[0]["date"])
    start_ordinal = first.toordinal() - ((first.weekday()+1)%7)
    total = sum(cell["count"] for cell in cells)
    body = frame(1200,280)
    body += text(28,36,"CONTRIBUTION SIGNAL",12,CYAN,600,True)
    body += text(1170,36,f"{total:,} CONTRIBUTIONS / DISPLAYED PERIOD",11,MUTED,mono=True,extra='text-anchor="end"')
    body += text(28,61,f"{cells[0]['date']} → {cells[-1]['date']}  /  Source: GitHub contribution calendar",11,MUTED,mono=True)
    levels = ["#162238","#204557","#267887","#3cbbc5",CYAN]
    points = []
    dates = {cell["date"]:cell for cell in cells}
    weeks = (date.fromisoformat(cells[-1]["date"]).toordinal()-start_ordinal)//7+1
    step = min(21,1100/weeks)
    grid_x = (1200-weeks*step)/2
    today = date.fromisoformat(data["updated"])
    for col in range(weeks):
        for row in range(7):
            current = date.fromordinal(start_ordinal+col*7+row)
            cell = dates.get(current.isoformat())
            if not cell or current > today:
                continue
            x,y = grid_x+col*step,94+row*18
            body += f'<rect x="{x:.2f}" y="{y}" width="{step-5:.2f}" height="13" rx="3" fill="{levels[cell["level"]]}"><title>{current}: {cell["count"]} contributions</title></rect>'
        for row in (range(7) if col%2 == 0 else range(6,-1,-1)):
            current = date.fromordinal(start_ordinal+col*7+row)
            if current.isoformat() in dates and current <= today:
                points.append((grid_x+col*step+(step-5)/2,100.5+row*18))
    if points:
        path = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x,y in points)
        body += f'<path class="signal" d="{path}" pathLength="1000" stroke="{WHITE}" stroke-width="3" fill="none" stroke-linecap="round" stroke-dasharray="3 997" opacity=".7"/>'
    body += text(28,251,"SMALL COMMITS. COMPOUND PROGRESS.",11,MUTED,mono=True)
    body += text(1000,251,"LESS",10,MUTED,mono=True)
    for i,color in enumerate(levels):
        body += f'<rect x="{1043+i*18}" y="240" width="12" height="12" rx="3" fill="{color}"/>'
    body += text(1140,251,"MORE",10,MUTED,mono=True)
    css = '.signal{animation:scan 40s linear infinite}@keyframes scan{from{stroke-dashoffset:0}to{stroke-dashoffset:-1000}}@media(prefers-reduced-motion:reduce){.signal{display:none}}'
    save("contributions.svg",svg(1200,280,f"Tommy Ren — {total:,} contributions in the displayed GitHub calendar",body,css))


def footer():
    body = frame(1200,88)
    body += text(28,36,"END OF TRANSMISSION",11,CYAN,mono=True)
    body += text(28,63,"Stay curious. Keep building.",18,WHITE,600)
    body += text(1170,54,"TOMMY-REN // GITHUB",12,MUTED,mono=True,extra='text-anchor="end"')
    save("footer.svg",svg(1200,88,"Stay curious. Keep building.",body))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh",action="store_true",help="Fetch current public GitHub data")
    args = parser.parse_args()
    ASSETS.mkdir(exist_ok=True)
    snapshot = ASSETS / "profile-data.json"
    data = refresh() if args.refresh or not snapshot.exists() else json.loads(snapshot.read_text(encoding="utf-8"))
    hero()
    buttons()
    mobile_art()
    divider()
    stack()
    activity(data)
    contributions(data)
    footer()
    snapshot.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
    print(f"Built {len(list(ASSETS.glob('*.svg')))} SVG assets for {USER}; data as of {data['updated']} UTC.")


if __name__ == "__main__":
    main()
