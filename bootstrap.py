"""Super JinX bootstrap: zero-touch setup for PasarGuard on Railway. Idempotent: safe on every boot."""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request

BASE = "http://127.0.0.1:8000"
DATA = os.getenv("JINX_DATA", "/var/lib/pasarguard")
DOMAIN = (os.getenv("PUBLIC_DOMAIN") or os.getenv("RAILWAY_PUBLIC_DOMAIN") or "").strip()
import subprocess
USER, PASS = "admin", "admin"          # first-boot login; change it later in the panel or with the owner key
RESELLER_USER, RESELLER_PASS, RESELLER_GB = "reseller", "reseller", 50
CORE_NAME, NODE_NAME = "JinX-Core", "JinX-Core"
PRO_GROUP, STD_GROUP = "جینکس پرو", "𝗝𝗶𝗻𝗫"   # 1 premium config / 4 different configs
OLD_GROUP = "jinx-all"                         # from earlier versions, renamed to STD_GROUP (keeps its users)
TITLE = os.getenv("CONFIG_TITLE", "جینکس | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫")   # shown after every config name
GB = 1024 ** 3
DAY = 86400

# All configs go through Railway's TLS edge on 443 with alpn=http/1.1 (the only thing Railway serves).
# جینکس پرو: the single most compatible + lowest-latency setup: VLESS + WebSocket + early data, Chrome fp.
# 𝗝𝗶𝗻𝗫: 4 configs that are really different (protocol / transport / fingerprint / path), all supported
#        by v2rayNG, V2Box, Hiddify, Streisand, NekoBox, Happ, Clash Meta and sing-box.
# ?ed=2560 = early data: the first packet rides on the handshake -> one round trip less per connection.
INBOUNDS = [
    # tag              proto     port  net            server path                                   fp         name       group
    ("JX-VLESS-WS-1", "vless",  10001, "ws",          "/ws/",     "chrome",  "𝗣𝗿𝗼",        "pro"),
    ("JX-VLESS-WS-2", "vless",  10002, "ws",          "/stream/", "firefox", "⚡ 𝗙𝗹𝗮𝘀𝗵",    "std"),
    ("JX-TROJAN-WS",  "trojan", 10003, "ws",          "/live/",   "safari",  "🔥 𝗙𝗶𝗿𝗲",     "std"),
    ("JX-VMESS-WS",   "vmess",  10004, "ws",          "/gw/",    "edge",    "💎 𝗗𝗶𝗮𝗺𝗼𝗻𝗱", "std"),
    ("JX-VLESS-HU",   "vless",  10005, "httpupgrade", "/cdn/",    "ios",     "🌙 𝗡𝗶𝗴𝗵𝘁",    "std"),
]
EARLY_DATA = "?ed=2560"
# real paths are unique per install (genpaths.py writes them to the volume before nginx starts)
try:
    _P = json.load(open(f"{DATA}/paths.json"))
    INBOUNDS = [(t, pr, po, n, _P.get(t, pa), fp, nm, g) for (t, pr, po, n, pa, fp, nm, g) in INBOUNDS]
except Exception as _e:
    print("[bootstrap] paths.json missing, run genpaths.py first:", _e, flush=True); sys.exit(1)
TEMPLATES = [  # name, GB, days, group
    ("10GB - 30 روز", 10, 30, "std"), ("30GB - 30 روز", 30, 30, "std"), ("50GB - 30 روز", 50, 30, "std"),
    ("100GB - 30 روز", 100, 30, "std"), ("200GB - 60 روز", 200, 60, "std"), ("نامحدود - 30 روز", 0, 30, "std"),
    ("Pro 30GB - 30 روز", 30, 30, "pro"), ("Pro 50GB - 30 روز", 50, 30, "pro"),
    ("Pro 100GB - 30 روز", 100, 30, "pro"), ("Pro نامحدود - 30 روز", 0, 30, "pro"),
]
OLD_TEST_USERS = ("jinx_user1",)   # 50 GB test user that very old versions created by themselves

TOKEN = None

def log(*a): print("[bootstrap]", *a, flush=True)

_GLOBAL = object()

