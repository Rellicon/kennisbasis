# Kennisbasis voor je AI-assistent

Een kleine uitbreiding die je AI-assistent een eigen notitieboek geeft. Daarmee kan de assistent bij een nieuw gesprek teruglezen wie je bent, wat je doet en waar je kennis staat. Het werkt met Claude, ChatGPT, Gemini en Mistral.

Gemaakt door Wim Wessels, op basis van hoe hij zelf dagelijks met AI werkt.

## Voor wie

Voor particulieren en eenpitters: iedereen die alleen werkt en de eigen kennis wil vastleggen. De vault staat op je eigen computer en is van jou en je AI-assistent.

Werk je in een team of een organisatie, dan is dit niet de juiste aanpak. Kennis die je collega's ook nodig hebben, hoort op een gedeelde plek waar iedereen bij kan, niet in het notitieboek van een persoonlijke assistent.

**Let op:** de kennis die je met deze kennisbasis opbouwt, is persoonlijk. Deel je die met collega's of anderen, dan is dat op eigen risico. Je gebruikt je AI-assistent vaak ook voor privézaken of voor werk dat niet voor hen bedoeld is, en dat staat allemaal in hetzelfde notitieboek. Wil je kennis en gegevens professioneel structureren, regel dat dan op het niveau van je organisatie.

## Waarom

Ingebouwd geheugen verschilt per AI-programma en bewaart niet vanzelf alle projectdetails. Met een eigen kennisbank houd je zelf controle over de context die je tussen gesprekken meeneemt.

Het eerste advies dat ik iedereen geef: **structureer je kennis, en zorg dat je AI-assistent bij elke sessie weet wie je bent, wat je doet en waar die informatie kan vinden.**

Deze kennisbasis regelt dat met drie afspraken:

1. **De assistent krijgt een eigen notitieboek, de vault.** Een gewone map met tekstbestanden. Daarin staat wie je bent, waar je aan werkt en wat er besloten is.
2. **Het geheugen van de assistent bevat alleen wegwijzers.** Een regel per project: waar het staat en wat de volgende stap is. De kennis zelf staat in de vault. Zo blijft het geheugen klein en de kennis vindbaar.
3. **Je bestanden blijven waar ze zijn.** Documenten, offertes en foto's staan in je eigen mappen. De vault verwijst ernaar.

Omdat de vault gewone tekst is, zit je niet vast aan een aanbieder. Stap je over van ChatGPT naar Claude of andersom, dan neem je je kennis mee. Gebruik je er meer naast elkaar, dan delen ze dezelfde vault.

## Wat heb je nodig

**Een AI-programma met toegang tot je lokale bestanden.** Deze versie is een lokale kennisbank.

| Omgeving | Ondersteuning in dit pakket |
|---|---|
| Codex lokaal (desktop of CLI) | Pluginmanifest en installatie als losse skills |
| ChatGPT desktop met lokale uitvoering | Pluginpakket met begeleide setup; bestandstoegang vereist |
| ChatGPT web/mobile of cloud zonder lokale uitvoering | Geen toegang tot deze lokale vault; deze versie is gemarkeerd als Desktop only |
| Claude Code | Claude-plugin en installatie als losse skills |
| Gemini CLI / Mistral Vibe | Handmatige installatie; gebruik de eigen documentatie |

