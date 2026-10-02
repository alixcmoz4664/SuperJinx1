<div align="center">

<img src="banner.svg" width="100%" alt="Super JinX Panel">

<a href="https://t.me/+WvKFv0lU_i5lNGE0"><img src="https://readme-typing-svg.demolab.com?font=Inter&weight=800&size=22&duration=2600&pause=700&color=6C7BFF&center=true&vCenter=true&width=620&lines=One-click+Reseller+Panel+on+Railway;PasarGuard+%2B+Xray+in+a+single+service;5+configs+%C2%B7+2+groups+%C2%B7+self-healing;Free+forever+%C2%B7+X4G+%C3%97+JinX" alt="Super JinX"></a>

<h1>Super JinX Panel</h1>

<p><b>پنل نمایندگی حرفه‌ای، رایگان و متن‌باز بر پایه‌ی PasarGuard</b><br>
یک Fork تا یک سرویس کامل: پنل، هسته‌ی Xray و ۵ کانفیگ آماده، همه روی Railway</p>

<a href="https://t.me/+WvKFv0lU_i5lNGE0"><img src="https://img.shields.io/badge/Telegram-Super%20JinX-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram"></a>
<img src="https://img.shields.io/badge/Version-6.1.2-5b6cff?style=for-the-badge" alt="Version">
<img src="https://img.shields.io/badge/Price-Free-16a34a?style=for-the-badge" alt="Free">
<br>
<img src="https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white" alt="Railway">
<img src="https://img.shields.io/badge/Panel-PasarGuard-1e3a8a?style=for-the-badge" alt="PasarGuard">
<img src="https://img.shields.io/badge/Core-Xray-7c4dff?style=for-the-badge" alt="Xray">
<img src="https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">

<br><br>

<a href="#install"><b>نصب</b></a> &nbsp;·&nbsp;
<a href="#guides"><b>آموزش‌ها</b></a> &nbsp;·&nbsp;
<a href="#configs"><b>کانفیگ‌ها</b></a> &nbsp;·&nbsp;
<a href="#reseller"><b>نمایندگی</b></a> &nbsp;·&nbsp;
<a href="#fix"><b>عیب‌یابی</b></a> &nbsp;·&nbsp;
<a href="https://t.me/+WvKFv0lU_i5lNGE0"><b>کانال</b></a>

</div>

<br>

> [!NOTE]
> **Super JinX** کاملاً رایگانه. ریپو رو Fork کن، روی Railway بساز و در کمتر از ۵ دقیقه پنل نمایندگی خودت رو تحویل بگیر. بدون VPS، بدون ترمینال، بدون تنظیم دستی.

<br>

> [!IMPORTANT]
> **تازه‌های نسخه‌ی 6.1.2:** ربات پشتیبان خودکار که هر خرابی رو همونجا درست می‌کنه · تغییر رمز از داخل تنظیمات · بازیابی ورود با کلید مالک از صفحه‌ی ورود · قفل گروه‌ها و هاست‌ها در برابر حذف · کانفیگ‌های سریع‌تر · صفحه‌ی اشتراک مقاوم‌تر

<br>

<div align="center">

| <img src="ic-features.svg" width="34"><br>**۱ سرویس** | <img src="ic-configs.svg" width="34"><br>**۵ کانفیگ** | <img src="ic-reseller.svg" width="34"><br>**۲ گروه** | <img src="ic-sub.svg" width="34"><br>**۱۰ قالب فروش** | <img src="ic-apps.svg" width="34"><br>**۶ اپ** | <img src="ic-heal.svg" width="34"><br>**خودترمیم** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| پنل + Xray + nginx | ۳ پروتکل، ۲ انتقال | پرو و 𝗝𝗶𝗻𝗫 | آماده‌ی فروش | اتصال با یک لمس | ۲۴ ساعته |

</div>

<br>

## فهرست مطالب

