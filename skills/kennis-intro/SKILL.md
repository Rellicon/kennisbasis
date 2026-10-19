---
name: kennis-intro
description: "Richt de persoonlijke lokale kennisbasis in of koppel een bestaande vault aan dit AI-programma. Legt uit waarom de assistent een eigen notitieboek (vault) krijgt, vraagt waar die komt, wie de gebruiker is en hoe die het werk indeelt, zet wegwijzers in het instructiebestand en stelt de wekelijkse controle in. Vereist lokale bestandstoegang. Triggers op /kennis-intro, kennis-intro, help me beginnen, richt mijn kennisbasis in, eerste setup, ontbrekende instellingen, en vanuit catchup, save-context of vault zolang de intro nog niet gedaan is."
---

# /kennis-intro

## Uitvoeringsomgeving

Deze workflow gebruikt een blijvende vault op de computer van de gebruiker. Controleer dat de beschikbare tools daadwerkelijk die lokale bestanden kunnen lezen en (voor wijzigingen) schrijven. Een tijdelijke cloudcontainer is niet de computer van de gebruiker. Zonder lokale toegang: leg uit dat deze versie een programma op de eigen computer nodig heeft (Claude Code, Codex lokaal, ChatGPT desktop met lokale uitvoering, Gemini CLI of Mistral Vibe); maak geen vervangende vault in een tijdelijke omgeving.

Gebruik de skillnaam uit de beschikbare skills: in Claude Code `/catchup` (als plugin `/kennisbasis:catchup`), in Codex bijvoorbeeld `$catchup`, in ChatGPT via de geïnstalleerde plugin of de naam in gewone taal. `/...` hieronder is de Claude-notatie. Lees benodigde andere skills uit dit pakket; verzin geen toolnamen of installatiepaden. Een toegangsfout betekent niet dat de kennisbasis ontbreekt: meld de ontbrekende toegang en overschrijf niets.


De gebruiker is geen developer. Praat in gewone taal, stel **een vraag per bericht**, en zeg bij elke technische stap wat je doet en waarom. Antwoordt de gebruiker in een andere taal dan Nederlands, ga dan over op die taal.

## Begrippen

- **Het AI-programma**: het programma waarin je nu draait. Claude Code (Claude), Codex, ChatGPT desktop met lokale uitvoering, Gemini CLI (Gemini) of Mistral Vibe (Mistral). Noem het in gesprekken bij die naam.
- **Het instructiebestand**: de plek voor het kennisbasis-blok. Claude Code, Codex en Gemini CLI lezen hun globale bestand (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) aan het begin van elk gesprek, in welke map de gebruiker ook werkt. ChatGPT krijgt een apart bestand dat de skills expliciet lezen. Neem niet aan dat ChatGPT `AGENTS.md` automatisch laadt.

| AI-programma | Instructiebestand | Map voor skills |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | `~/.claude/skills/` |
| Codex | `$CODEX_HOME/AGENTS.md` (standaard `~/.codex/AGENTS.md`) | `~/.agents/skills/` voor losse skills; bij plugininstallatie de pakketmap |
| ChatGPT desktop met lokale uitvoering | `~/.kennisbasis/chatgpt.md` (expliciet lezen bij elke kennisbasis-workflow) | via de geïnstalleerde plugin |
| Gemini CLI | `~/.gemini/GEMINI.md` | `~/.gemini/skills/` |
| Mistral Vibe | zoek op in de documentatie van Vibe | zoek op in de documentatie van Vibe |

- **De instellingen**: `~/.kennisbasis/instellingen.txt`. Daarin staat welk programma, welk instructiebestand en welke vault. `install.md` schrijft de eerste drie regels, deze intro de regel `Vault:`.

Voor ChatGPT kies je `~/.kennisbasis/chatgpt.md` als instructiebestand; voor Codex respecteer je een ingestelde `CODEX_HOME`. Registreer de eigen combinatie `Programma:`, `Instructiebestand:` en `Skills:` ook als instellingen al bestaan: voeg die drie regels als groep toe onder de bestaande, zodat bij elk programma zijn eigen instructiebestand staat. Bewaar de bestaande regels en het vault-pad. Gebruik voor `Skills:` de werkelijke pakketmap.

## Stap 0: Is de intro al geweest?

Lees `~/.kennisbasis/instellingen.txt`. Ontbreekt het, bepaal dan zelf welk programma je bent, zoek het instructiebestand op in de tabel, en schrijf het bestand aan met:

```
Programma: <naam>
Instructiebestand: <pad>
Skills: <pad>
```

Lees daarna het instructiebestand en zoek het blok tussen `<!-- kennisbasis:start -->` en `<!-- kennisbasis:end -->`.

