#!/usr/bin/env python3
"""Générateur du site Maison Valeria (multi-pages, statique)."""
import os, re, json, shutil, html as H

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SRC, 'dist')
SITE = 'https://maisonvaleria.net'   # à remplacer par le domaine définitif

def U(i, w=1400):
    return f'https://images.unsplash.com/photo-{i}?auto=format&fit=crop&q=74&w={w}'

def part(n):
    return open(os.path.join(SRC, f'_p_{n}.html'), encoding='utf-8').read()

LOGO = '<svg viewBox="0 0 100 100" aria-hidden="true" fill="currentColor"><text x="10" y="60" font-family="Cormorant,Georgia,serif" font-size="66" font-weight="500">M</text><text x="42" y="91" font-family="Cormorant,Georgia,serif" font-size="56" font-weight="500">V</text><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M64 70 C72 58 80 50 92 40"></path></g><g><path d="M72 58c-1-6 3-9 7-9-1 5-4 8-7 9z"></path><path d="M79 50c0-6 4-8 8-8-1 5-4 7-8 8z"></path><path d="M85 44c1-5 5-6 8-5-2 4-5 5-8 5z"></path><path d="M74 60c5-1 9 1 10 4-4 1-8 0-10-4z"></path><path d="M81 52c5-1 8 1 9 4-4 1-7 0-9-4z"></path></g></svg>'
ARR = '<span class="arr"></span>'

