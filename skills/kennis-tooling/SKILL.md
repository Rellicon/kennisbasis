---
name: kennis-tooling
description: "Controleer Python voor het onderhoud van de kennisbasis en help ontbrekend gereedschap installeren. Node.js en npx alleen als de gebruiker een toepassing wil die ze nodig heeft. Triggers op /kennis-tooling, kennis-tooling, Python ontbreekt, installeer Python, installeer Node, npx werkt niet, en vanuit de installatie of de vault-skill als iets mist."
---

# /kennis-tooling

## Uitvoeringsomgeving

Deze workflow gebruikt een blijvende vault op de computer van de gebruiker. Controleer dat de beschikbare tools daadwerkelijk die lokale bestanden kunnen lezen en (voor wijzigingen) schrijven. Een tijdelijke cloudcontainer is niet de computer van de gebruiker. Zonder lokale toegang: leg uit dat deze versie een programma op de eigen computer nodig heeft (Claude Code, Codex lokaal, ChatGPT desktop met lokale uitvoering, Gemini CLI of Mistral Vibe); maak geen vervangende vault in een tijdelijke omgeving.

Gebruik de skillnaam uit de beschikbare skills: in Claude Code `/catchup` (als plugin `/kennisbasis:catchup`), in Codex bijvoorbeeld `$catchup`, in ChatGPT via de geïnstalleerde plugin of de naam in gewone taal. `/...` hieronder is de Claude-notatie. Lees benodigde andere skills uit dit pakket; verzin geen toolnamen of installatiepaden. Een toegangsfout betekent niet dat de kennisbasis ontbreekt: meld de ontbrekende toegang en overschrijf niets.


De gebruiker is geen developer. Doe wat je zelf kunt doen, vraag alleen om een klik of een wachtwoord als het echt moet, en zeg bij elke stap wat de gebruiker op het scherm moet zien.

## Wat en waarom

Leg dit in drie zinnen uit voor je begint:

- **Python** is een programmeertaal. De kennisbasis gebruikt het voor de wekelijkse controle van je vault. Nodig.
- **Node.js** is ook een programmeertaal, en **npx** hoort erbij: het start kleine hulpprogramma's zonder dat je ze apart installeert. Codex (ChatGPT) en Gemini CLI installeer je ermee, en veel uitbreidingen (koppelingen met je agenda, mail of andere apps, MCP-servers genoemd) draaien erop. Niet nodig voor de kennisbasis zelf, wel handig om nu te regelen.
- Je installeert ze een keer, daarna hoef je er niet meer naar om te kijken.

## Stap 1: Wat is er al

Bepaal het systeem en kijk wat er al staat. Doe dit zelf:

- Mac en Linux: `uname -s`, `python3 --version`, `node --version`, `npx --version`
- Windows (PowerShell): `python --version`, `py --version`, `node --version`, `npx --version`

Let op de Mac: staat er geen Python, dan kan `python3 --version` een venster openen met de vraag om "ontwikkelaarshulpmiddelen" te installeren. Waarschuw de gebruiker vooraf dat dat venster kan komen, en zeg dat "Installeer" kiezen ook goed is: daarmee komt Python erbij.

Meld de uitkomst in een tabel:

| Gereedschap | Staat erop? | Versie | Nodig |
|---|---|---|---|
| Python | ja/nee | ... | Python 3.8 of nieuwer |
| Node.js | ja/nee | ... | de LTS-versie (de stabiele) |
| npx | ja/nee | ... | komt mee met Node.js |

Staat alles er in een goede versie: zeg dat en stop.

Node.js en npx zijn optioneel voor de kennisbasis. Installeer ze alleen als de gebruiker ook een toepassing wil die ze nodig heeft. Een al werkende Codex- of ChatGPT-desktopapp hoeft niet opnieuw via npm geïnstalleerd te worden.

## Stap 2: Installeren

Vraag eerst of je mag beginnen. Installeer per onderdeel, controleer na elk onderdeel of het werkt.

### Mac

Kies de route op basis van wat er is:

- **Homebrew staat er al** (`brew --version` werkt): `brew install python` en `brew install node`. Geen klikken nodig.
- **Geen Homebrew** (de normale situatie voor niet-developers): gebruik de officiele installatieprogramma's. Zo gaat het:
  1. Zoek de nieuwste versie op. Voor Node.js: de nieuwste LTS uit `https://nodejs.org/dist/index.json` (het eerste item met een `lts`-naam). Voor Python: de nieuwste stabiele 3.x op `https://www.python.org/downloads/macos/`.
  2. Download het `.pkg`-bestand naar de map Downloads met `curl -L -o`.
  3. Open het met `open ~/Downloads/<bestand>.pkg`. Er verschijnt een installatievenster.
  4. Zeg de gebruiker: "Klik steeds op Ga door en dan Installeer. Je Mac vraagt je wachtwoord, dat is je gewone inlogwachtwoord. Zeg het als het venster 'De installatie is voltooid' toont."
  5. Na Python vanaf python.org: open de map `/Applications/Python 3.x/` en dubbelklik op `Install Certificates.command`, of draai dat bestand zelf. Anders lukken downloads vanuit Python later niet.

### Windows

Gebruik `winget` (zit standaard in Windows 10 en 11):

```
winget install --id Python.Python.3.12 -e
winget install --id OpenJS.NodeJS.LTS -e
```

Werkt `winget` niet: download de installers van python.org en nodejs.org. Zeg bij Python nadrukkelijk: **zet het vinkje "Add python.exe to PATH" aan** onderaan het eerste scherm.

### Linux

Gebruik het pakketbeheer van het systeem (`sudo apt install python3 nodejs npm` op Ubuntu of Debian). Leg uit dat `sudo` om het wachtwoord vraagt.

## Stap 3: Controleren

Nieuw geinstalleerd gereedschap is vaak pas zichtbaar in een nieuw terminalvenster. Werkt een commando direct na de installatie nog niet:

- Probeer het volledige pad (Mac: `/usr/local/bin/python3`, `/usr/local/bin/node`, of onder `/opt/homebrew/bin/`).
- Lukt dat, vraag de gebruiker dan het AI-programma een keer af te sluiten en opnieuw te openen.

Draai daarna opnieuw de commando's uit stap 1 en toon de tabel opnieuw. Klaar is: Python en Node.js tonen een versie, `npx --version` ook.

Test tot slot npx echt met `npx --yes cowsay "Het werkt"`. Verschijnt er een koe met de tekst, dan werkt alles.

## Stap 4: Terugmelding

```
✓ Python <versie>
✓ Node.js <versie>, npx <versie>
```

Ging iets mis, noem wat er misging in gewone taal en wat de volgende poging is. Probeer niet meer dan twee routes per onderdeel; lukt het dan nog niet, zeg dat eerlijk en raad aan iemand met wat technische kennis vijf minuten mee te laten kijken.

## Wat NIET

- Gereedschap installeren zonder het eerst te vragen.
- Homebrew installeren bij een niet-developer. Het installatieprogramma is een `.pkg` met klikken, dat is voor deze gebruiker begrijpelijker.
- Systeemmappen aanpassen of bestaande versies verwijderen.
- `sudo` gebruiken op een Mac. Het installatievenster vraagt zelf om het wachtwoord.