| | | |
|---|---|---|
| [معرفی](#intro) | [امکانات](#features) | [معماری](#arch) |
| [نصب](#install) | [آموزش‌ها](#guides) | [ورود و امنیت](#login) |
| [گروه‌ها و کانفیگ‌ها](#configs) | [اپ‌های پشتیبانی‌شده](#apps) | [پنل نمایندگی](#reseller) |
| [صفحه‌ی اشتراک](#sub) | [خودترمیمی](#heal) | [سرعت و پینگ](#speed) |
| [متغیرها](#vars) | [آپدیت](#update) | [عیب‌یابی](#fix) |
| [مستندات](#docs) | [همکاری](#collab) | [پشتیبانی](#support) |

<br>

<a id="intro"></a>
## <img src="ic-intro.svg" width="30" align="center"> &nbsp;معرفی

**Super JinX** یک پنل نمایندگی کامل و آماده‌ی فروشه که روی [PasarGuard](https://github.com/PasarGuard/panel) ساخته شده. پنل، هسته‌ی Xray و وب‌سرور همه داخل **یک سرویس** روی Railway اجرا میشن و همه‌ی تنظیمات **خودکار** انجام میشه: اینباندها، هاست‌ها، گروه‌ها، قالب‌های فروش، نقش نماینده و صفحه‌ی اشتراک.

<a id="why"></a>
### <img src="ic-why.svg" width="24" align="center"> &nbsp;چرا Super JinX؟

| | پنل معمولی روی VPS | **Super JinX** |
|---|:---:|:---:|
| خرید سرور | لازم | **لازم نیست** |
| نصب با ترمینال | لازم | **لازم نیست** |
| ساخت اینباند و هاست | دستی | **خودکار** |
| گروه و قالب فروش | دستی | **آماده** |
| صفحه‌ی اشتراک اختصاصی | ندارد | **دارد** |
| بازگشت خودکار بعد از خطا | ندارد | **ربات پشتیبان ۲۴ ساعته** |
| محافظت از گروه‌ها در برابر حذف | ندارد | **دارد** |
| تغییر و بازیابی رمز بدون ترمینال | ندارد | **دارد** |
| هزینه | ماهانه | **رایگان** |

<br>

<a id="features"></a>
## <img src="ic-features.svg" width="30" align="center"> &nbsp;امکانات

<table>
<tr>
<td width="50%" valign="top">

### <img src="ic-install.svg" width="22" align="center"> &nbsp;نصب بدون دردسر
- Fork و Deploy، بدون ویرایش حتی یک فایل
- پنل، هسته‌ی Xray و nginx در **یک سرویس**
- بدون نیاز به VPS یا نصب نود جداگانه
- همه چیز روی پورت `8080`

</td>
<td width="50%" valign="top">

### <img src="ic-configs.svg" width="22" align="center"> &nbsp;کانفیگ‌های حرفه‌ای
- **۵ کانفیگ** با ۳ پروتکل: VLESS، Trojan و VMess
- دو نوع انتقال: WebSocket و HTTPUpgrade
- TLS روی پورت 443 با `alpn=http/1.1`
- Early Data (`ed=2560`) برای پینگ کمتر

</td>
</tr>
<tr>
<td valign="top">

### <img src="ic-reseller.svg" width="22" align="center"> &nbsp;سیستم نمایندگی
- نقش آماده‌ی **«نماینده»** با سهمیه‌ی حجم
- هر نماینده فقط کاربرهای خودش رو می‌بینه
- ۱۰ قالب فروش آماده برای هر دو گروه
- منوی تمیز و ساده

</td>
<td valign="top">

### <img src="ic-sub.svg" width="22" align="center"> &nbsp;صفحه‌ی اشتراک اختصاصی
- طراحی شیشه‌ای تیره با حلقه‌ی مصرف
- پینگ زنده‌ی سرور و تاریخ شمسی
- **QR داخلی** با ذخیره‌ی تصویر
- اتصال با یک لمس به ۶ اپ محبوب

</td>
</tr>
<tr>
<td valign="top">

### <img src="ic-heal.svg" width="22" align="center"> &nbsp;ربات پشتیبان و پایداری
- **ربات پشتیبان خودکار** داخل سرور، بدون هیچ دکمه‌ی اضافه
- هر ۱ دقیقه: هسته و گروه‌ها · هر ۵ دقیقه: هاست‌ها، اشتراک، قالب‌ها
- تست ساب لینک واقعی و ری‌استارت تمیز در صورت خرابی
- گروه‌ها، هاست‌ها و هسته در برابر حذف **قفل** هستن

</td>
<td valign="top">

### <img src="ic-login.svg" width="22" align="center"> &nbsp;امنیت
- مسیرهای کانفیگ **اختصاصی برای هر نصب**
- همه‌ی پورت‌های داخلی فقط روی `127.0.0.1`
- **تغییر رمز عبور از داخل تنظیمات**، با تأیید رمز فعلی
- **بازیابی ورود** با کلید یک‌بار مصرف ۵ دقیقه‌ای
- قفل ۱۰ دقیقه‌ای بعد از ۵ تلاش اشتباه

</td>
</tr>
</table>

<br>

<a id="arch"></a>
## <img src="ic-arch.svg" width="30" align="center"> &nbsp;معماری

```mermaid
flowchart LR
    U["User App<br/>V2Box · v2rayNG · Hiddify"] -- "TLS 443" --> R["Railway Edge"]
    R -- "8080" --> N["nginx"]
    N -- "/dashboard · /api · /sub" --> P["PasarGuard Panel"]
    N -- "5 secret paths" --> X["Xray Core"]
    P -- "gRPC 127.0.0.1" --> X
    B["JinX Bootstrap<br/>auto setup + self-heal"] --> P
    X --> I(("Internet"))
```

<br>

<a id="install"></a>
## <img src="ic-install.svg" width="30" align="center"> &nbsp;نصب

> [!TIP]
> زمان نصب حدود **۵ دقیقه**ست. فقط یک اکانت [GitHub](https://github.com) و یک اکانت [Railway](https://railway.com) لازم داری.

<details open>
<summary><b>مرحله‌ی ۱ &nbsp;·&nbsp; Fork کردن ریپو</b></summary>

<br>

1. بالای همین صفحه روی **Fork** بزن.
2. اسم ریپو رو هر چی خواستی بذار و **Create fork** رو بزن.
3. حالا یک نسخه از پروژه توی اکانت خودت داری. هیچ فایلی رو لازم نیست تغییر بدی.

</details>

<details open>
<summary><b>مرحله‌ی ۲ &nbsp;·&nbsp; ساخت سرویس روی Railway</b></summary>

<br>

1. وارد [Railway](https://railway.com) شو و بزن **New Project**.
2. گزینه‌ی **Deploy from GitHub repo** رو انتخاب کن و ریپوی Fork شده‌ی خودت رو بزن.
3. Railway خودش شروع به ساختن می‌کنه. صبر کن تا مرحله‌ی بعد.

</details>

<details open>
<summary><b>مرحله‌ی ۳ &nbsp;·&nbsp; اتصال Volume (خیلی مهم)</b></summary>

<br>

1. روی سرویس **راست‌کلیک** کن (روی گوشی: نگه دار) و **Attach Volume** رو بزن.
2. مسیر رو دقیقاً این بذار:

```text
/var/lib/pasarguard
```

> [!IMPORTANT]
> بدون Volume با هر ری‌استارت همه‌ی کاربرها و تنظیمات پاک میشن.

</details>

<details open>
<summary><b>مرحله‌ی ۴ &nbsp;·&nbsp; دامنه و پورت</b></summary>

<br>

1. برو **Settings ← Networking**.
2. بزن **Generate Domain** و پورت رو **`8080`** بذار.
3. یک آدرس مثل `xxxx.up.railway.app` می‌گیری. این آدرس پنلته.

</details>

<details open>
<summary><b>مرحله‌ی ۵ &nbsp;·&nbsp; Region و اجرای دوباره</b></summary>

<br>

1. برو **Settings ← Deploy ← Region** و **EU West (Amsterdam)** رو انتخاب کن (بهترین پینگ برای ایران).
2. از تب **Deployments** یک بار **Redeploy** بزن.
3. توی **Deploy Logs** این خط یعنی همه چیز آماده‌ست:

```text
[bootstrap] DONE -> https://YOUR-DOMAIN/dashboard/
```

</details>

> [!NOTE]
> **هر نصب، مسیرهای اختصاصی خودش رو داره.** موقع اولین اجرا مسیر هر ۵ کانفیگ تصادفی ساخته میشه و روی Volume می‌مونه. هر Fork روی سرور جداگانه‌ی خودش اجرا میشه، پس پنل‌ها هیچ منبعی رو با هم شریک نیستن و از سرعت هم کم نمی‌کنن.

<br>

<a id="guides"></a>
## <img src="ic-docs.svg" width="30" align="center"> &nbsp;آموزش‌ها

<details>
<summary><b>اولین ورود به پنل</b></summary>

<br>

1. آدرس `https://YOUR-DOMAIN/dashboard/` رو باز کن.
2. با `admin` و رمز `admin` وارد شو.
3. **همون اول رمز رو عوض کن**: **تنظیمات ← تغییر رمز عبور** (آموزش بعدی).

</details>

<details>
<summary><b>تغییر رمز عبور از تنظیمات</b></summary>

<br>

1. توی پنل برو **«تنظیمات»**. بالای صفحه کارت **«تغییر رمز عبور»** هست.
2. **نام کاربری فعلی** و **رمز عبور فعلی** رو وارد کن.
3. **رمز عبور جدید** و تکرارش رو بنویس و **«ثبت رمز جدید»** رو بزن.
4. پنل خودکار خارج میشه. از این به بعد با رمز جدید وارد شو.

مالک و نماینده‌ها هر کدوم رمز اکانت خودشون رو از همینجا عوض می‌کنن. بعد از ۵ بار رمز اشتباه، ۱۰ دقیقه قفل میشه.

</details>

<details>
<summary><b>بازیابی رمز با کلید ۵ دقیقه‌ای مالک</b></summary>

<br>

1. توی پنل برو **«کلیدهای API»**. بالای صفحه بخش **«کلید ۵ دقیقه‌ای مالک»** هست.
2. روی **«دریافت کلید»** بزن و کلید رو کپی کن.
3. از پنل خارج شو. زیر فرم ورود روی **«رمز رو فراموش کردی؟ ورود با کلید مالک»** بزن.
4. کلید رو پیست کن، نام کاربری و رمز جدید (دو بار) رو بذار و **«ثبت و ورود با اطلاعات جدید»** رو بزن.
5. با نام کاربری و رمز جدید وارد شو.

رمز یادت رفته؟ سرویس رو توی Railway **Restart** کن و کلید رو از خط **`OWNER KEY`** توی لاگ بردار.

</details>

<details>
<summary><b>ساخت کاربر و فروش اشتراک</b></summary>

<br>

1. برو **کاربران ← ساخت کاربر**.
2. یک **نام کاربری** بنویس.
3. از بخش قالب، یکی رو انتخاب کن. مثلاً `30GB - 30 روز` (گروه 𝗝𝗶𝗻𝗫، ۴ کانفیگ) یا `Pro 30GB - 30 روز` (گروه جینکس پرو، ۱ کانفیگ).
4. ذخیره کن. حجم، تاریخ انقضا و کانفیگ‌ها خودکار تنظیم میشن.
5. روی کاربر بزن و **لینک اشتراک** رو کپی کن و برای مشتری بفرست.

</details>

<details>
<summary><b>وصل شدن با V2Box (iOS و Android)</b></summary>

<br>

1. لینک اشتراک رو توی مرورگر گوشی باز کن.
2. بزن **«افزودن به اپ با یک لمس»** و **V2Box** رو انتخاب کن.
3. توی V2Box کانفیگ‌ها اضافه میشن. یکی رو انتخاب کن و وصل شو.
4. برای تست پینگ از **Real Delay / URL Test** استفاده کن.

</details>

<details>
<summary><b>وصل شدن با v2rayNG (Android)</b></summary>

<br>

1. لینک اشتراک رو کپی کن.
2. توی v2rayNG از منوی بالا **Subscription group setting** رو باز کن و **+** بزن.
3. لینک رو توی **URL** پیست کن و ذخیره کن.
4. برگرد، از منو **Update subscription** رو بزن و یکی از کانفیگ‌ها رو انتخاب کن.

</details>

<details>
<summary><b>وصل شدن با Hiddify، Streisand، Happ و NekoBox</b></summary>

<br>

1. لینک اشتراک رو توی مرورگر باز کن.
2. بزن **«افزودن به اپ با یک لمس»** و اپ خودت رو انتخاب کن.
3. اشتراک خودکار اضافه میشه. اگه اپ باز نشد، لینک رو کپی کن و توی اپ از بخش **Add / Import from clipboard** اضافه کن.

</details>

<details>
<summary><b>ساخت نماینده</b></summary>

<br>

1. با اکانت مالک برو **مدیران ← افزودن مدیر** (این منو فقط برای مالک دیده میشه).
2. نقش رو **«نماینده»** بذار و سهمیه‌ی حجم رو مشخص کن (مثلاً **50 GB**).
3. یوزر و رمز رو به نماینده بده. نماینده فقط کاربرهای خودش رو می‌بینه و فقط با قالب‌ها کاربر می‌سازه.

</details>

<details>
<summary><b>آپدیت پنل به نسخه‌ی جدید</b></summary>

<br>

1. توی ریپوی خودت روی گیتهاب بزن **Sync fork ← Update branch**.
2. Railway خودکار Deploy می‌کنه. کاربرها، رمزها و کانفیگ‌ها دست نمی‌خورن.

</details>

<br>

<a id="login"></a>
## <img src="ic-login.svg" width="30" align="center"> &nbsp;ورود و امنیت

| نقش | آدرس | نام کاربری | رمز |
|---|---|---|---|
| **مالک** | `https://YOUR-DOMAIN/dashboard/` | `admin` | `admin` |
| **نماینده‌ی نمونه** (۵۰ گیگ) | `https://YOUR-DOMAIN/dashboard/` | `reseller` | `reseller` |

> [!WARNING]
> `admin` / `admin` فقط برای **اولین ورود** هست. همون اول رمز مالک رو عوض کن و رمز نماینده‌ی نمونه رو هم تغییر بده یا پاکش کن (دیگه ساخته نمیشه). رمزی که خودت بذاری هیچ وقت خودکار عوض نمیشه.

<br>

<a id="configs"></a>
## <img src="ic-configs.svg" width="30" align="center"> &nbsp;گروه‌ها و کانفیگ‌ها

| گروه | کانفیگ | پروتکل | انتقال | اثرانگشت TLS | ویژگی |
|---|---|---|---|---|---|
| **جینکس پرو** | 𝗣𝗿𝗼 | VLESS | WebSocket + Early Data | Chrome | تک‌کانفیگ با کمترین پینگ |
| **𝗝𝗶𝗻𝗫** | ⚡ 𝗙𝗹𝗮𝘀𝗵 | VLESS | WebSocket | Firefox | سریع و سبک |
| | 🔥 𝗙𝗶𝗿𝗲 | Trojan | WebSocket | Safari | مناسب iOS |
| | 💎 𝗗𝗶𝗮𝗺𝗼𝗻𝗱 | VMess | WebSocket | Edge | سازگاری با اپ‌های قدیمی |
| | 🌙 𝗡𝗶𝗴𝗵𝘁 | VLESS | HTTPUpgrade | iOS | پایدار در شبکه‌های سخت |

اسم هر کانفیگ توی اپ کاربر اینجوری دیده میشه: `𝗣𝗿𝗼 | جینکس | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫`

> [!TIP]
> اگه موقع ساخت کاربر گروهی انتخاب نکنی، پنل خودکار اون رو به گروه **𝗝𝗶𝗻𝗫** وصل می‌کنه.

**لینک اشتراک**

```text
https://YOUR-DOMAIN/sub/<token>
```

<a id="apps"></a>
### <img src="ic-apps.svg" width="24" align="center"> &nbsp;اپ‌های پشتیبانی‌شده

| اپ | Android | iOS | Windows | اتصال با یک لمس |
|---|:---:|:---:|:---:|:---:|
| **V2Box** | ✓ | ✓ | | ✓ |
| **v2rayNG** | ✓ | | | ✓ |
| **Hiddify** | ✓ | ✓ | ✓ | ✓ |
| **Streisand** | | ✓ | | ✓ |
| **Happ** | ✓ | ✓ | ✓ | ✓ |
| **NekoBox** | ✓ | | ✓ | ✓ |
| **Clash Meta / sing-box** | ✓ | ✓ | ✓ | |

<br>

<a id="reseller"></a>
## <img src="ic-reseller.svg" width="30" align="center"> &nbsp;پنل نمایندگی

| گروه | قالب‌های فروش آماده |
|---|---|
| **𝗝𝗶𝗻𝗫** | 10، 30، 50 و 100 گیگ (۳۰ روزه) · 200 گیگ (۶۰ روزه) · نامحدود (۳۰ روزه) |
| **جینکس پرو** | Pro 30، 50 و 100 گیگ · Pro نامحدود (همه ۳۰ روزه) |

**منوی پنل**: داشبورد · کاربران · کلیدهای API · قالب‌ها · عملیات گروهی · تنظیمات · پشتیبانی

نماینده‌ها فقط کاربرهای خودشون رو می‌بینن، فقط با قالب‌ها کاربر می‌سازن و با تموم شدن سهمیه‌شون خودکار محدود میشن.

<br>

<a id="sub"></a>
## <img src="ic-sub.svg" width="30" align="center"> &nbsp;صفحه‌ی اشتراک

- حلقه‌ی مصرف با حجم مصرف‌شده، باقی‌مانده و روزهای باقی‌مانده
- تاریخ انقضا به **تقویم شمسی** و هشدار نزدیک شدن به پایان
- **پینگ زنده‌ی سرور** با برچسب کیفیت
- اتصال با یک لمس به V2Box، v2rayNG، Hiddify، Streisand، Happ و NekoBox
- فهرست کانفیگ‌ها با برچسب پروتکل، **QR داخلی** و کپی سریع

<br>

<a id="heal"></a>
## <img src="ic-heal.svg" width="30" align="center"> &nbsp;ربات پشتیبان و خودترمیمی

ربات پشتیبان Super JinX داخل خود سرور اجرا میشه، توی پنل هیچ دکمه‌ای نداره و همه‌ی کارهاش رو توی لاگ Railway با کلمه‌ی `doctor` ثبت می‌کنه.

```mermaid
flowchart LR
    D(("Doctor<br/>every 15s")) --> C{"Core connected?"}
    C -- no --> RC["Restart core<br/>+ reconnect node"]
    D --> G{"Groups OK?"}
    G -- no --> RG["Re-create / fix groups"]
    D --> S{"Sub link OK?"}
    S -- "3 errors" --> RP["Clean panel restart"]
    D --> H{"Hosts · settings ·<br/>templates OK?"}
    H -- no --> FX["Fix on the spot"]
```

| مشکل | واکنش خودکار پنل |
|---|---|
| قطع شدن هسته‌ی Xray | ری‌استارت خودکار هسته و اتصال دوباره‌ی نود |
| جواب ندادن پنل یا nginx به مدت ۳ دقیقه | ری‌استارت کامل سرویس |
| خطا در اسکریپت راه‌اندازی | اجرای دوباره‌ی خودکار بعد از ۱۰ ثانیه |
| تغییر یا حذف اشتباهی گروه‌ها و هاست‌ها | بررسی هر ۱ دقیقه (گروه‌ها) و ۵ دقیقه (هاست‌ها) و اصلاح خودکار |
| ساخت کاربر بدون گروه | اتصال خودکار به گروه 𝗝𝗶𝗻𝗫 |
| حذف یا تغییر گروه‌ها، هاست‌ها، هسته و نقش‌ها از بیرون | **قفل**: از پنل و API فقط قابل دیدنه، نه پاک کردن |
| خراب شدن لینک‌های اشتراک | تست خودکار هر ۵ دقیقه، ری‌استارت تمیز پنل در صورت خطای پشت سر هم |

<br>

<a id="speed"></a>
## <img src="ic-speed.svg" width="30" align="center"> &nbsp;سرعت و پینگ

| تنظیم | اثر |
|---|---|
| Region روی **EU West (Amsterdam)** | کوتاه‌ترین مسیر تا ایران |
| Early Data (`ed=2560`) | یک رفت‌وبرگشت کمتر در هر اتصال |
| `alpn=http/1.1` | سازگار با لبه‌ی Railway، بدون مذاکره‌ی اضافه |
| مسیریابی `AsIs` بدون DNS اضافه | یک رفت‌وبرگشت کمتر سر هر اتصال جدید |
| DNS خود سرور با کش | جواب DNS تقریباً فوری |
| WebSocket بدون بافر | آپلود و دانلود بدون معطلی |
| اتصال‌های Keep-Alive در nginx | پنل و اشتراک سریع‌تر باز میشن |

پینگ واقعی در V2Box حدود **۱۵۰ تا ۲۵۰** میلی‌ثانیه روی اینترنت خوب و **۲۵۰ تا ۴۰۰** روی اینترنت همراهه و به اپراتور کاربر بستگی داره. برای تست از **Real Delay / URL Test** استفاده کن.

<br>

<a id="vars"></a>
## <img src="ic-vars.svg" width="30" align="center"> &nbsp;متغیرهای اختیاری

هیچ متغیری الزامی نیست. از **Variables** سرویس در Railway اضافه‌شون کن:

| متغیر | پیش‌فرض | کاربرد |
|---|---|---|
| `CONFIG_TITLE` | `جینکس \| 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫` | متنی که بعد از اسم هر کانفیگ دیده میشه |
| `SUBSCRIPTION_PATH` | `sub` | مسیر لینک اشتراک |
| `PUBLIC_DOMAIN` | دامنه‌ی Railway | فقط برای دامنه‌ی شخصی یا Cloudflare |
| `DEMO_RESELLER` | `on` | با `off` نماینده‌ی نمونه ساخته نمیشه |

<br>

<a id="update"></a>
## <img src="ic-update.svg" width="30" align="center"> &nbsp;آپدیت

توی ریپوی خودت روی **Sync fork ← Update branch** بزن. Railway خودکار Deploy می‌کنه و **کاربرها، رمزها و کانفیگ‌ها دست نمی‌خورن.** هر Redeploy آخرین نسخه‌ی PasarGuard و Xray رو هم می‌گیره.

<br>

<a id="fix"></a>
## <img src="ic-fix.svg" width="30" align="center"> &nbsp;عیب‌یابی

| خطا | راه‌حل |
|---|---|
| `Application failed to respond` | پورت دامنه رو **8080** بذار |
| کانفیگ‌ها وصل نمیشن | دامنه بعد از اولین Deploy ساخته شده، یک بار **Redeploy** کن |
| کاربرها بعد از Deploy پاک شدن | Volume روی `/var/lib/pasarguard` وصل نیست |
| `Incorrect username or password` | یک دقیقه صبر کن تا سرویس کامل بالا بیاد |
| پینگ قرمز ولی وصل میشه | تست TCP رو کنار بذار و از **Real Delay** استفاده کن |

راهنمای کامل: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) · سوال‌های رایج: [FAQ.md](FAQ.md)

<br>

<details>
<summary><b>سوال‌های پرتکرار</b></summary>

<br>

**اگه بقیه هم از این ریپو بسازن، سرعت پنل من کم میشه؟**
نه. هر Fork روی سرور جداگانه‌ی خودش با CPU، رم و اینترنت جدا اجرا میشه.

**پینگ دقیقاً چقدر میشه؟**
روی V2Box با اینترنت خوب حدود ۱۵۰ تا ۲۰۰ میلی‌ثانیه، به شرطی که Region روی EU West باشه.

**رمزم یادم رفت؟**
سرویس رو Restart کن، کلید رو از خط `OWNER KEY` لاگ بردار و توی صفحه‌ی ورود «رمز رو فراموش کردی؟» رو بزن.

**کسی می‌تونه گروه‌ها رو پاک کنه؟**
نه. گروه‌ها، هاست‌ها، هسته و نقش‌ها از بیرون قفل هستن و اگه هم به هر دلیلی خراب بشن، ربات پشتیبان درستشون می‌کنه.

</details>

<br>

<a id="docs"></a>
## <img src="ic-docs.svg" width="30" align="center"> &nbsp;مستندات

| فایل | محتوا |
|---|---|
| [INSTALL.md](INSTALL.md) | نصب قدم‌به‌قدم |
| [FAQ.md](FAQ.md) | سوال‌های رایج: پینگ، رمز، نماینده |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | حل خطاهای Railway |
| [SECURITY.md](SECURITY.md) | نکات امنیتی |
| [CHANGELOG.md](CHANGELOG.md) | تغییرات هر نسخه |
| [env.example](env.example) | نمونه‌ی متغیرها |

<br>

<a id="collab"></a>
## <img src="ic-collab.svg" width="30" align="center"> &nbsp;همکاری

<div align="center">

<h3>X4G &nbsp;×&nbsp; 𝗝𝗶𝗻𝗫</h3>

این پروژه با همکاری **X4G** و **𝗝𝗶𝗻𝗫** طراحی، ساخته و منتشر شده.

</div>

<br>

<a id="support"></a>
## <img src="ic-channel.svg" width="30" align="center"> &nbsp;پشتیبانی و کانال رسمی

<div align="center">

<a href="https://t.me/+WvKFv0lU_i5lNGE0"><img src="https://img.shields.io/badge/Join-%D8%AC%DB%8C%D9%86%DA%A9%D8%B3%20%7C%20Super%20JinX-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Join Channel"></a>

آپدیت‌ها، آموزش‌ها و پشتیبانی فقط از طریق کانال رسمی<br>
**[جینکس | 𝙎𝙪𝙥𝙚𝙧 𝗝𝗶𝗻𝗫](https://t.me/+WvKFv0lU_i5lNGE0)**

اگه این پروژه به کارت اومد، با یک **Star** حمایتش کن.

</div>

<br>

## <img src="ic-license.svg" width="30" align="center"> &nbsp;مجوز و قدردانی

- استفاده و نصب **رایگانه**. تغییر نام، فروش یا انتشار دوباره‌ی این پروژه به اسم خودتون مجاز نیست. جزئیات در [LICENSE](LICENSE).
- ساخته‌شده بر پایه‌ی [PasarGuard Panel](https://github.com/PasarGuard/panel) و [PasarGuard Node](https://github.com/PasarGuard/node) (مجوز AGPL-3.0) و هسته‌ی [Xray-core](https://github.com/XTLS/Xray-core).

<br>

<div align="center">

<sub><b>Super JinX Panel</b> · X4G × 𝗝𝗶𝗻𝗫 · ساخته‌شده برای اینترنت آزاد</sub>

</div>