def req(method, path, body=None, form=False, ok=(200, 201, 204), token=_GLOBAL):
    url = BASE + path
    headers = {"Accept": "application/json"}
    data = None
    if body is not None:
        if form:
            data = urllib.parse.urlencode(body).encode(); headers["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    tok = TOKEN if token is _GLOBAL else token
    if tok: headers["Authorization"] = f"Bearer {tok}"
    r = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            raw = resp.read().decode()
            try: return resp.status, json.loads(raw) if raw.strip() else None
            except ValueError: return resp.status, raw
    except urllib.error.HTTPError as e:
        txt = e.read().decode(errors="ignore")
        try: return e.code, json.loads(txt)
        except Exception: return e.code, txt

def must(method, path, body=None):
    code, res = req(method, path, body)
    if code not in (200, 201, 204):
        raise RuntimeError(f"{method} {path} -> {code}: {res}")
    return res

def as_list(res, key):
    if isinstance(res, list): return res
    if isinstance(res, dict): return res.get(key) or []
    return []

def wait_panel():
    for _ in range(180):
        try:
            code, _ = req("GET", "/api/system")
            if code in (200, 401, 403): return
        except Exception: pass
        time.sleep(2)
    raise RuntimeError("panel did not come up")

TEMP_KEY_PY = """
import asyncio
from app.db.base import GetDB
from app.db.crud.temp_key import create_temp_key
async def main():
    async with GetDB() as db:
        k = await create_temp_key(db)
        print("KEY=" + k.key)
asyncio.run(main())
"""

def temp_key():
    out = subprocess.run([sys.executable, "-c", TEMP_KEY_PY], cwd="/code", capture_output=True, text=True, timeout=60)
    for line in out.stdout.splitlines():
        if line.startswith("KEY="): return line[4:].strip()
    raise RuntimeError(f"temp key failed: {out.stderr[-500:]}")

ADMIN_PW_PY = """
import asyncio, sys
from app.db.base import GetDB
from app.db.crud.admin import get_owner, get_admin
from app.models.admin import _hash_password_sync
async def main():
    mode, user, pw = sys.argv[1], sys.argv[2], sys.argv[3]
    async with GetDB() as db:
        if mode == "owner":
            o = await get_owner(db)
        else:
            o = await get_admin(db, user, load_users=False, load_usage_logs=False)
        if o is None:
            print("MISSING"); return
        o.username = user
        o.hashed_password = _hash_password_sync(pw)
        await db.commit()
        print("OK")
asyncio.run(main())
"""

def write_password(mode, user, pw):
    out = subprocess.run([sys.executable, "-c", ADMIN_PW_PY, mode, user, pw], cwd="/code",
                         capture_output=True, text=True, timeout=90)
    ok = out.stdout.strip().splitlines()[-1:] == ["OK"]
    if not ok: log(f"password write ({mode} {user}) failed:", (out.stdout + out.stderr)[-400:])
    return ok

def strong_tmp():
    import secrets
    return "Jx" + secrets.token_hex(8) + "Aa9!Zz7"

TOKEN_PY = """
import asyncio
from app.db.base import GetDB
from app.db.crud.admin import get_owner
from app.utils.jwt import create_admin_token
async def main():
    async with GetDB() as db:
        o = await get_owner(db)
        if o is None:
            print("NOOWNER"); return
        print("TOKEN=" + await create_admin_token(o.id, o.username))
asyncio.run(main())
"""

def owner_token():
    out = subprocess.run([sys.executable, "-c", TOKEN_PY], cwd="/code", capture_output=True, text=True, timeout=60)
    for line in out.stdout.splitlines():
        if line.startswith("TOKEN="): return line[6:].strip()
        if line.strip() == "NOOWNER": return None
    raise RuntimeError(f"token failed: {(out.stdout + out.stderr)[-400:]}")

MARKER = f"{DATA}/.owner_initialized"
RESELLER_MARKER = f"{DATA}/.reseller_initialized"

def ensure_owner():
    """First boot: owner = admin/admin. After that the password is YOURS: change it in the panel
    or with the owner key (API Keys page). Bootstrap never touches it again."""
    if owner_token() is None:
        code, res = req("POST", "/api/setup/owner", {"key": temp_key(), "username": "jinxowner", "password": strong_tmp()})
        if code not in (200, 201, 409): log(f"owner create failed {code}: {res}")
        if os.path.exists(MARKER): os.remove(MARKER)
    if not os.path.exists(MARKER):
        if write_password("owner", USER, PASS):
            open(MARKER, "w").write(str(int(time.time())))
            log("owner ready:", USER, "/", PASS, "(first boot)")

_owner_keys = {}            # key -> expiry time (memory only, one use, 5 minutes)
KEY_TTL = 300

def new_owner_key():
    import secrets
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"            # no 0/O/1/I: easy to read and type
    k = "JX-" + "-".join("".join(secrets.choice(alphabet) for _ in range(4)) for _ in range(3))
    now = time.time()
    for old in [x for x, exp in _owner_keys.items() if exp < now]: _owner_keys.pop(old, None)
    _owner_keys[k] = now + KEY_TTL
    return k

def use_owner_key(k):
    k = str(k or "").strip().upper()
    exp = _owner_keys.pop(k, None)
    return bool(exp and exp >= time.time())

def print_owner_key():
    k = new_owner_key()
    log("=" * 60)
    log("OWNER KEY (valid 5 min, one use):", k)
    log("login page > Forgot password? > paste the key > set a new username and password")
    log("need a new key? Restart the service in Railway")
    log("=" * 60)

def login():
    global TOKEN
    ensure_owner()
    for _ in range(30):
        tok = owner_token()
        if tok:
            TOKEN = tok; return
        time.sleep(3)
    raise RuntimeError("could not get an owner token")

def inbound(tag, proto, port, net, path):
    stream = {"network": net, "security": "none"}
    if net == "ws": stream["wsSettings"] = {"path": path}
    elif net == "httpupgrade": stream["httpupgradeSettings"] = {"path": path}
    elif net == "xhttp": stream["xhttpSettings"] = {"path": path, "mode": "auto"}
    settings = {"clients": []}
    if proto == "vless": settings["decryption"] = "none"
    return {"tag": tag, "listen": "127.0.0.1", "port": port, "protocol": proto,
            "settings": settings, "streamSettings": stream,
            "sniffing": {"enabled": True, "destOverride": ["http", "tls", "quic"], "routeOnly": True}}

CORE_CONFIG = {
    "log": {"loglevel": "warning"},
    # system resolver first (fastest inside Railway), DoH only as backup; Xray caches every answer
    "dns": {"servers": ["localhost", "https+local://1.1.1.1/dns-query", "8.8.8.8"], "queryStrategy": "UseIPv4"},
    "inbounds": [inbound(*i[:5]) for i in INBOUNDS],
    "outbounds": [
        {"protocol": "freedom", "tag": "DIRECT", "settings": {"domainStrategy": "UseIPv4"}},
        {"protocol": "blackhole", "tag": "BLOCK"},
    ],
    # AsIs: route without an extra DNS lookup = one round trip less on every new connection
    "routing": {"domainStrategy": "AsIs", "rules": [
        {"type": "field", "ip": ["geoip:private"], "outboundTag": "BLOCK"},
        {"type": "field", "protocol": ["bittorrent"], "outboundTag": "BLOCK"},
    ]},
    "policy": {"levels": {"0": {"handshake": 4, "connIdle": 300, "uplinkOnly": 1, "downlinkOnly": 1, "bufferSize": 512}}},
}

def ensure_core():
    cores = as_list(must("GET", "/api/cores"), "cores")
    for c in cores:
        if c.get("name") in (CORE_NAME, "jinx-core"):
            if c.get("name") == CORE_NAME and c.get("config") == CORE_CONFIG:
                log("core ok (unchanged)", c["id"]); return c["id"]
            body = {"name": CORE_NAME, "config": CORE_CONFIG, "exclude_inbound_tags": [], "fallbacks_inbound_tags": []}
            code, res = req("PUT", f"/api/core/{c['id']}?restart_nodes=true", body)
            if code not in (200, 201):  # node may still be starting: save config without restart
                code, res = req("PUT", f"/api/core/{c['id']}?restart_nodes=false", body)
            log("core updated" if code in (200, 201) else f"core update failed {code}: {res}", c["id"])
            return c["id"]
    c = must("POST", "/api/core", {"name": CORE_NAME, "config": CORE_CONFIG,
                                    "exclude_inbound_tags": [], "fallbacks_inbound_tags": []})
    log("core created", c["id"]); return c["id"]

def ensure_node(core_id):
    api_key = open(f"{DATA}/node_api_key").read().strip()
    cert = open(f"{DATA}/node-certs/cert.pem").read().strip()
    body = {"name": NODE_NAME, "address": "127.0.0.1", "port": 62050, "usage_coefficient": 1,
            "connection_type": "grpc", "server_ca": cert, "keep_alive": 60,
            "core_config_id": core_id, "api_key": api_key}
    for n in as_list(must("GET", "/api/nodes"), "nodes"):
        if n.get("name") in (NODE_NAME, "jinx-local"):
            must("PUT", f"/api/node/{n['id']}", body); log("node updated"); return
    must("POST", "/api/node", body); log("node created")

def ensure_groups():
    """Two groups: PRO_GROUP -> the 1 Pro config, STD_GROUP -> the other 4. Returns {"pro": id, "std": id}."""
    want = {"pro": (PRO_GROUP, [i[0] for i in INBOUNDS if i[7] == "pro"]),
            "std": (STD_GROUP, [i[0] for i in INBOUNDS if i[7] == "std"])}
    groups = as_list(must("GET", "/api/groups"), "groups")
    by_name = {g.get("name"): g for g in groups}
    if STD_GROUP not in by_name and OLD_GROUP in by_name:      # upgrade: keep users of the old group
        by_name[STD_GROUP] = by_name.pop(OLD_GROUP)
    ids = {}
    for key, (name, tags) in want.items():
        g = by_name.get(name)
        if g:
            if g.get("name") != name or sorted(g.get("inbound_tags") or []) != sorted(tags):
                must("PUT", f"/api/group/{g['id']}", {"name": name, "inbound_tags": tags}); log("group fixed:", name)
            ids[key] = g["id"]
        else:
            g = must("POST", "/api/group", {"name": name, "inbound_tags": tags}); ids[key] = g["id"]
            log("group created:", name, f"({len(tags)} config)")
    return ids

QUIET = {}

def _norm(v):
    """compare host fields the same way whether the API returns a string, a list or an enum"""
    if isinstance(v, list): return [str(x).lower() for x in v]
    if v is None: return None
    if isinstance(v, bool): return v
    return [str(v).lower()] if isinstance(v, str) and "," not in v else str(v).lower()

def ensure_hosts():
    if not DOMAIN:
        log("WARNING: no public domain yet (Settings > Networking > Generate Domain), hosts skipped"); return
    existing = as_list(must("GET", "/api/hosts"), "hosts")
    wanted = {i[0] for i in INBOUNDS}
    for h in existing:  # clean hosts left from older JinX versions
        if str(h.get("inbound_tag") or "").startswith("JX-") and h.get("inbound_tag") not in wanted:
            req("DELETE", f"/api/host/{h['id']}")
    changed = 0
    for idx, (tag, proto, port, net, path, fp, name, grp) in enumerate(INBOUNDS):
        body = {"remark": f"{name} | {TITLE}", "allowinsecure": False, "address": [DOMAIN], "inbound_tag": tag,
                "port": 443, "sni": [DOMAIN], "host": [DOMAIN], "path": path + EARLY_DATA, "security": "tls",
                "alpn": ["http/1.1"], "fingerprint": fp, "priority": idx + 1, "is_disabled": False}
        mine = [h for h in existing if h.get("inbound_tag") == tag]
        if mine:
            cur = mine[0]
            if any(_norm(cur.get(k)) != _norm(v) for k, v in body.items()):
                must("PUT", f"/api/host/{cur['id']}", {**body, "id": cur["id"]}); changed += 1
            for extra in mine[1:]:  # remove auto-created duplicates
                req("DELETE", f"/api/host/{extra['id']}")
        else:
            must("POST", "/api/host/", body); changed += 1
    if changed or not QUIET.get("hosts"): log(f"{len(INBOUNDS)} hosts ready on", DOMAIN); QUIET["hosts"] = True

def ensure_settings():
    if not DOMAIN: return
    code, s = req("GET", "/api/settings")
    if code != 200 or not isinstance(s, dict) or "subscription" not in s:
        log("settings endpoint not as expected, skipped"); return
    sub = s["subscription"]
    want = {"url_prefix": f"https://{DOMAIN}", "profile_title": TITLE, "update_interval": 12}
    if all(sub.get(k) == v for k, v in want.items()):
        if not QUIET.get("settings"): log("subscription settings ok"); QUIET["settings"] = True
        return
    sub.update(want)
    code, res = req("PUT", "/api/settings", {"subscription": sub})
    log("subscription settings", "ok" if code in (200, 201) else f"skipped ({code})")

RESELLER_ROLE = "نماینده"

def ensure_reseller_role(gids):
    """Reseller role: manages only its own users, must use the ready-made templates."""
    own = {"scope": 1}
    role = {
        "name": RESELLER_ROLE,
        "permissions": {
            "users": {"create": own, "read": own, "read_simple": own, "update": own, "delete": own,
                      "reset_usage": own, "revoke_sub": own, "activate_next_plan": own},
            "templates": {"read": True, "read_simple": True},
            "groups": {"read_simple": True},
            "system": {"read": True},
            "settings": {"read_general": True},
        },
        "access": {"require_template": True, "allowed_group_ids": sorted(gids.values())},
        "disabled_when_limited": True,
    }
    for base in ("/api/admin-role",):
        code, res = req("GET", base + "s")
        if code != 200: continue
        roles = as_list(res, "roles")
        mine = [r for r in roles if r.get("name") == RESELLER_ROLE]
        if mine:
            acc = mine[0].get("access") or {}
            if (sorted(acc.get("allowed_group_ids") or []) != role["access"]["allowed_group_ids"]
                    or acc.get("require_template") is not True):
                req("PUT", f"{base}/{mine[0]['id']}", {"access": role["access"]})
            if not QUIET.get("role"): log("reseller role ready"); QUIET["role"] = True
            return
        code, res = req("POST", base, role)
        if code in (200, 201): log("reseller role created"); return
        log(f"reseller role failed {code}: {res}"); return
    log("reseller role endpoint not found, skipped")

def role_id_by_name(name):
    code, res = req("GET", "/api/admin-roles")
    for r in as_list(res, "roles") if code == 200 else []:
        if r.get("name") == name: return r["id"]
    return None

def ensure_demo_reseller():
    """A ready reseller account (like the reseller panels): 50 GB quota, own users only."""
    if os.getenv("DEMO_RESELLER", "on").lower() in ("off", "false", "0", "no"):
        return
    if os.path.exists(RESELLER_MARKER): return      # created once; deleting it in the panel is respected
    rid = role_id_by_name(RESELLER_ROLE)
    if not rid: log("demo reseller skipped (no role)"); return
    code, _ = req("POST", "/api/admin/token", {"username": RESELLER_USER, "password": RESELLER_PASS}, form=True)
    if code == 200: open(RESELLER_MARKER, "w").write("1"); return
    code, res = req("POST", "/api/admin", {"username": RESELLER_USER, "password": strong_tmp(),
                                           "role_id": rid, "data_limit": RESELLER_GB * GB,
                                           "profile_title": TITLE})
    if code in (200, 201):
        if write_password("user", RESELLER_USER, RESELLER_PASS):
            open(RESELLER_MARKER, "w").write("1"); log("demo reseller ready:", RESELLER_USER)
    elif code == 409:
        open(RESELLER_MARKER, "w").write("1")   # already exists with its own password
    else:
        log(f"demo reseller failed {code}: {res}")

def ensure_templates(gids):
    have = {t.get("name"): t for t in as_list(must("GET", "/api/user_templates"), "templates")}
    for name, gb, days, grp in TEMPLATES:
        body = {"name": name, "data_limit": gb * GB, "expire_duration": days * DAY, "group_ids": [gids[grp]],
                "status": "active", "data_limit_reset_strategy": "no_reset"}
        if name in have:
            if have[name].get("group_ids") != [gids[grp]]: req("PUT", f"/api/user_template/{have[name]['id']}", body)
        else:
            must("POST", "/api/user_template", body); QUIET["tpl"] = False
    if not QUIET.get("tpl"): log("user templates ready"); QUIET["tpl"] = True

def remove_demo_user():
    """Users list is 100% yours: this panel NEVER creates users. It only deletes the 50 GB test user
    that very old versions made automatically, if it is still there."""
    for name in OLD_TEST_USERS:
        code, u = req("GET", f"/api/user/{name}")
        if code == 200 and isinstance(u, dict):
            c, _ = req("DELETE", f"/api/user/{name}")
            log("removed old auto-created test user", name) if c in (200, 204) else log(f"could not remove {name}: {c}")

def attach_orphans(gids):
    """Users created without a group are put in the 𝗝𝗶𝗻𝗫 group (4 configs). Users with a group are never touched."""
    code, res = req("GET", "/api/users?no_group=true&limit=200")
    if code == 401:
        login(); code, res = req("GET", "/api/users?no_group=true&limit=200")
    if code != 200: return
    for u in as_list(res, "users"):
        # only touch users the API clearly reports as having NO group (never move Pro users)
        if not isinstance(u, dict) or "group_ids" not in u or u.get("group_ids"): continue
        c, r = req("PUT", f"/api/user/{u['username']}", {"group_ids": [gids["std"]]})
        log(f"no group picked for {u['username']} -> {STD_GROUP}" if c == 200 else f"attach {u['username']} failed {c}: {r}")

def heal_node(state):
    """Self-healing: if the built-in core is not connected twice in a row, restart it."""
    code, res = req("GET", "/api/nodes")
    if code == 401: login(); code, res = req("GET", "/api/nodes")
    if code != 200: return
    for n in as_list(res, "nodes"):
        if n.get("name") != NODE_NAME: continue
        st = str(n.get("status") or "")
        if st in ("connected", "disabled"):
            state["bad"] = 0; return
        state["bad"] = state.get("bad", 0) + 1
        if state["bad"] >= 2:
            log(f"core status '{st}' -> auto-restart")
            c, _ = req("POST", f"/api/core/{n.get('core_config_id')}/restart")
            if c not in (200, 204):
                try: ensure_node(n.get("core_config_id"))
                except Exception as e: log("node reconnect failed:", e)
            state["bad"] = 0
        return

def restart_panel(reason):
    """Last resort: stop the panel process; the container restarts it cleanly (all data stays on the volume)."""
    mark = f"{DATA}/.doctor_restart"
    try:
        if time.time() - os.path.getmtime(mark) < 3600:
            log("doctor: panel already restarted in the last hour, waiting ->", reason); return
    except OSError: pass
    open(mark, "w").write(reason)
    log("doctor: restarting the panel ->", reason)
    me = os.getpid()
    for pid in os.listdir("/proc"):
        if not pid.isdigit() or int(pid) == me: continue
        try:
            cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="ignore")
        except Exception: continue
        if "main.py" in cmd and "python" in cmd:
            try: os.kill(int(pid), 15)
            except Exception: pass

