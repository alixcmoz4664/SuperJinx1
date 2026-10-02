/* Super JinX dashboard add-on
   1) Sidebar shows only: Dashboard, Users, API Keys, Templates, Bulk Actions, Settings, Support
      (+ Admins for the owner only, to create resellers).
   2) The "API Keys" page gets a small built-in section to get the 5-minute owner key
      (no new menu items, no extra buttons in the sidebar).
   3) The "Settings" page gets a "Change password" card (current username + password -> new password). */
(function () {
  "use strict";
  function norm(t) { return String(t || "").replace(/[\u200c\s]+/g, " ").trim().toLowerCase(); }

  /* ---------- 1) sidebar filter ---------- */
  var HIDE = [
    "نودها", "نود", "Nodes", "Node",
    "هاست‌ها", "هاست ها", "هاستها", "میزبان‌ها", "Hosts", "Host Settings",
    "هسته‌ها", "هسته", "پیکربندی هسته", "تنظیمات هسته", "Cores", "Core", "Core Settings", "Core Config",
    "گروه‌ها", "گروه ها", "گروهها", "Groups",
    "نقش‌ها", "نقش ها", "Roles", "Admin Roles",
    "آمار", "Statistics", "Stats"
  ].map(norm);
  /* "Admins" is only for the owner (to create resellers); resellers never see it */
  var ADMINS = ["مدیران", "ادمین‌ها", "ادمین ها", "Admins", "Admin"].map(norm);
  var OWNER = null, askedFor = null, busy = false;
  function whoAmI() {                      /* asks once per login token, never spams the API */
    var t = findToken();
    if (!t) { OWNER = null; askedFor = null; return; }
    if (t === askedFor || busy) return;
    busy = true;
    fetch("/api/admin", { headers: { Authorization: "Bearer " + t } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (me) {
        busy = false; askedFor = t;
        OWNER = me ? !!(me.role && me.role.is_owner) : null;   /* expired token: unknown, not "reseller" */
        schedule();
      })
      .catch(function () { busy = false; setTimeout(schedule, 30000); });
  }
  function hidden(txt) { return HIDE.indexOf(txt) > -1 || (ADMINS.indexOf(txt) > -1 && OWNER !== true); }
  function sweep() {
    whoAmI();
    var nodes = document.querySelectorAll('aside a, aside button, nav a, nav button, [data-sidebar="menu-button"], [data-sidebar="menu-sub-button"]');
    for (var i = 0; i < nodes.length; i++) {
      var item = nodes[i].closest('[data-sidebar="menu-sub-item"], [data-sidebar="menu-item"], li') || nodes[i];
      var want = hidden(norm(nodes[i].textContent)) ? "none" : "";
      if (item.dataset.jx === "1" || want) { if (item.style.display !== want) item.style.display = want; item.dataset.jx = "1"; }
    }
  }

  /* ---------- 2) owner key inside "API Keys" ---------- */
  var TITLES = ["کلیدهای api", "کلید های api", "api keys", "api key"].map(norm);
  function apiKeysHeading() {
    if (!/api[-_]?key/i.test(location.pathname + location.hash)) {
      var hs = document.querySelectorAll("main h1, main h2, h1, h2");
      for (var i = 0; i < hs.length; i++) if (TITLES.indexOf(norm(hs[i].textContent)) > -1) return hs[i];
      return null;
    }
    return document.querySelector("main h1, main h2, h1, h2") || document.querySelector("main") || null;
  }
  function findToken() {
    var jwt = /(eyJ[\w-]+\.[\w-]+\.[\w-]+)/, stores = [];
    try { stores.push(localStorage); } catch (e) {}
    try { stores.push(sessionStorage); } catch (e) {}
    for (var s = 0; s < stores.length; s++) {
      for (var i = 0; i < stores[s].length; i++) {
        var m = jwt.exec(String(stores[s].getItem(stores[s].key(i)) || ""));
        if (m) return m[1];
      }
    }
    var c = jwt.exec(document.cookie || ""); return c ? c[1] : null;
  }
  function fa(n) { return String(n).replace(/[0-9]/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹"[d]; }); }
  /* same card look as the PasarGuard dashboard (uses its theme colors, light and dark) */
  var KCSS = ".jx-k{margin:0 0 20px;border:1px solid hsl(var(--border,240 5.9% 90%));border-radius:calc(var(--radius,.5rem) + 4px);background:hsl(var(--card,0 0% 100%));color:hsl(var(--card-foreground,240 10% 3.9%));box-shadow:0 1px 2px rgba(0,0,0,.05);font:inherit}" +
    ".jx-k .h{padding:20px 20px 0;display:flex;align-items:flex-start;gap:14px;flex-wrap:wrap}.jx-k .t{flex:1;min-width:200px}" +
    ".jx-k .t b{display:block;font-size:16px;font-weight:600;line-height:1.4}.jx-k .t small{display:block;margin-top:4px;font-size:13px;line-height:1.7;color:hsl(var(--muted-foreground,240 3.8% 46.1%))}" +
    ".jx-k .p{padding:16px 20px 20px}" +
    ".jx-k .btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:40px;padding:0 18px;border-radius:var(--radius,.5rem);cursor:pointer;font:inherit;font-size:14px;font-weight:500;white-space:nowrap;transition:opacity .15s,background .15s}" +
    ".jx-k .btn.pri{border:0;background:hsl(var(--primary,240 5.9% 10%));color:hsl(var(--primary-foreground,0 0% 98%))}" +
    ".jx-k .btn.out{border:1px solid hsl(var(--input,240 5.9% 90%));background:transparent;color:inherit}.jx-k .btn.out:hover{background:hsl(var(--accent,240 4.8% 95.9%))}" +
    ".jx-k .btn.pri:hover{opacity:.9}.jx-k .btn:focus-visible{outline:none;box-shadow:0 0 0 2px hsl(var(--background,0 0% 100%)),0 0 0 4px hsl(var(--ring,240 5% 64.9%))}.jx-k .btn:disabled{opacity:.55;cursor:default}.jx-k .btn svg{width:16px;height:16px}" +
    ".jx-k .key{display:none;margin-top:4px}.jx-k .key.on{display:block}" +
    ".jx-k .row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}" +
    ".jx-k .val{flex:1;min-width:220px;height:40px;display:flex;align-items:center;padding:0 12px;border-radius:var(--radius,.5rem);border:1px solid hsl(var(--input,240 5.9% 90%));background:hsl(var(--muted,240 4.8% 95.9%));font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:14px;font-weight:600;letter-spacing:.02em;direction:ltr;user-select:all;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}" +
    ".jx-k .bar{height:4px;border-radius:9px;background:hsl(var(--muted,240 4.8% 95.9%));overflow:hidden;margin-top:12px}.jx-k .bar i{display:block;height:100%;width:100%;background:hsl(var(--primary,240 5.9% 10%));transition:width .5s linear}" +
    ".jx-k .meta{display:flex;justify-content:space-between;gap:10px;margin-top:6px;font-size:12px;color:hsl(var(--muted-foreground,240 3.8% 46.1%))}" +
    ".jx-k .f{display:none;gap:12px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));align-items:end;margin-top:4px}.jx-k .f.on{display:grid}" +
    ".jx-k label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:500}" +
    ".jx-k input{height:40px;padding:0 12px;border-radius:var(--radius,.5rem);border:1px solid hsl(var(--input,240 5.9% 90%));background:transparent;color:inherit;font:inherit;font-size:14px;direction:ltr;text-align:left;outline:none}" +
    ".jx-k input:focus{border-color:hsl(var(--ring,240 5% 64.9%));box-shadow:0 0 0 3px hsl(var(--ring,240 5% 64.9%) / .25)}" +
    ".jx-k .m{display:none;margin-top:10px;font-size:13px}.jx-k .m.bad{display:block;color:hsl(var(--destructive,0 84.2% 60.2%))}.jx-k .m.good{display:block;color:#16a34a}";
  var I_KEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/></svg>';
  var I_COPY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/></svg>';
  var I_RE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12a8 8 0 1 1-2.35-5.65M20 4v5h-5"/></svg>';
  function mount() {
    var old = document.getElementById("jx-owner-key");
    if (OWNER === false) { if (old) old.remove(); return; }   /* resellers don't see the owner key */
    if (old) return;
    var h = apiKeysHeading(); if (!h) return;
    if (!document.getElementById("jx-k-css")) { var st = document.createElement("style"); st.id = "jx-k-css"; st.textContent = KCSS; document.head.appendChild(st); }
    var box = document.createElement("section"); box.id = "jx-owner-key"; box.className = "jx-k"; box.dir = "rtl";
    box.innerHTML = '<div class="h"><div class="t"><b>کلید ۵ دقیقه‌ای مالک</b><small>برای بازیابی ورود مالک: کلید بگیر، از پنل خارج شو و توی صفحه‌ی ورود «رمز رو فراموش کردی؟» رو بزن. برای تغییر عادی رمز از «تنظیمات» استفاده کن.</small></div>' +
      '<button type="button" class="btn pri g">' + I_KEY + '<span>دریافت کلید</span></button></div>' +
      '<div class="p"><div class="key"><div class="row"><div class="val" title="کلید"></div><button type="button" class="btn out c">' + I_COPY + '<span>کپی کلید</span></button></div>' +
      '<div class="bar"><i></i></div><div class="meta"><span class="l"></span><span>یک‌بار مصرف</span></div></div>' +
      '<form class="f" onsubmit="return false"><label>نام کاربری مالک<input name="u" autocomplete="username" spellcheck="false" autocapitalize="off"></label>' +
      '<label>رمز عبور مالک<input name="p" type="password" autocomplete="current-password"></label><button type="button" class="btn pri ok">تأیید و دریافت کلید</button></form>' +
      '<div class="m"></div></div>';
    var anchor = h.closest("header") || h.parentElement || h;
    if (anchor.parentNode) anchor.parentNode.insertBefore(box, anchor.nextSibling); else return;
    var get = box.querySelector(".g"), getT = get.querySelector("span"), form = box.querySelector(".f"), okb = form.querySelector(".ok"),
        keyBox = box.querySelector(".key"), val = box.querySelector(".val"), cp = box.querySelector(".c"), cpT = cp.querySelector("span"),
        bar = box.querySelector(".bar i"), lab = box.querySelector(".l"), m = box.querySelector(".m"), timer, cur = "";
    function say(cls, t) { m.className = "m " + cls; m.textContent = t; }
    function busy(on) { get.disabled = okb.disabled = on; getT.textContent = on ? "در حال ساخت…" : (cur ? "کلید تازه" : "دریافت کلید"); }
    function request(body, token) {
      say("", ""); busy(true);
      var hd = { "Content-Type": "application/json" }; if (token) hd.Authorization = "Bearer " + token;
      fetch("/jinx/key", { method: "POST", headers: hd, body: JSON.stringify(body || {}), credentials: "same-origin" })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return [r.status, j]; }); })
        .then(function (x) {
          busy(false);
          if (x[0] === 200 && x[1].key) return show(x[1]);
          if (x[0] === 401 && !body) { form.classList.add("on"); form.u.focus(); return say("", ""); }
          say("bad", (x[1] && x[1].detail) || "خطا، دوباره امتحان کن");
        })
        .catch(function () { busy(false); say("bad", "ارتباط با سرور برقرار نشد"); });
    }
    function show(j) {
      form.classList.remove("on"); form.reset(); cur = j.key; val.textContent = j.key; keyBox.classList.add("on");
      get.innerHTML = I_RE + "<span>کلید تازه</span>"; getT = get.querySelector("span");
      var ttl = (j.ttl || 300) * 1000, end = Date.now() + ttl;
      clearInterval(timer);
      function upd() {
        var left = Math.max(0, end - Date.now()), s = Math.round(left / 1000);
        bar.style.width = (left / ttl * 100) + "%";
        if (s) { lab.textContent = "اعتبار " + fa(Math.floor(s / 60) + ":" + ("0" + s % 60).slice(-2)); val.style.opacity = ""; return; }
        lab.textContent = "منقضی شد، کلید تازه بگیر"; val.style.opacity = ".45"; cur = ""; clearInterval(timer);
      }
      upd(); timer = setInterval(upd, 500);
      say("good", "کلید ساخته شد.");
    }
    function copyKey() {
      if (!cur) return say("bad", "کلید منقضی شده، کلید تازه بگیر");
      function done() { cpT.textContent = "کپی شد"; setTimeout(function () { cpT.textContent = "کپی کلید"; }, 1500); }
      try {
        if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(cur).then(done, fallback);
      } catch (e) {}
      fallback();
      function fallback() { var r = document.createRange(); r.selectNodeContents(val); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); try { document.execCommand("copy"); done(); } catch (e) { say("bad", "کلید رو انتخاب و دستی کپی کن"); } }
    }
    get.onclick = function () { request(null, findToken()); };
    okb.onclick = function () { var u = form.u.value.trim(), p = form.p.value; if (!u || !p) return say("bad", "نام کاربری و رمز مالک رو وارد کن"); request({ username: u, password: p }); };
    form.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); okb.click(); } });
    cp.onclick = copyKey;
  }

  /* ---------- 3) Settings > change password (looks like the PasarGuard cards) ---------- */
  var PCSS = ".jx-pw{margin:0 0 20px;border:1px solid hsl(var(--border,240 5.9% 90%));border-radius:calc(var(--radius,.5rem) + 4px);background:hsl(var(--card,0 0% 100%));color:hsl(var(--card-foreground,240 10% 3.9%));box-shadow:0 1px 2px rgba(0,0,0,.05);font:inherit}" +
    ".jx-pw .h{padding:20px 20px 4px}.jx-pw .h b{display:block;font-size:16px;font-weight:600;line-height:1.4}.jx-pw .h small{display:block;margin-top:4px;font-size:13px;color:hsl(var(--muted-foreground,240 3.8% 46.1%))}" +
    ".jx-pw .b{padding:16px 20px 20px;display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}" +
    ".jx-pw label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:500}" +
    ".jx-pw input{height:40px;padding:0 12px;border-radius:var(--radius,.5rem);border:1px solid hsl(var(--input,240 5.9% 90%));background:transparent;color:inherit;font:inherit;font-size:14px;direction:ltr;text-align:left;outline:none;transition:box-shadow .15s,border-color .15s}" +
    ".jx-pw input:focus{border-color:hsl(var(--ring,240 5% 64.9%));box-shadow:0 0 0 3px hsl(var(--ring,240 5% 64.9%) / .25)}" +
    ".jx-pw .f{padding:0 20px 20px;display:flex;align-items:center;gap:12px;flex-wrap:wrap}" +
    ".jx-pw button{height:40px;padding:0 18px;border:0;border-radius:var(--radius,.5rem);cursor:pointer;font:inherit;font-size:14px;font-weight:500;background:hsl(var(--primary,240 5.9% 10%));color:hsl(var(--primary-foreground,0 0% 98%));transition:opacity .15s}" +
    ".jx-pw button:hover{opacity:.9}.jx-pw button:focus-visible{outline:none;box-shadow:0 0 0 2px hsl(var(--background,0 0% 100%)),0 0 0 4px hsl(var(--ring,240 5% 64.9%))}.jx-pw button:disabled{opacity:.55;cursor:default}.jx-pw .m{font-size:13px}.jx-pw .m.bad{color:hsl(var(--destructive,0 84.2% 60.2%))}.jx-pw .m.good{color:#16a34a}";
  function settingsHeading() {
    var words = ["تنظیمات", "settings", "تنظیمات عمومی", "general settings", "general"].map(norm);
    var hs = document.querySelectorAll("main h1, main h2, h1, h2");
    for (var i = 0; i < hs.length; i++) if (words.indexOf(norm(hs[i].textContent)) > -1) return hs[i];
    if (/\/settings(\/|$|\?|#)/i.test(location.pathname + location.hash)) return document.querySelector("main h1, main h2, h1, h2");
    return null;
  }
  function logout() {
    var jwt = /eyJ[\w-]+\.[\w-]+\.[\w-]+/, stores = [];
    try { stores.push(localStorage); } catch (e) {}
    try { stores.push(sessionStorage); } catch (e) {}
    stores.forEach(function (st) { for (var i = st.length - 1; i >= 0; i--) { var k = st.key(i); if (jwt.test(String(st.getItem(k) || ""))) st.removeItem(k); } });
    location.href = "/dashboard/";
  }
  function mountPass() {
    if (document.getElementById("jx-pass")) return;
    var h = settingsHeading(); if (!h) return;
    var anchor = h.closest("header") || h.parentElement || h; if (!anchor.parentNode) return;
    if (!document.getElementById("jx-pw-css")) { var st = document.createElement("style"); st.id = "jx-pw-css"; st.textContent = PCSS; document.head.appendChild(st); }
    var box = document.createElement("section"); box.id = "jx-pass"; box.className = "jx-pw"; box.dir = "rtl";
    box.innerHTML = '<div class="h"><b>تغییر رمز عبور</b><small>نام کاربری و رمز فعلی رو وارد کن و رمز جدید رو بذار. بعد از ثبت، از این به بعد با رمز جدید وارد پنل میشی.</small></div>' +
      '<form class="b" autocomplete="off" onsubmit="return false">' +
      '<label>نام کاربری فعلی<input name="u" autocomplete="username" spellcheck="false" autocapitalize="off"></label>' +
      '<label>رمز عبور فعلی<input name="c" type="password" autocomplete="current-password"></label>' +
      '<label>رمز عبور جدید<input name="n" type="password" autocomplete="new-password"></label>' +
      '<label>تکرار رمز عبور جدید<input name="r" type="password" autocomplete="new-password"></label></form>' +
      '<div class="f"><button type="button">ثبت رمز جدید</button><span class="m"></span></div>';
    anchor.parentNode.insertBefore(box, anchor.nextSibling);
    var f = box.querySelector("form"), btn = box.querySelector("button"), m = box.querySelector(".m");
    function say(cls, t) { m.className = "m " + cls; m.textContent = t; }
    function submit() {
      var u = f.u.value.trim(), c = f.c.value, n = f.n.value, r = f.r.value;
      if (!u || !c) return say("bad", "نام کاربری و رمز فعلی رو وارد کن");
      if (n.length < 4 || !n.trim()) return say("bad", "رمز جدید حداقل ۴ کاراکتر باشه");
      if (n !== r) return say("bad", "تکرار رمز جدید با خودش یکی نیست");
      if (n === c) return say("bad", "رمز جدید با رمز فعلی یکیه");
      btn.disabled = true; say("", "در حال ثبت…");
      fetch("/jinx/password", { method: "POST", headers: { "Content-Type": "application/json" }, credentials: "same-origin",
        body: JSON.stringify({ username: u, current: c, new: n }) })
        .then(function (res) { return res.json().catch(function () { return {}; }).then(function (j) { return [res.status, j]; }); })
        .then(function (x) {
          if (x[0] === 200) { f.reset(); say("good", "رمز عوض شد. چند لحظه دیگه با رمز جدید وارد شو…"); setTimeout(logout, 2500); return; }
          btn.disabled = false; say("bad", (x[1] && x[1].detail) || "خطا، دوباره امتحان کن");
        })
        .catch(function () { btn.disabled = false; say("bad", "ارتباط با سرور برقرار نشد"); });
    }
    btn.onclick = submit;
    f.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); submit(); } });
  }


  /* ---------- 4) Login page > "Forgot password?" (owner key -> new owner username + password) ---------- */
  function loginForm() {
    if (document.querySelector('[data-sidebar], aside')) return null;            /* inside the dashboard: not the login page */
    var pw = document.querySelector('form input[type="password"]'); if (!pw) return null;
    var f = pw.closest("form"); if (!f || f.closest(".jx-k, .jx-pw")) return null;
    return f;
  }
  function mountReset() {
    var f = loginForm(); if (!f || document.getElementById("jx-reset-link")) return;
    if (!document.getElementById("jx-k-css")) { var st = document.createElement("style"); st.id = "jx-k-css"; st.textContent = KCSS; document.head.appendChild(st); }
    var wrap = document.createElement("div"); wrap.id = "jx-reset-link"; wrap.dir = "rtl"; wrap.style.cssText = "margin-top:14px;text-align:center";
    wrap.innerHTML = '<button type="button" class="jx-k-link" style="background:none;border:0;padding:4px;cursor:pointer;font:inherit;font-size:13px;color:hsl(var(--muted-foreground,240 3.8% 46.1%));text-decoration:underline;text-underline-offset:4px">رمز رو فراموش کردی؟ ورود با کلید مالک</button>';
    f.parentNode.insertBefore(wrap, f.nextSibling);
    var card = document.createElement("section"); card.className = "jx-k"; card.dir = "rtl"; card.style.cssText = "display:none;margin:14px 0 0;text-align:right";
    card.innerHTML = '<div class="h"><div class="t"><b>بازیابی ورود مالک</b><small>کلید رو از «کلیدهای API» یا از خط OWNER KEY توی لاگ Railway بردار (بعد از Restart). کلید ۵ دقیقه اعتبار داره و یک‌بار مصرفه.</small></div></div>' +
      '<div class="p"><form class="f on" onsubmit="return false" style="grid-template-columns:1fr">' +
      '<label>کلید مالک<input name="k" placeholder="JX-XXXX-XXXX-XXXX" autocomplete="one-time-code" spellcheck="false" autocapitalize="characters"></label>' +
      '<label>نام کاربری جدید<input name="u" value="admin" autocomplete="username" spellcheck="false" autocapitalize="off"></label>' +
      '<label>رمز عبور جدید<input name="p" type="password" autocomplete="new-password"></label>' +
      '<label>تکرار رمز عبور جدید<input name="r" type="password" autocomplete="new-password"></label>' +
      '<button type="button" class="btn pri ok">ثبت و ورود با اطلاعات جدید</button></form><div class="m"></div></div>';
    wrap.appendChild(card);
    var form = card.querySelector("form"), ok = card.querySelector(".ok"), m = card.querySelector(".m");
    function say(cls, t) { m.className = "m " + cls; m.textContent = t; }
    wrap.querySelector(".jx-k-link").onclick = function () { card.style.display = card.style.display === "none" ? "block" : "none"; if (card.style.display === "block") form.k.focus(); };
    ok.onclick = function () {
      var k = form.k.value.trim().toUpperCase(), u = form.u.value.trim(), p = form.p.value, r = form.r.value;
      if (!k) return say("bad", "کلید مالک رو وارد کن");
      if (u.length < 3 || !/^[A-Za-z0-9_.-]+$/.test(u)) return say("bad", "نام کاربری حداقل ۳ حرف انگلیسی یا عدد باشه");
      if (p.length < 4 || !p.trim()) return say("bad", "رمز جدید حداقل ۴ کاراکتر باشه");
      if (p !== r) return say("bad", "تکرار رمز جدید با خودش یکی نیست");
      ok.disabled = true; say("", "");
      fetch("/jinx/reset", { method: "POST", headers: { "Content-Type": "application/json" }, credentials: "same-origin", body: JSON.stringify({ key: k, username: u, password: p }) })
        .then(function (res) { return res.json().catch(function () { return {}; }).then(function (j) { return [res.status, j]; }); })
        .then(function (x) {
          ok.disabled = false;
          if (x[0] === 200) {
            say("good", "انجام شد. حالا با «" + u + "» و رمز جدید وارد شو.");
            var uIn = f.querySelector('input:not([type="password"])'), pIn = f.querySelector('input[type="password"]');
            form.reset(); form.u.value = u;
            setTimeout(function () { card.style.display = "none"; if (uIn) uIn.focus(); }, 2200);
            return;
          }
          say("bad", (x[1] && x[1].detail) || "خطا، دوباره امتحان کن");
        })
        .catch(function () { ok.disabled = false; say("bad", "ارتباط با سرور برقرار نشد"); });
    };
    form.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); ok.click(); } });
  }

  /* ---------- run + keep up with page changes ---------- */
  var queued = false;
  function tick() { try { sweep(); mount(); } catch (e) { /* never break the panel */ } try { mountPass(); } catch (e) {} try { mountReset(); } catch (e) {} }
  function schedule() { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; tick(); }); }
  function start() { tick(); new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true }); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
