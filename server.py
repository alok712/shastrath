"""Astra Wars: Epics of Bharat - server.
Run:  pip install aiohttp  &&  python server.py   ->  http://localhost:8765
Modes: 1, 2, 3, and 4 players (Solo Sadhana, 1v1 Dvanda, 3P Tri-Yuddha, 4P Kurukshetra Mahayuddha).
Tracks seen questions persistently to avoid repetition across games.
"""
import asyncio, json, random, time, os, re, shutil, socket, threading, webbrowser, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from aiohttp import web, WSMsgType

QFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "questions.json")
_qcache = {"mtime": None, "data": []}


def load_questions():
    """Reads questions.json (re-read automatically whenever the file changes)."""
    try:
        mt = os.path.getmtime(QFILE)
        if mt != _qcache["mtime"]:
            raw = json.load(open(QFILE, encoding="utf-8"))["questions"]; good = []
            for i, q in enumerate(raw):
                ok = (q.get("epic") in ("M", "R") and q.get("level") in (1, 2, 3) and q.get("q")
                      and isinstance(q.get("options"), list) and len(q["options"]) == 4 and q.get("answer") in (0, 1, 2, 3))
                if ok: good.append(q)
                else: print(f"  questions.json: skipped invalid question #{i + 1}")
            _qcache.update(mtime=mt, data=good); print(f"  Loaded {len(good)} questions.")
    except (OSError, ValueError, KeyError) as e:
        print(f"  Could not read questions.json: {e}")
    return _qcache["data"]


BOT_SKILL = {"easy": (0.45, 5.5), "medium": (0.72, 3.8), "hard": (0.92, 2.2)}
BOT_NAMES = [
    "Rakshasa Overlord",
    "Gandharva Champion",
    "Kinnara Warrior",
    "Asura Titan",
    "Yakshara King",
    "Naga Chieftain"
]

rooms, waiting = {}, {}  # waiting: key -> list of players


class Player:
    def __init__(s, ws, name, seen_ref=None):
        s.ws = ws
        s.name = name
        s.hp = 100
        s.gauge = 0
        s.ans = None
        s.lang = "en"
        s.score = 0
        s.streak = 0
        s.max_streak = 0
        s.right = 0
        s.fastest_ans = 99.0
        s.plan = None
        s.is_bot = (ws is None)
        s.seen_questions = seen_ref if seen_ref is not None else set()

    async def send(s, **m):
        if s.ws is not None and not s.ws.closed:
            try:
                await s.ws.send_str(json.dumps(m))
            except Exception:
                pass


def new_player(ws, d, seen_ref=None):
    p = Player(ws, (d.get("name") or "").strip()[:16] or "Warrior", seen_ref=seen_ref)
    p.lang = d["lang"] if isinstance(d.get("lang"), str) else "en"
    return p


def localize(q, lang):
    """Question text/options in the player's language (optional 'tr' block in questions.json), else English."""
    tr = (q.get("tr") or {}).get(lang)
    if isinstance(tr, dict) and tr.get("q") and isinstance(tr.get("options"), list) and len(tr["options"]) == 4:
        return tr["q"], tr["options"]
    return q["q"], q["options"]


