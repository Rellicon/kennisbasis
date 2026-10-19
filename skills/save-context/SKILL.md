---
name: save-context
description: "Bewaar veranderingen, besluiten en de volgende stap van dit gesprek in de lokale kennisbasis. Schrijft een korte sessienotitie, werkt stand en besluiten van het project bij en zet de wegwijzer in het instructiebestand van elk gekoppeld AI-programma op de nieuwste volgende stap. Slaat alleen veranderingen op, geen samenvattingen. Ondersteunt een projectnaam en --kort. Triggers op /save-context, save-context, sla op, leg vast, bewaar dit gesprek, einde van een sessie."
---

# /save-context

## Uitvoeringsomgeving

Kies het instructiebestand van dit programma: Claude Code `~/.claude/CLAUDE.md`, Codex `$CODEX_HOME/AGENTS.md` (standaard `~/.codex/AGENTS.md`), ChatGPT desktop `~/.kennisbasis/chatgpt.md`, Gemini CLI `~/.gemini/GEMINI.md`. Staan er in `~/.kennisbasis/instellingen.txt` meer regels `Instructiebestand:`, gebruik dan die van dit programma en nooit zomaar de eerste. Lees dat bestand expliciet. Ontbreekt de registratie voor dit programma, gebruik `kennis-intro` om de bestaande vault te koppelen, zonder die opnieuw aan te maken.

Deze workflow gebruikt een blijvende vault op de computer van de gebruiker. Controleer dat de beschikbare tools daadwerkelijk die lokale bestanden kunnen lezen en (voor wijzigingen) schrijven. Een tijdelijke cloudcontainer is niet de computer van de gebruiker. Zonder lokale toegang: leg uit dat deze versie een programma op de eigen computer nodig heeft (Claude Code, Codex lokaal, ChatGPT desktop met lokale uitvoering, Gemini CLI of Mistral Vibe); maak geen vervangende vault in een tijdelijke omgeving.

Gebruik de skillnaam uit de beschikbare skills: in Claude Code `/catchup` (als plugin `/kennisbasis:catchup`), in Codex bijvoorbeeld `$catchup`, in ChatGPT via de geïnstalleerde plugin of de naam in gewone taal. `/...` hieronder is de Claude-notatie. Lees benodigde andere skills uit dit pakket; verzin geen toolnamen of installatiepaden. Een toegangsfout betekent niet dat de kennisbasis ontbreekt: meld de ontbrekende toegang en overschrijf niets.


Schrijf alleen op wat verloren gaat als je het niet opschrijft. De kennis gaat naar de vault, in het instructiebestand komt alleen een wegwijzer.

## Input

- Geen argument: het project waar dit gesprek over ging.
- Een projectnaam: dat project.
- `--kort`: alleen de wegwijzer bijwerken, geen sessienotitie.

## Stap 1: Lees instellingen en blok

