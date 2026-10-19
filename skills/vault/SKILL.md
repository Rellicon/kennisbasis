---
name: vault
description: "Lees, schrijf en onderhoud notities in de ingerichte lokale kennisbasis (vault): leesroute, regels voor notities en links, een nieuw project of nieuwe kennis toevoegen, verhuizen zonder links te breken, onderhoud met scripts/onderhoud.py en de wekelijkse controle. Gebruik bij elke lees-, schrijf- of onderhoudsactie in de vault; niet voor willekeurige bestanden of andere kluizen. Triggers op /vault, zet dit in de vault, onthoud dit, maak een notitie, nieuw project, waar staat dat, ruim de vault op, controleer de vault, weekcontrole."
---

# /vault

## Uitvoeringsomgeving

Kies het instructiebestand van dit programma: Claude Code `~/.claude/CLAUDE.md`, Codex `$CODEX_HOME/AGENTS.md` (standaard `~/.codex/AGENTS.md`), ChatGPT desktop `~/.kennisbasis/chatgpt.md`, Gemini CLI `~/.gemini/GEMINI.md`. Staan er in `~/.kennisbasis/instellingen.txt` meer regels `Instructiebestand:`, gebruik dan die van dit programma en nooit zomaar de eerste. Lees dat bestand expliciet. Ontbreekt de registratie voor dit programma, gebruik `kennis-intro` om de bestaande vault te koppelen, zonder die opnieuw aan te maken.

Deze workflow gebruikt een blijvende vault op de computer van de gebruiker. Controleer dat de beschikbare tools daadwerkelijk die lokale bestanden kunnen lezen en (voor wijzigingen) schrijven. Een tijdelijke cloudcontainer is niet de computer van de gebruiker. Zonder lokale toegang: leg uit dat deze versie een programma op de eigen computer nodig heeft (Claude Code, Codex lokaal, ChatGPT desktop met lokale uitvoering, Gemini CLI of Mistral Vibe); maak geen vervangende vault in een tijdelijke omgeving.

Gebruik de skillnaam uit de beschikbare skills: in Claude Code `/catchup` (als plugin `/kennisbasis:catchup`), in Codex bijvoorbeeld `$catchup`, in ChatGPT via de geïnstalleerde plugin of de naam in gewone taal. `/...` hieronder is de Claude-notatie. Lees benodigde andere skills uit dit pakket; verzin geen toolnamen of installatiepaden. Een toegangsfout betekent niet dat de kennisbasis ontbreekt: meld de ontbrekende toegang en overschrijf niets.


De vault is het notitieboek van de AI-assistent: gewone tekstbestanden (markdown) in een map. Omdat het gewone tekst is, werkt hij met elk AI-programma (Claude Code, Codex, Gemini CLI, Mistral Vibe); meerdere programma's kunnen dezelfde vault delen. Het pad staat bij `Vault:` in `~/.kennisbasis/instellingen.txt`, net als het pad van het instructiebestand (het bestand dat het programma elke sessie leest). Ontbreekt dat bestand, start dan eerst `kennis-intro`.

## Drie plekken, nooit mengen

| Plek | Wat | Regel |
|---|---|---|
| De vault | Kennis: wat je weet over de gebruiker, projecten, mensen, afspraken, besluiten | Alleen `.md`-bestanden. Geen PDF, Word of foto's |
| De bestandsmap (`Bestanden:` in de instellingen) | De bestanden zelf: documenten, offertes, foto's, exports | Van de gebruiker. Niet verplaatsen of hernoemen zonder akkoord. De vault verwijst ernaar met het pad in backticks |
| Het instructiebestand en het ingebouwde geheugen van het programma | Wegwijzers: waar staat iets, wat is de volgende stap | Een regel per project. Nooit de kennis zelf |

Twijfel je waar iets hoort? Dan is het antwoord niet memory, maar de vault.

## Leesroute

1. Begin bij `README.md` in de hoofdmap van de vault.
2. Elke map heeft een overzichtsnotitie met dezelfde naam als de map (`Klanten/Klanten.md`, `Klanten/BakkerijDeGoudenKorst/BakkerijDeGoudenKorst.md`). Volg de links naar beneden. **Raad geen paden.**
3. Zoeken mag, maar lees een gevonden notitie samen met de overzichtsnotitie van de map, zodat je de context meekrijgt.