def check_sub(state):
    """Doctor: open a real subscription link like a customer would. 3 server errors in a row -> restart panel."""
    code, res = req("GET", "/api/users?limit=1")
    if code == 401: login(); code, res = req("GET", "/api/users?limit=1")
    users = as_list(res, "users") if code == 200 else []
    url = (users[0].get("subscription_url") or "") if users and isinstance(users[0], dict) else ""
    if not url: state["sub_bad"] = 0; return                # no users yet: nothing to test
    path = "/" + url.split("://", 1)[-1].split("/", 1)[-1] if "://" in url else url
    try:
        with urllib.request.urlopen(urllib.request.Request(BASE + path, headers={"User-Agent": "Mozilla/5.0 JinX-Doctor"}), timeout=20) as r:
            ok = r.status < 500
    except urllib.error.HTTPError as e: ok = e.code < 500
    except Exception: ok = False
    if ok:
        if state.get("sub_bad"): log("doctor: subscription pages are fine again")
        state["sub_bad"] = 0; return
    state["sub_bad"] = state.get("sub_bad", 0) + 1
    log(f"doctor: subscription page error ({state['sub_bad']}/3)")
    if state["sub_bad"] >= 3:
        state["sub_bad"] = 0; restart_panel("subscription pages keep failing")

def watch(gids):
    """Doctor loop (every 15 s tick): finds problems and fixes them on its own.
    - core/node not connected            -> restart core, reconnect node      (every 1 min)
    - a group deleted or changed          -> re-created / fixed                (every 1 min)
    - hosts, subscription settings, templates, reseller role changed -> fixed (every 5 min)
    - subscription links return errors    -> panel restarted cleanly           (every 5 min)"""
    log("doctor on: self-heal core, groups, hosts, subscription, templates")
    state, i = {}, 0
    def regroup():
        new = ensure_groups()
        if new: gids.update(new)
    jobs = ((lambda: attach_orphans(gids), 1), (lambda: heal_node(state), 4), (regroup, 4),
            (ensure_hosts, 20), (ensure_settings, 20), (lambda: ensure_templates(gids), 20),
            (lambda: ensure_reseller_role(gids), 20), (lambda: check_sub(state), 20))
    while True:
        for job, every in jobs:
            if i % every == 0:
                try: job()
                except Exception as e: log("doctor:", e)
        i += 1
        time.sleep(15)

