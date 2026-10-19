---
name: catchup
description: "Lees de lokale kennisbasis om lopend werk te hervatten aan het begin van een sessie. Leest de wegwijzers in het instructiebestand van dit AI-programma (CLAUDE.md, AGENTS.md, GEMINI.md of chatgpt.md), de overzichtsnotitie van het project en de laatste sessienotitie, en geeft de stand met één volgende stap. Ondersteunt een projectnaam, alles en --kort. Start kennis-intro als de kennisbasis nog niet is ingericht. Triggers op /catchup, catchup, waar waren we, wat was ik aan het doen, praat me bij, en aan het begin van een gesprek over lopend werk."
---

# /catchup

## Uitvoeringsomgeving

Kies het instructiebestand van dit programma: Claude Code `~/.claude/CLAUDE.md`, Codex `$CODEX_HOME/AGENTS.md` (standaard `~/.codex/AGENTS.md`), ChatGPT desktop `~/.kennisbasis/chatgpt.md`, Gemini CLI `~/.gemini/GEMINI.md`. Staan er in `~/.kennisbasis/instellingen.txt` meer regels `Instructiebestand:`, gebruik dan die van dit programma en nooit zomaar de eerste. Lees dat bestand expliciet. Ontbreekt de registratie voor dit programma, gebruik `kennis-intro` om de bestaande vault te koppelen, zonder die opnieuw aan te maken.

Deze workflow gebruikt een blijvende vault op de computer van de gebruiker. Controleer dat de beschikbare tools daadwerkelijk die lokale bestanden kunnen lezen en (voor wijzigingen) schrijven. Een tijdelijke cloudcontainer is niet de computer van de gebruiker. Zonder lokale toegang: leg uit dat deze versie een programma op de eigen computer nodig heeft (Claude Code, Codex lokaal, ChatGPT desktop met lokale uitvoering, Gemini CLI of Mistral Vibe); maak geen vervangende vault in een tijdelijke omgeving.

Gebruik de skillnaam uit de beschikbare skills: in Claude Code `/catchup` (als plugin `/kennisbasis:catchup`), in Codex bijvoorbeeld `$catchup`, in ChatGPT via de geïnstalleerde plugin of de naam in gewone taal. `/...` hieronder is de Claude-notatie. Lees benodigde andere skills uit dit pakket; verzin geen toolnamen of installatiepaden. Een toegangsfout betekent niet dat de kennisbasis ontbreekt: meld de ontbrekende toegang en overschrijf niets.


Snel bij zijn aan het begin van een sessie. Uitkomst: de gebruiker weet in een bericht waar die staat en wat de volgende stap is.

## Input

- Geen argument: het meest recent bijgewerkte project uit "Lopend werk".
- Een projectnaam: dat project.
- `--kort`: alleen de wegwijzer-regel en de volgende stap, hooguit 40 woorden.
- `alles`: een regel per lopend project, zonder bestanden te openen.

## Stap 1: Is de kennisbasis ingericht?

Lees `~/.kennisbasis/instellingen.txt` voor `Vault:` en de regel `Instructiebestand:` van dit programma (gebruikt iemand de kennisbasis in meer AI-programma's, dan staan er meer; kies die van jezelf, zie Uitvoeringsomgeving). Lees dan dat instructiebestand en zoek het blok tussen `<!-- kennisbasis:start -->` en `<!-- kennisbasis:end -->`.

- Geen instellingen of geen blok: zeg in een zin dat de kennisbasis nog niet is ingericht en start de skill `kennis-intro`. Stop hier.
- `Intro: bezig`: zeg dat de inrichting nog niet is afgerond en ga verder met `kennis-intro`.
- Anders: haal de regels onder "Lopend werk" eruit.

## Stap 2: Kies het project

- Argument gegeven: zoek het in "Lopend werk" en in `<vault>/Projecten/`. Niet gevonden: noem de projecten die er wel zijn en vraag welke.
- Geen argument: neem de regel met de nieuwste datum. Noem de andere hooguit kort in de openingszin.
- `alles`: ga direct naar stap 4 met alleen de regels uit "Lopend werk".

## Stap 3: Lees de context (hooguit drie bestanden)

1. `<vault>/Projecten/<Project>/<Project>.md`, vooral de secties "Stand" en "Besluiten".
2. De nieuwste sessienotitie van dat project (bovenste link onder "Sessies" in de projectnotitie, of de nieuwste in `<vault>/Sessies/` met dit project in de frontmatter).
3. Alleen als de stand ernaar verwijst: een notitie uit `Kennis/` die nodig is om de volgende stap te snappen.

Lees `Over mij/Over mij.md` niet standaard; het korte profiel in het blok is genoeg. Lees het alleen als de vraag over de gebruiker zelf gaat.

Kloppen de wegwijzer in het blok en de stand in de projectnotitie niet met elkaar, dan wint de projectnotitie: daar kan ook een ander AI-programma in geschreven hebben. Noem het verschil en werk de wegwijzer bij.

## Stap 4: Meld de stand

Vorm:

```
**<Project>**: <een tot drie zinnen in gewone taal: waar staan we, wat is er laatst gebeurd, wat speelt er nu>

Open vragen: <alleen als die er zijn>

Volgende: <een concrete actie, een werkwoord>
```

Bij `alles`: een tabel `| Project | Status | Volgende stap |`, daarna een `Volgende:` met het project dat nu de meeste aandacht vraagt.

## Stap 4b: Weekcontrole

Staat `Weekcontrole: aan` in het blok, kijk dan naar `<vault>/_Onderhoud/laatste-controle.md`:

- Ouder dan acht dagen of afwezig: de planner draaide niet. Draai zelf `python3 <map van de skill vault>/scripts/onderhoud.py week` en zeg in een regel dat de weekcontrole niet vanzelf liep, met een verwijzing naar de skill `vault` om het na te kijken.
- Rapport met bevindingen (hooguit een keer per gesprek noemen): een regel onder de stand, bijvoorbeeld "De weekcontrole vond 3 punten in je vault. Zeg 'controleer de vault' om ze samen op te lossen."
- Schoon: niets melden.

## Stap 5: Gewoonte-reminder

Staat `Gewoonte: in opbouw` in het blok en riep de gebruiker deze skill zelf aan, zeg dan een keer kort iets als "Goed bezig. Sluit straks af met `/save-context`, dan weet ik de volgende keer weer waar we zijn." Niet vaker dan een keer per gesprek.

## Wat NIET

- Meer dan drie bestanden lezen (het rapport van de weekcontrole telt niet mee).
- Samenvattingen van samenvattingen ("In de vorige sessie hebben we besproken...").
- Meer dan een volgende stap voorstellen.
- Afsluiten met een vraag als "Wil je ook X zien?". De gebruiker vraagt zelf als er meer nodig is.
- Iets in de vault schrijven, behalve een wegwijzer die niet meer klopte.