## Indeling

```
<vault>/
  README.md               ingang, tabel van de mappen
  Over mij/Over mij.md    wie de gebruiker is, voorkeuren, geleerde lessen
  Klanten/
    Klanten.md            lijst van alle klanten
    <Klant>/<Klant>.md    wie de klant is, contactpersonen, afspraken
    <Klant>/<Project>/<Project>.md   stand, besluiten, kennis, sessies
  Projecten/
    Projecten.md          lijst van eigen projecten en onderwerpen
    <Project>/<Project>.md   stand, besluiten, kennis, sessies
  Kennis/
    Kennis.md             lijst van onderwerpen
    <onderwerp>.md        een begrip, persoon of werkwijze per notitie
  Sessies/
    Sessies.md
    YYYY-MM-DD <onderwerp>.md
  _Bijlagen/              afbeeldingen die in een notitie getoond worden
  _Prullenbak/            wat weg mag
  _Onderhoud/             rapport van de weekcontrole en moves.tsv
```

`Klanten` is voor werk voor een ander, `Projecten` voor eigen werk. Een vault kan een van beide hebben of allebei. Overal waar deze skills "de projectnotitie" zeggen, is dat `Klanten/<Klant>/<Project>/<Project>.md` of `Projecten/<Project>/<Project>.md`.

**Namen.** Mappen en notities van klanten en projecten heten in PascalCase: woorden aan elkaar, elk met een hoofdletter, geen spaties (`BakkerijDeGoudenKorst`). Die vul je met Tab aan en ze breken niet in links of cloudmappen. De nette naam staat bij `title:` in de frontmatter en als kop in de notitie.

**Bestanden.** De bestandsmap (`Bestanden:` in de instellingen, standaard `~/Workspace/Drive`) heeft dezelfde indeling: `Klanten/<Klant>/<Project>/`. In de vault staan alleen notities, en afbeeldingen die in een notitie getoond worden in `_Bijlagen/`. Al het andere hoort in de bestandsmap.

Wordt een project groot, dan mag de projectmap extra notities krijgen (`Klanten/<Klant>/<Project>/planning.md`). De projectnotitie linkt ernaar.

## Regels voor elke notitie

- **Frontmatter bovenaan**, tussen twee regels `---`:
  ```
  ---
  title: <titel>
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  type: hub | project | kennis | persoon | sessie
  tags: [<een of twee woorden>]
  ---
  ```
- **Minstens twee links naar andere notities**, waarvan een naar de overzichtsnotitie van de map. Zo raakt niets zoek.
- **Links met het volledige pad vanaf de hoofdmap**: `[[Klanten/BakkerijDeGoudenKorst/BakkerijDeGoudenKorst|Bakkerij De Gouden Korst]]`, niet `[[BakkerijDeGoudenKorst]]`. Een kale naam gaat mis zodra twee notities zo heten.
- **Verwijzing naar een bestand buiten de vault**: het pad in backticks, `~/Documents/Werk/Bakkerij/offerte.pdf`.
- **Bestandsnamen** zonder `# / \ : * ? " < > |`.
- **Een onderwerp, een notitie.** Bestaat het onderwerp al, werk die notitie bij in plaats van een tweede te maken. Zoek dus eerst.
- **Geen geheimen**: geen wachtwoorden, pincodes, sleutels of medische gegevens.

## Een nieuw project

1. Zoek of het project al bestaat in `Klanten/` of `Projecten/`.
2. Is het werk voor een klant: maak `Klanten/<Klant>/<Project>/<Project>.md` uit `project-sjabloon.md` naast deze skill, met als `{{OUDER_LINK}}` de link naar de klantnotitie. Bestaat de klant nog niet, maak dan eerst `Klanten/<Klant>/<Klant>.md` uit `klant-sjabloon.md`. Is het eigen werk: `Projecten/<Project>/<Project>.md`, met als `{{OUDER_LINK}}` `[[Projecten/Projecten|Projecten]]`. Mapnamen in PascalCase, de nette naam bij `title:`.
3. Zet bij "Bestanden" de map met dezelfde indeling in de bestandsmap (`<Bestanden>/Klanten/<Klant>/<Project>/`). Maak die map aan als hij er niet is.
4. Draai `hubs`, zodat de klant en het project in de overzichtsnotities verschijnen.
5. Zet een wegwijzer onder "Lopend werk" in het kennisbasis-blok van het instructiebestand (formaat in de skill `save-context`).

