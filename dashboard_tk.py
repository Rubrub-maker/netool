#----------------Rubrub-maker--------------------------------------------------
#!/usr/bin/env python3

import tkinter as tk
from tkinter import scrolledtext
import subprocess
import socket
import requests
import datetime
import time
import threading

# ––––––––– COULEURS –––––––––––––––––––––––––––––––––––––––––––
BG          = "#111111"
BG2         = "#1e1e1e"
BG3         = "#2a2a2a"
ACCENT      = "#00ff88"
ROUGE       = "#ff4444"
TEXTE       = "#e0e0e0"
TEXTE_DIM   = "#888888"

# ––––––––– SERVEURS –––––––––––––––––––––––––––––––––––––––––––
serveurs = {
    "Google":     "8.8.8.8",
    "Cloudflare": "1.1.1.1",
    "OpenDNS":    "208.67.222.222"
}

# ––––––––– UTILITAIRES –––––––––––––––––––––––––––––––––––––––

def valider_ip(ip):
    parties = ip.split(".")
    return len(parties) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parties)

def log(message):
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("historique.txt", "a") as f:
        f.write(f"[{now}] {message}\n")

def style_bouton(parent, texte, commande):
    return tk.Button(
        parent, text=texte, command=commande,
        bg=BG3, fg=BG, activebackground=ACCENT, activeforeground=BG,
        font=("Courier", 13, "bold"), width=18, height=3,
        relief="flat", cursor="hand2", bd=0
    )

def style_label(parent, texte, taille=11, couleur=None):
    return tk.Label(parent, text=texte, bg=BG, fg=couleur or TEXTE_DIM, font=("Courier", taille))

def style_entry(parent):
    e = tk.Entry(parent, bg=BG3, fg=TEXTE, insertbackground=ACCENT,
                 font=("Courier", 12), relief="flat", bd=5)
    return e

def style_zone_texte(parent):
    z = scrolledtext.ScrolledText(parent, bg=BG2, fg=ACCENT,
                                  font=("Courier", 11), relief="flat",
                                  height=15, width=60, wrap=tk.WORD)
    return z

def ecrire(zone, texte, couleur=None):
    zone.config(state=tk.NORMAL)
    zone.insert(tk.END, texte + "\n")
    zone.see(tk.END)

def effacer(zone):
    zone.config(state=tk.NORMAL)
    zone.delete("1.0", tk.END)

# ––––––––– FENETRE PRINCIPALE –––––––––––––––––––––––––––––––––

fenetre = tk.Tk()
fenetre.title("DASH — Network Technician Tool")
fenetre.geometry("900x620")
fenetre.configure(bg=BG)
fenetre.resizable(False, False)

# Logo
logo = tk.Label(fenetre, text="DASH  //  Network Technician Tool",
                bg=BG, fg=ACCENT, font=("Courier", 18, "bold"))
logo.pack(pady=(20, 5))

separateur = tk.Frame(fenetre, bg=ACCENT, height=1)
separateur.pack(fill="x", padx=30, pady=(0, 15))

# Grille de boutons
grille = tk.Frame(fenetre, bg=BG)
grille.pack()

outils = [
    ("⬡  Ping",              "popup_ping"),
    ("⬡  Scan de ports",     "popup_scan"),
    ("⬡  Traceroute",        "popup_traceroute"),
    ("⬡  DNS Lookup",        "popup_dns"),
    ("⬡  Infos IP",          "popup_infos"),
    ("⬡  Vitesse / Latence", "popup_vitesse"),
    ("⬡  Scan local",        "popup_scan_local"),
    ("⬡  Logs",              "popup_logs"),
    ("✕  Quitter",           "quitter"),
]

# ––––––––– POPUPS –––––––––––––––––––––––––––––––––––––––––––––

