#!/usr/bin/env python3
"""Vault-onderhoud voor de kennisbasis. Alleen de standaardbibliotheek van Python, geen taalmodel nodig.

Gebruik:
  python3 onderhoud.py controle  [--vault PAD]   # rapport, exit 1 bij bevindingen
  python3 onderhoud.py hubs      [--vault PAD]   # lijsten in de overzichtsnotities bijwerken
  python3 onderhoud.py fix-links [--vault PAD]   # kale [[naam]]-links aanvullen met het pad
  python3 onderhoud.py fix-moves [--vault PAD]   # verhuisde paden uit _Onderhoud/moves.tsv herschrijven
  python3 onderhoud.py fix-paths [--vault PAD]   # `pad` naar een vault-notitie omzetten in een link
  python3 onderhoud.py week      [--vault PAD]   # fix-moves, hubs, fix-links, controle; rapport in _Onderhoud/

Zonder --vault leest het script de regel `Vault:` uit ~/.kennisbasis/instellingen.txt.

Verhuizingen: zet in <vault>/_Onderhoud/moves.tsv per regel `oud<TAB>nieuw`, gerekend vanaf de
hoofdmap van de vault, zonder .md. Het langste pad wint.
"""
import os, re, sys, argparse, datetime
from collections import Counter

MS, ME = "<!-- hub:auto -->", "<!-- /hub:auto -->"
# Only markers alone on a line count as block boundaries, so a note that mentions
# the marker in prose or a code span is never mistaken for a hub block.
BLOCK_RE = re.compile(r'^[ \t]*<!-- hub:auto -->[ \t]*$.*?^[ \t]*<!-- /hub:auto -->[ \t]*$',
                      re.S | re.M)
TODAY = datetime.date.today().isoformat()
ALLOWED_NONMD = {'.gitkeep', '.gitignore', '.DS_Store'}
ALLOWED_NONMD_EXT = {'.base', '.canvas'}
REQUIRED_FM = ('title', 'created', 'updated', 'type')
MAINTENANCE_DIR = '_Onderhoud'
SETTINGS_FILE = os.path.expanduser('~/.kennisbasis/instellingen.txt')
# Fallback when the settings file is missing: the instruction files of the supported AI programs.
INSTRUCTION_FILES = [os.path.expanduser(p) for p in (
    '~/.claude/CLAUDE.md', '~/.codex/AGENTS.md', '~/.gemini/GEMINI.md')]


def skip_dir(name):
    # Hidden folders (.obsidian, .git, .trash) and underscore folders (_Prullenbak, _Onderhoud) are not notes.
    return name.startswith('.') or name.startswith('_') or name in ('node_modules', '__pycache__')


def vault_from_settings():
    for path in [SETTINGS_FILE] + INSTRUCTION_FILES:
        if not os.path.exists(path):
            continue
        text = open(path, encoding='utf-8', errors='ignore').read()
        m = re.search(r'^Vault:\s*(.+?)\s*$', text, re.M)
        if m:
            return m.group(1).strip('`"\'')
    return None


def vault_path(args):
    raw = args.vault or vault_from_settings()
    if not raw:
        sys.exit("Geen vault gevonden. Geef --vault PAD mee, of zet `Vault: <pad>` in ~/.kennisbasis/instellingen.txt.")
    v = os.path.realpath(os.path.expanduser(raw))
    if not os.path.isdir(v):
        sys.exit(f"Vault niet gevonden: {v}")
    return v


def walk(K):
    for r, d, f in os.walk(K):
        d[:] = [x for x in d if not skip_dir(x)]
        yield r, d, f


def walk_md(K):
    for r, d, f in walk(K):
        for n in f:
            if n.endswith('.md'):
                yield os.path.join(r, n)


def walk_text_files(K):
    for r, d, f in walk(K):
        for n in f:
            if n.endswith('.md') or n.endswith('.base'):
                yield os.path.join(r, n)


def vr(K, p):
    return os.path.relpath(p, K).replace('\\', '/')


def read(p):
    return open(p, encoding='utf-8', errors='ignore').read()


def write(p, t):
    with open(p, 'w', encoding='utf-8') as fh:
        fh.write(t)