class Match:
    def __init__(s, players, realm, level=0, bot_difficulty="medium", rounds_total=12, max_hp=100):
        s.p = players
        s.realm = realm
        s.level = level
        s.bot_difficulty = bot_difficulty
        s.rounds_total = rounds_total
        s.max_hp = max_hp
        for p in s.p:
            p.hp = max_hp
        s.n = 0
        s.used = set()
        s.last_epic = None
        s.qs = load_questions()
        s.extra = [0] * len(players)
        s.ts = [10] * len(players)
        s.event = asyncio.Event()
        s.task = asyncio.create_task(s.run())

    def pick(s):
        """Draws without repeats across games and current match."""
        pool = [i for i, q in enumerate(s.qs) if s.realm == "A" or q["epic"] == s.realm]
        want = s.level or min(3, 1 + (s.n - 1) // 3)

        # Union of seen questions among all human players
        human_seen = set()
        for p in s.p:
            if not p.is_bot:
                human_seen.update(p.seen_questions)

        # Filter out questions used in this match AND previously seen in session
        fresh = [i for i in pool if i not in s.used and i not in human_seen]
        if len(fresh) < 3:
            # Pool exhausted! Reset persistent seen questions for human players
            for p in s.p:
                if not p.is_bot:
                    p.seen_questions.clear()
            fresh = [i for i in pool if i not in s.used]

        # Prioritize matching level
        c = [i for i in fresh if s.qs[i]["level"] == want]
        if not c:
            c = sorted(fresh, key=lambda i: abs(s.qs[i]["level"] - want))
            if c:
                min_diff = abs(s.qs[c[0]]["level"] - want)
                c = [i for i in c if abs(s.qs[i]["level"] - want) == min_diff]
        if not c:
            s.used.clear()
            c = [i for i in pool if s.qs[i]["epic"] != s.last_epic] or pool

        if s.realm == "A":
            alt = [i for i in c if s.qs[i]["epic"] != s.last_epic]
            if alt:
                c = alt

        chosen = random.choice(c) if c else random.choice(pool)
        s.used.add(chosen)
        s.last_epic = s.qs[chosen]["epic"]
        # Mark as seen for all human players
        for p in s.p:
            if not p.is_bot:
                p.seen_questions.add(chosen)
        return chosen

    def snap(s, gain):
        return dict(
            sc=[p.score for p in s.p],
            gain=gain,
            st=[p.streak for p in s.p],
            rt=[p.right for p in s.p]
        )

    async def bcast(s, **m):
        for p in s.p:
            await p.send(**m)

    async def run(s):
        await s.bcast(type="start", names=[p.name for p in s.p], count=len(s.p), rounds=s.rounds_total, max_hp=s.max_hp)
        await asyncio.sleep(1.5)
        final = False

        while s.n < s.rounds_total:
            s.n += 1
            q_idx = s.pick()
            q = s.qs[q_idx]
            order = random.sample(range(4), 4)
            ok = order.index(q["answer"])

            # Bonus question every 4th round (except final)
            bonus = (not final) and (s.n % 4 == 0) and (s.n < s.rounds_total)
            base_t = 5 if final else 10
            s.ts = [base_t + (0 if final else extra_val) for extra_val in s.extra]
            s.extra = [0] * len(s.p)
            max_wait = max(s.ts)

            for p in s.p:
                p.ans = None
                p.plan = None

            s.event.clear()
            s.t0 = time.time()

            all_tr = {}
            for lang_k in ("en", "hi", "mr", "sa", "ta", "te"):
                t_txt, t_opts = localize(q, lang_k)
                all_tr[lang_k] = {"text": t_txt, "opts": [t_opts[k] for k in order]}

            # Plan bot responses
            for idx, p in enumerate(s.p):
                if p.is_bot:
                    acc, avg = BOT_SKILL.get(s.bot_difficulty, (0.7, 3.8))
                    el = max(0.8, random.gauss(avg, 0.9))
                    pick = ok if random.random() < acc else random.choice([k for k in range(4) if k != ok])
                    p.plan = (pick, el) if el <= s.ts[idx] else (-1, 99.0)

            # Send question to all players
            for i, p in enumerate(s.p):
                lt, lo = localize(q, p.lang)
                await p.send(
                    type="q",
                    n=s.n,
                    total_rounds=s.rounds_total,
                    text=lt,
                    opts=[lo[k] for k in order],
                    all_tr=all_tr,
                    t=s.ts[i],
                    you=i,
                    final=final,
                    bonus=bonus,
                    epic=q["epic"],
                    lvl=q["level"],
                    players=[{"name": x.name, "hp": x.hp, "score": x.score, "streak": x.streak} for x in s.p]
                )

            # Wait for humans to answer or timeout
            try:
                await asyncio.wait_for(s.event.wait(), max_wait + 0.3)
            except asyncio.TimeoutError:
                pass

            # Fill bot answers
            for p in s.p:
                if p.is_bot and p.ans is None:
                    p.ans = p.plan if p.plan else (-1, 99.0)

            # Compile results
            res = []
            for idx, p in enumerate(s.p):
                good = (p.ans is not None and p.ans[0] == ok and p.ans[1] <= s.ts[idx])
                ans_time = p.ans[1] if (p.ans and good) else 99.0
                res.append((good, ans_time))

            gain = [0] * len(s.p)

            # Brahmastra / Final Sudden Death round
            if final:
                correct_indices = [i for i, r in enumerate(res) if r[0]]
                if correct_indices:
                    winner_idx = min(correct_indices, key=lambda i: res[i][1])
                    s.p[winner_idx].score += 300
                    s.p[winner_idx].right += 1
                    await s.finish(winner_idx)
                    return
                # Defender recovers if no one solved
                for p in s.p:
                    if p.hp <= 20: p.hp = 30
                final = False
                await s.bcast(
                    type="res",
                    **s.snap(gain),
                    correct=ok,
                    hp=[p.hp for p in s.p],
                    g=[p.gauge for p in s.p],
                    fast=[False] * len(s.p),
                    clash=False,
                    hit=[False] * len(s.p),
                    final=True
                )
                await asyncio.sleep(2.5)
                continue

            # Bonus Round
            if bonus:
                for i, r in enumerate(res):
                    if r[0]:
                        s.extra[i] = 5
                        gain[i] = 50
                        s.p[i].score += 50
                        s.p[i].right += 1
                await s.bcast(
                    type="res",
                    **s.snap(gain),
                    correct=ok,
                    hp=[p.hp for p in s.p],
                    g=[p.gauge for p in s.p],
                    fast=[False] * len(s.p),
                    clash=False,
                    hit=[False] * len(s.p),
                    final=False,
                    bonus=True,
                    extra=s.extra[:]
                )
                await asyncio.sleep(2.2)
                continue

            # Standard Round Resolution
            fast = [r[0] and r[1] <= 3.0 for r in res]
            hit = [False] * len(s.p)
            correct_count = sum(1 for r in res if r[0])
            clash = (len(s.p) == 2 and fast[0] and fast[1]) or (len(s.p) > 2 and sum(1 for f in fast if f) >= 2)

            for i, r in enumerate(res):
                if r[0]:
                    ans_time = r[1]
                    s.p[i].right += 1
                    s.p[i].streak += 1
                    if s.p[i].streak > s.p[i].max_streak:
                        s.p[i].max_streak = s.p[i].streak
                    if ans_time < s.p[i].fastest_ans:
                        s.p[i].fastest_ans = ans_time

                    gain[i] = 100 + (50 if fast[i] else 0) + 25 * min(s.p[i].streak - 1, 4)
                    s.p[i].score += gain[i]
                    s.p[i].gauge = min(100, s.p[i].gauge + (34 if fast[i] else 17))

                    dmg = (20 if fast[i] else 12) // (2 if clash else 1)
                    if len(s.p) == 2:
                        target = 1 - i
                        s.p[target].hp = max(0, s.p[target].hp - dmg)
                        hit[target] = True
                    else:
                        # 3 or 4 players FFA: strike rival with highest HP among alive opponents
                        opponents = [idx for idx in range(len(s.p)) if idx != i and s.p[idx].hp > 0]
                        if opponents:
                            target = max(opponents, key=lambda idx: s.p[idx].hp)
                            s.p[target].hp = max(0, s.p[target].hp - dmg)
                            hit[target] = True
                else:
                    s.p[i].streak = 0

            await s.bcast(
                type="res",
                **s.snap(gain),
                correct=ok,
                hp=[p.hp for p in s.p],
                g=[p.gauge for p in s.p],
                fast=fast,
                clash=clash,
                hit=hit,
                final=False
            )
            await asyncio.sleep(2.4)

            # Check eliminations
            alive = [i for i, p in enumerate(s.p) if p.hp > 0]
            if len(s.p) == 2:
                dead = [i for i, p in enumerate(s.p) if p.hp <= 0]
                if dead:
                    winner = 1 - dead[0] if len(dead) == 1 else (0 if s.p[0].gauge >= s.p[1].gauge else 1)
                    await s.finish(winner)
                    return
                if any(p.hp < 20 for p in s.p):
                    final = True
                    await s.bcast(type="brahma")
                    await asyncio.sleep(2.8)
            else:
                if len(alive) <= 1:
                    winner = alive[0] if alive else max(range(len(s.p)), key=lambda i: s.p[i].score)
                    await s.finish(winner)
                    return

        # End of rounds: highest score wins
        top_winner = max(range(len(s.p)), key=lambda i: (s.p[i].score, s.p[i].hp))
        await s.finish(top_winner)

    def answer(s, i, idx):
        if i >= len(s.p):
            return
        p = s.p[i]
        if p.ans is None:
            p.ans = (idx, time.time() - s.t0)
            human_unanswered = [x for x in s.p if not x.is_bot and x.ans is None]
            if not human_unanswered:
                s.event.set()

    async def finish(s, w):
        rank_order = sorted(range(len(s.p)), key=lambda i: (s.p[i].score, s.p[i].right), reverse=True)
        await s.bcast(
            type="end",
            winner=w,
            ranks=rank_order,
            names=[p.name for p in s.p],
            sc=[p.score for p in s.p],
            rt=[p.right for p in s.p],
            hp=[p.hp for p in s.p],
            st=[p.max_streak for p in s.p],
            fastest=[round(p.fastest_ans, 2) if p.fastest_ans < 90 else None for p in s.p]
        )
        s.task = None


async def ws_handler(req):
    ws = web.WebSocketResponse(heartbeat=20)
    await ws.prepare(req)
    # Persistent seen questions for this connection session
    seen_set = set()
    me, match, idx = None, None, 0

    async for msg in ws:
        if msg.type != WSMsgType.TEXT:
            continue
        try:
            d = json.loads(msg.data)
        except Exception:
            continue
        t = d.get("type")

        if t in ("bot", "rematch"):
            num_players = max(1, min(4, int(d.get("players_count", 2))))
            bot_level = d.get("level", "medium")
            rounds_count = int(d.get("rounds", 12))
            realm_choice = d.get("realm", "A")
            q_level = int(d.get("qlevel", 0))

            me = new_player(ws, d, seen_ref=seen_set)
            players_list = [me]

            # In 1P, add 1 Bot so player has an opponent to test against
            bots_to_add = max(1, num_players - 1)
            for b_i in range(bots_to_add):
                b_name = BOT_NAMES[b_i % len(BOT_NAMES)]
                players_list.append(Player(None, b_name))

            match = Match(
                players_list,
                realm=realm_choice,
                level=q_level,
                bot_difficulty=bot_level,
                rounds_total=rounds_count
            )
            idx = 0

        elif t == "online":
            target_count = max(2, min(4, int(d.get("players_count", 2))))
            me = new_player(ws, d, seen_ref=seen_set)
            room_key = (d.get("room") or "").upper() or f"_M_{d.get('realm', 'A')}_{d.get('qlevel', 0)}_{target_count}"
            
            queue = waiting.setdefault(room_key, [])
            # Filter closed
            queue = [p for p in queue if p.ws and not p.ws.closed]
            waiting[room_key] = queue

            queue.append(me)
            me.wait_key = room_key

            if len(queue) >= target_count:
                match_players = queue[:target_count]
                waiting[room_key] = queue[target_count:]
                m = Match(
                    match_players,
                    realm=d.get("realm", "A"),
                    level=int(d.get("qlevel", 0)),
                    rounds_total=int(d.get("rounds", 12))
                )
                for slot_idx, player in enumerate(match_players):
                    player.match_ref = m
                    player.match_idx = slot_idx
                match = m
                idx = match_players.index(me)
            else:
                await me.send(
                    type="wait",
                    room=room_key if not room_key.startswith("_") else "",
                    current=len(queue),
                    needed=target_count
                )
                me.match_ref = None

        elif t == "ans":
            m = match or getattr(me, "match_ref", None)
            active_idx = idx if match else getattr(me, "match_idx", 0)
            if m:
                m.answer(active_idx, d.get("i", 0))

        elif t == "set_lang":
            if me:
                me.lang = d.get("lang", "en")

    # Cleanup on disconnect
    if me and getattr(me, "wait_key", None) in waiting:
        waiting[me.wait_key] = [p for p in waiting[me.wait_key] if p is not me]
        if not waiting[me.wait_key]:
            waiting.pop(me.wait_key, None)

    m = match or getattr(me, "match_ref", None)
    if m and m.task:
        m.task.cancel()
        await m.bcast(type="end", winner=-1)

    return ws


HERE = os.path.dirname(os.path.abspath(__file__))
app = web.Application()

async def index(r): return web.FileResponse(os.path.join(HERE, "index.html"))
async def css(r): return web.FileResponse(os.path.join(HERE, "style.css"))
async def langjs(r): return web.FileResponse(os.path.join(HERE, "lang.js"))

app.add_routes([
    web.get("/ws", ws_handler),
    web.get("/", index),
    web.get("/style.css", css),
    web.get("/lang.js", langjs),
    web.get("/api/link", lambda r: link(r))
])

PORT = int(os.environ.get("PORT", 8765))
HOSTED = bool(os.environ.get("PORT"))


def lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


URL_RE = re.compile(r"https://[\w.-]+\.(?:trycloudflare\.com|lhr\.life|localhost\.run|serveo\.net|serveousercontent\.com)\S*")
PIPE, STDOUT = asyncio.subprocess.PIPE, asyncio.subprocess.STDOUT


def get_cloudflared():
    exe = shutil.which("cloudflared")
    if exe: return exe
    import platform, urllib.request
    sysn, mach = platform.system(), platform.machine().lower()
    arch = "arm64" if ("arm" in mach or "aarch" in mach) else "amd64"
    if sysn == "Windows": fn, asset = "cloudflared.exe", "cloudflared-windows-amd64.exe"
    elif sysn == "Linux": fn, asset = "cloudflared", f"cloudflared-linux-{arch}"
    else: return None
    path = os.path.join(HERE, fn)
    if not os.path.exists(path):
        print("  Downloading cloudflared (one time only, about 40 MB) ...")
        urllib.request.urlretrieve("https://github.com/cloudflare/cloudflared/releases/latest/download/" + asset, path)
        os.chmod(path, 0o755)
    return path


async def try_cmd(name, cmd, app, wait=40):
    print(f"  Trying {name} tunnel ...")
    try: p = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=STDOUT)
    except OSError as e: print(f"    {name}: could not start ({e})"); return None
    async def read():
        async for line in p.stdout:
            m = URL_RE.search(line.decode(errors="ignore"))
            if m and "api." not in m.group(0): return m.group(0)
    async def drain():
        async for _ in p.stdout: pass
    try: url = await asyncio.wait_for(read(), wait)
    except asyncio.TimeoutError: url = None
    if url:
        app["tunnel"] = p; app["drain"] = asyncio.create_task(drain()); return url
    print(f"    {name}: no link received")
    try: p.terminate()
    except ProcessLookupError: pass
    return None


