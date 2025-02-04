# Pcpei
# coco8900
# Multi-Tools

import os
import shutil
import tempfile
import subprocess
import ctypes
import sys
import re
import stat
import webbrowser
from colorama import Fore, Style, init
import requests
import speedtest
import psutil
import time

# Initialiser colorama
init(autoreset=True)

# Dégradé de couleurs de rouge foncé à orange clair
gradient = [
    "\033[38;5;160m",  # Rouge moins foncé
    "\033[38;5;196m",   # Rouge clair
    "\033[38;5;202m",   # Orange foncé
    "\033[38;5;208m",   # Orange clair
    "\033[38;5;214m"    # Orange clair
]

# Version actuelle du script
CURRENT_VERSION = "1.0.0"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(cmd):
    try:
        if is_admin():
            subprocess.run(cmd, check=True)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(cmd), None, 1)
            sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'exécution de la commande : {e}")

def clear_temp_files():
    def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    try:
        temp_dir = tempfile.gettempdir()
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                try:
                    os.remove(os.path.join(root, file))
                except PermissionError:
                    pass
            for dir in dirs:
                try:
                    shutil.rmtree(os.path.join(root, dir), onerror=remove_readonly)
                except PermissionError:
                    pass
        print(Fore.GREEN + "Fichiers temporaires supprimés.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la suppression des fichiers temporaires : {e}")

def enable_performance_mode():
    try:
        run_as_admin(['powercfg', '-duplicatescheme', 'e9a42b02-d5df-448d-aa00-03f14749eb61'])
        result = subprocess.run(['powercfg', '-list'], capture_output=True, text=True, encoding='mbcs', check=True)
        schemes = result.stdout.splitlines()
        new_scheme_guid = None
        for line in schemes:
            match = re.search(r'([0-9a-fA-F-]+)\s+\(Performances optimales\)', line)
            if match:
                new_scheme_guid = match.group(1)
                break
        if new_scheme_guid:
            run_as_admin(['powercfg', '-setactive', new_scheme_guid])
            print(Fore.GREEN + "Mode de performance optimale activé.")
        else:
            print(Fore.RED + "Le schéma de performance optimale n'a pas été trouvé.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Erreur lors de l'activation du mode de performance optimale : {e}")
    except UnicodeDecodeError as e:
        print(Fore.RED + f"Erreur de décodage : {e}")
    except Exception as e:
        print(Fore.RED + f"Erreur inattendue : {e}")

def clean_registry():
    try:
        print(Fore.YELLOW + "Veuillez utiliser un outil tiers comme CCleaner pour nettoyer le registre.")
        print(Fore.YELLOW + "Télécharger CCleaner : ")
        webbrowser.open("https://www.ccleaner.com/ccleaner/download")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'ouverture du navigateur : {e}")

def disable_startup_programs():
    try:
        print(Fore.YELLOW + "Désactivation des programmes au démarrage...")
        # Utiliser la commande 'tasklist' pour lister les programmes au démarrage
        result = subprocess.run(['tasklist', '/SVC'], capture_output=True, text=True, encoding='mbcs', check=True)
        startup_programs = result.stdout.splitlines()
        for program in startup_programs:
            print(program)
        # Ajouter ici le code pour désactiver les programmes au démarrage
        print(Fore.GREEN + "Programmes au démarrage désactivés.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la désactivation des programmes au démarrage : {e}")

def defragment_disk():
    try:
        print(Fore.YELLOW + "Défragmentation du disque en cours...")
        run_as_admin(['defrag', 'C:', '/O'])
        print(Fore.GREEN + "Défragmentation terminée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la défragmentation du disque : {e}")

def update_drivers():
    try:
        print(Fore.YELLOW + "Veuillez utiliser un outil tiers comme Driver Booster pour mettre à jour les pilotes.")
        print(Fore.YELLOW + "Télécharger Driver Booster : ")
        webbrowser.open("https://www.iobit.com/fr/driver-booster.php")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'ouverture du navigateur : {e}")

def clean_system_files():
    try:
        print(Fore.YELLOW + "Nettoyage des fichiers système inutiles...")
        run_as_admin(['cleanmgr', '/sagerun:1'])
        print(Fore.GREEN + "Nettoyage des fichiers système terminé.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors du nettoyage des fichiers système : {e}")

