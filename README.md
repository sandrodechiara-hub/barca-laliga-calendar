# Calendari dinamic Barca - LALIGA

Font de dades unica: pagina oficial de LALIGA del FC Barcelona.

## Posada en marxa
1. Crea un repositori de GitHub i copia `update_calendar.py` a l'arrel.
2. Copia `update.yml` a `.github/workflows/update.yml`.
3. Executa manualment el workflow una vegada.
4. Publica `barca-laliga.ics` en una URL HTTPS estable (per exemple GitHub Pages).
5. A l'iPhone, afegeix aquesta URL com a calendari per subscripcio, no importis el fitxer.

El workflow revisa periodicament la font i torna a generar el mateix fitxer. Els UID son estables per partit/data per facilitar que el client de calendari interpreti les actualitzacions.

Nota: la web de LALIGA pot canviar la seva estructura; si passa, caldra adaptar l'extractor.