## Nieuwe kennis ("onthoud dit")

- Over de gebruiker of hoe die wil werken: `Over mij/Over mij.md`, sectie "Geleerde lessen", een regel met datum.
- Over een project: de sectie "Kennis" of "Besluiten" van dat project.
- Los bruikbaar (een begrip, een persoon, een werkwijze): een notitie in `Kennis/` met een link in `Kennis/Kennis.md` en een link vanuit het project waar het vandaan kwam.

Zeg na het schrijven in een regel waar het staat.

## Verhuizen of hernoemen

1. Verplaats de notitie of map.
2. Zet een regel in `<vault>/_Onderhoud/moves.tsv`: `oud<TAB>nieuw`, gerekend vanaf de hoofdmap van de vault, zonder `.md`.
3. Draai `fix-moves`, dan `hubs`, dan `controle`. De soort `verhuisd-pad` moet leeg zijn.
4. Controleer dat de oude map echt leeg is voor je zegt dat het klaar is.

Weggooien bestaat niet: verplaats naar `_Prullenbak/` en zeg dat.

## Het onderhoudsscript

Naast deze skill staat `scripts/onderhoud.py`: een Python-script zonder extra pakketten dat de vault controleert en het vaste werk zelf doet. Het leest het vault-pad uit de regel `Vault:` in `~/.kennisbasis/instellingen.txt`. Ontbreekt Python, start dan eerst `kennis-tooling`.

```bash
S=<map van deze skill>/scripts/onderhoud.py
python3 "$S" controle    # rapport, past niets aan
python3 "$S" hubs        # lijsten in de overzichtsnotities bijwerken
python3 "$S" fix-links   # kale [[naam]]-links aanvullen met het pad
python3 "$S" fix-moves   # verhuisde paden herschrijven (zie "Verhuizen")
python3 "$S" fix-paths   # `pad` naar een vault-notitie omzetten in een link
python3 "$S" week        # fix-moves, hubs, fix-links, controle; rapport in _Onderhoud/laatste-controle.md
```

- **Overzichtsnotities** hebben een blok tussen `<!-- hub:auto -->` en `<!-- /hub:auto -->`. Dat blok is van het script: nooit met de hand aanpassen, draai `hubs`. Eigen uitleg staat boven het blok.
- Mappen die met `_` of `.` beginnen (`_Prullenbak`, `_Onderhoud`, `.obsidian`) slaat het script over.
- Draai `hubs` na elke nieuwe notitie of map, en `controle` na elke grotere klus.

## Onderhoudsronde ("controleer de vault")

1. Draai `week`. Dat lost het vaste werk zelf op en schrijft het rapport.
2. Loop wat het script niet kan beoordelen zelf na:
   - Projecten met status `actief` waarvan `updated` ouder is dan twee maanden: nog actief?
   - Regels onder "Lopend werk" in het instructiebestand zonder bijbehorende projectnotitie, of andersom.
3. Meld alles in een tabel `| Wat | Waar | Voorstel |` in gewone taal. Repareer de rest pas na een "ja".

## Wekelijkse controle instellen

Zo draait de onderhoudsronde elke week vanzelf, ook als het AI-programma niet openstaat. Leg dat eerst in twee zinnen uit en vraag dan welke dag en tijd goed is (voorstel: maandag 09:00; slaapt de computer dan, dan draait de controle bij het wakker worden, staat hij uit, dan wacht hij een week en vangt `/catchup` het op).