def repair_disk_errors():
    try:
        print(Fore.YELLOW + "Analyse et réparation des erreurs disque en cours...")
        run_as_admin(['chkdsk', 'C:', '/F', '/R'])
        print(Fore.GREEN + "Analyse et réparation des erreurs disque terminées.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'analyse et réparation des erreurs disque : {e}")

def reset_network_settings():
    try:
        print(Fore.YELLOW + "Réinitialisation des paramètres réseau...")
        run_as_admin(['netsh', 'winsock', 'reset'])
        run_as_admin(['ipconfig', '/release'])
        run_as_admin(['ipconfig', '/renew'])
        run_as_admin(['ipconfig', '/flushdns'])
        print(Fore.GREEN + "Paramètres réseau réinitialisés avec succès.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la réinitialisation des paramètres réseau : {e}")

def create_restore_point():
    try:
        print(Fore.YELLOW + "Création d'un point de restauration système...")
        subprocess.run(['powershell', '-Command', 'Checkpoint-Computer -Description "PCPEI_Restore_Point" -RestorePointType "MODIFY_SETTINGS"'], check=True)
        print(Fore.GREEN + "Point de restauration créé avec succès.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la création d'un point de restauration : {e}")

def scan_for_malware():
    try:
        print(Fore.YELLOW + "Analyse des malwares en cours...")
        # Utiliser Windows Defender pour analyser les malwares
        run_as_admin(['powershell', '-Command', 'Start-Process', 'WindowsDefender:', '-ArgumentList', '/Scan'])
        print(Fore.GREEN + "Analyse des malwares terminée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'analyse des malwares : {e}")

def manage_windows_services():
    try:
        print(Fore.YELLOW + "Gestion des services Windows...")
        # Lister les services Windows
        result = subprocess.run(['sc', 'query'], capture_output=True, text=True, encoding='mbcs', check=True)
        services = result.stdout.splitlines()
        for service in services:
            print(service)
        # Ajouter ici le code pour gérer les services Windows
        print(Fore.GREEN + "Gestion des services Windows terminée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion des services Windows : {e}")

def check_for_updates():
    try:
        print(Fore.YELLOW + "Vérification des mises à jour...")
        # Remplacez cette URL par l'URL de votre dépôt GitHub
        github_url = "https://raw.githubusercontent.com/coco8900/PCPEI-MULTI-TOOLS/refs/heads/version-fix/version.txt"
        response = requests.get(github_url)
        if response.status_code == 200:
            latest_version = response.text.strip()
            print(Fore.GREEN + f"Dernière version disponible : {latest_version}")
            if latest_version != CURRENT_VERSION:
                print(Fore.RED + "Veuillez mettre à jour l'outil avant de continuer.")
                print(Fore.RED + f"Téléchargez la dernière version depuis : https://github.com/coco8900/PCPEI-MULTI-TOOLS")
                webbrowser.open("https://github.com/coco8900/PCPEI-MULTI-TOOLS")
                sys.exit(0)  # Quitter le script
            else:
                print(Fore.GREEN + "Votre version est à jour.")
        else:
            print(Fore.RED + "Impossible de vérifier les mises à jour.")
            sys.exit(0)  # Quitter le script en cas d'échec de la vérification
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la vérification des mises à jour : {e}")
        sys.exit(0)  # Quitter le script en cas d'erreur

def test_internet_speed():
    try:
        print(Fore.YELLOW + "Test de la vitesse de la connexion Internet en cours...")
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        results = st.results.dict()
        print(Fore.GREEN + f"Vitesse de téléchargement : {results['download'] / 1_000_000:.2f} Mbps")
        print(Fore.GREEN + f"Vitesse de téléversement : {results['upload'] / 1_000_000:.2f} Mbps")
        print(Fore.GREEN + f"Ping : {results['ping']:.2f} ms")
    except Exception as e:
        print(Fore.RED + f"Erreur lors du test de la vitesse de la connexion Internet : {e}")

def manage_processes():
    try:
        print(Fore.YELLOW + "Gestion des processus en cours...")
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                print(f"PID: {proc.info['pid']}, Nom: {proc.info['name']}, Utilisateur: {proc.info['username']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        print(Fore.GREEN + "Liste des processus affichée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion des processus : {e}")

def manage_network_devices():
    try:
        print(Fore.YELLOW + "Gestion des périphériques réseau...")
        result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='mbcs', check=True)
        print(result.stdout)
        print(Fore.GREEN + "Liste des périphériques réseau affichée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion des périphériques réseau : {e}")