# ---------------------------------------------------------------- Univers
UNI = [
    dict(slug='beaute-du-sourire', p=0, nav='Beauté du sourire', short='Sourire', title='Beauté du sourire',
         h1='Un sourire <em>lumineux.</em>', img='/img/sourire.webp', thumb='/img/sourire.webp',
         hero='/img/cabine.webp',
         sub='Blanchiment dentaire esthétique et conseils personnalisés pour un sourire éclatant.',
         lead='Un sourire plus lumineux, avec un suivi pour en préserver l’éclat.',
         intro=('Le sourire est la première chose que l’on remarque. Chez Maison Valeria, le blanchiment dentaire esthétique est pensé comme un véritable soin de beauté : un moment confortable, dans un cadre apaisant, suivi de conseils simples pour faire durer le résultat.',
                ['Blanchiment dentaire esthétique', 'Conseils d’entretien personnalisés', 'Un cadre calme et haut de gamme']),
         svc=[('Blanchiment dentaire esthétique', 'Un protocole esthétique pour raviver l’éclat naturel de votre sourire, réalisé dans le confort de l’institut.'),
              ('Accompagnement & conseils personnalisés', 'Les bons gestes et les bonnes habitudes pour préserver la blancheur de votre sourire au quotidien.')],
         flow=[('Échange', 'Vos attentes, vos habitudes et le résultat souhaité.'), ('Séance', 'Le blanchiment esthétique, en toute détente.'), ('Conseils', 'Une routine simple pour prolonger l’éclat.')],
         faq=[('Le blanchiment est-il adapté à tout le monde ?', 'Lors de votre venue, nous échangeons sur vos attentes et vos habitudes afin de vous orienter vers la solution la plus adaptée.'),
              ('Combien de temps dure le résultat ?', 'La tenue dépend notamment de vos habitudes au quotidien (café, thé, tabac…). Nos conseils personnalisés vous aident à la prolonger.'),
              ('Comment réserver ?', 'En ligne, en quelques secondes : choisissez la prestation, le jour et l’heure, l’institut vous recontacte pour confirmer.')],
         desc='Blanchiment dentaire esthétique et conseils personnalisés chez Maison Valeria, institut de beauté à Oran. Réservez en ligne.'),
    dict(slug='coiffure-lissages', p=1, nav='Coiffure & lissages', short='Coiffure', title='Coiffure & beauté capillaire',
         h1='Coiffure <em>&amp; lissages.</em>', img='/img/coiffure.webp', thumb='/img/coiffure.webp',
         hero='/img/coiffure.webp',
         sub='Coiffure, brushing, lissages brésilien, indien, japonais et coréen, soins profonds Kérastase.',
         lead='De la mise en beauté aux lissages, des protocoles pensés pour la nature de chaque chevelure.',
         intro=('Chaque chevelure a son histoire. Avant toute prestation, votre diagnostic capillaire offert permet de comprendre l’état de votre cuir chevelu et de vos longueurs, pour choisir la coupe, le lissage ou le soin vraiment adapté.',
                ['Quatre techniques de lissage', 'Soins professionnels Kérastase Paris', 'Diagnostic capillaire offert avant votre soin']),
         svc=[('Coiffure féminine', 'Coupe, coiffage et mise en forme pensés pour votre visage et votre style.'),
              ('Brushing et mise en beauté', 'Un brushing soigné, lisse, volumineux ou ondulé, selon l’occasion.'),
              ('Lissage brésilien', 'Discipline les frisottis et apporte brillance et souplesse, pour des cheveux faciles à coiffer.'),
              ('Lissage indien', 'Un lissage aux actifs nourrissants pour un cheveu lisse, doux et naturellement brillant.'),
              ('Lissage japonais', 'Une technique de lissage durable pour un résultat très lisse, idéale pour les cheveux rebelles.'),
              ('Lissage coréen', 'Un lissage tout en douceur qui préserve le mouvement naturel du cheveu.'),
              ('Soins capillaires profonds', 'Des soins réparateurs et nourrissants, avec les rituels professionnels Kérastase.'),
              ('Protocole personnalisé', 'Un programme sur mesure, construit à partir de votre diagnostic capillaire.')],
         flow=[('Diagnostic', 'Analyse du cuir chevelu par caméra HD, offerte.'), ('Conseil', 'La technique et le soin adaptés à vos cheveux.'), ('Prestation', 'Coiffure, lissage ou soin, réalisé avec précision.'), ('Entretien', 'Une routine Kérastase pour prolonger le résultat.')],
         faq=[('Quel lissage choisir ?', 'Brésilien, indien, japonais ou coréen : chaque technique répond à une nature de cheveu différente. Votre diagnostic capillaire offert nous permet de vous orienter vers la plus adaptée.'),
              ('Combien de temps tient un lissage ?', 'La tenue varie selon la technique, la nature de vos cheveux et leur entretien. Elle vous est précisée lors de votre diagnostic.'),
              ('Quels produits utilisez-vous ?', 'Maison Valeria a fait le choix de Kérastase Paris pour ses soins et rituels capillaires.')],
         desc='Coiffure féminine, brushing, lissages brésilien, indien, japonais et coréen, soins capillaires Kérastase à Oran. Diagnostic capillaire offert.'),
    dict(slug='soins-visage', p=2, nav='Visage & skincare', short='Visage', title='Soins du visage & skincare',
         h1='Une peau <em>révélée.</em>', img=U('1570172619644-dfd03ed5d881', 1100), thumb=U('1570172619644-dfd03ed5d881', 120),
         hero=U('1570172619644-dfd03ed5d881', 1920),
         sub='Soins du visage personnalisés, masques, éclat et hydratation, routines skincare sur mesure.',
         lead='Des soins sur mesure et des routines adaptées à chaque type de peau.',
         intro=('Votre peau change avec les saisons, le rythme de vie et le temps. Nos soins du visage partent de son état réel, mesuré lors du diagnostic esthétique offert, pour vous proposer le soin du moment et une routine simple à suivre chez vous.',
                ['Soins construits selon votre type de peau', 'Diagnostic du visage par appareil spécialisé, offert', 'Une routine claire à reproduire à la maison']),
         svc=[('Soin du visage personnalisé', 'Un soin construit selon l’état et les besoins de votre peau.'),
              ('Masques', 'Des masques ciblés pour purifier, apaiser ou repulper.'),
              ('Soin éclat & hydratation', 'Pour une peau désaltérée, lumineuse et reposée.'),
              ('Routine skincare adaptée', 'Une routine simple et efficace, pensée pour vous.'),
              ('Conseils produits & habitudes de soins', 'Les bons produits et les bons gestes pour prolonger les bienfaits de vos soins.')],
         flow=[('Diagnostic', 'Analyse de la peau par appareil spécialisé, offerte.'), ('Soin', 'Nettoyage, actifs et masque adaptés.'), ('Routine', 'Vos gestes et produits pour la maison.')],
         faq=[('Je ne connais pas mon type de peau, est-ce un problème ?', 'Pas du tout : c’est justement le rôle du diagnostic esthétique du visage, offert à chaque cliente, avant de choisir votre soin.'),
              ('Puis-je combiner un soin du visage avec une autre prestation ?', 'Oui. Indiquez-le simplement dans votre demande de rendez-vous ou dans le message destiné à l’institut.'),
              ('Comment réserver ?', 'En ligne : choisissez le soin, le jour et l’heure. Vous pouvez ajouter le diagnostic du visage offert en un clic.')],
         desc='Soins du visage personnalisés, masques, soin éclat et hydratation, routines skincare à Oran. Diagnostic du visage offert chez Maison Valeria.'),
    dict(slug='diagnostic-beaute', p=3, nav='Diagnostic beauté offert', short='Diagnostic', title='Diagnostics beauté',
         h1='Le diagnostic, <em>offert.</em>', img='/img/diagnostic-coin.webp', thumb='/img/diagnostic-coin.webp',
         hero='/img/diagnostic-coin.webp',
         sub='Diagnostic capillaire par caméra haute définition et diagnostic du visage par appareil spécialisé, offerts à chaque cliente.',
         lead='Des équipements de dernière génération pour comprendre vos besoins avant de choisir un soin.',
         svc=[('Diagnostic capillaire', 'Analyse du cuir chevelu par caméra haute définition, observation de l’état des cheveux, évaluation de vos besoins et recommandation de soins et de produits adaptés.'),
              ('Diagnostic esthétique du visage', 'Analyse de la peau par un appareil spécialisé, évaluation de l’hydratation, des imperfections et des besoins cutanés, recommandations de soins personnalisées.')],
         faq=[('Le diagnostic est-il vraiment gratuit ?', 'Oui. Le diagnostic capillaire et le diagnostic du visage sont offerts à chaque cliente de Maison Valeria.'),
              ('Avec quel appareil est-il réalisé ?', 'L’institut est équipé du X5 Pro Skin Detector, qui réalise une analyse multi-spectrale du visage et du cuir chevelu.'),
              ('Comment en bénéficier ?', 'Réservez-le seul, ou ajoutez-le en option à n’importe quelle prestation lors de votre prise de rendez-vous en ligne.')],
         desc='Diagnostic capillaire par caméra HD et diagnostic du visage X5 Pro offerts chez Maison Valeria, institut de beauté à Oran.'),
    dict(slug='mains-ongles', p=4, nav='Mains & ongles', short='Ongles', title='Beauté des mains & ongles',
         h1='Jusqu’au bout <em>des ongles.</em>', img='/img/ongles.webp', thumb='/img/ongles.webp',
         hero='/img/espace-ongles.webp',
         sub='Manucure, pose d’ongles, nail art et soins esthétiques des mains.',
         lead='Mains soignées et ongles sublimés, jusque dans les finitions.',
         intro=('Des mains soignées disent beaucoup. De la manucure classique au nail art le plus détaillé, chaque prestation est réalisée avec minutie, dans un espace dédié, pour un résultat net et élégant.',
                ['Manucure et soins des mains', 'Pose d’ongles à la forme de votre choix', 'Nail art et finitions personnalisées']),
         svc=[('Manucure & mise en beauté des mains', 'Soin des ongles et des cuticules, mise en forme et pose de couleur.'),
              ('Pose d’ongles', 'Des ongles allongés ou renforcés, à la forme et à la longueur de votre choix.'),
              ('Nail art & finitions personnalisées', 'Motifs, effets et détails pour des ongles qui vous ressemblent.'),
              ('Soins esthétiques des mains', 'Gommage, hydratation et massage pour des mains douces et soignées.')],
         flow=[('Choix', 'Forme, longueur, teinte ou motif.'), ('Préparation', 'Soin des ongles et des cuticules.'), ('Finitions', 'Pose, couleur ou nail art, avec précision.')],
         faq=[('Puis-je venir avec une idée de nail art ?', 'Bien sûr : apportez une photo ou une inspiration, nous l’adaptons à la forme de vos ongles.'),
              ('Combien de temps dure une pose ?', 'Cela dépend de la technique et des finitions choisies. La durée vous est indiquée lors de la confirmation de votre rendez-vous.'),
              ('Comment réserver ?', 'En ligne, en choisissant la prestation, le jour et l’heure qui vous conviennent.')],
         desc='Manucure, pose d’ongles, nail art et soins des mains chez Maison Valeria, institut de beauté à Oran. Réservation en ligne.'),
]
BYP = {u['p']: u for u in UNI}