# ---------------- owner key service (POST /jinx/key, used by the "API Keys" page) ----------------
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
_attempts = {}

class KeyHandler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body):
        data = json.dumps(body, ensure_ascii=False).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store"); self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def do_GET(self): self._send(405, {"detail": "use POST"})
    def do_POST(self):
        route = self.path.split("?")[0].rstrip("/")
        if route not in ("/jinx/key", "/jinx/password", "/jinx/reset"): return self._send(404, {"detail": "not found"})
        try: body = json.loads(self.rfile.read(min(int(self.headers.get("Content-Length") or 0), 4096)) or b"{}") or {}
        except Exception: body = {}
        if not isinstance(body, dict): body = {}
        if route == "/jinx/reset":
            try: return reset_with_key(self, body)
            except Exception as e:
                log("owner reset error:", e); return self._send(500, {"detail": "خطای داخلی، دوباره امتحان کن"})
        if route == "/jinx/password":
            try: return change_password(self, body)
            except Exception as e:
                log("password change error:", e); return self._send(500, {"detail": "خطای داخلی، دوباره امتحان کن"})
        token = None
        auth = self.headers.get("Authorization", "")
        if auth.lower().startswith("bearer ") and not body.get("username"):
            token = auth[7:].strip()                     # already logged in to the panel
        else:
            ip = (self.headers.get("X-Real-IP") or self.client_address[0]).strip()
            now = time.time(); hist = [t for t in _attempts.get(ip, []) if now - t < 600]
            if len(hist) >= 5: return self._send(429, {"detail": "تلاش زیاد بود، ۱۰ دقیقه دیگه امتحان کن"})
            u, p = str(body.get("username", ""))[:64], str(body.get("password", ""))[:128]
            if not u or not p: return self._send(401, {"detail": "یوزر و رمز مالک رو وارد کن"})
            code, res = req_anon("POST", "/api/admin/token", {"username": u, "password": p}, form=True)
            if code != 200:
                hist.append(now); _attempts[ip] = hist
                return self._send(401, {"detail": "یوزر یا رمز اشتباهه"})
            token = (res or {}).get("access_token") if isinstance(res, dict) else None
            if not token: return self._send(401, {"detail": "یوزر یا رمز اشتباهه"})
        code, me = req_anon("GET", "/api/admin", token=token)
        if code != 200: return self._send(401, {"detail": "دوباره وارد پنل شو"})
        if not ((me or {}).get("role") or {}).get("is_owner"):
            return self._send(403, {"detail": "فقط مالک پنل می‌تونه کلید بگیره"})
        key = new_owner_key()
        if len(_attempts) > 1000: _attempts.clear()
        log("owner key issued from API Keys page for", me.get("username"))
        self._send(200, {"key": key, "ttl": KEY_TTL})