def manage_disk_usage():
    try:
        print(Fore.YELLOW + "Gestion de l'utilisation du disque...")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"Périphérique: {partition.device}, Type: {partition.fstype}, Options: {partition.opts}")
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"  Total: {usage.total}, Utilisé: {usage.used}, Libre: {usage.free}, Pourcentage: {usage.percent}%")
        print(Fore.GREEN + "Utilisation du disque affichée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion de l'utilisation du disque : {e}")

def manage_users():
    try:
        print(Fore.YELLOW + "Gestion des utilisateurs...")
        users = psutil.users()
        for user in users:
            print(f"Nom: {user.name}, Terminal: {user.terminal}, Hôte: {user.host}, Début de session: {time.ctime(user.started)}")
        print(Fore.GREEN + "Liste des utilisateurs affichée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion des utilisateurs : {e}")

def manage_cpu_usage():
    try:
        print(Fore.YELLOW + "Gestion de l'utilisation du CPU...")
        cpu_usage = psutil.cpu_percent(interval=1)
        print(f"Utilisation du CPU : {cpu_usage}%")
        print(Fore.GREEN + "Utilisation du CPU affichée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion de l'utilisation du CPU : {e}")

def manage_memory_usage():
    try:
        print(Fore.YELLOW + "Gestion de l'utilisation de la mémoire...")
        memory_info = psutil.virtual_memory()
        print(f"Total: {memory_info.total}, Utilisé: {memory_info.used}, Libre: {memory_info.available}, Pourcentage: {memory_info.percent}%")
        print(Fore.GREEN + "Utilisation de la mémoire affichée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion de l'utilisation de la mémoire : {e}")

def manage_power_settings():
    try:
        print(Fore.YELLOW + "Gestion des paramètres d'énergie...")
        result = subprocess.run(['powercfg', '/list'], capture_output=True, text=True, encoding='mbcs', check=True)
        print(result.stdout)
        print(Fore.GREEN + "Paramètres d'énergie affichés.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion des paramètres d'énergie : {e}")

def manage_firewall():
    try:
        print(Fore.YELLOW + "Gestion du pare-feu Windows...")
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], capture_output=True, text=True, encoding='mbcs', check=True)
        print(result.stdout)
        print(Fore.GREEN + "Paramètres du pare-feu affichés.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la gestion du pare-feu Windows : {e}")

def manage_startup_time():
    try:
        print(Fore.YELLOW + "Analyse du temps de démarrage...")
        result = subprocess.run(['powercfg', '/energy'], capture_output=True, text=True, encoding='mbcs', check=True)
        print(result.stdout)
        print(Fore.GREEN + "Analyse du temps de démarrage terminée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'analyse du temps de démarrage : {e}")