# ---------------------------------------------------------------- Gabarit
def header(cur):
    dd = ''.join(f'<a href="/{u["slug"]}"><img src="{u["thumb"]}" alt="" loading="lazy"><span>{u["nav"]}</span></a>' for u in UNI)
    dd += '<a href="/kerastase"><img src="/img/kerastase.webp" alt="" loading="lazy"><span>Rituels Kérastase</span></a>'
    def c(k): return ' class="cur"' if cur == k else ''
    nav = (f'<div class="dd"><a href="/#prestations"{c("prestations")}>Prestations</a><div class="ddm">{dd}</div></div>'
           f'<a href="/diagnostic-beaute"{c("diagnostic-beaute")}>Diagnostic offert</a>'
           f'<a href="/tarifs"{c("tarifs")}>Tarifs</a>'
           f'<a href="/institut"{c("institut")}>L’institut</a>'
           f'<a href="/contact"{c("contact")}>Contact</a>')
    msub = ''.join(f'<a href="/{u["slug"]}">{u["nav"]}</a>' for u in UNI) + '<a href="/kerastase">Rituels Kérastase</a>'
    return (f'<header class="hdr"><div class="wrap"><a href="/" class="brand" aria-label="Maison Valeria, accueil">{LOGO}<span><b>MAISON VALERIA</b><small>Institut de beauté</small></span></a>'
            f'<nav class="nav" aria-label="Navigation principale">{nav}</nav>'
            f'<a class="btn btn-dark hdr-cta" href="/rendez-vous">Prendre rendez-vous</a>'
            f'<button class="burger" data-menu aria-label="Menu"><span></span></button></div></header>'
            f'<div class="mnav"><button class="x" data-menu aria-label="Fermer">×</button>'
            f'<a href="/">Accueil</a><a href="/#prestations">Prestations</a><div class="sub">{msub}</div>'
            f'<a href="/diagnostic-beaute">Diagnostic offert</a><a href="/tarifs">Tarifs</a><a href="/institut">L’institut</a><a href="/contact">Contact</a>'
            f'<a href="/rendez-vous" class="btn btn-gold mcta">Prendre rendez-vous</a></div>')

def footer():
    pre = ''.join(f'<li><a href="/{u["slug"]}">{u["nav"]}</a></li>' for u in UNI) + '<li><a href="/kerastase">Rituels Kérastase</a></li>'
    return (f'<footer class="ftr"><div class="wrap">'
            f'<div><a href="/" class="brand">{LOGO}<span><b>MAISON VALERIA</b><small>Institut de beauté</small></span></a>'
            f'<p style="margin-top:18px;max-width:36ch">Beauté, bien-être et soins personnalisés. Ouverture prochaine à Oran.</p></div>'
            f'<div><h5>Prestations</h5><ul>{pre}</ul></div>'
            f'<div><h5>Maison Valeria</h5><ul><li><a href="/institut">L’institut</a></li><li><a href="/tarifs">Tarifs</a></li><li><a href="/rendez-vous">Prendre rendez-vous</a></li><li><a href="/contact">Contact</a></li></ul></div>'
            f'<div><h5>Nous trouver</h5><ul><li>Résidence Hasnaoui, îlot 95<br>Oran, Algérie</li><li style="font-size:12.5px">Horaires et téléphone communiqués prochainement</li><li style="color:var(--gold-l)">Diagnostics beauté offerts</li></ul></div>'
            f'<div class="copy"><span>© <span id="yr">2026</span> Maison Valeria</span><span>Institut de beauté · Oran</span>'
            f'<span class="mv-credit">Site web réalisé par Webminds · <a href="https://www.webminds.dz" target="_blank" rel="noopener">www.webminds.dz</a></span></div>'
            f'</div></footer><a class="btn btn-gold fab" href="/rendez-vous">Réserver</a>')

def page(path, title, desc, body, cur='', og='/img/og.jpg', extra_head='', bodycls='lx'):
    url = SITE + ('/' if path == 'index' else '/' + path)
    t = H.escape(title, quote=True); d = H.escape(desc, quote=True)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{d}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#221912">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_DZ">
