#!/usr/bin/env python3
"""Static-site generator for tobianoapps.com. Pure Python, no deps.

Emits plain HTML (committed and served directly by GitHub Pages — no build at
serve time). Legal pages are generated from the Markdown in src/legal/ so the
copy stays verbatim. Run:  python3 build.py
"""
import os, re, html as _html

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- shared shell
FA = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"

def esc_attr(url):
    return url.replace("&", "&amp;")

def head(title, description):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{_html.escape(title)}</title>
<meta name="description" content="{_html.escape(description)}">
<link rel="icon" href="/favicon.ico">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/fonts/faces.css">
<link rel="stylesheet" href="{FA}">
<link rel="stylesheet" href="/styles.css">
<script>(function(){{var t=localStorage.getItem('theme');if(!t)t=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.classList.toggle('dark',t==='dark');}})();</script>
<script defer src="/theme.js"></script>
</head>"""

HEADER = """<header class="site-header">
  <a class="brand" href="/">
    <img src="/logo.png" alt="Tobiano Apps logo">
    <span>tobiano apps</span>
  </a>
  <div class="header-spacer"></div>
  <button class="theme-switch" type="button" aria-label="Toggle light and dark theme" onclick="toggleTheme()">
    <span class="fa-regular fa-sun"></span>
    <span class="fa-solid fa-moon"></span>
  </button>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="socials">
    <a href="https://github.com/sebastinto" aria-label="GitHub" target="_blank" rel="noopener"><span class="fa-brands fa-github"></span></a>
    <a href="mailto:contact@tobianoapps.com" aria-label="Email"><span class="fa-regular fa-envelope"></span></a>
  </div>
  <div class="copyright">&copy; 2026, Tobiano apps</div>
</footer>"""

def page(title, description, main):
    return head(title, description) + "\n<body>\n" + HEADER + \
        '\n<main class="page">\n' + main + "\n</main>\n" + FOOTER + "\n</body>\n</html>\n"

def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", rel)

# ---------------------------------------------------------------- landing page
GP = "google_play_badge.png"
APP_STORE_IMG = "https://tools.applemediaservices.com/api/badges/download-on-the-app-store/black/en-US?size=250x83&releaseDate=1276560000&h=fbdb5b4ea9418f75555a911d01d7610e"

def project(title, subtitles, features, img, badges):
    subs = "".join(f'<p class="subtitle">{s}</p>' for s in subtitles)
    feats = "".join(
        f'<a href="{esc_attr(u)}" target="_blank" rel="noopener">{t}</a>' for t, u in features)
    feats_html = f'<div class="features">{feats}</div>' if features else ""
    def badge(src, u, alt):
        img = f'<img src="{esc_attr(src)}" alt="{alt}">'
        # A badge with no URL (e.g. "coming soon") renders as a plain image, not a dead link.
        return f'<a href="{esc_attr(u)}" target="_blank" rel="noopener">{img}</a>' if u else img
    bs = "".join(badge(src, u, alt) for src, u, alt in badges)
    return f"""<section class="project">
  <div class="project-text">
    <h2>{title}</h2>
    {subs}
    {feats_html}
    <div class="badges">{bs}</div>
  </div>
  <div class="project-image"><img src="{img}" alt="{title}"></div>