# ---------- hubs ----------

def find_hub(d):
    hub = f"{os.path.basename(d)}.md"
    return hub if os.path.exists(os.path.join(d, hub)) else None


def cmd_hubs(K, out=print):
    hubs = {}
    created = []
    for root, dirs, files in walk(K):
        if root == K:
            continue
        has_notes = any(n.endswith('.md') for _, _, f2 in walk(root) for n in f2)
        if not has_notes:
            continue  # sync tools sometimes restore empty folders; those get no hub
        hub = find_hub(root)
        if hub is None:
            base = os.path.basename(root)
            hub = f"{base}.md"
            write(os.path.join(root, hub),
                  f"---\ntitle: {base}\ncreated: {TODAY}\nupdated: {TODAY}\n"
                  f"type: hub\ntags: [hub]\n---\n\n# {base}\n")
            created.append(vr(K, os.path.join(root, hub)))
        hubs[root] = hub

    def wl(p, label=None):
        return f"[[{vr(K, p)[:-3]}|{label or os.path.splitext(os.path.basename(p))[0]}]]"

    for d, hub in hubs.items():
        hubp = os.path.join(d, hub)
        files = sorted(f for f in os.listdir(d) if f.endswith('.md') and f != hub)
        subdirs = sorted(x for x in os.listdir(d) if os.path.join(d, x) in hubs)
        parent = os.path.dirname(d)
        up = os.path.join(K, 'README.md') if parent == K else (
            os.path.join(parent, hubs[parent]) if parent in hubs else None)
        lines = []
        if up and os.path.exists(up):
            lines.append(f"⬆ {wl(up, 'vault' if parent == K else os.path.basename(parent))}")
        if subdirs:
            lines.append("\n**Mappen:**")
            lines += [f"- {wl(os.path.join(d, s, hubs[os.path.join(d, s)]), s)}" for s in subdirs]
        if files:
            lines.append("\n**Notities:**")
            lines += [f"- {wl(os.path.join(d, f))}" for f in files]
        block = MS + "\n" + "\n".join(lines) + "\n" + ME
        t = read(hubp)
        new = BLOCK_RE.sub(lambda _: block, t, count=1) if BLOCK_RE.search(t) else t.rstrip() + "\n\n" + block + "\n"
        if new != t:
            write(hubp, new)
    out(f"hubs: {len(hubs)} overzichtsnotities bijgewerkt, {len(created)} nieuw" + (f": {created[:5]}" if created else ""))
    return 0


# ---------- verhuizingen ----------

def moves_file(K):
    return os.path.join(K, MAINTENANCE_DIR, 'moves.tsv')


def load_moves(K):
    rows = []
    p = moves_file(K)
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            line = line.rstrip('\n')
            if not line or line.startswith('#') or '\t' not in line:
                continue
            old, new = line.split('\t')[:2]
            rows.append((old.strip().strip('/'), new.strip().strip('/')))
    rows.sort(key=lambda r: -len(r[0]))
    return rows


def move_pattern(old):
    # Not inside a word; followed by a path boundary.
    return re.compile(r'(?<![A-Za-z0-9_\-])' + re.escape(old) + r'(\.md)?(?=$|[/|#\]\)\s`"\'.,:;])', re.M)


def cmd_fixmoves(K, out=print):
    moves = load_moves(K)
    if not moves:
        out("fix-moves: geen verhuizingen in _Onderhoud/moves.tsv")
        return 0
    pats = [(move_pattern(o), n) for o, n in moves]
    changed = files = 0
    for p in walk_text_files(K):
        t = read(p)
        t2 = t
        for pat, new in pats:
            t2, c = pat.subn(lambda m, new=new: new + (m.group(1) or ''), t2)
            changed += c
        if t2 != t:
            files += 1
            write(p, t2)
    out(f"fix-moves: {changed} verwijzingen in {files} bestanden herschreven")
    return 0


# ---------- paden en links ----------

PATH_TEXT_RE = re.compile(r'`([^`\n]+)`')


def vault_prefix_re(K):
    home = os.path.expanduser('~')
    forms = [re.escape(K + '/')]
    if K.startswith(home + '/'):
        forms.append(re.escape('~' + K[len(home):] + '/'))
    return re.compile('(?:' + '|'.join(forms) + ')')