async def start_tunnel(app):
    if HOSTED or os.environ.get("NO_TUNNEL"): return
    loop = asyncio.get_running_loop(); attempts = []
    try: exe = await loop.run_in_executor(None, get_cloudflared)
    except Exception as e: print(f"  cloudflared unavailable: {e}"); exe = None
    if exe: attempts.append(("Cloudflare", [exe, "tunnel", "--url", f"http://localhost:{PORT}", "--no-autoupdate"]))
    if shutil.which("ssh"):
        o = ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "ServerAliveInterval=30", "-o", "ExitOnForwardFailure=yes"]
        attempts += [("localhost.run", o + ["-R", f"80:localhost:{PORT}", "nokey@localhost.run"]), ("serveo", o + ["-R", f"80:localhost:{PORT}", "serveo.net"])]
    for name, cmd in attempts:
        url = await try_cmd(name, cmd, app)
        if url:
            app["public_url"] = url.rstrip("/")
            print(f"\n  ===== PUBLIC LINK =====\n  {app['public_url']}\n"); return


async def link(r):
    return web.json_response({"url": app.get("public_url", "")}, headers={"Access-Control-Allow-Origin": "*"})


def open_browser(url):
    """Robustly opens the URL in the user's default web browser."""
    try:
        if sys.platform == "win32":
            os.startfile(url)
            return
    except Exception:
        pass
    try:
        webbrowser.open(url)
    except Exception:
        pass