_pw_lock = threading.Lock()

def change_password(handler, body):
    """Settings > Change password. POST /jinx/password {username, current, new}.
    Needs the account's CURRENT username + password (checked by the panel itself), rate limited per IP.
    Works for the owner and for resellers, each for their own account."""
    ip = (handler.headers.get("X-Real-IP") or handler.client_address[0]).strip()
    now = time.time(); hist = [t for t in _attempts.get(ip, []) if now - t < 600]
    if len(hist) >= 5: return handler._send(429, {"detail": "تلاش زیاد بود، ۱۰ دقیقه دیگه امتحان کن"})
    user = str(body.get("username", "")).strip()[:64]
    cur, new = str(body.get("current", ""))[:128], str(body.get("new", ""))[:128]
    if not user or not cur: return handler._send(400, {"detail": "نام کاربری و رمز فعلی رو وارد کن"})
    if len(new) < 4 or not new.strip(): return handler._send(400, {"detail": "رمز جدید حداقل ۴ کاراکتر باشه"})
    if new == cur: return handler._send(400, {"detail": "رمز جدید با رمز فعلی یکیه"})
    code, res = req_anon("POST", "/api/admin/token", {"username": user, "password": cur}, form=True)
    token = res.get("access_token") if (code == 200 and isinstance(res, dict)) else None
    if not token:
        hist.append(now); _attempts[ip] = hist
        return handler._send(401, {"detail": "نام کاربری یا رمز فعلی اشتباهه"})
    code, me = req_anon("GET", "/api/admin", token=token)
    if code != 200 or not isinstance(me, dict): return handler._send(500, {"detail": "اطلاعات اکانت پیدا نشد، دوباره امتحان کن"})
    name = me.get("username") or user
    mode = "owner" if ((me.get("role") or {}).get("is_owner")) else "user"
    with _pw_lock:
        if not write_password(mode, name, new):
            return handler._send(500, {"detail": "ذخیره‌ی رمز ممکن نشد، دوباره امتحان کن"})
    c2, _ = req_anon("POST", "/api/admin/token", {"username": name, "password": new}, form=True)   # double check
    if c2 != 200:
        log("password change: verify failed for", name)
        return handler._send(500, {"detail": "رمز ذخیره شد ولی تأیید نشد، یک بار با رمز جدید وارد شو"})
    _attempts.pop(ip, None)
    log("password changed from Settings for", name)
    handler._send(200, {"ok": True, "username": name})