- Staat er `Intro: gedaan`: zeg dat de kennisbasis al is ingericht, noem het vault-pad en stop. Wil de gebruiker opnieuw beginnen, vraag dan of de bestaande vault blijft (ja is de standaard).
- Staat er `Intro: bezig`: de vorige keer is halverwege gestopt. Ga verder bij de eerste stap die nog niet af is.
- Geen blok, maar wel een `Vault:` in de instellingen: de gebruiker heeft de kennisbasis al in een ander AI-programma. Vraag of dit programma dezelfde vault mag gebruiken (ja is de standaard). Bij ja: sla stap 2 tot en met 5 over, neem het profiel over uit `Over mij/Over mij.md` en ga naar stap 6.
- Anders: begin bij stap 1.

## Stap 1: Welkom en uitleg

Leg in hooguit zeven korte zinnen uit:

- Ingebouwd geheugen verschilt per programma en bewaart niet vanzelf alle projectdetails. Een eigen kennisbank maakt de context controleerbaar en overdraagbaar.
- Daarom krijg ik een eigen notitieboek: de **vault**. Een map met gewone tekstbestanden waarin staat wie je bent, waar je aan werkt en wat er besloten is.
- Ik lees dat notitieboek aan het begin van een gesprek en schrijf erin aan het eind. Zo hoef je jezelf niet steeds opnieuw uit te leggen.
- Het notitieboek is van gewone tekst, dus het werkt met elk AI-model: Claude, ChatGPT, Gemini of Mistral. Stap je later over, dan neem je je kennis gewoon mee.
- Twee gewoontes maken het af: `/catchup` aan het begin van een sessie, `/save-context` aan het eind. Werkt de schuine streep niet in jouw programma, dan zeg je gewoon "catchup" of "save-context".
- Dit notitieboek is voor je eigen kennis, als particulier of eenpitter. Werk je in een team, dan hoort kennis die je collega's nodig hebben op een gedeelde plek waar zij ook bij kunnen, niet in mijn notitieboek. **Let op:** wat we hier opbouwen is persoonlijk. Delen met collega's of anderen is op eigen risico, want je gebruikt mij vaak ook voor privézaken. Professionele kennis regel je beter op het niveau van je organisatie.
- We gaan nu samen drie dingen regelen: waar het notitieboek komt, wie je bent, en hoe je je werk indeelt.

Vraag daarna of de gebruiker klaar is om te beginnen.

## Stap 2: De hoofdmap van de vault

Leg eerst uit, in eigen woorden:

> Dit wordt mijn notitieboek en mijn externe geheugen, niet het jouwe. Daarom wil ik een eigen hoofdmap, los van de mappen en projectmappen die je al hebt. Zo raak ik jouw bestanden niet aan en weet ik precies wat van mij is. Je mag er altijd in kijken.

Stel dan een map voor en vraag of die goed is:

- Standaard op de Mac: `~/Kennis` (een map Kennis direct in je thuismap, naast Documenten). Daar kan de wekelijkse controle zonder extra toestemming bij. Op Windows: `%USERPROFILE%\Kennis`.
- Werkt de gebruiker op meer computers: een map in iCloud Drive, Google Drive, OneDrive of Dropbox. Zeg dan eerlijk dat de Mac voor de wekelijkse controle een keer om toestemming vraagt, en dat je daar samen doorheen loopt.

Controleer daarna zelf (niet vragen) of de gekozen map al bestaat en wat erin staat:

- Bestaat hij niet: maak hem straks aan in stap 5.
- Bestaat hij en is hij leeg: prima.
- Staan er al bestanden in: noem wat je ziet en vraag of je daar echt in mag werken of liever een submap `Kennis` maakt. Overschrijf nooit iets.

### Back-up

Vraag daarna welke back-up de gebruiker wil, met deze opties in gewone taal:

1. **Een cloudmap** (iCloud Drive, Google Drive, OneDrive, Dropbox). Staat de vault in zo'n map, loop dan samen twee dingen na:
   - **Offline beschikbaar.** Cloudopslag zet bestanden vaak alleen online; dan kun jij en de wekelijkse controle ze niet lezen. Laat de gebruiker met rechts op de vault-map klikken en kiezen: iCloud Drive "Houd gedownload", Google Drive "Offline beschikbaar", OneDrive "Altijd op dit apparaat bewaren", Dropbox "Offline beschikbaar maken". Controleer daarna zelf of je een bestand in de map kunt lezen.
   - **Synchronisatie aan.** Het programma van de cloudopslag moet draaien. Zeg erbij: niet tegelijk op twee computers in dezelfde notitie werken, anders ontstaat een kopie met "conflict" in de naam.
