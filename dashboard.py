#----------------Rubrub-maker--------------------------------------------------
#!/usr/bin/env python3

import subprocess
import socket
import requests
import datetime
import time
import os

dossier = os.path.dirname(os.path.abspath(__file__))
chemin_tk = os.path.join(dossier, "dashboard_tk.py")

validité = False
trouve = 0

# ––––––––– LOGO –––––––––––––––––––––––––––––––––––––––––––––––
LOGO = """ 
╔══════════════════════════════════════════╗
║  ██████╗  █████╗ ███████╗██╗  ██╗        ║
║  ██╔══██╗██╔══██╗██╔════╝██║  ██║        ║
║  ██║  ██║███████║███████╗███████║        ║
║  ██║  ██║██╔══██║╚════██║██╔══██║        ║
║  ██████╔╝██║  ██║███████║██║  ██║        ║
║  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝        ║
║         Network Technician Tool          ║
╚══════════════════════════════════════════╝
"""

#–––––––––– COULEURS –––––––––––––––––––––––––––––––––––––––––––
ROUGE   = "\033[31m"
VERT    = "\033[32m"
JAUNE   = "\033[33m"
RESET   = "\033[0m"


#–––––––––– SERVEURS –––––––––––––––––––––––––––––––––––––––––––
serveurs = {
    "Google":       "8.8.8.8",
    "Cloudflare":   "1.1.1.1",
    "OpenDNS":      "208.67.222.222"
}

# ––––––––– DEF DE FONCTIONS –––––––––––––––––––––––––––––––––––

# fonction 1
def outil_ping(ip) :
    subprocess.run(["ping", "-c", "4", ip]) #Linux/Mac sinon remplacer "-c" par "-n"

# fonction 2
def outil_scan(ip, port_debut, port_fin):
    print(f"Scan de {ip} : ports {port_debut} -> {port_fin}")
    for port in range(port_debut, port_fin + 1):
        sock = socket.socket()
        sock.settimeout(0.5)
        resultat = sock.connect_ex((ip, port))
        if resultat == 0:
           print(f"Port {port} : OUVERT")
        sock.close()
    print("Scan terminé")

# fonction 3
def outil_traceroute(ip):
    try:
        subprocess.run(["traceroute", ip])
    except subprocess.SubprocessError:
        print("Erreur : domaine introuvable ou pas de connexion réseau")

# fonction 4
def outil_dns(domaine):
    try:
        ip = socket.gethostbyname(domaine)
        print(f"{domaine} -> {ip}")
    except socket.gaierror:
        print("Erreur : domaine introuvable ou pas de connexion réseau")

# fonction 5
def outil_infos(ip):
    reponse = requests.get(f"http://ip-api.com/json/{ip}")
    data = reponse.json()
    print(f"Pays : {data['country']}")
    print(f"Ville : {data['city']}")
    print(f"FAI : {data['isp']}")

# fonction 6
def outil_vitesse():
    réseaux = 0
    inaccessible = 0
    for nom, ip in serveurs.items():
        debut    = time.time()
        resultat = subprocess.run(["ping", "-c", "1", ip], capture_output=True)
        fin      = time.time()
        latence  = round((fin - debut) * 1000, 2)

        if resultat.returncode == 0:
            print(f"{VERT}{nom} : {latence} ms {RESET}")
        else:
            print(f"{ROUGE}{nom} : inaccessible{RESET}")
            inaccessible += 1

    if inaccessible == len(serveurs):
        print(f"{ROUGE}Réseau down - aucun serveur accessible{RESET}")

            

# fonction 7
def outil_scan_local():
    global trouve
    trouve = 0
    base = input("Base réseau (ex: 192.168.1) : ")
    print("Scan en cours...")
    for i in range(1, 255):
        ip = f"{base}.{i}"
        resultat = subprocess.run(["ping", "-c", "1", "-t", "1", ip], capture_output=True)
        if resultat.returncode == 0:
            print(f"{VERT}Appareil trouvé : {ip}{RESET}")
            trouve += 1
    print(f"Scan terminé – {trouve} appareil(s) trouvé(s)")


# fonction 8
def ouverture_TK():
    print("à venir")

    
# fonction 9
def log(message):
    now = datetime.datetime.now().strftime("%d/%m/%Y/%H:%M:%S")
    with open("historique.txt", "a") as f:
        f.write(f"[{now}] {message}\n")

if __name__ == "__main__":
    while True:
        print(LOGO)
        print("1. Ping")
        print("2. Scan de ports")
        print("3. Traceroute")
        print("4. DNS Lookup")
        print("5. Infos IP (Geo / WHOIS)")
        print("6. vitesse/latence")
        print("7. scan local")
        print("8. logs")
        print("9. interface graphique")
        print("0. Quitter")

        choix = input("Choix : ")


        if choix == "0":
            break
        
        elif choix == "1":

            ip = input("IP : ")
            parties = ip.split(".")

            if len(parties) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parties):
                print(f"{VERT}IP valide{RESET}")
                outil_ping(ip)
                log(f"Ping vers {ip}")
                validité = False

            else:
                print(f"{ROUGE}IP invalide {RESET}")
                validité = False
                break



        elif choix == "2":

            ip          = input("IP : ")
            parties     = ip.split(".")

            if len(parties) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parties):
                print(f"{VERT}IP valide{RESET}")
                validité = True
            else:
                print(f"{ROUGE}IP invalide {RESET}")
                validité = False
                break

            port_debut  = int(input("Port début : "))
            port_fin    = int(input("Port fin : "))

            if validité == True :
                outil_scan(ip, port_debut, port_fin)
                log(f"Scan de {ip} ports {port_debut}-{port_fin}")
                validité = False
            


        elif choix == "3":
            ip          = input("IP : ")
            parties     = ip.split(".")

            if len(parties) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parties):
                print(f"{VERT}IP valide{RESET}")
                validité = True
            else:
                print(f"{ROUGE}IP invalide {RESET}")
                validité = False
                break

            if validité == True :    
                outil_traceroute(ip)
                validité = False



        elif choix == "4":
            domaine = input(" domaine : ")
            outil_dns(domaine)



        elif choix == "5":
            ip = input("IP : ")
            parties = ip.split(".")

            if len(parties) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parties):
                print(f"{VERT}IP valide{RESET}")
                validité = True

            else:
                print(f"{ROUGE}IP invalide {RESET}")
                validité = False
                break
            if validité == True:
                outil_infos(ip)
                validité = False



        elif choix == "6":
            outil_vitesse()

        

        elif choix == "7":
            outil_scan_local()

        
        
        elif choix == "8":
            with open("historique.txt", "r") as f:
                print(f.read())
            print("fin des logs")    

        elif choix == "9":
            subprocess.Popen([sys.executable, chemin_tk], start_new_session=True)

#----------------Rubrub-maker--------------------------------------------------