def reset_with_key(handler, body):
    """Login page > Forgot password. POST /jinx/reset {key, username, password}: one-time owner key -> new owner login."""
    ip = (handler.headers.get("X-Real-IP") or handler.client_address[0]).strip()
    now = time.time(); hist = [t for t in _attempts.get(ip, []) if now - t < 600]
    if len(hist) >= 5: return handler._send(429, {"detail": "تلاش زیاد بود، ۱۰ دقیقه دیگه امتحان کن"})
    key = str(body.get("key", "")).strip()[:40]
    user = str(body.get("username", "")).strip()[:32]
    pw = str(body.get("password", ""))[:128]
    if not key: return handler._send(400, {"detail": "کلید مالک رو وارد کن"})
    if len(user) < 3 or not all(ch.isalnum() or ch in "_.-" for ch in user):
        return handler._send(400, {"detail": "نام کاربری حداقل ۳ حرف باشه (حروف انگلیسی، عدد، _ . -)"})
    if len(pw) < 4 or not pw.strip(): return handler._send(400, {"detail": "رمز جدید حداقل ۴ کاراکتر باشه"})
    if not use_owner_key(key):
        hist.append(now); _attempts[ip] = hist
        return handler._send(401, {"detail": "کلید اشتباهه یا منقضی شده، کلید تازه بگیر"})
    with _pw_lock:
        if not write_password("owner", user, pw):
            return handler._send(500, {"detail": "ذخیره نشد. شاید این نام کاربری مال یک نماینده‌ست، یکی دیگه انتخاب کن"})
    c2, _ = req_anon("POST", "/api/admin/token", {"username": user, "password": pw}, form=True)
    if c2 != 200:
        log("owner reset: verify failed for", user)
        return handler._send(500, {"detail": "ذخیره شد ولی تأیید نشد، یک بار با اطلاعات جدید وارد شو"})
    _attempts.pop(ip, None)
    log("owner login reset with owner key ->", user)
    handler._send(200, {"ok": True, "username": user})

