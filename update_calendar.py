#!/usr/bin/env python3
"""Genera barca-laliga.ics des de la pagina oficial de LALIGA.
Pensat per executar-se periodicament en un hosting/GitHub Actions.
"""
import re, urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
URL="https://www.laliga.com/clubes/fc-barcelona/proximos-partidos"
OUT=Path(__file__).with_name("barca-laliga.ics")
html=urllib.request.urlopen(URL, timeout=30).read().decode("utf-8","ignore")
# La web pot canviar estructura; extraiem fragments visibles amb data/hora i FC Barcelona.
text=re.sub(r'<[^>]+>',' ', html); text=re.sub(r'\\s+',' ',text)
pat=re.compile(r'(\\d{2}\\.\\d{2}\\.\\d{4}).{0,100}?(\\d{2}:\\d{2}|--\\s*:\\s*--).{0,250}?(FC Barcelona.{0,80}?(?:VS|vs).{0,80}?|.{0,80}?(?:VS|vs).{0,80}?FC Barcelona)',re.I)
rows=[]
for m in pat.finditer(text):
 d,h,p=m.groups(); p=re.sub(r'\\s+',' ',p).strip(); rows.append((d,h.replace(' ',''),p))
# Deduplicar
seen=set(); matches=[]
for r in rows:
 if (r[0],r[2]) not in seen: seen.add((r[0],r[2])); matches.append(r)
def esc(s): return s.replace('\\','\\\\').replace(',','\\,').replace(';','\\;').replace('\\n','\\n')
now=datetime.now(ZoneInfo('UTC')).strftime('%Y%m%dT%H%M%SZ')
L=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Barca LaLiga Dynamic//CA','CALSCALE:GREGORIAN','METHOD:PUBLISH','X-WR-CALNAME:Barca - LALIGA','X-WR-TIMEZONE:Europe/Madrid','REFRESH-INTERVAL;VALUE=DURATION:PT6H','X-PUBLISHED-TTL:PT6H']
for d,h,title in matches:
 dt=datetime.strptime(d,'%d.%m.%Y'); uid='laliga-'+dt.strftime('%Y%m%d')+'-'+re.sub(r'[^a-z0-9]','',title.lower())[:40]+'@barca-dynamic'
 L += ['BEGIN:VEVENT',f'UID:{uid}',f'DTSTAMP:{now}',f'SUMMARY:{esc(title)}']
 if h!='--:--':
  start=datetime.strptime(d+' '+h,'%d.%m.%Y %H:%M'); end=start+timedelta(hours=2)
  L += [f'DTSTART;TZID=Europe/Madrid:{start:%Y%m%dT%H%M%S}',f'DTEND;TZID=Europe/Madrid:{end:%Y%m%dT%H%M%S}']
 else:
  L += [f'DTSTART;VALUE=DATE:{dt:%Y%m%d}',f'DTEND;VALUE=DATE:{(dt+timedelta(days=1)):%Y%m%d}']
 L += [f'DESCRIPTION:Font oficial LALIGA: {URL}',f'URL:{URL}','TRANSP:TRANSPARENT','END:VEVENT']
L.append('END:VCALENDAR'); OUT.write_text('\r\n'.join(L)+'\r\n',encoding='utf-8')
print(f"Creat {OUT} amb {len(matches)} partits")