2. **GitHub**: een online kluis met de geschiedenis van elke notitie. Altijd een **privé**-repository, nooit openbaar, want de vault gaat over de gebruiker en diens werk. Begeleid zo:
   - Een gratis account op github.com (de gebruiker doet dit zelf in de browser).
   - De app GitHub Desktop installeren en inloggen.
   - In GitHub Desktop: "Add an Existing Repository" (of "Create a New Repository") met de vault-map, daarna "Publish repository" met het vinkje **Keep this code private** aan. Controleer of het vinkje echt aan staat voor de gebruiker op Publish klikt.
   - Zet `_Prullenbak/` in een bestand `.gitignore` in de vault, zodat weggegooide notities niet online blijven staan.
   - Vraag of je na elke `/save-context` zelf een back-up mag maken en naar GitHub mag sturen. Bij ja: `Back-up: GitHub (na elke save)` in het blok. Bij nee: `Back-up: GitHub (zelf via GitHub Desktop)`.
3. **Beide**: een cloudmap om op meer computers te werken, GitHub voor de geschiedenis.
4. **Nog niet**: prima, zeg dat het later kan met "regel een back-up".

Schrijf de keuze in het blok bij `Back-up:` (stap 6).

### Obsidian

Leg ook kort uit dat de gebruiker de vault kan bekijken met **Obsidian** (gratis, obsidian.md): dat maakt van de map een doorklikbaar notitieboek. Het is optioneel, alles werkt ook zonder.

## Stap 3: Wie ben je en wat doe je

Stel deze vragen een voor een. Vat elk antwoord in een zin samen en ga door; vraag niet door op details die later vanzelf komen.

1. Hoe heet je, en wat doe je voor werk? (rol, vak, zelfstandig of in loondienst)
2. Voor wie of waaraan werk je? (klanten, afdelingen, onderwerpen, een studie, een hobby)
3. Hoe wil je dat ik met je praat? (kort of uitgebreid, formeel of los, taal, dingen die je irriteren)

## Stap 4: Hoe deel je je projecten en bestanden in

Vraag eerst:

> Hoe houd je je projecten of onderwerpen nu bij? Heb je een vaste map waar je bestanden staan, en hoe is die ingedeeld?

Kijk mee als de gebruiker een map noemt: toon de bovenste twee niveaus (alleen mapnamen, geen bestanden openen) en vat de indeling samen.

**Heeft de gebruiker al een indeling:** neem die over. De vault krijgt per project of onderwerp een notitie die naar de bijbehorende map verwijst. Je verplaatst of hernoemt niets in de mappen van de gebruiker.

**Heeft de gebruiker nog geen indeling:** stel vragen tot je een voorstel kunt doen:

- Werk je vooral voor klanten, aan eigen projecten, of rond onderwerpen?
- Hoeveel lopen er tegelijk, ongeveer?
- Wat bewaar je per project: offertes, documenten, foto's, mails?

Doe dan een voorstel voor een vaste projectmap, bijvoorbeeld:

```
~/Documents/Werk/
  Klanten/<Klant>/<Project>/
  Eigen/<Onderwerp>/
  Administratie/
```

of, voor iemand die rond onderwerpen werkt:

```
~/Documents/Werk/
  <Onderwerp>/
  Archief/
```

Leg uit dat deze map voor de bestanden is (zoals een Drive) en de vault voor de kennis erover. Maak de mappen pas aan na een "ja". Verplaats nooit bestaande bestanden zonder dat de gebruiker per stap akkoord geeft; dat is een aparte klus voor een volgende sessie.

Vraag tot slot welke twee of drie projecten of onderwerpen nu het meest spelen. Die zet je als eerste in de vault.

## Stap 5: Richt de vault in

Doe dit zelf, zeg kort wat je doet:

1. Maak de hoofdmap met daarin `Over mij/`, `Projecten/`, `Kennis/`, `Sessies/`, `_Prullenbak/` en `_Onderhoud/`.
2. Vul de sjablonen in uit de map `templates/vault/` naast deze skill:
   - `README.md` naar de hoofdmap van de vault.
   - `Over mij.md` naar `Over mij/Over mij.md`, ingevuld met de antwoorden uit stap 3 en 4.
3. Maak `Projecten/Projecten.md`, `Kennis/Kennis.md` en `Sessies/Sessies.md`: elk een overzichtsnotitie met frontmatter (zie de skill `vault`), een zin over wat erin hoort en een link terug naar `[[README|vault]]`.
4. Maak per genoemd project `Projecten/<Project>/<Project>.md` uit het sjabloon `project-sjabloon.md` in de map van de skill `vault` (de map `../vault/` naast deze skill).
5. Zet `Vault: <pad>` en `Bestanden: <pad>` in `~/.kennisbasis/instellingen.txt`.
6. Draai `python3 <map van de skill vault>/scripts/onderhoud.py hubs` en daarna `controle`. Dat zet de lijsten in de overzichtsnotities klaar. Ontbreekt Python, start dan eerst `/kennis-tooling` en kom daarna hier terug.