</section>"""

def build_index():
    sunny = project(
        "Sunny Side",
        ["UV index", "UV protection guidelines"],
        [("&#9733; 19 Best Weather Apps &#9733;", "https://androidappsforme.com/weather-apps-for-android/"),
         ("&#9733; Featured on Android Police &#9733;", "https://www.androidpolice.com/2021/07/03/14-new-and-notable-android-apps-from-the-last-two-weeks-including-stadia-for-android-tv-elabels-and-zoom-for-chrome-6-19-21-7-3-21/#sunny-side")],
        "sunnyside_hero.webp",
        [("https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/en-us?releaseDate=1785283200",
          "https://apps.apple.com/us/app/sunny-side-uv-index/id6783180537?itscg=30200&itsct=apps_box_badge&mttnsubad=6783180537",
          "Download on the App Store"),
         (GP, "https://play.google.com/store/apps/details?id=com.tobianoapps.sunnyside&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1", "Get it on Google Play")])
    dotscape = project(
        "Dotscape",
        ["3D dot-particle live wallpaper", "Deeply customizable, tap to ripple"],
        [],
        "dotscape_hero.webp",
        [(GP, "https://play.google.com/store/apps/details?id=com.tobianoapps.dotscape&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1", "Get it on Google Play")])
    depths = project(
        "The Depths",
        ["Underwater live wallpaper", "Light shafts, caustics and drifting marine snow"],
        [],
        "thedepths_hero.webp",
        [(GP, "https://play.google.com/store/apps/details?id=com.tobianoapps.thedepths&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1", "Get it on Google Play")])
    timerise = project(
        "Time Rise",
        ["Minimal Digital Hourglass"],
        [("&#9733; Best Kitchen Timer Apps &#9733;", "https://freeappsforme.com/kitchen-timer-apps"),
         ("&#9733; Featured on Android Headlines &#9733;", "https://www.androidheadlines.com/2022/05/time-rise-android-app.html"),
         ("&#9733; Featured on Android Police &#9733;", "https://www.androidpolice.com/2021/04/24/12-new-and-notable-android-apps-and-live-wallpapers-from-the-last-three-weeks-including-weatherback-wallpaper-microsoft-edge-canary-and-sketch-360-4-3-21-4-24-21/#time-rise")],
        "android_timerise.png",
        [(GP, "https://play.google.com/store/apps/details?id=com.tobianoapps.timerise&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1", "Get it on Google Play")])
    lake = project(
        "Lake &amp; Coast",
        ["Pontchartrain Conservancy Water Quality Program"],
        [],
        "lake_coast_teaser.jpg",
        [(APP_STORE_IMG, "https://apps.apple.com/us/app/lake-and-coast/id1559404216?itsct=apps_box_badge&itscg=30200", "Download on the App Store"),
         (GP, "https://play.google.com/store/apps/details?id=org.scienceforourcoast.lakeandcoastnew", "Get it on Google Play")])
    main = '<div class="container">\n' + sunny + dotscape + depths + timerise + lake + "\n</div>"
    write("index.html", page("Tobiano Apps", "Home of Tobiano Apps.", main))

# ---------------------------------------------------------------- FAQ page
MET = "https://www.met.no/"
HELP = "mailto:sunnyside_help@tobianoapps.com?subject=Feedback for Sunny Side Android"

FAQ = [
 ("UV index is inaccurate",
  f'<p>Sunny Side uses the <a href="{MET}">Meteorologisk Institute\'s</a> API for its data. '
  f'<a href="mailto:klima@met.no">Feel free to report any inaccuracy to them.</a></p>'),
 ("Can you add more data sources?",
  f'<p>The <a href="{MET}">Meteorologisk Institute\'s</a> API was the only free, reliable source providing '
  'current UV index and forecast. Other sources were either unreliable or required a recurring fee. If better '
  'data sources pop up, they will be considered, but in the meantime this is the best option for Sunny Side.</p>'),
 ("Will you be adding a premium / paid version / subscription?",
  '<p>I have not built Sunny Side as a profit generating project. I intend to keep it free. The downside is that '
  'I will have limited time to add new features or maintain it. I will do my best to update Sunny Side if any '
  'breaking change is introduced by new Android versions.</p>'),
 ("Can you add feature x, y and z?",
  f'<p>Please share your idea by sending an email to <a href="{esc_attr(HELP)}">sunnyside_help@tobianoapps.com.</a> '
  'Just keep in mind that this free app is developed and maintained in my spare time so I cannot guarantee that '
  'any new feature will actually be implemented.</p>'),
 ("Do you track my location?",
  '<p>The short answer is: Sunny Side does NOT track your location but third-parties may.</p>'
  f'<p>The long answer is: Sunny Side stores your location on your device only. There is no analytics, ads or any '
  'tracking logic implemented in the app. However, the app needs to communicate your location to the '
  f'<a href="{MET}">Meteorologisk Institute\'s</a> API to get UV index data back. Please refer to their '
  '<a href="https://www.met.no/en/About-us/privacy">privacy policy</a> to learn more.</p>'
  '<p>Also, getting your location either through a location request via GPS or via the '
  '<a href="https://cloud.google.com/maps-platform/places">Google Places SDK</a> shares some of your data with '
  'Google. Please refer to <a href="https://policies.google.com/privacy">Google\'s privacy policy center</a> '
  'to learn more.</p>'),
 ("Widget not updating?",
  '<p>Widgets require that you grant background and works better with precise location permission.</p>'
  '<p>To check these:</p>'
  '<ol><li>Go to Settings -&gt; Apps -&gt; Sunny Side -&gt; Permissions -&gt; Location</li>'
  '<li>Select "Allow all the time" AND "Use precise location"</li>'
  '<li>Delete and re-add widgets</li></ol>'
  "<p>If you've been switching launchers, make sure you also delete widgets on launchers that you're not using.</p>"
  "<p>If that does not work, try clearing the app's data and cache:</p>"
  '<ol><li>Go to Settings -&gt; Apps</li><li>Click on See all apps</li><li>Look for and click on Sunny Side</li>'
  '<li>Click on Storage &amp; cache</li><li>Click on Clear cache and Clear storage</li></ol>'
  '<p>If that does not work, try deleting Sunny Side, reboot your phone and re-install the app.</p>'
  '<p>Unfortunately some manufacturers implement overly aggressive battery optimization that breaks basic '
  "functionality. This is especially true if you're using a Samsung, OnePlus, Huawei or Xiaomi device. To learn "
  'more, as well as to view detailed steps for possible fixes, please click on the manufacturer of your device '
  'on this website: <a href="https://dontkillmyapp.com/">https://dontkillmyapp.com/</a></p>'
  f'<p>Please don\'t hesitate to send an email to <a href="{esc_attr(HELP)}">sunnyside_help@tobianoapps.com</a> '
  'to report bugs or if you need any help troubleshooting issues.</p>'),
 ("Widget battery usage?",
  '<p>Due to the time-sensitive nature of UV data, and restrictions in the Android OS, a running service is '
  'required to keep the widgets up to date.</p>'
  "<p>I have benchmarked Sunny Side's widgets against acclaimed, popular apps and found similar or better "
  'performance.</p>'),
 ("Location fail / slow update?",
  '<p>GPS location is fetched through Google Play Services. It may take up to 30 seconds for a location refresh</p>'
  '<p>There are a few things you can try to improve refresh speed and reliability:</p>'
  '<ol><li>grant precise location permission</li>'
  '<li>as a quick check, go outside and open Google Maps. Check if you can refresh your location in the app. '
  'Then try updating your location in Sunny Side</li>'
  '<li>make sure Google Play Services are up-to-date and not blocked in any way</li>'
  '<li>go to "Location Services" in system settings and make sure "Google Location Accuracy", "Wi-Fi Scanning" '
  'and "Bluetooth Scanning" are on</li>'
  '<li>do not spoof your location</li>'
  '<li>do not use a VPN, ad blocker or other networking restrictions</li></ol>'
  '<p>As an alternative, instead of using GPS location, use the '
  '<a href="https://tobianoapps.com/android/sunnyside/images/sunnyside_search_location.png">search function</a> '
  "instead. Location won't update automatically but as long as you're not travelling long distances, UV data "
  'will remain accurate.</p>'),
 ("I asked for help in the Google Play Store review section so why are you asking me to send an email?",
  '<p>The review section of the Google Play Store has a 350 character limit, does not allow sharing url links, '
  'images, videos or files of any type. Conversation history is also difficult to read. '
  f'<a href="{esc_attr(HELP)}">Email</a> is the best way to provide support.</p>'),
 ("City name / region displayed as coordinates",
  '<p>On rare occasions, fetching city name &amp; region may fail. Instead of showing nothing, shortened '
  'coordinates will be displayed.</p>'
  '<p>A few things you can check in the meantime are:</p>'
  '<ol><li>restart the app</li>'
  '<li>make sure that you have a strong, consistent internet connection</li>'
  '<li>make sure Google Play Services are up to date and not blocked in any way</li>'
  '<li>make sure that you are using the latest version of Sunny Side by checking for updates in the Google Play '
  'Store</li>'
  '<li>if you are using a VPN, or any ad blocking software, turn them off and try again</li></ol>'),
 ("Network, location, data empty? Problem not listed here?",
  f'<p>Please send an email to <a href="{esc_attr(HELP)}">sunnyside_help@tobianoapps.com</a> and I\'d be happy to '
  'help troubleshoot or fix a bug if there is one to fix. The Google Play Store review section is not the right '
  'place for troubleshooting these issues.</p>'
  '<p>A few things you can check in the meantime are:</p>'
  '<ol><li>make sure that you are using the latest version of Sunny Side by checking for updates in the Google '
  'Play Store</li>'
  '<li>if you are using a VPN, or any ad blocking software, turn them off and try again</li>'
  '<li>make sure that you have a strong, consistent internet connection</li>'
  '<li>for location, please see the section above entitled "Location slow update"</li>'
  '<li>make sure your device system time is correct. The best way to do so is to: go to System Settings -&gt; '
  'System -&gt; Date &amp; Time and set every option to "automatic" or "network-provided". Then restart your '
  'device.</li></ol>'),
]

def build_faq():
    items = ""
    for q, a in FAQ:
        items += (
            "<details>\n"
            f'  <summary>{q}<span class="chevron fa-solid fa-chevron-down"></span></summary>\n'
            f'  <div class="answer">{a}</div>\n'
            "</details>\n")
    main = '<h1 class="faq-title">Sunny Side FAQ</h1>\n<div class="faq">\n' + items + "</div>"
    write("android/sunnyside/faq.html",
          page("Sunny Side FAQ — Tobiano Apps", "Frequently asked questions about the Sunny Side app.", main))

# ---------------------------------------------------------------- markdown -> html (legal)
def inline(text):
    text = _html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f'<a href="{esc_attr(m.group(2))}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text

def md_to_html(body):
    out, para, items = [], [], []
    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para).strip()) + "</p>"); para.clear()
    def flush_list():
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"); items.clear()
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            flush_para(); flush_list(); continue
        if s.startswith("### "):
            flush_para(); flush_list(); out.append("<h3>" + inline(s[4:].replace("**", "")) + "</h3>")
        elif s.startswith("## "):
            flush_para(); flush_list(); out.append("<h2>" + inline(s[3:].replace("**", "")) + "</h2>")
        elif re.match(r"\*\s+", s):
            flush_para(); items.append(re.sub(r"^\*\s+", "", s))
        else:
            flush_list(); para.append(s)
    flush_para(); flush_list()
    return "\n".join(out)

def parse_md(path):
    raw = open(path, encoding="utf-8").read()
    title = description = ""
    if raw.startswith("---"):
        end = raw.index("---", 3)
        for ln in raw[3:end].strip().splitlines():
            if ln.startswith("title:"): title = ln.split(":", 1)[1].strip()
            elif ln.startswith("description:"): description = ln.split(":", 1)[1].strip()
        raw = raw[end + 3:]
    return title, description, md_to_html(raw)

LEGAL = [
    ("src/legal/android/sunnyside/Privacy.md", "android/sunnyside/legal/privacy.html"),
    ("src/legal/android/sunnyside/Terms.md",   "android/sunnyside/legal/terms.html"),
    ("src/legal/android/timerise/Privacy.md",  "android/timerise/legal/privacy.html"),
    ("src/legal/android/timerise/Terms.md",    "android/timerise/legal/terms.html"),
    ("src/legal/android/dotscape/Privacy.md",  "android/dotscape/legal/privacy.html"),
    ("src/legal/android/dotscape/Terms.md",    "android/dotscape/legal/terms.html"),
    ("src/legal/android/thedepths/Privacy.md", "android/thedepths/legal/privacy.html"),
    ("src/legal/android/thedepths/Terms.md",   "android/thedepths/legal/terms.html"),
    ("src/legal/ios/sunnyside/Privacy.md",     "ios/sunnyside/legal/privacy.html"),
    ("src/legal/ios/sunnyside/Terms.md",       "ios/sunnyside/legal/terms.html"),
]

def build_legal():
    for md, out in LEGAL:
        title, description, body = parse_md(os.path.join(ROOT, md))
        main = f'<article class="doc">\n{body}\n</article>'
        write(out, page(f"{title} — Tobiano Apps", description, main))

if __name__ == "__main__":
    build_index()
    build_faq()
    build_legal()
    print("done.")