Lees `~/.kennisbasis/instellingen.txt` voor `Vault:` en elke regel `Instructiebestand:` (gebruikt iemand de kennisbasis in meer AI-programma's, dan staan er meer). Lees in het instructiebestand van dit programma het blok tussen `<!-- kennisbasis:start -->` en `<!-- kennisbasis:end -->`.

- Geen instellingen of geen blok: de kennisbasis is nog niet ingericht. Zeg dat en start `kennis-intro`. Stop hier.
- `Intro: bezig`: dit is de eerste save, na de intro. Ga door met stap 2, met als project "Kennisbasis" en als onderwerp "Kennisbasis ingericht". Wat er veranderde: de vault is aangemaakt, het profiel staat erin, de projecten zijn aangemaakt. Maak daarvoor ook `Projecten/Kennisbasis/Kennisbasis.md` aan als die er niet is. Volgende stap: de eerstvolgende keer starten met `/catchup`.

## Stap 2: Bepaal project en delta

- Gaat het gesprek over meer dan een project: vraag kort welke, of sla elk apart op.
- Gaat het gesprek over iets nieuws dat nog geen project heeft: stel een naam voor en maak het project aan volgens de skill `vault` (na een "ja").

Verzamel wat er sinds het begin van het gesprek **veranderd** is:

- Wat is er gedaan of gemaakt (met het pad als het een bestand is)?
- Wat is er besloten?
- Welke vragen staan nog open, en bij wie?
- Wat is de volgende stap?
- Wat heeft de gebruiker je geleerd over hoe die wil werken? (gaat naar `Over mij/Over mij.md`, sectie "Geleerde lessen")

## Stap 3: Sessienotitie (niet bij --kort)

Maak `<vault>/Sessies/YYYY-MM-DD <onderwerp>.md` uit `sessie-sjabloon.md` naast deze skill. Bestaat die naam al, voeg dan `(2)` toe. Geen `/ \ : * ? " < > | #` in de bestandsnaam.

Kort houden: bullets, geen verslag van het gesprek.

## Stap 4: Projectnotitie bijwerken

In `<vault>/Projecten/<Project>/<Project>.md`:

- **Stand**: status, volgende stap, open vragen. Vervang de oude waarden, laat geen geschiedenis staan.
- **Besluiten**: voeg een regel toe per echt besluit (iets wat later niet per ongeluk teruggedraaid mag worden).
- **Sessies**: een link naar de nieuwe sessienotitie bovenaan.
- `updated:` in de frontmatter op vandaag.
- Is het project klaar: status `afgerond` en de regel uit "Lopend werk" halen (stap 5).

Nieuwe kennis die los van dit project bruikbaar is (een begrip, een persoon, hoe iets werkt) gaat naar een eigen notitie in `Kennis/`, volgens de skill `vault`.

## Stap 5: Wegwijzer in het instructiebestand

Werk onder "Lopend werk" alleen de regel van dit project bij, of voeg hem toe:

```
- <Project> (<status>, YYYY-MM-DD) -> volgende: <een zin concrete actie>
```

Regels:

- Een regel per project, hooguit zo'n 150 tekens. Past het niet op een regel, dan hoort het in de vault.
- Afgeronde projecten: regel weg.
- Meer dan tien regels: haal de oudste weg (de projectnotitie in de vault blijft) en zeg dat.
- Raak niets buiten het kennisbasis-blok aan.
- Staan er meer instructiebestanden in de instellingen, werk het blok dan in elk ervan bij, zodat elk AI-programma dezelfde wegwijzers ziet.

Heeft het programma daarnaast een eigen ingebouwd geheugen (memory): daar mag hooguit dezelfde wegwijzer-regel in, nooit de inhoud.

## Stap 6: Intro en gewoonte

- Stond er `Intro: bezig`: maak er `Intro: gedaan op YYYY-MM-DD` van.
- Staat er `Gewoonte: in opbouw (opgeslagen sessies: N van 10)`: verhoog N met een. Bij 10 wordt het `Gewoonte: vast` en zeg je: "Dit is je tiende save. Ik herinner je er vanaf nu niet meer aan."

## Stap 6b: Back-up naar GitHub

Alleen als in het blok `Back-up: GitHub (na elke save)` staat:

1. Ga naar de vault-map en controleer dat het een git-repository is met een remote (`git remote -v`). Zo niet: meld het in de terugmelding en sla de rest over.
2. Controleer een keer per gesprek dat de repository op GitHub privé is (`gh repo view --json visibility` als `gh` er is). Is hij openbaar: niet pushen, meld het met een ⚠.
3. `git add -A`, `git commit -m "Sessie YYYY-MM-DD: <onderwerp>"`, `git push`.
4. Mislukt de push (geen internet, inloggen verlopen): de commit blijft lokaal staan en gaat de volgende keer mee. Zeg dat in een regel, zonder het technisch uit te leggen.

## Stap 7: Terugmelding

Alleen dit, geen samenvatting eronder:

```
✓ Sessie opgeslagen: <pad naar sessienotitie>
✓ <Project>: <status>, volgende stap bijgewerkt
✓ Wegwijzer bijgewerkt
[alleen bij GitHub-back-up] ✓ Back-up op GitHub
[alleen bij de eerste save] ✓ Intro afgerond. Begin je volgende gesprek met /catchup.
[alleen als er iets openstaat] ⚠ <open vraag of beslissing voor de gebruiker>
```

Is dit de eerste save (na de intro), voeg dan een zin toe: "Open de map <vault> maar eens: daar staat nu je notitieboek." Gebruikt de gebruiker Obsidian, noem dat de vault daar als map geopend kan worden.

## Wat NIET

- Het hele gesprek samenvatten.
- Feiten dubbel opslaan: wat in de projectnotitie staat hoeft niet in de sessienotitie, en andersom.
- Kennis in het instructiebestand of in het ingebouwde geheugen zetten.
- De projectnotitie helemaal herschrijven; alleen de secties hierboven bijwerken.
- Een "volgende keer doen we X, Y en Z"-lijst. Een volgende stap is genoeg.