def exists_cs(K, rel):
    """Case-sensitive existence check, also on a case-insensitive filesystem."""
    cur = K
    for part in rel.split('/'):
        if not part:
            continue
        try:
            if part not in os.listdir(cur):
                return False
        except OSError:
            return False
        cur = os.path.join(cur, part)
    return True


def resolve_vault_target(K, raw, prefix_re):
    raw = raw.strip()
    if prefix_re.match(raw):
        raw = prefix_re.sub('', raw, count=1)
    if raw.startswith(('~', '/', '<', '$')) or '*' in raw or '[' in raw:
        return None
    rel = raw.strip('/')
    if '/' not in rel and not rel.endswith(('.md', '.base')):
        return None  # a single word is a tag or term, not a path
    if not exists_cs(K, rel):
        return None
    full = os.path.join(K, rel)
    if os.path.isfile(full) and rel.endswith('.md'):
        return rel[:-3], os.path.basename(rel)[:-3]
    if os.path.isfile(full) and rel.endswith('.base'):
        return rel, os.path.basename(rel)[:-5]
    if os.path.isdir(full):
        hub = find_hub(full)
        if hub:
            return f"{rel}/{hub[:-3]}", os.path.basename(rel)
    return None


def cmd_fixpaths(K, out=print):
    prefix_re = vault_prefix_re(K)
    changed = files = 0
    for p in walk_md(K):
        t = read(p)
        parts = re.split(r'(```.*?```)', t, flags=re.S)
        for i in range(0, len(parts), 2):
            def sub(m):
                nonlocal changed
                r = resolve_vault_target(K, m.group(1), prefix_re)
                if not r:
                    return m.group(0)
                changed += 1
                return f"[[{r[0]}|{r[1]}]]"
            parts[i] = PATH_TEXT_RE.sub(sub, parts[i])
        t2 = ''.join(parts)
        if t2 != t:
            files += 1
            write(p, t2)
    out(f"fix-paths: {changed} paden in {files} bestanden omgezet naar links")
    return 0


def cmd_fixlinks(K, out=print):
    """Qualify bare [[name]] links with the full path where the name resolves to one note."""
    mds = list(walk_md(K))
    by_base = {}
    for p in mds:
        by_base.setdefault(os.path.splitext(os.path.basename(p))[0].lower(), []).append(p)
    by_rel = {vr(K, p)[:-3].lower() for p in mds}
    pat = re.compile(r'(?<!\!)\[\[([^\]|#]+)(\|[^\]]*)?\]\]')
    changed = ambiguous = 0
    for p in mds:
        t = read(p)
        parts = re.split(r'(```.*?```|`[^`]*`)', t, flags=re.S)
        for i in range(0, len(parts), 2):
            def sub(m):
                nonlocal changed, ambiguous
                tgt, label = m.group(1).strip().rstrip('\\'), m.group(2)
                if tgt.lower() in by_rel:
                    return m.group(0)
                cands = by_base.get(tgt.lower(), [])
                if len(cands) == 1:
                    changed += 1
                    return f"[[{vr(K, cands[0])[:-3]}{label or '|' + tgt}]]"
                if len(cands) > 1:
                    # Proximity: same folder wins, then the shortest walk through the tree.
                    src_dir = os.path.dirname(p)

                    def dist(c):
                        cd = os.path.dirname(c)
                        if cd == src_dir:
                            return 0
                        common = os.path.commonpath([src_dir, cd])
                        return (len(os.path.relpath(src_dir, common).split(os.sep))
                                + len(os.path.relpath(cd, common).split(os.sep)))
                    ranked = sorted(cands, key=dist)
                    if dist(ranked[0]) < dist(ranked[1]):
                        changed += 1
                        return f"[[{vr(K, ranked[0])[:-3]}{label or '|' + tgt}]]"
                    ambiguous += 1
                return m.group(0)
            parts[i] = pat.sub(sub, parts[i])
        t2 = ''.join(parts)
        if t2 != t:
            write(p, t2)
    out(f"fix-links: {changed} links aangevuld, {ambiguous} niet eenduidig (met de hand kiezen)")
    return 0