def req_anon(method, path, body=None, form=False, token=None):
    return req(method, path, body, form=form, token=token)  # thread-safe: never touches the global token

def start_key_service():
    srv = ThreadingHTTPServer(("127.0.0.1", 8100), KeyHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    log("owner key (API Keys page) and password change (Settings page) ready")

def step(name, fn, *a):
    try: return fn(*a)
    except Exception as e: log(f"{name} failed: {e}")

def main():
    wait_panel(); login(); print_owner_key()
    step("key service", start_key_service)
    core_id = ensure_core()
    time.sleep(2)
    step("node", ensure_node, core_id)
    gid = None
    for _ in range(10):  # inbounds appear after the core is saved
        gid = step("groups", ensure_groups)
        if gid: break
        time.sleep(3)
    if not gid: raise RuntimeError("groups could not be created")
    step("hosts", ensure_hosts)
    step("settings", ensure_settings)
    step("templates", ensure_templates, gid)
    step("reseller role", ensure_reseller_role, gid)
    step("demo reseller", ensure_demo_reseller)
    step("clean users", remove_demo_user)
    log("DONE ->", f"https://{DOMAIN}/dashboard/" if DOMAIN else "generate a Railway domain")
    watch(gid)

if __name__ == "__main__":
    try: main()
    except Exception as e: log("FATAL", e); sys.exit(1)