def find_free_port(start_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", start_port))
            return start_port
        except OSError:
            pass
    for p in range(start_port + 1, start_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", p))
                print(f"  [Notice] Port {start_port} was busy. Using port {p} instead.")
                return p
            except OSError:
                continue
    return start_port


async def on_start(app):
    url = f"http://localhost:{PORT}"
    print("\n  =======================================================")
    print("  [ Astra Wars: Epics of Bharat - Server Online ]")
    print(f"  Local Browser : {url}")
    print(f"  Same Wi-Fi    : http://{lan_ip()}:{PORT}")
    print("  Launching game in your default browser...")
    print("  Keep this terminal window open while playing.")
    print("  Press Ctrl+C to stop the server.")
    print("  =======================================================\n")
    if not HOSTED:
        threading.Timer(0.6, lambda: open_browser(url)).start()
    app["tunnel_task"] = asyncio.create_task(start_tunnel(app))


async def on_stop(app):
    try:
        if "tunnel" in app and app["tunnel"].returncode is None:
            app["tunnel"].terminate()
    except ProcessLookupError:
        pass


app.on_startup.append(on_start)
app.on_cleanup.append(on_stop)


if __name__ == "__main__":
    PORT = find_free_port(PORT)
    web.run_app(app, host="0.0.0.0", port=PORT, print=None)