1. **Vaste plek voor het script.** Kopieer `scripts/onderhoud.py` naar `~/.kennisbasis/onderhoud.py`. Die map valt buiten Documenten en cloudmappen, zodat de planner er altijd bij kan. Bij een nieuwe versie van deze skill kopieer je hem opnieuw.
2. **Volledig pad naar Python**: `command -v python3` (Mac en Linux) of `where python` (Windows). De planner kent alleen volledige paden.
3. **De planner, per systeem:**

   **Mac (launchd).** Schrijf `~/Library/LaunchAgents/nl.kennisbasis.onderhoud.plist`:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key><string>nl.kennisbasis.onderhoud</string>
     <key>ProgramArguments</key>
     <array>
       <string>/volledig/pad/naar/python3</string>
       <string>/Users/GEBRUIKERSNAAM/.kennisbasis/onderhoud.py</string>
       <string>week</string>
       <string>--vault</string>
       <string>/volledig/pad/naar/vault</string>
     </array>
     <key>StartCalendarInterval</key>
     <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>0</integer></dict>
     <key>StandardOutPath</key><string>/Users/GEBRUIKERSNAAM/.kennisbasis/onderhoud.log</string>
     <key>StandardErrorPath</key><string>/Users/GEBRUIKERSNAAM/.kennisbasis/onderhoud.log</string>
   </dict>
   </plist>
   ```

   Weekday: 0 of 7 is zondag, 1 is maandag. Vervang GEBRUIKERSNAAM door de uitkomst van `whoami` en gebruik overal volledige paden, geen `~`. Zet hem aan met `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/nl.kennisbasis.onderhoud.plist`.

   **Windows (Taakplanner):**

   ```
   schtasks /Create /TN "Kennisbasis onderhoud" /SC WEEKLY /D MON /ST 09:00 /TR "\"C:\pad\naar\python.exe\" \"%USERPROFILE%\.kennisbasis\onderhoud.py\" week --vault \"C:\pad\naar\vault\""
   ```

   **Linux (cron):** een regel via `crontab -e`: `0 9 * * 1 /usr/bin/python3 ~/.kennisbasis/onderhoud.py week --vault /pad/naar/vault >> ~/.kennisbasis/onderhoud.log 2>&1`

4. **Meteen testen.** Start de taak een keer met de hand (Mac: `launchctl kickstart gui/$(id -u)/nl.kennisbasis.onderhoud`, Windows: `schtasks /Run /TN "Kennisbasis onderhoud"`), wacht een paar seconden en controleer dat `<vault>/_Onderhoud/laatste-controle.md` de tijd van nu heeft. Toon de gebruiker het rapport.
5. **Mac: staat de vault in Documenten, Bureaublad of een cloudmap en meldt het log `Operation not permitted`?** Dan houdt macOS de planner buiten die map. Leg uit dat dit een privacy-instelling van de Mac is en loop samen door: Systeeminstellingen, Privacy en beveiliging, Volledige schijftoegang, plusje, `Cmd+Shift+G`, het pad van Python uit stap 2 plakken, toevoegen en aanzetten. Test daarna opnieuw. Wil de gebruiker dat niet, laat de planner dan staan en zeg dat `/catchup` het opvangt (zie hieronder).
6. **Vastleggen.** Zet in het kennisbasis-blok van elk instructiebestand uit de instellingen de regel `Weekcontrole: aan (<dag> <tijd>)`.

Uitzetten: Mac `launchctl bootout gui/$(id -u)/nl.kennisbasis.onderhoud` en het plist-bestand naar `_Prullenbak`; Windows `schtasks /Delete /TN "Kennisbasis onderhoud" /F`; Linux de regel uit `crontab -e`. Zet daarna de regel in het blok op `Weekcontrole: uit`.

`/catchup` leest het rapport. Is het ouder dan acht dagen terwijl de weekcontrole aan staat, dan draaide de planner niet en draait `/catchup` de controle zelf.

## Valkuilen

- **Een lege of bijna lege map die vol hoort te zijn is een alarm.** Meld het en stop. Vul een gat nooit op met verzonnen inhoud.
- **Synchronisatie (iCloud, Drive, Obsidian Sync) kan na een verhuizing oude mappen terugzetten.** Kijk na een verhuizing nog een keer of de oude map leeg is.
- **Overzichtsnotities raken achter** als je een notitie maakt en `hubs` vergeet. Draai het meteen na elke nieuwe notitie.
- **Een overzichtsnotitie helemaal overschrijven wist het hub-blok.** Draai daarna altijd `hubs`.