# ---------- controle ----------

def frontmatter_keys(t):
    m = re.match(r'^---\n(.*?)\n---', t, re.S)
    if not m:
        return None
    return {mm.group(1) for mm in re.finditer(r'^([A-Za-z_][A-Za-z0-9_-]*):', m.group(1), re.M)}


def collect_findings(K):
    findings = []
    mds = {p: read(p) for p in walk_md(K)}
    prefix_re = vault_prefix_re(K)

    # Images a note shows inline belong in the vault; every other file belongs in the files folder.
    inline_used = set()
    for t in mds.values():
        for m in re.finditer(r'!\[\[([^\]|#]+)', t):
            inline_used.add(os.path.basename(m.group(1).strip()).lower())
        fmm = re.match(r'^---\n(.*?)\n---\n', t, re.S)
        if fmm:
            for m in re.finditer(r'^(?:cover|image|banner):\s*"?([^"\n]+)"?', fmm.group(1), re.M):
                inline_used.add(os.path.basename(m.group(1).strip()).lower())

    for r, d, f in walk(K):
        for n in f:
            if n.endswith('.md') or n in ALLOWED_NONMD or os.path.splitext(n)[1].lower() in ALLOWED_NONMD_EXT:
                continue
            if n.lower() in inline_used:
                continue
            findings.append(("geen-notitie", vr(K, os.path.join(r, n))))
        if 'README.md' in f and r != K:
            findings.append(("readme-niet-in-hoofdmap", vr(K, os.path.join(r, 'README.md'))))
        for n in f:
            if '#' in n and n.endswith('.md'):
                findings.append(("hekje-in-naam", vr(K, os.path.join(r, n))))

    for p, t in mds.items():
        keys = frontmatter_keys(t)
        if keys is None:
            findings.append(("geen-frontmatter", vr(K, p)))
        else:
            missing = [k for k in REQUIRED_FM if k not in keys]
            if missing:
                findings.append(("frontmatter-mist", f"{vr(K, p)} -> {', '.join(missing)}"))

    for old, new in load_moves(K):
        pat = move_pattern(old)
        for p in walk_text_files(K):
            if pat.search(mds.get(p) or read(p)):
                findings.append(("verhuisd-pad", f"{vr(K, p)} -> {old} (nu {new})"))

    for p, t in mds.items():
        body = re.sub(r'```.*?```', '', t, flags=re.S)
        for m in PATH_TEXT_RE.finditer(body):
            if resolve_vault_target(K, m.group(1), prefix_re):
                findings.append(("pad-als-tekst", f"{vr(K, p)} -> `{m.group(1)[:60]}`"))

    for r, d, f in walk(K):
        for n in f:
            if n.endswith('.base'):
                bp = os.path.join(r, n)
                for m in re.finditer(r'file\.folder\s*==\s*"([^"]+)"', read(bp)):
                    if not os.path.isdir(os.path.join(K, m.group(1))):
                        findings.append(("base-map-bestaat-niet", f"{vr(K, bp)} -> \"{m.group(1)}\""))

    by_rel = {vr(K, p)[:-3].lower(): p for p in mds}
    by_base = {}
    for p in mds:
        by_base.setdefault(os.path.splitext(os.path.basename(p))[0].lower(), []).append(p)
    assets = set()
    for r, d, f in walk(K):
        for n in f:
            if not n.endswith('.md'):
                assets.add(n.lower())
                assets.add(vr(K, os.path.join(r, n)).lower())
    link_re = re.compile(r'(?<!\!)\[\[([^\]|#]+)')
    inbound = {}
    for p, t in mds.items():
        t2 = re.sub(r'```.*?```', '', t, flags=re.S)
        t2 = re.sub(r'`[^`]*`', '', t2)
        for m in link_re.findall(t2):
            tgt = m.strip().rstrip('\\').lower()  # `\|` in a table is a valid alias separator
            if tgt in by_rel:
                inbound[by_rel[tgt]] = inbound.get(by_rel[tgt], 0) + 1
            elif tgt in assets or os.path.basename(tgt) in assets:
                continue
            elif tgt in by_base:
                for c in by_base[tgt]:
                    inbound[c] = inbound.get(c, 0) + 1
                findings.append(("kale-link", f"{vr(K, p)} -> [[{m.strip()[:60]}]]"))
            elif not any(c in tgt for c in ('$', '"', '^', '...', '<')):
                findings.append(("kapotte-link", f"{vr(K, p)} -> [[{m.strip()[:60]}]]"))
    for p in mds:
        if vr(K, p) != 'README.md' and inbound.get(p, 0) == 0:
            findings.append(("zwevend", vr(K, p)))
    return findings, len(mds)