De OpenAI-verpakking volgt de [pluginstructuur](https://developers.openai.com/plugins/build/plugins) en de [Desktop-only-instelling](https://developers.openai.com/plugins/deploy/desktop-only). Het pakket bevat geen MCP-server. Een toekomstige cloudversie vereist een aparte opslag- en toegangsoplossing.

Waar je het programma vindt:

| Je gebruikt | Programma | Waar te vinden | Abonnement |
|---|---|---|---|
| Claude | Claude Code | In de Claude-app voor Mac of Windows (tabblad Code), of los: claude.com/claude-code | Claude Pro of hoger |
| ChatGPT | Codex of de ChatGPT-desktopapp | De Codex-app of het terminalprogramma: developers.openai.com/codex | ChatGPT Plus of hoger |
| Gemini | Gemini CLI | geminicli.com | Gratis met een Google-account, ruimer met een abonnement |
| Mistral | Mistral Vibe | docs.mistral.ai/mistral-vibe | Mistral-account |

Getest met Claude Code. Codex, ChatGPT desktop, Gemini CLI en Mistral Vibe zijn nog niet getest.

**Daarnaast:**

- **Python** voor de wekelijkse controle, en **Node.js met npx** voor veel andere uitbreidingen. Heb je die niet, dan helpt `/kennis-tooling` je ze te installeren. Je hoeft daar niets van te weten.
- **Optioneel: Obsidian** (gratis, obsidian.md). Daarmee bekijk je de vault als een doorklikbaar notitieboek. Zonder Obsidian werkt alles ook.

## Wat zit erin

| Commando | Wanneer | Wat het doet |
|---|---|---|
| `/kennis-intro` | Een keer, bij de start | Legt uit hoe het werkt, vraagt waar de vault komt, wie je bent en hoe je je werk indeelt, en richt alles in |
| `/catchup` | Begin van een gesprek | Leest de vault en vertelt in een paar regels waar je was en wat de volgende stap is |
| `/save-context` | Eind van een gesprek | Schrijft op wat er veranderde, wat er besloten is en wat de volgende stap is |
| `/vault` | Vanzelf, als de assistent in de vault werkt | De regels voor het notitieboek: waar wat hoort, hoe notities eruitzien, opruimen, de wekelijkse controle |
| `/kennis-tooling` | Bij de installatie, of als iets mist | Helpt Python, Node.js en npx installeren |

In Codex gebruik je `$kennis-intro`, `$catchup` en `$save-context` (of de aangeboden plugin-skillnaam). In ChatGPT selecteer je de plugin en noem je de workflow. Je kunt ook gewoon de naam zeggen: "catchup", "save-context".

De eerste tien keer herinnert de assistent je af en toe aan `/catchup` en `/save-context`. Daarna is het een gewoonte en houdt het op.

### De wekelijkse controle

Een notitieboek raakt rommelig als niemand het bijhoudt. Tijdens de intro zet de assistent een controle klaar die elke week vanzelf draait, ook als je AI-programma niet openstaat. Die werkt de lijsten in je overzichtsnotities bij, repareert links en schrijft een kort rapport in `_Onderhoud/laatste-controle.md`. Wat het niet zelf mag oplossen, noemt `/catchup` bij je volgende gesprek.

Op de Mac gebeurt dat met de ingebouwde planner (launchd), op Windows met Taakplanner, op Linux met cron.

## Installeren

### ChatGPT desktop en Codex: als plugin

Het pakket bevat `plugin.json`, `.codex-plugin/plugin.json` en een lokale catalogus in `.agents/plugins/marketplace.json`.

1. Download `kennisbasis-openai-<versie>.zip` bij de nieuwste release (rechts op de GitHub-pagina, onder Releases) en pak hem uit op een vaste plek.
2. Heb je de Codex CLI, voer dan vanuit die uitgepakte map `codex plugin marketplace add .` uit. Je kunt ook deze bronmap als project openen; de catalogus hoort bij de projectmap.
3. Herstart de desktopapp, open de pluginbibliotheek en kies de bron **Rellicon**. Installeer **Kennisbasis**.
4. Start een nieuw lokaal gesprek en vraag: **"Gebruik kennis-intro om mijn kennisbasis in te richten."** Geef toegang tot de gekozen vault-map wanneer de app daarom vraagt.

Beschikbaarheid van lokale catalogi verschilt per clientversie. Gebruik voor Codex zo nodig de handmatige route hieronder. Voor upload in het OpenAI-pluginportaal is dezelfde ZIP bruikbaar als pakket; publicatie vereist aparte accounttoegang en beoordeling. Dit pakket is nog niet gepubliceerd of door OpenAI goedgekeurd.

In ChatGPT staan wegwijzers in `~/.kennisbasis/chatgpt.md`. De skills lezen dat expliciet; ChatGPT laadt Codex' `AGENTS.md` niet automatisch. Begin daarom met `catchup` en sluit af met `save-context`.

### Lokale AI-programma's: via install.md

1. Download deze repo (groene knop "Code", dan "Download ZIP") en pak hem uit, bijvoorbeeld in Documenten.
2. Open je AI-programma en kies die map als werkmap.
3. Open `install.md`, kopieer alles onder de streep en plak het in je AI-programma.
4. De assistent installeert de skills, helpt met Python en Node.js, en begint daarna met `/kennis-intro`.

### Alleen Claude Code: als plugin

Typ in Claude Code deze twee regels, een voor een:

```
/plugin marketplace add Rellicon/kennisbasis
/plugin install kennisbasis@rellicon
```

Start daarna een nieuw gesprek en typ `/kennisbasis:kennis-intro`. Als plugin krijgen de commando's `kennisbasis:` ervoor, zoals `/kennisbasis:catchup`.

## Hoe de vault eruitziet

```
Kennis/
  README.md               de ingang
  Over mij/Over mij.md    wie je bent en hoe je wilt dat je assistent werkt
  Projecten/<Project>/    per project de stand, besluiten en kennis
  Kennis/                 losse kennis: begrippen, personen, werkwijzen
  Sessies/                per opgeslagen gesprek een korte notitie
  _Prullenbak/            wat weg mag; de assistent gooit nooit iets echt weg
  _Onderhoud/             rapport van de wekelijkse controle
```

Daarnaast zet `/kennis-intro` een kort blok in het instructiebestand van je programma: het bestand dat het aan het begin van elk gesprek leest (`CLAUDE.md` bij Claude Code, `AGENTS.md` bij Codex, `GEMINI.md` bij Gemini CLI). Daarin staan het pad naar je vault, een paar regels en de wegwijzers naar je lopende projecten. Er wordt eerst een kopie van je bestaande bestand gemaakt. Bij ChatGPT gebruikt de plugin het expliciet gelezen `~/.kennisbasis/chatgpt.md`. Waar alles staat, onthoudt de kennisbasis in `~/.kennisbasis/instellingen.txt`.

## Privacy

De vault staat op je eigen computer. Tijdens een gesprek leest je AI-programma de notities die het nodig heeft en stuurt die, net als de rest van het gesprek, naar je aanbieder. Zet er daarom geen wachtwoorden, pincodes of medische gegevens in.

## Back-up

De intro vraagt welke back-up je wilt. Er zijn twee goede opties.

**Een cloudmap** (iCloud Drive, Google Drive, OneDrive of Dropbox). Handig als je op meer computers werkt. Twee dingen moeten dan goed staan:

- **Houd de map offline beschikbaar.** Cloudopslag zet bestanden vaak alleen online om ruimte te sparen. Je AI-assistent en de wekelijkse controle kunnen die dan niet lezen. Klik met rechts op de vault-map en kies:

  | Dienst | Optie |
  |---|---|
  | iCloud Drive | Houd gedownload |
  | Google Drive | Offline beschikbaar |
  | OneDrive | Altijd op dit apparaat bewaren |
  | Dropbox | Offline beschikbaar maken |

- **Houd de synchronisatie aan.** Het programma van je cloudopslag moet draaien, anders staat de back-up stil. Werk niet tegelijk op twee computers in dezelfde notitie: dan maakt de cloud een kopie met "conflict" in de naam.

**GitHub** (gratis, github.com). Een online kluis met geschiedenis: elke versie van elke notitie blijft bewaard, dus je kunt altijd terug. Zet de vault in een **privé**-repository, nooit openbaar. Met de app GitHub Desktop hoef je er niets technisch voor te kunnen. Kies je deze optie, dan zet de assistent na elke `/save-context` een back-up klaar en stuurt die naar je eigen GitHub.

Je kunt ook beide gebruiken: een cloudmap om op meer computers te werken, GitHub voor de geschiedenis.

## Verwijderen

Vraag je assistent eerst "zet de wekelijkse controle uit". Verwijder daarna de mappen `kennis-intro`, `kennis-tooling`, `catchup`, `save-context` en `vault` uit de map voor skills van je programma, de map `~/.kennisbasis`, en haal het blok tussen `<!-- kennisbasis:start -->` en `<!-- kennisbasis:end -->` uit het instructiebestand. Je vault blijft gewoon staan.