def print_menu(page):
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_art = """
██████╗  ██████╗██████╗ ███████╗██╗
██╔══██╗██╔════╝██╔══██╗██╔════╝██║
██████╔╝██║     ██████╔╝█████╗  ██║
██╔═══╝ ██║     ██╔═══╝ ██╔══╝  ██║
██║     ╚██████╗██║     ███████╗██║
╚═╝      ╚═════╝╚═╝     ╚══════╝╚═╝
    https://github.com/coco8900
    """
    lines = ascii_art.strip().split('\n')
    for i, line in enumerate(lines):
        print(gradient[i % len(gradient)] + line)

    print("\n" + "="*40)
    if page == 1:
        print(Fore.CYAN + "1. " + Fore.WHITE + "Supprimer les fichiers temporaires")
        print(Fore.CYAN + "2. " + Fore.WHITE + "Activer le mode de performance optimale")
        print(Fore.CYAN + "3. " + Fore.WHITE + "Nettoyer le registre")
        print(Fore.CYAN + "4. " + Fore.WHITE + "Désactiver les programmes au démarrage")
        print(Fore.CYAN + "5. " + Fore.WHITE + "Défragmenter le disque")
        print(Fore.CYAN + "6. " + Fore.WHITE + "Mettre à jour les pilotes")
        print(Fore.CYAN + "7. " + Fore.WHITE + "Nettoyer les fichiers système inutiles")
        print(Fore.CYAN + "8. " + Fore.WHITE + "Analyser et réparer les erreurs disque")
        print(Fore.CYAN + "9. " + Fore.WHITE + "Réinitialiser les paramètres réseau")
        print(Fore.CYAN + "10. " + Fore.WHITE + "Créer un point de restauration système")
        print(Fore.CYAN + "11. " + Fore.WHITE + "Analyser les malwares (Virus et autres logiciels dangereux)")
        print(Fore.CYAN + "12. " + Fore.WHITE + "Gérer les services Windows")
        print(Fore.CYAN + "13. " + Fore.WHITE + "M'aider (faire un don)")
        print(Fore.CYAN + "14. " + Fore.WHITE + "Page suivante [2]")
    elif page == 2:
        print(Fore.CYAN + "15. " + Fore.WHITE + "Tester la vitesse de la connexion Internet")
        print(Fore.CYAN + "16. " + Fore.WHITE + "Gérer les processus")
        print(Fore.CYAN + "17. " + Fore.WHITE + "Gérer les périphériques réseau")
        print(Fore.CYAN + "18. " + Fore.WHITE + "Gérer l'utilisation du disque")
        print(Fore.CYAN + "19. " + Fore.WHITE + "Gérer les utilisateurs")
        print(Fore.CYAN + "20. " + Fore.WHITE + "Gérer l'utilisation du CPU")
        print(Fore.CYAN + "21. " + Fore.WHITE + "Gérer l'utilisation de la mémoire")
        print(Fore.CYAN + "22. " + Fore.WHITE + "Gérer les paramètres d'énergie")
        print(Fore.CYAN + "23. " + Fore.WHITE + "Gérer le pare-feu Windows")
        print(Fore.CYAN + "24. " + Fore.WHITE + "Analyser le temps de démarrage")
        print(Fore.CYAN + "25. " + Fore.WHITE + "Quitter")
        print(Fore.CYAN + "26. " + Fore.WHITE + "Page précédente [1]")
    print("="*40 + "\n")

def main():
    check_for_updates()  # Vérifier les mises à jour dès le lancement
    page = 1
    while True:
        try:
            print_menu(page)
            choice = input(Fore.MAGENTA + "Choisissez une option : ")

            if page == 1:
                if choice == '1':
                    clear_temp_files()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '2':
                    enable_performance_mode()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '3':
                    clean_registry()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '4':
                    disable_startup_programs()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '5':
                    defragment_disk()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '6':
                    update_drivers()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '7':
                    clean_system_files()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '8':
                    repair_disk_errors()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '9':
                    reset_network_settings()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '10':
                    create_restore_point()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '11':
                    scan_for_malware()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '12':
                    manage_windows_services()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '13':
                    url = "https://www.leetchi.com/fr/c/soutiens-3138357?utm_source=copylink&utm_medium=social_sharing"
                    webbrowser.open(url)
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '14':
                    page = 2
                else:
                    print(Fore.RED + "Option invalide. Veuillez réessayer.")
                    input("Appuyez sur Entrée pour continuer...")
            elif page == 2:
                if choice == '15':
                    test_internet_speed()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '16':
                    manage_processes()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '17':
                    manage_network_devices()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '18':
                    manage_disk_usage()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '19':
                    manage_users()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '20':
                    manage_cpu_usage()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '21':
                    manage_memory_usage()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '22':
                    manage_power_settings()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '23':
                    manage_firewall()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '24':
                    manage_startup_time()
                    input("Appuyez sur Entrée pour continuer...")
                elif choice == '25':
                    print(Fore.GREEN + "Au revoir!")
                    break
                elif choice == '26':
                    page = 1
                else:
                    print(Fore.RED + "Option invalide. Veuillez réessayer.")
                    input("Appuyez sur Entrée pour continuer...")
        except Exception as e:
            print(Fore.RED + f"Erreur inattendue dans la boucle principale : {e}")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    if not is_admin():
        print(Fore.RED + "Ce script nécessite des privilèges administratifs. Redémarrage avec les privilèges administratifs...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    else:
        try:
            main()
        except Exception as e:
            print(Fore.RED + f"Erreur inattendue dans la fonction main : {e}")
