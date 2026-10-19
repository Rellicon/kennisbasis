# Installatie

Kopieer alles onder de streep en plak het in je AI-programma: Claude Code, Codex, Gemini CLI of Mistral Vibe. Open het programma eerst in de map waarin dit bestand staat, of noem het pad naar die map in je bericht.

Deze handmatige route is voor lokale AI-programma's. Voor ChatGPT desktop installeer je de plugin via de route in README.md. Zonder lokale bestandstoegang werkt deze versie niet; een cloudcontainer is geen blijvende vault op je computer.

---

Je gaat de kennisbasis voor mij installeren en inrichten. Ik ben geen developer: leg elke stap in gewone taal uit, doe een stap per keer, en zeg wat ik moet zien als het goed ging.

Doe dit:

1. **Bepaal in welk programma je draait** en zoek je mappen op in deze tabel:

   | AI-programma | Map voor skills | Instructiebestand (lees je elke sessie) |
   |---|---|---|
   | Claude Code | `~/.claude/skills/` | `~/.claude/CLAUDE.md` |
   | Codex | `~/.agents/skills/` | `$CODEX_HOME/AGENTS.md` (standaard `~/.codex/AGENTS.md`) |
   | Gemini CLI | `~/.gemini/skills/` | `~/.gemini/GEMINI.md` |
   | Mistral Vibe | zoek op in je eigen documentatie | zoek op in je eigen documentatie |

   Zie je jezelf niet in de tabel, of weet je niet zeker welke map je gebruikt: zoek het op in je eigen documentatie of help. Lukt dat niet, zeg het mij dan eerlijk in plaats van te raden.

2. **Zoek de map van de kennisbasis.** Dat is de map waarin dit bestand `install.md` staat, met daarin de map `skills/`. Kun je hem niet vinden, vraag mij dan waar ik hem heb neergezet (bijvoorbeeld in Downloads).

3. **Controleer of er al skills met dezelfde naam zijn.** Controleer bij Codex ook de oudere map `~/.codex/skills/` en geïnstalleerde plugins. Installeer niet daarnaast een tweede exemplaar; kies één installatievorm. Kijk in je map voor skills of daar al een map `kennis-intro`, `kennis-tooling`, `catchup`, `save-context` of `vault` staat.
   - Staat er niets: ga door.
   - Staat er wel iets: vertel mij welke, en vraag of je ze mag vervangen. Zeg ik ja, maak dan eerst een kopie met `.oud` achter de naam.

4. **Installeer de vijf skills.** Kopieer de mappen uit `skills/` van de kennisbasis naar je map voor skills. Kopieer, verplaats niets. Maak de map aan als die nog niet bestaat. Laat daarna zien welke vijf mappen er nu staan.

5. **Leg vast waar alles staat.** Schrijf `~/.kennisbasis/instellingen.txt` (maak de map aan als die er niet is). Bestaat het bestand al, omdat ik de kennisbasis ook in een ander programma gebruik, voeg dan alleen je eigen regels toe:

   ```
   Programma: <jouw naam uit de tabel>
   Instructiebestand: <pad>
   Skills: <pad>
   ```

6. **Vertel me wat ik heb geinstalleerd**, in vijf regels:
   - `/kennis-intro`: de eerste kennismaking, richt mijn kennisbasis in.
   - `/catchup`: aan het begin van een gesprek, praat je bij.
   - `/save-context`: aan het eind van een gesprek, legt vast wat er veranderde.
   - `/vault`: hoe je in mijn kennisbasis leest en schrijft, en de wekelijkse controle.
   - `/kennis-tooling`: helpt Python en Node.js installeren.

   Zeg erbij hoe ik een skill in jouw programma aanroep. Werkt de schuine streep niet, dan kan ik altijd gewoon de naam zeggen, bijvoorbeeld "catchup".

7. **Controleer het gereedschap.** Volg de skill `kennis-tooling` (lees `SKILL.md` in die map): kijk of Python, Node.js en npx er staan en help mij installeren wat ontbreekt.

8. **Begin met de intro.** Nieuwe skills werken soms pas in een nieuw gesprek. Probeer `kennis-intro`; werkt dat niet, vraag mij dan een nieuw gesprek te starten en daar `/kennis-intro` te typen of "kennis-intro" te zeggen.

Pas niets aan buiten je map voor skills, `~/.kennisbasis/` en wat nodig is om het gereedschap te installeren. Het instructiebestand en de wekelijkse controle komen pas aan bod in de intro, en daar vraag je eerst.