Gebruik voor `{{DATUM}}` de datum van vandaag als `YYYY-MM-DD`.

## Stap 6: Het blok in het instructiebestand

Leg uit: het instructiebestand bewaart de wegwijzers. Bij Claude Code, Codex en Gemini CLI wordt het bij de start van elk gesprek ingelezen, in welke map je ook werkt; bij ChatGPT lezen de kennisbasis-skills het expliciet zodra de gebruiker ze aanroept. Beloof daar geen automatische herinneringen buiten de workflow. Daar komt een kort blok met waar de vault staat, je regels en de lopende projecten. Alleen wegwijzers, de kennis zelf staat in de vault.

1. Bestaat het instructiebestand al: maak eerst een kopie met `.voor-kennisbasis` achter de naam en zeg dat. Bestaat de map niet, maak hem aan.
2. Vul `templates/instructie-blok.md` in:
   - `{{VAULT_PAD}}` en `{{BESTANDEN_PAD}}` met de gekozen paden (met `~` als het in de thuismap staat).
   - `{{INTRO_STAND}}` met `bezig`.
   - `{{BACKUP}}` met de keuze uit stap 2, bijvoorbeeld `cloudmap (iCloud Drive)`, `GitHub (na elke save)` of `nog niet`.
   - `{{KORT_PROFIEL}}` met twee of drie zinnen: naam, werk, hoe de gebruiker wil dat je praat.
   - Onder "Lopend werk" een regel per project: `- <Project> (actief, YYYY-MM-DD) -> volgende: <stap>`.
3. Staat er al een blok tussen `<!-- kennisbasis:start -->` en `<!-- kennisbasis:end -->`, vervang dan alleen dat blok. Anders: voeg het blok onderaan toe. Raak de rest van het bestand nooit aan.

## Stap 6b: De wekelijkse controle

Leg uit: "Een notitieboek raakt rommelig als niemand het bijhoudt. Ik zet een controle klaar die elke week vanzelf je vault nakijkt: lijsten bijwerken, links repareren en een kort rapport schrijven van wat ik niet zelf mag oplossen. Je hoeft er niets voor te doen, en het werkt ook als ik niet openstaat."

Vraag of dat goed is. Bij ja: volg de sectie "Wekelijkse controle instellen" van de skill `vault`, inclusief de test en de regel `Weekcontrole:` in het blok. Bij nee: laat `Weekcontrole: uit` staan en zeg dat het later alsnog kan met "zet de wekelijkse controle aan". Draait de kennisbasis al in een ander programma met de controle aan, sla deze stap dan over: de controle hoort bij de vault, niet bij het programma.

## Stap 7: De gewoonte en de eerste save

Zeg in gewone taal:

- Ik heb mezelf een herinnering gegeven: zolang dit nog geen gewoonte is, wijs ik je af en toe op `/catchup` en `/save-context`. Na tien opgeslagen sessies stop ik daarmee.
- Bij je volgende gesprek begin je met `/catchup`. Dan lees ik de vault en weet ik waar we waren.
- Na een gesprek waarin iets is besloten of veranderd, typ je `/save-context`. Dan schrijf ik op wat er veranderde en wat de volgende stap is.

Vraag de gebruiker dan om nu zelf `/save-context` te typen (of "save-context" te zeggen), zodat de gebruiker ziet hoe het werkt. Doe het niet zelf.

`/save-context` herkent dat dit de eerste keer is: het schrijft de sessie "Kennisbasis ingericht" weg in de vault en zet `Intro: bezig` op `Intro: gedaan op YYYY-MM-DD`. Daarna toon je de gebruiker waar het opgeslagen is.

## Stap 8: Wat er daarna kan

Noem als afsluiting een of twee vervolgstappen, als keuze, niet als opdracht:

- Bestaande notities, documenten of een oude map met kennis stap voor stap overzetten naar de vault.
- Een project uitwerken: wie erbij betrokken is, afspraken, wat er speelt.

## Wat NIET

- Meer dan een vraag per bericht.
- Bestanden of mappen van de gebruiker verplaatsen, hernoemen of verwijderen.
- Het instructiebestand overschrijven; alleen het eigen blok toevoegen of vervangen, na een kopie.
- Kennis over de gebruiker in het ingebouwde geheugen van het programma zetten; die hoort in `Over mij/Over mij.md`.
- Vakjargon zonder uitleg (frontmatter, markdown, repo, terminal). Moet een woord, leg het in een halve zin uit.
- `Intro: gedaan` zetten voordat de gebruiker zelf `/save-context` heeft gedraaid.
- Raden welk instructiebestand Mistral Vibe of een ander programma leest. Weet je het niet zeker, zoek het op in de eigen documentatie of help van het programma, en zeg het eerlijk als het niet lukt.