<meta property="og:site_name" content="Maison Valeria">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/cg-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/style.css?v={VER}">
{extra_head}</head>
<body class="{bodycls}">
{header(cur)}
<main id="top">
{body}
</main>
{footer()}
<script src="/assets/app.js?v={VER}" defer></script>
</body>
</html>
'''

def ph(img, eyebrow, h1, p, crumbs, acts='', short=False):
    cr = '<a href="/">Accueil</a>' + ''.join(f'<span>{c}</span>' if not isinstance(c, tuple) else f'<span><a href="{c[1]}">{c[0]}</a></span>' for c in crumbs)
    return (f'<section class="ph{" short" if short else ""}"><img class="bg" src="{img}" alt="" fetchpriority="high">'
            f'<div class="wrap"><nav class="crumb" aria-label="Fil d’Ariane">{cr}</nav><span class="eyebrow">{eyebrow}</span>'
            f'<h1>{h1}</h1><p>{p}</p>' + (f'<div class="acts">{acts}</div>' if acts else '') + '</div></section>')

def faq(items):
    return '<div class="faq">' + ''.join(f'<details class="rv"><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'

def faq_ld(items):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}, ensure_ascii=False) + '</script>\n'

def xlinks(skip):
    items = [u for u in UNI if u['slug'] != skip]
    if skip != 'kerastase' and len(items) > 3:
        items = items[:3]
    out = ''.join(f'<a href="/{u["slug"]}" class="rv"><img src="{u["img"]}" alt="{u["title"]}" loading="lazy"><span><small>Univers</small>{u["title"]}</span></a>' for u in items)
    if skip != 'kerastase':
        out += '<a href="/kerastase" class="rv"><img src="/img/kerastase.webp" alt="Rituels Kérastase" loading="lazy"><span><small>Rituels</small>Kérastase Paris</span></a>'
    return ('<section class="sec alt"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Explorer</span>'
            '<h2 style="margin-top:14px">Les autres <em>univers.</em></h2></div><p class="lead">Cinq univers de soin réunis sous un même toit, à Oran.</p></div>'
            f'<div class="xl">{out}</div></div></section>')

def cta(title='Réservez <em>votre moment.</em>', text='Choisissez votre soin et votre créneau en moins d’une minute. Le diagnostic beauté est offert.', code=''):
    db = f' data-book="{code}"' if code else ''
    return (f'<section class="ctab"><div class="wrap rv"><span class="eyebrow">Rendez-vous en ligne</span><h2>{title}</h2><p>{text}</p>'
            f'<div class="acts"><a href="/rendez-vous" class="btn btn-gold"{db}>Prendre rendez-vous {ARR}</a>'
            f'<a href="/diagnostic-beaute" class="btn btn-line">Le diagnostic offert</a></div></div></section>')

def diag_band():
    return ('<section class="sec"><div class="wrap"><div class="dgb rv"><div class="t"><span class="eyebrow">Notre particularité</span>'
            '<h2 style="margin-top:14px">Un diagnostic beauté <em>offert.</em></h2>'
            '<p>Avant chaque soin, comprenez vos besoins grâce à nos technologies avancées : analyse du cuir chevelu par caméra haute définition et analyse de la peau par appareil spécialisé.</p>'
            f'<a href="/diagnostic-beaute" class="btn btn-gold">Découvrir le diagnostic {ARR}</a><span class="zero">0 DA</span></div>'
            '<div class="im"><img src="/img/diagnostic-x5.webp" alt="X5 Pro Skin Detector, diagnostic visage et cuir chevelu" loading="lazy"></div></div></div></section>')

# ---------------------------------------------------------------- Accueil
def booking_section(head=True):
    s = part('rdv')
    s = s.replace('<p class="sub" style="margin-top:16px;font-size:12.5px">Démonstration : aucune donnée n’a été enregistrée.</p>', '<div id="bkAct"></div>')
    s = re.sub(r'<div class="bk-nav" id="bkNav"[^>]*>', '<div class="bk-nav" id="bkNav">', s)
    s = s.replace('<button class="back" id="bkBack" style="visibility: hidden;">', '<button type="button" class="back" id="bkBack">')
    s = s.replace('<button class="btn btn-gold" id="bkNext" disabled="">', '<button type="button" class="btn btn-gold" id="bkNext" disabled>')
    s = s.replace('<button class="btn btn-line" id="bkAgain"', '<button type="button" class="btn btn-line" id="bkAgain"')
    if not head:
        s = re.sub(r'<div class="rdv-head rv">.*?</div>', '', s, count=1, flags=re.S)
    return s

def home():
    hx = part('hx').replace('href="#rendez-vous"', 'href="/rendez-vous"').replace('href="#diagnostic" class="btn bg2" data-book="3:0"', 'href="/diagnostic-beaute" class="btn bg2"')
    hx = hx.replace('src="img/', 'src="/img/').replace('<section class="hx" id="top">', '<section class="hx" aria-label="Maison Valeria en images">')
    hx = hx.replace('<div class="s on"><img src="/img/accueil.webp" alt="">', '<div class="s on"><img src="/img/accueil.webp" alt="Accueil de l’institut Maison Valeria à Oran" fetchpriority="high">')
    ix = part('ix')
    video = ('<section class="mvv" id="video" aria-label="Vidéo de présentation"><div class="mvv-in"><span class="mvv-k">En images</span>'
             '<h2>Découvrez <em>Maison Valeria</em></h2><p class="mvv-sub">Cinq univers de soin et un diagnostic beauté offert, en quarante secondes.</p>'
             '<div class="mvv-frame"><video muted loop playsinline preload="none" poster="/video/poster.webp" disablepictureinpicture controlslist="nodownload noplaybackrate">'
             '<source src="/video/maison-valeria.mp4" type="video/mp4"></video>'
             '<div class="mvv-ctl"><button type="button" class="mvv-pp" aria-label="Lecture"></button><button type="button" class="mvv-rs" aria-label="Revoir depuis le début"><svg viewBox="0 0 24 24"><path d="M12 5V1L7 6l5 5V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/></svg></button></div>'
             '<div class="mvv-bar"><i></i></div></div><a class="mvv-cta" href="/diagnostic-beaute">Mon diagnostic offert</a></div></section>')
    cards = ''
    for u in UNI:
        lis = ''.join(f'<li><button type="button" data-book="{u["p"]}:{k}">{n}{" <em>offert</em>" if u["p"] == 3 else ""}<span>Réserver</span></button></li>' for k, (n, _) in enumerate(u['svc']))
        cards += (f'<article class="uc uc{u["p"]} rv"><a class="uc-img" href="/{u["slug"]}"><img src="{u["img"]}" alt="{u["title"]}" loading="lazy"></a>'
                  f'<div class="uc-body"><span class="uc-n">0{u["p"]+1}</span><h3><a href="/{u["slug"]}">{u["title"]}</a></h3><p>{u["lead"]}</p><ul>{lis}</ul>'
                  f'<a class="uc-more" href="/{u["slug"]}">Découvrir l’univers {ARR}</a></div></article>')
    ux = ('<section class="ux" id="prestations"><div class="wrap"><div class="ux-head rv"><div><span class="eyebrow">Prestations</span>'
          '<h2 style="margin-top:14px">Cinq univers <em>de soin.</em></h2></div><p>Touchez un soin pour réserver directement, ou découvrez chaque univers en détail.</p></div>'
          f'<div id="univers">{cards}</div></div></section>')
    kx = part('kx').replace('src="img/', 'src="/img/').replace('<a href="#rendez-vous" class="btn btn-dark kx-btn" data-book="3:0">Diagnostic &amp; rituel sur mesure <span class="arr"></span></a>',
                                                              f'<a href="/kerastase" class="btn btn-dark kx-btn">Découvrir les rituels {ARR}</a>')
    dx = part('dx').replace('src="img/', 'src="/img/').replace('href="#rendez-vous"', 'href="/rendez-vous"')
    dx = dx.replace('<ol class="dsteps" id="dsteps"></ol>', '<ol class="dsteps" id="dsteps"></ol><a href="/diagnostic-beaute" class="more-l">En savoir plus sur le diagnostic ' + ARR + '</a>')
    bx2 = part('bx2').replace('href="#rendez-vous"', 'href="/rendez-vous"')
    gx = part('gx').replace('href="#rendez-vous"', 'href="/rendez-vous"').replace('src="img/', 'src="/img/')
    nx = ('<section class="nx" id="institut"><div class="wrap"><div class="pics rv"><div class="a"><img src="/img/accueil.webp" alt="Accueil de Maison Valeria" loading="lazy"></div>'
          '<div class="b"><img src="/img/devanture.webp" alt="Devanture Maison Valeria" loading="lazy"></div></div>'
          '<div class="rv"><span class="eyebrow">L’institut</span><h2 style="margin-top:14px">Bientôt <em>à Oran.</em></h2>'
          '<p class="lead" style="margin-bottom:12px;color:var(--gold-d)">Résidence Hasnaoui, îlot 95, Oran</p><p class="lead">Maison Valeria réunit sous un même toit la beauté du sourire, la coiffure, les soins du visage, les diagnostics technologiques et la beauté des mains.</p>'
          '<div class="facts"><div class="fact"><b>5</b><span>univers de soins</span></div><div class="fact"><b>2</b><span>diagnostics offerts</span></div>'
          '<div class="fact"><b>4</b><span>techniques de lissage</span></div><div class="fact"><b>Oran</b><span>ouverture prochaine</span></div></div>'
          f'<a href="/institut" class="more-l">Visiter l’institut {ARR}</a></div></div></section>')
    rdv = booking_section(True).replace('L\'institut vous rappelle pour confirmer.', 'L’institut vous recontacte pour confirmer.')
    ld = '<script type="application/ld+json">' + json.dumps({
        "@context": "https://schema.org", "@type": "BeautySalon", "name": "Maison Valeria", "description": "Institut de beauté à Oran : beauté du sourire, coiffure et lissages, soins du visage, diagnostics beauté offerts, mains et ongles.",
        "url": SITE + '/', "image": SITE + '/img/og.jpg', "logo": SITE + '/apple-touch-icon.png',
        "address": {"@type": "PostalAddress", "streetAddress": "Résidence Hasnaoui, îlot 95", "addressLocality": "Oran", "addressCountry": "DZ"},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": u['title']}} for u in UNI]}, ensure_ascii=False) + '</script>\n'
    body = hx + ix + video + ux + kx + dx + bx2 + gx + nx + rdv
    return page('index', 'Maison Valeria · Institut de beauté à Oran', 'Maison Valeria, institut de beauté à Oran : coiffure et lissages, soins du visage, beauté du sourire, mains et ongles. Diagnostic capillaire et visage offerts. Réservation en ligne.', body, '', extra_head=ld)

# ---------------------------------------------------------------- Pages univers
def univers_page(u):
    p = u['p']
    acts = f'<a href="/rendez-vous" class="btn bw" data-book="{p}">Réserver {ARR}</a><a href="/diagnostic-beaute" class="btn bg2">Diagnostic offert</a>'
    if p == 3:
        acts = f'<a href="/rendez-vous" class="btn bw" data-book="3:0">Réserver mon diagnostic {ARR}</a>'
    body = ph(u['hero'], 'Prestations · ' + u['short'], u['h1'], u['sub'], [('Prestations', '/#prestations'), u['title']], acts)
    n = len(u['svc'])
    cards = ''.join(f'<article class="sv rv"><span class="n">{k+1:02d}</span><h3>{t}</h3><p>{d}</p><div class="foot">'
                    f'<span class="tag{" free" if p == 3 else ""}">{"Offert" if p == 3 else "Tarif sur la grille"}</span>'
                    f'<a href="/rendez-vous?s={p}:{k}" class="bk-l" data-book="{p}:{k}">Réserver {ARR}</a></div></article>'
                    for k, (t, d) in enumerate(u['svc']))
    if p == 3:
        dx = part('dx').replace('src="img/', 'src="/img/').replace('href="#rendez-vous"', 'href="/rendez-vous"')
        dx = dx.replace('<h2 style="margin-top:14px">Le diagnostic beauté, <em>offert.</em></h2>', '<h2 style="margin-top:14px">Comprendre <em>avant de soigner.</em></h2>')
        body += dx
        body += ('<section class="sec alt"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Deux diagnostics</span>'
                 '<h2 style="margin-top:14px">Cheveux <em>&amp; visage.</em></h2></div><p class="lead">Réservez-les seuls, ou ajoutez-les en option à n’importe quelle prestation.</p></div>'
                 f'<div class="svl">{cards}</div></div></section>')
        body += ('<section class="sec"><div class="wrap split"><div class="rv"><span class="eyebrow">Pourquoi un diagnostic</span>'
                 '<h2 style="margin-top:14px">Le bon soin, <em>du premier coup.</em></h2>'
                 '<p class="lead">Choisir un soin ou un produit sans connaître l’état réel de sa peau ou de son cuir chevelu, c’est avancer à l’aveugle. Le diagnostic vous donne une lecture claire de vos besoins.</p>'
                 '<ul class="ticks"><li>Une analyse précise, par technologies avancées</li><li>Des recommandations de soins personnalisées</li><li>Des conseils produits adaptés, notamment Kérastase pour les cheveux</li><li>Offert à chaque cliente</li></ul></div>'
                 '<div class="pic rv"><img src="/img/diagnostic-coin.webp" alt="Espace diagnostic X5 Pro de Maison Valeria" loading="lazy"></div></div></section>')
    else:
        intro, ticks = u['intro']
        tl = ''.join(f'<li>{t}</li>' for t in ticks)
        body += (f'<section class="sec"><div class="wrap split"><div class="rv"><span class="eyebrow">L’univers</span><h2 style="margin-top:14px">{u["title"].replace(" & ", " <em>&amp; ", 1) + "</em>" if " & " in u["title"] else u["title"]}</h2>'
                 f'<p class="lead">{intro}</p><ul class="ticks">{tl}</ul></div>'
                 f'<div class="pic rv"><img src="{u["img"]}" alt="{u["title"]}, Maison Valeria" loading="lazy"></div></div></section>')
        body += (f'<section class="sec alt"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Les prestations</span>'
                 f'<h2 style="margin-top:14px">{n} soin{"s" if n > 1 else ""} <em>sur mesure.</em></h2></div><p class="lead">Touchez « Réserver » pour choisir directement votre créneau.</p></div>'
                 f'<div class="svl{" c3" if n in (3, 5, 6, 8) else ""}">{cards}</div></div></section>')
        fl = ''.join(f'<li class="rv"><b>{a}</b><span>{b}</span></li>' for a, b in u['flow'])
        body += (f'<section class="sec"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Votre visite</span>'
                 f'<h2 style="margin-top:14px">Comment <em>ça se passe.</em></h2></div></div><ol class="flow{" f3" if len(u["flow"]) == 3 else ""}">{fl}</ol></div></section>')
        if p == 1:
            body += part('kx').replace('src="img/', 'src="/img/').replace('<a href="#rendez-vous" class="btn btn-dark kx-btn" data-book="3:0">Diagnostic &amp; rituel sur mesure <span class="arr"></span></a>',
                                                                         f'<a href="/kerastase" class="btn btn-dark kx-btn">Les rituels Kérastase {ARR}</a>')
        body += diag_band()
    body += (f'<section class="sec{" alt" if p == 3 else ""}"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Questions fréquentes</span>'
             f'<h2 style="margin-top:14px">Bon <em>à savoir.</em></h2></div></div>{faq(u["faq"])}</div></section>')
    body += xlinks(u['slug']) + cta(code=f'{p}')
    title = f'{u["title"]} à Oran · Maison Valeria'
    return page(u['slug'], title, u['desc'], body, 'diagnostic-beaute' if p == 3 else 'prestations', extra_head=faq_ld(u['faq']))

# ---------------------------------------------------------------- Kérastase
RIT = [('Discipline', 'Lissage & anti-frisottis', '#E8A7A9', 'Pour les cheveux rebelles et sujets aux frisottis : une chevelure disciplinée, fluide et facile à coiffer.'),
       ('Nutritive', 'Nutrition intense', '#EFE6DA', 'Pour les cheveux secs à très secs : nutrition, douceur et souplesse retrouvées.'),
       ('Résistance', 'Force & réparation', '#1F7C80', 'Pour les cheveux fragilisés ou abîmés : un rituel qui renforce la fibre et répare les longueurs.'),
       ('Blond Absolu', 'Éclat & neutralisation', '#B7A3DC', 'Pour les cheveux blonds, éclaircis ou méchés : un blond lumineux, débarrassé des reflets indésirables.'),
       ('Chronologiste', 'Régénération d’exception', '#1C1712', 'Le rituel d’exception de Kérastase, pour régénérer le cuir chevelu et sublimer tous les types de cheveux.'),
       ('Elixir Ultime', 'Brillance & beauté', '#D9A63E', 'Les huiles sublimatrices iconiques pour une brillance intense et une chevelure magnifiée.')]

def kerastase():
    body = ph('/img/kerastase.webp', 'Rituels capillaires professionnels', 'L’excellence, <em>signée Kérastase.</em>',
              'Maison Valeria a fait le choix de Kérastase Paris, référence prestigieuse des soins capillaires professionnels.',
              [('Prestations', '/#prestations'), 'Kérastase'], f'<a href="/rendez-vous" class="btn bw" data-book="1:6">Réserver un soin {ARR}</a><a href="/diagnostic-beaute" class="btn bg2">Diagnostic offert</a>')
    body += ('<section class="sec"><div class="wrap split"><div class="rv"><span class="eyebrow">Notre choix</span><h2 style="margin-top:14px">Un rituel pour <em>chaque chevelure.</em></h2>'
             '<p class="lead">Parce que chaque chevelure est unique, votre diagnostic capillaire offert vous oriente vers le rituel Kérastase le plus adapté, en institut comme à la maison.</p>'
             '<ul class="ticks"><li>Soins profonds réalisés en institut</li><li>Rituel choisi d’après votre diagnostic capillaire</li><li>Conseils produits pour prolonger les résultats chez vous</li></ul></div>'
             '<div class="pic rv"><img src="/img/accueil.webp" alt="Accueil et corner Kérastase de Maison Valeria" loading="lazy"></div></div></section>')
    cards = ''.join(f'<article class="rt rv"><i style="background:{c}"></i><small>{s}</small><h3>{n}</h3><p>{d}</p></article>' for n, s, c, d in RIT)
    body += ('<section class="sec alt"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Les gammes</span><h2 style="margin-top:14px">Six rituels, <em>six besoins.</em></h2></div>'
             '<p class="lead">Les gammes Kérastase proposées à l’institut, pour répondre à chaque nature et à chaque état de cheveux.</p></div>'
             f'<div class="rits">{cards}</div></div></section>')
    fl = ''.join(f'<li class="rv"><b>{a}</b><span>{b}</span></li>' for a, b in [('Diagnostic', 'Analyse du cuir chevelu par caméra haute définition, offerte.'), ('Rituel en institut', 'Le soin Kérastase adapté, réalisé par l’équipe.'), ('À la maison', 'Votre routine Kérastase pour prolonger les bienfaits.')])
    body += (f'<section class="sec"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Votre rituel</span><h2 style="margin-top:14px">En trois <em>temps.</em></h2></div></div><ol class="flow f3">{fl}</ol></div></section>')
    body += xlinks('kerastase') + cta('Votre rituel <em>sur mesure.</em>', 'Réservez un soin capillaire profond et ajoutez votre diagnostic capillaire offert.', '1:6')
    return page('kerastase', 'Rituels Kérastase à Oran · Maison Valeria', 'Soins capillaires professionnels Kérastase Paris chez Maison Valeria à Oran : Discipline, Nutritive, Résistance, Blond Absolu, Chronologiste, Elixir Ultime.', body, 'prestations')

# ---------------------------------------------------------------- Tarifs
# Pour publier un prix : remplacer None par la chaîne voulue, ex. '4 500 DA' ou 'dès 12 000 DA'
PRIX = {}

def tarifs():
    body = ph('/img/coiffure.webp', 'Tarifs', 'Nos <em>tarifs.</em>', 'L’ensemble des prestations de Maison Valeria. Les diagnostics beauté sont offerts à chaque cliente.', ['Tarifs'],
              f'<a href="/rendez-vous" class="btn bw">Prendre rendez-vous {ARR}</a>', short=True)
    cards = ''
    for u in UNI:
        lis = ''
        for k, (n, _) in enumerate(u['svc']):
            pr = PRIX.get((u['p'], k))
            if u['p'] == 3: v = '<span class="pr free">Offert</span>'
            elif pr: v = f'<span class="pr">{pr}</span>'
            else: v = '<span class="pr soon">bientôt</span>'
            lis += f'<li><a href="/rendez-vous?s={u["p"]}:{k}" data-book="{u["p"]}:{k}">{n}</a><span class="ln"></span>{v}</li>'
        cards += f'<article class="tcard rv"><header><h3>{u["title"]}</h3><a href="/{u["slug"]}">Détails</a></header><ul>{lis}</ul></article>'
    body += ('<section class="sec"><div class="wrap"><div class="tnote rv"><div><b>Grille tarifaire en cours de finalisation</b>'
             '<span>Les prix de chaque prestation seront publiés ici très prochainement, avant l’ouverture de l’institut. Vous pouvez dès maintenant préparer votre rendez-vous en ligne.</span></div></div>'
             f'<div class="tgrid">{cards}</div></div></section>')
    body += diag_band() + cta()
    return page('tarifs', 'Tarifs · Maison Valeria, institut de beauté à Oran', 'Tarifs des prestations de Maison Valeria à Oran : coiffure et lissages, soins du visage, beauté du sourire, mains et ongles. Diagnostics beauté offerts.', body, 'tarifs')

# ---------------------------------------------------------------- L'institut
def institut():
    body = ph('/img/accueil.webp', 'L’institut', 'Maison <em>Valeria.</em>', 'Un institut dédié à la beauté, au bien-être et aux soins personnalisés, qui ouvre bientôt ses portes à Oran.', ['L’institut'],
              f'<a href="/rendez-vous" class="btn bw">Prendre rendez-vous {ARR}</a>')
    body += ('<section class="sec"><div class="wrap split"><div class="rv"><span class="eyebrow">Notre vision</span><h2 style="margin-top:14px">Comprise avant <em>d’être soignée.</em></h2>'
             '<p class="lead">Maison Valeria réunit sous un même toit la beauté du sourire, la coiffure, les soins du visage, les diagnostics par technologies avancées et la beauté des mains.</p>'
             '<p>Notre particularité : chaque cliente peut comprendre ses besoins avant de choisir une prestation ou un produit, grâce à un diagnostic capillaire et un diagnostic du visage offerts.</p>'
             '<div class="facts"><div class="fact"><b>5</b><span>univers de soins</span></div><div class="fact"><b>2</b><span>diagnostics offerts</span></div>'
             '<div class="fact"><b>4</b><span>techniques de lissage</span></div><div class="fact"><b>Oran</b><span>ouverture prochaine</span></div></div></div>'
             '<div class="pic rv"><img src="/img/coiffure.webp" alt="Espace coiffure de Maison Valeria" loading="lazy"></div></div></section>')
    body += ('<section class="sec alt"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Nos engagements</span><h2 style="margin-top:14px">Trois <em>promesses.</em></h2></div></div>'
             '<div class="vals"><div class="rv"><b>i.</b><h3>L’excellence des prestations</h3><p>Des gestes précis et des protocoles adaptés à chaque cliente, du diagnostic jusqu’aux finitions.</p></div>'
             '<div class="rv"><b>ii.</b><h3>Des technologies modernes</h3><p>Caméra haute définition et X5 Pro Skin Detector pour analyser cuir chevelu et peau avant chaque soin.</p></div>'
             '<div class="rv"><b>iii.</b><h3>Une expérience haut de gamme</h3><p>Marbre, lumière dorée et produits professionnels Kérastase : chaque visite est une parenthèse.</p></div></div></div></section>')
    video = ('<section class="mvv" id="video" aria-label="Vidéo de présentation"><div class="mvv-in"><span class="mvv-k">En images</span>'
             '<h2>Découvrez <em>Maison Valeria</em></h2><p class="mvv-sub">Cinq univers de soin et un diagnostic beauté offert, en quarante secondes.</p>'
             '<div class="mvv-frame"><video muted loop playsinline preload="none" poster="/video/poster.webp" disablepictureinpicture controlslist="nodownload noplaybackrate">'
             '<source src="/video/maison-valeria.mp4" type="video/mp4"></video>'
             '<div class="mvv-ctl"><button type="button" class="mvv-pp" aria-label="Lecture"></button><button type="button" class="mvv-rs" aria-label="Revoir depuis le début"><svg viewBox="0 0 24 24"><path d="M12 5V1L7 6l5 5V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/></svg></button></div>'
             '<div class="mvv-bar"><i></i></div></div><a class="mvv-cta" href="/rendez-vous">Prendre rendez-vous</a></div></section>')
    body += video
    gal = [('accueil.webp', 'L’accueil', 'w2 h2'), ('diagnostic-coin.webp', 'L’espace diagnostic', 'h2'), ('cabine.webp', 'La cabine sourire', ''),
           ('espace-ongles.webp', 'L’espace ongles', ''), ('coiffure.webp', 'L’espace coiffure', 'w2'), ('kerastase.webp', 'Le corner Kérastase', 'w2')]
    figs = ''.join(f'<figure class="{c} rv"><img src="/img/{f}" alt="{t}, Maison Valeria" loading="lazy"><figcaption>{t}</figcaption></figure>' for f, t, c in gal)
    body += (f'<section class="sec"><div class="wrap"><div class="sec-head rv"><div><span class="eyebrow">Les lieux</span><h2 style="margin-top:14px">Un cadre <em>d’exception.</em></h2></div>'
             f'<p class="lead">Un aperçu de l’institut, avant de vous y accueillir.</p></div><div class="igal">{figs}</div></div></section>')
    body += xlinks('institut') + cta()
    return page('institut', 'L’institut · Maison Valeria, institut de beauté à Oran', 'Découvrez Maison Valeria, nouvel institut de beauté haut de gamme à Oran : cinq univers de soin, diagnostics par technologies avancées et rituels Kérastase.', body, 'institut', og='/img/og.jpg')

# ---------------------------------------------------------------- Rendez-vous
def rendezvous():
    body = ph('/img/accueil.webp', 'Rendez-vous en ligne', 'Réservez <em>votre moment.</em>', 'Choisissez votre soin, votre créneau, et ajoutez si vous le souhaitez un diagnostic beauté offert.', ['Rendez-vous'], short=True)
    body += booking_section(False)
    body += diag_band()
    return page('rendez-vous', 'Prendre rendez-vous · Maison Valeria, Oran', 'Réservez en ligne votre prestation chez Maison Valeria à Oran : coiffure, lissages, soins du visage, sourire, ongles. Diagnostic beauté offert.', body, '')

# ---------------------------------------------------------------- Contact
MAPS = 'https://www.google.com/maps/search/?api=1&query=R%C3%A9sidence+Hasnaoui+%C3%AElot+95+Oran'

IC = {
    'pin': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    'tel': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    'clock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
}

def contact():
    body = ph('/img/devanture.webp', 'Contact', 'Venir à <em>l’institut.</em>', 'Maison Valeria vous accueille prochainement Résidence Hasnaoui, îlot 95, à Oran.', ['Contact'],
              f'<a href="/rendez-vous" class="btn bw">Prendre rendez-vous {ARR}</a>', short=True)
    body += ('<section class="sec"><div class="wrap"><div class="cgrid">'
             f'<div class="cc rv">{IC["pin"]}<h3>Adresse</h3><p>Résidence Hasnaoui, îlot 95<br>Oran, Algérie</p><a class="v" style="font-size:18px" href="' + MAPS + '" target="_blank" rel="noopener">Itinéraire →</a></div>'
             f'<div class="cc rv">{IC["tel"]}<h3>Téléphone</h3><p>Fixe et mobile de l’institut</p><span class="soon">Numéros communiqués prochainement</span></div>'
             f'<div class="cc rv">{IC["clock"]}<h3>Horaires</h3><p>Accueil sur rendez-vous</p><span class="soon">Horaires définitifs à l’ouverture</span></div>'
             f'<div class="cc rv">{IC["cal"]}<h3>Rendez-vous</h3><p>Réservez votre soin en ligne, en moins d’une minute.</p><a class="v" href="/rendez-vous">Réserver en ligne →</a></div>'
             '</div>'
             '<div class="mapph rv"><img src="/img/s1.webp" alt="Devanture de Maison Valeria à Oran" loading="lazy"><div><span class="eyebrow" style="color:#ebd3ae">Plan d’accès</span>'
             '<h3 style="margin-top:12px">Résidence Hasnaoui, <em style="color:#ebd3ae">îlot 95.</em></h3><p>Oran, Algérie</p><a href="' + MAPS + '" target="_blank" rel="noopener" class="btn bw" style="margin-top:22px;background:#fff;color:var(--espresso)">Ouvrir dans Google Maps ' + ARR + '</a></div></div>'
             '</div></section>')
    body += diag_band() + cta()
    return page('contact', 'Contact · Maison Valeria, institut de beauté à Oran', 'Contactez Maison Valeria, institut de beauté à Oran : adresse, téléphone, horaires et prise de rendez-vous en ligne.', body, 'contact')

# ---------------------------------------------------------------- Build
VER = '1'

def build():
    global VER
    import hashlib
    css = open(os.path.join(SRC, 'style.css'), encoding='utf-8').read() + '\n' + open(os.path.join(SRC, '_video.css'), encoding='utf-8').read() + '\n' + open(os.path.join(SRC, 'extra.css'), encoding='utf-8').read()
    js = open(os.path.join(SRC, 'app.js'), encoding='utf-8').read()
    VER = hashlib.md5((css + js).encode()).hexdigest()[:8]
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets'))
    open(os.path.join(OUT, 'assets/style.css'), 'w', encoding='utf-8').write(css)
    open(os.path.join(OUT, 'assets/app.js'), 'w', encoding='utf-8').write(js)
    pages = {'index': home(), 'kerastase': kerastase(), 'tarifs': tarifs(), 'institut': institut(), 'rendez-vous': rendezvous(), 'contact': contact()}
    for u in UNI: pages[u['slug']] = univers_page(u)
    for k, v in pages.items():
        open(os.path.join(OUT, k + '.html'), 'w', encoding='utf-8').write(v)
    urls = ''.join(f'<url><loc>{SITE}{"/" if k == "index" else "/" + k}</loc><changefreq>monthly</changefreq><priority>{"1.0" if k == "index" else "0.8"}</priority></url>' for k in pages)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    print('pages:', len(pages), 'ver', VER)

if __name__ == '__main__':
    build()