def creer_popup(titre, avec_ip=True, avec_domaine=False):
    popup = tk.Toplevel(fenetre)
    popup.title(titre)
    popup.configure(bg=BG)
    popup.geometry("700x500")
    popup.resizable(False, False)

    tk.Label(popup, text=titre, bg=BG, fg=ACCENT,
             font=("Courier", 15, "bold")).pack(pady=(15, 5))
    tk.Frame(popup, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    champs = {}

    if avec_ip:
        f = tk.Frame(popup, bg=BG)
        f.pack(fill="x", padx=30, pady=3)
        tk.Label(f, text="IP cible :", bg=BG, fg=TEXTE_DIM,
                 font=("Courier", 11), width=14, anchor="w").pack(side="left")
        e = style_entry(f)
        e.pack(side="left", fill="x", expand=True)
        champs["ip"] = e

    if avec_domaine:
        f = tk.Frame(popup, bg=BG)
        f.pack(fill="x", padx=30, pady=3)
        tk.Label(f, text="Domaine :", bg=BG, fg=TEXTE_DIM,
                 font=("Courier", 11), width=14, anchor="w").pack(side="left")
        e = style_entry(f)
        e.pack(side="left", fill="x", expand=True)
        champs["domaine"] = e

    zone = style_zone_texte(popup)
    zone.pack(padx=20, pady=10, fill="both", expand=True)

    return popup, champs, zone

# –– Ping ––
def popup_ping():
    popup, champs, zone = creer_popup("Ping", avec_ip=True)

    def lancer():
        ip = champs["ip"].get().strip()
        effacer(zone)
        if not valider_ip(ip):
            ecrire(zone, "❌ IP invalide")
            return
        ecrire(zone, f"Ping vers {ip}...\n")
        def run():
            r = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
            ecrire(zone, r.stdout or r.stderr)
            log(f"Ping vers {ip}")
        threading.Thread(target=run, daemon=True).start()

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– Scan de ports ––
def popup_scan():
    popup, champs, zone = creer_popup("Scan de ports", avec_ip=True)

    f = tk.Frame(popup, bg=BG)
    f.pack(fill="x", padx=30, pady=3)
    tk.Label(f, text="Port début :", bg=BG, fg=TEXTE_DIM,
             font=("Courier", 11), width=14, anchor="w").pack(side="left")
    e_debut = style_entry(f)
    e_debut.pack(side="left")

    f2 = tk.Frame(popup, bg=BG)
    f2.pack(fill="x", padx=30, pady=3)
    tk.Label(f2, text="Port fin :", bg=BG, fg=TEXTE_DIM,
             font=("Courier", 11), width=14, anchor="w").pack(side="left")
    e_fin = style_entry(f2)
    e_fin.pack(side="left")

    def lancer():
        ip = champs["ip"].get().strip()
        effacer(zone)
        if not valider_ip(ip):
            ecrire(zone, "❌ IP invalide")
            return
        try:
            debut = int(e_debut.get())
            fin   = int(e_fin.get())
        except ValueError:
            ecrire(zone, "❌ Ports invalides")
            return
        ecrire(zone, f"Scan de {ip} : ports {debut} → {fin}\n")
        def run():
            for port in range(debut, fin + 1):
                sock = socket.socket()
                sock.settimeout(0.5)
                if sock.connect_ex((ip, port)) == 0:
                    ecrire(zone, f"  Port {port} : OUVERT")
                sock.close()
            ecrire(zone, "\nScan terminé.")
            log(f"Scan de {ip} ports {debut}-{fin}")
        threading.Thread(target=run, daemon=True).start()

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– Traceroute ––
def popup_traceroute():
    popup, champs, zone = creer_popup("Traceroute", avec_ip=True)

    def lancer():
        ip = champs["ip"].get().strip()
        effacer(zone)
        if not valider_ip(ip):
            ecrire(zone, "❌ IP invalide")
            return
        ecrire(zone, f"Traceroute vers {ip}...\n")
        def run():
            r = subprocess.run(["traceroute", ip], capture_output=True, text=True)
            ecrire(zone, r.stdout or r.stderr)
            log(f"Traceroute vers {ip}")
        threading.Thread(target=run, daemon=True).start()

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– DNS Lookup ––
def popup_dns():
    popup, champs, zone = creer_popup("DNS Lookup", avec_ip=False, avec_domaine=True)

    def lancer():
        domaine = champs["domaine"].get().strip()
        effacer(zone)
        try:
            ip = socket.gethostbyname(domaine)
            ecrire(zone, f"{domaine}  →  {ip}")
            log(f"DNS Lookup : {domaine}")
        except socket.gaierror:
            ecrire(zone, "❌ Domaine introuvable ou pas de connexion réseau")

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– Infos IP ––
def popup_infos():
    popup, champs, zone = creer_popup("Infos IP", avec_ip=True)

    def lancer():
        ip = champs["ip"].get().strip()
        effacer(zone)
        if not valider_ip(ip):
            ecrire(zone, "❌ IP invalide")
            return
        def run():
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                d = r.json()
                ecrire(zone, f"Pays    : {d.get('country', 'N/A')}")
                ecrire(zone, f"Région  : {d.get('regionName', 'N/A')}")
                ecrire(zone, f"Ville   : {d.get('city', 'N/A')}")
                ecrire(zone, f"FAI     : {d.get('isp', 'N/A')}")
                ecrire(zone, f"Org     : {d.get('org', 'N/A')}")
                ecrire(zone, f"Lat/Lon : {d.get('lat', 'N/A')} / {d.get('lon', 'N/A')}")
                log(f"Infos IP : {ip}")
            except Exception as e:
                ecrire(zone, f"❌ Erreur : {e}")
        threading.Thread(target=run, daemon=True).start()

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– Vitesse / Latence ––
def popup_vitesse():
    popup = tk.Toplevel(fenetre)
    popup.title("Vitesse / Latence")
    popup.configure(bg=BG)
    popup.geometry("700x500")

    tk.Label(popup, text="Vitesse / Latence", bg=BG, fg=ACCENT,
             font=("Courier", 15, "bold")).pack(pady=(15, 5))
    tk.Frame(popup, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    zone = style_zone_texte(popup)
    zone.pack(padx=20, pady=10, fill="both", expand=True)

    def lancer():
        effacer(zone)
        ecrire(zone, "Test de latence en cours...\n")
        def run():
            inaccessible = 0
            for nom, ip in serveurs.items():
                debut    = time.time()
                resultat = subprocess.run(["ping", "-c", "1", ip], capture_output=True)
                fin      = time.time()
                latence  = round((fin - debut) * 1000, 2)
                if resultat.returncode == 0:
                    ecrire(zone, f"  ✅ {nom} ({ip}) : {latence} ms")
                else:
                    ecrire(zone, f"  ❌ {nom} ({ip}) : inaccessible")
                    inaccessible += 1
            if inaccessible == len(serveurs):
                ecrire(zone, "\n⚠️  Réseau down — aucun serveur accessible")
            else:
                ecrire(zone, "\nTest terminé.")
            log("Test de latence")
        threading.Thread(target=run, daemon=True).start()

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– Scan local ––
def popup_scan_local():
    popup = tk.Toplevel(fenetre)
    popup.title("Scan réseau local")
    popup.configure(bg=BG)
    popup.geometry("700x500")

    tk.Label(popup, text="Scan réseau local", bg=BG, fg=ACCENT,
             font=("Courier", 15, "bold")).pack(pady=(15, 5))
    tk.Frame(popup, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    f = tk.Frame(popup, bg=BG)
    f.pack(fill="x", padx=30, pady=5)
    tk.Label(f, text="Base réseau :", bg=BG, fg=TEXTE_DIM,
             font=("Courier", 11), width=14, anchor="w").pack(side="left")
    e_base = style_entry(f)
    e_base.insert(0, "192.168.1")
    e_base.pack(side="left", fill="x", expand=True)

    zone = style_zone_texte(popup)
    zone.pack(padx=20, pady=10, fill="both", expand=True)

    def lancer():
        base = e_base.get().strip()
        effacer(zone)
        ecrire(zone, f"Scan de {base}.1 → {base}.254 en cours...\n")
        def run():
            trouve = 0
            for i in range(1, 255):
                ip = f"{base}.{i}"
                r = subprocess.run(["ping", "-c", "1", "-t", "1", ip], capture_output=True)
                if r.returncode == 0:
                    ecrire(zone, f"  ✅ Appareil trouvé : {ip}")
                    trouve += 1
            if trouve == 0:
                ecrire(zone, "❌ Aucun appareil trouvé — réseau down ou base incorrecte")
            else:
                ecrire(zone, f"\nScan terminé — {trouve} appareil(s) trouvé(s)")
            log(f"Scan local sur {base}")
        threading.Thread(target=run, daemon=True).start()

    tk.Button(popup, text="▶  Lancer", command=lancer,
              bg=ACCENT, fg=BG, font=("Courier", 12, "bold"),
              relief="flat", padx=20, pady=6).pack(pady=5)

# –– Logs ––
def popup_logs():
    popup = tk.Toplevel(fenetre)
    popup.title("Historique")
    popup.configure(bg=BG)
    popup.geometry("700x500")

    tk.Label(popup, text="Historique", bg=BG, fg=ACCENT,
             font=("Courier", 15, "bold")).pack(pady=(15, 5))
    tk.Frame(popup, bg=ACCENT, height=1).pack(fill="x", padx=20, pady=(0, 10))

    zone = style_zone_texte(popup)
    zone.pack(padx=20, pady=10, fill="both", expand=True)

    try:
        with open("historique.txt", "r") as f:
            contenu = f.read()
        ecrire(zone, contenu if contenu else "Aucun historique.")
    except FileNotFoundError:
        ecrire(zone, "Aucun historique pour le moment.")

def quitter():
    fenetre.destroy()

# ––––––––– CONSTRUCTION DE LA GRILLE ––––––––––––––––––––––––––

fonctions = [
    popup_ping, popup_scan, popup_traceroute, popup_dns,
    popup_infos, popup_vitesse, popup_scan_local, popup_logs, quitter
]

for i, (label, _) in enumerate(outils):
    rang   = i // 3
    colone = i % 3
    btn = style_bouton(grille, label, fonctions[i])
    btn.grid(row=rang, column=colone, padx=12, pady=8)

# Pied de page
tk.Label(fenetre, text="DASH v1.0  //  Rubrub-maker",
         bg=BG, fg=TEXTE_DIM, font=("Courier", 9)).pack(pady=(10, 5))

fenetre.mainloop()
#----------------Rubrub-maker--------------------------------------------------