EXPLAIN = {
    "geen-notitie": "Een bestand dat geen notitie is. Hoort in je bestandsmap, niet in de vault.",
    "readme-niet-in-hoofdmap": "Alleen de hoofdmap heeft een README.md. Een map heeft een notitie met de naam van de map.",
    "hekje-in-naam": "Een # in een bestandsnaam breekt links.",
    "geen-frontmatter": "De notitie mist het blok met titel en datums bovenaan.",
    "frontmatter-mist": "Het blok bovenaan mist een verplicht veld.",
    "verhuisd-pad": "Verwijst nog naar een oude plek. `fix-moves` lost dit op.",
    "pad-als-tekst": "Een pad naar een notitie staat als tekst. `fix-paths` maakt er een link van.",
    "base-map-bestaat-niet": "Een Obsidian-overzicht (.base) zoekt in een map die niet bestaat.",
    "kale-link": "Link zonder pad. `fix-links` vult hem aan.",
    "kapotte-link": "Link naar een notitie die niet bestaat.",
    "zwevend": "Geen enkele notitie linkt hierheen. `hubs` lost dit meestal op.",
}


def cmd_controle(K, out=print):
    findings, count = collect_findings(K)
    if not findings:
        out(f"controle: schoon ({count} notities)")
        return 0, findings, count
    out(f"controle: {len(findings)} bevindingen in {count} notities")
    for k, c in Counter(x[0] for x in findings).most_common():
        out(f"  {k}: {c}")
    for k, v in findings[:40]:
        out(f"  [{k}] {v}")
    if len(findings) > 40:
        out(f"  ... en {len(findings) - 40} meer")
    return 1, findings, count


def cmd_week(K):
    log = []
    out = log.append
    cmd_fixmoves(K, out)
    cmd_hubs(K, out)
    cmd_fixlinks(K, out)
    code, findings, count = cmd_controle(K, out)

    d = os.path.join(K, MAINTENANCE_DIR)
    os.makedirs(d, exist_ok=True)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = [f"# Weekcontrole {now}", "",
             f"Resultaat: {'schoon' if not findings else f'{len(findings)} bevindingen'} ({count} notities)", ""]
    if findings:
        lines += ["## Bevindingen", "", "| Soort | Waar | Wat het betekent |", "|---|---|---|"]
        for k, v in findings:
            lines.append(f"| {k} | {v.replace('|', '/')} | {EXPLAIN.get(k, '')} |")
        lines.append("")
    lines += ["## Wat er vanzelf is bijgewerkt", "", *[f"- {x}" for x in log if not x.startswith('  ')], ""]
    write(os.path.join(d, 'laatste-controle.md'), "\n".join(lines))
    print("\n".join(log))
    print(f"rapport: {os.path.join(d, 'laatste-controle.md')}")
    return code


def main():
    ap = argparse.ArgumentParser(description="Onderhoud voor de vault van de kennisbasis.")
    ap.add_argument('command', choices=['controle', 'hubs', 'fix-links', 'fix-moves', 'fix-paths', 'week'])
    ap.add_argument('--vault', default=None)
    args = ap.parse_args()
    K = vault_path(args)
    if args.command == 'controle':
        sys.exit(cmd_controle(K)[0])
    if args.command == 'week':
        sys.exit(cmd_week(K))
    sys.exit({'hubs': cmd_hubs, 'fix-links': cmd_fixlinks,
              'fix-moves': cmd_fixmoves, 'fix-paths': cmd_fixpaths}[args.command](K))


if __name__ == '__main__':
    main()
