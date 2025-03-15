#Version 1.1
import ctypes
import time
import threading
import tkinter as tk
from tkinter import ttk
import pyfiglet
from colorama import init, Fore
import sys
import os
from pynput.mouse import Controller, Button
##MAJ##
import requests
from tqdm import tqdm



# Modifier avec ton utilisateur et ton repo GitHub
GITHUB_USER = "Brainzappp"
GITHUB_REPO = "https://github.com/Brainzappp/PUBG_ASSIST"
VERSION_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
SCRIPT_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/script.py"

def get_online_version():
    """Récupère la version disponible en ligne"""
    try:
        response = requests.get(VERSION_URL)
        return response.text.strip()
    except Exception as e:
        print(f"Erreur lors de la récupération de la version en ligne : {e}")
        return None

def get_local_version():
    """Lit la version locale du script"""
    if not os.path.exists("version.txt"):
        return "0"
    with open("version.txt", "r") as f:
        return f.read().strip()

def download_with_progress(url, file_path):
    """Télécharge un fichier avec une barre de progression"""
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # Taille des blocs (1 Ko)
        
        with open(file_path, "wb") as file, tqdm(
            desc="Téléchargement", total=total_size, unit="o", unit_scale=True
        ) as progress_bar:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))
        return True
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False

def update_script():
    """Télécharge la nouvelle version du script et remplace l'ancien fichier"""
    print("Téléchargement de la mise à jour...")
    if download_with_progress(SCRIPT_URL, sys.argv[0]):
        print("Mise à jour réussie. Redémarrage du script...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    online_version = get_online_version()
    local_version = get_local_version()

    if online_version and online_version > local_version:
        print(f"Nouvelle version détectée ({local_version} → {online_version}) ! Mise à jour en cours...")
        update_script()
    else:
        print("Aucune mise à jour nécessaire.")

    # Écrit la nouvelle version dans le fichier local
    with open("version.txt", "w") as f:
        f.write(online_version)
























































# Vérifier si nous sommes déjà en cours d'exécution sans console
def is_hidden_console_process():
    if sys.platform.startswith('win'):
        try:
            console_window = ctypes.windll.kernel32.GetConsoleWindow()
            return console_window == 0
        except:
            return False
    return False

# Masquer la fenêtre console - approche directe sans relancer le processus
if sys.platform.startswith('win') and not is_hidden_console_process():
    try:
        # Masquer la fenêtre de la console
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        # Essayer de détacher complètement la console
        ctypes.windll.kernel32.FreeConsole()
    except:
        pass

# Rediriger stdout et stderr vers null
class NullWriter:
    def write(self, text): pass
    def flush(self): pass

sys.stdout = NullWriter()
sys.stderr = NullWriter()

# Initialisation
init()
VK_CAPITAL = 0x14
VK_LBUTTON = 0x01
VK_RBUTTON = 0x02
VK_F5 = 0x74  # Ajoutez cette ligne pour définir la touche F5

# Couleurs et constantes
DARK_GRAY = "#222222"
LIGHT_GRAY = "#AAAAAA"
ACTIVE_RED = "#FF4444"
INACTIVE_BLUE = "#4477FF"
HIGHLIGHT_COLOR = "#FF6600"
INDICATOR_COLOR = "#FF0000"  # Rouge pour le rectangle de contrôle de recul

# Couleurs pour les catégories d'armes
CATEGORY_COLORS = {
    "Défaut": "#FFFFFF",
    "AR": "#77CCFF",
    "DMR": "#FFCC44",
    "SR": "#FF9999",
    "SMG": "#99FF99",
    "LMG": "#CC88FF",
    "SG": "#FFBB77",
    "PISTOL": "#77DDDD"
}

# Paramètres de résolution
RESOLUTION_SETTINGS = {
    "1080p": {"width": 415, "height": 69, "y_offset": 28},
    "2K": {"width": 550, "height": 90, "y_offset": 39},
    "4K": {"width": 750, "height": 120, "y_offset": 50}
}

# Variables globales
aim_active = False
rapid_fire_active = False  # Nouvel état pour Rapid Fire
crosshair_active = False  # État pour le viseur
running = True
recoil_window = None
rapid_fire_window = None
crosshair_window = None
correction_level = 2 # Niveau de correction par défaut
selected_weapon = "Défaut" # Arme sélectionnée par défaut
selected_resolution = "2K" # Résolution par défaut

# Controller pour les clics de souris
mouse = Controller()

# Liste de couleurs pour l'indicateur clignotant
RAINBOW_COLORS = [
    "#FF0000", # Rouge
    "#FF7F00", # Orange
    "#FFFF00", # Jaune
    "#00FF00", # Vert
    "#0000FF", # Bleu
    "#4B0082", # Indigo
    "#9400D3" # Violet
]
color_index = 0

# Configurer les valeurs de recul des armes PUBG - VALEURS AMPLIFIÉES (x20)
PUBG_WEAPONS = {
    "Défaut": {"recul": 40, "category": "Défaut"},
    
    # Fusils d'Assaut (AR)
    "M416": {"recul": 37, "category": "AR"},
    "M16A4": {"recul": 43, "category": "AR"},
    "AKM": {"recul": 46, "category": "AR"},
    "SCAR-L": {"recul": 36, "category": "AR"},
    "ACE32": {"recul": 42, "category": "AR"},
    "BERYL": {"recul": 52, "category": "AR"},
    "MK47 MUTANT": {"recul": 41, "category": "AR"},
    "G36C": {"recul": 38, "category": "AR"},
    "GROZA": {"recul": 48, "category": "AR"},
    "QBZ95": {"recul": 38, "category": "AR"},
    "K2": {"recul": 40, "category": "AR"},
    "AUG A3": {"recul": 36, "category": "AR"},

    # Mitraillettes (SMG)
    "BIZON": {"recul": 25, "category": "SMG"},
    "VECTOR": {"recul": 24, "category": "SMG"},
    "MP5K": {"recul": 27, "category": "SMG"},
    "THOMPSON": {"recul": 32, "category": "SMG"},
    "UMP45": {"recul": 30, "category": "SMG"},
    "P90": {"recul": 28, "category": "SMG"},
    

    # Fusils de désignation (DMR)
    "SKS": {"recul": 62, "category": "DMR"},
    "MINI14": {"recul": 45, "category": "DMR"},
    "MK14": {"recul": 70, "category": "DMR"},
    "SLR": {"recul": 65, "category": "DMR"},
    "MK12": {"recul": 48, "category": "DMR"},
    "QBU": {"recul": 47, "category": "DMR"},
    "VSS": {"recul": 30, "category": "DMR"},
    "DRAGUNOV": {"recul": 54, "category": "DMR"},
    
    # Fusils de précision (SR)
    "KAR98K": {"recul": 75, "category": "SR"},
    "M24": {"recul": 73, "category": "SR"},
    "AWM": {"recul": 80, "category": "SR"},
    "MOSIN": {"recul": 76, "category": "SR"},
    "WIN94": {"recul": 60, "category": "SR"},
    "LYNX AMR": {"recul": 90, "category": "SR"},

    # Fusils à pompe (SG)
    "S12K": {"recul": 60, "category": "SG"},
    "S1897": {"recul": 65, "category": "SG"},
    "S686": {"recul": 70, "category": "SG"},
    "DBS": {"recul": 55, "category": "SG"},
    
    # Mitrailleuses légères (LMG)
    "DP-28": {"recul": 52, "category": "LMG"},
    "M249": {"recul": 46, "category": "LMG"},
    "MG3": {"recul": 50, "category": "LMG"},
    
    
    # Pistolets
    "P92": {"recul": 25, "category": "PISTOL"},
    "P1911": {"recul": 28, "category": "PISTOL"},
    "R45": {"recul": 35, "category": "PISTOL"},
    "DEAGLE": {"recul": 40, "category": "PISTOL"},
    "SKORPION": {"recul": 20, "category": "PISTOL"},
    "P18C": {"recul": 18, "category": "PISTOL"}
}

def is_capslock_on():
    return ctypes.windll.user32.GetKeyState(VK_CAPITAL) & 0x0001 != 0

def is_left_mouse_button_pressed():
    return ctypes.windll.user32.GetKeyState(VK_LBUTTON) & 0x8000 != 0

def is_right_mouse_button_pressed():
    return ctypes.windll.user32.GetKeyState(VK_RBUTTON) & 0x8000 != 0

def move_mouse_relative(x, y):
    ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)

def mouse_control():
    global aim_active, running, selected_weapon, selected_resolution

    while running:
        time.sleep(0.01) # Même délai que le script original

        if aim_active:
            # Obtenir la valeur de recul pour l'arme sélectionnée
            weapon_info = PUBG_WEAPONS.get(selected_weapon, PUBG_WEAPONS["Défaut"])
            base_recoil = weapon_info["recul"] / 20.0  # Division par 20 pour retrouver la valeur de base

            # Appliquer un multiplicateur basé sur la résolution
            if selected_resolution == "1080p":
                recoil_multiplier = 1.0  # Base de référence pour 1080p
            elif selected_resolution == "2K":
                recoil_multiplier = 1.5  # Pour 2K, on multiplie par 1.5
            elif selected_resolution == "4K":
                recoil_multiplier = 2.5  # Pour 4K, on multiplie par 2.5
            else:
                recoil_multiplier = 1.0  # Valeur par défaut
            
            # Ajuster le recul en fonction de la résolution
            adjusted_recoil = base_recoil * recoil_multiplier

            if is_left_mouse_button_pressed() and is_right_mouse_button_pressed():
                # Mode renforcé (équivalent à 4 dans le script original)
                moveinX = 0
                moveinY = int(adjusted_recoil * 2)  # 2x le recul ajusté
                move_mouse_relative(moveinX, moveinY)
                time.sleep(0.01)

            elif is_left_mouse_button_pressed():
                # Mode normal (équivalent à 2 dans le script original)
                moveinX = 0
                moveinY = int(adjusted_recoil)  # Recul ajusté
                move_mouse_relative(moveinX, moveinY)
                time.sleep(0.01)


def rapid_fire_control():
    global rapid_fire_active, running
    
    last_click_time = time.time()
    click_interval = 0.1  # Intervalle de tir automatique (en secondes)
    button_pressed_last_check = False
    press_start_time = None  # Moment où le clic a commencé

    while running:
        time.sleep(0.005)  # Vérification fréquente pour meilleure réactivité
        
        button_pressed_now = is_left_mouse_button_pressed()

        if button_pressed_now:
            if press_start_time is None:
                press_start_time = time.time()  # Enregistre le début du maintien
            elif (time.time() - press_start_time) >= 0.12:  # Vérifie si 0.12s se sont écoulées
                if rapid_fire_active:
                    current_time = time.time()
                    if current_time - last_click_time >= click_interval:
                        # Exécuter un clic programmatique
                        mouse.release(Button.left)
                        time.sleep(0.01)
                        mouse.press(Button.left)
                        last_click_time = current_time
        else:
            press_start_time = None  # Réinitialise si le bouton est relâché

        button_pressed_last_check = button_pressed_now

def create_indicator():
    global recoil_window, rapid_fire_window
    
    try:
        # Obtenir les dimensions d'écran
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Obtenir les dimensions selon la résolution sélectionnée
        res_settings = RESOLUTION_SETTINGS.get(selected_resolution, RESOLUTION_SETTINGS["2K"])
        width = res_settings["width"]
        height = res_settings["height"]
        y_offset = res_settings["y_offset"]
        
        # Positionner au centre, en bas de l'écran
        x = (screen_width - width) // 2
        y = screen_height - height - y_offset
        
        # --- FENÊTRE POUR LE CONTRÔLE DE RECUL (CONTOUR ROUGE) ---
        recoil_window = tk.Toplevel(root)
        recoil_window.overrideredirect(True)
        recoil_window.attributes('-topmost', True)
        
        # Rendre la fenêtre transparente
        recoil_window.attributes('-transparent', 'black')
        recoil_window.configure(bg='black')
        recoil_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Créer un canvas pour dessiner le contour
        recoil_canvas = tk.Canvas(recoil_window, bg='black', highlightthickness=0)
        recoil_canvas.pack(fill='both', expand=True)
        
        # Dessiner le contour rouge
        border_width = 3  # Épaisseur du contour
        recoil_canvas.create_rectangle(
            border_width//2, border_width//2, 
            width-border_width//2, height-border_width//2, 
            outline=ACTIVE_RED, width=border_width
        )
        
        # Rendre le fond transparent
        recoil_window.attributes('-transparentcolor', 'black')
        
        # Cacher au démarrage
        recoil_window.withdraw()
        
        # --- FENÊTRE POUR LE RAPID FIRE (CONTOUR JAUNE) ---
        # Légèrement plus grande pour entourer la fenêtre rouge
        rapid_fire_margin = 8  # Légèrement augmenté pour avoir une meilleure visibilité des deux contours
        rapid_width = width + rapid_fire_margin * 2
        rapid_height = height + rapid_fire_margin * 2
        rapid_x = x - rapid_fire_margin
        rapid_y = y - rapid_fire_margin
        
        rapid_fire_window = tk.Toplevel(root)
        rapid_fire_window.overrideredirect(True)
        rapid_fire_window.attributes('-topmost', True)
        
        # Rendre la fenêtre transparente
        rapid_fire_window.attributes('-transparent', 'black')
        rapid_fire_window.configure(bg='black')
        rapid_fire_window.geometry(f"{rapid_width}x{rapid_height}+{rapid_x}+{rapid_y}")
        
        # Créer un canvas pour dessiner le contour
        rapid_fire_canvas = tk.Canvas(rapid_fire_window, bg='black', highlightthickness=0)
        rapid_fire_canvas.pack(fill='both', expand=True)
        
        # Dessiner le contour jaune
        border_width = 3  # Épaisseur du contour
        rapid_fire_canvas.create_rectangle(
            border_width//2, border_width//2, 
            rapid_width-border_width//2, rapid_height-border_width//2, 
            outline="#FFFF00", width=border_width
        )
        
        # Rendre le fond transparent
        rapid_fire_window.attributes('-transparentcolor', 'black')
        
        # Cacher au démarrage
        rapid_fire_window.withdraw()
        
    except Exception as e:
        pass


def create_crosshair():
    global crosshair_window
    
    try:
        # Créer une fenêtre pour le crosshair
        crosshair_window = tk.Toplevel(root)
        crosshair_window.overrideredirect(True)  # Enlever les décorations de fenêtre
        crosshair_window.attributes('-topmost', True)  # Toujours au premier plan
        
        # Obtenir les dimensions d'écran
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        
        # Taille du crosshair
        crosshair_size = 5
        
        # Positionner au centre de l'écran
        x = (screen_width - crosshair_size) // 2
        y = (screen_height - crosshair_size) // 2
        
        # Définir la géométrie de la fenêtre
        crosshair_window.geometry(f"{crosshair_size}x{crosshair_size}+{x}+{y}")
        
        # Créer un cadre avec fond transparent
        frame = tk.Frame(crosshair_window, bg=DARK_GRAY)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Utiliser un Canvas pour dessiner le X
        canvas = tk.Canvas(frame, highlightthickness=0, bg=DARK_GRAY)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Rendre le fond transparent
        crosshair_window.attributes("-transparentcolor", DARK_GRAY)
        
        # Dessiner le X rouge
        canvas.create_line(0, 0, crosshair_size, crosshair_size, fill="#FF0000", width=2)
        canvas.create_line(0, crosshair_size, crosshair_size, 0, fill="#FF0000", width=2)
        
        # Cacher au démarrage
        crosshair_window.withdraw()
        
    except Exception as e:
        pass

def show_recoil_indicator():
    global recoil_window
    if recoil_window:
        try:
            recoil_window.deiconify()
            recoil_window.attributes('-topmost', True)
        except:
            pass

def hide_recoil_indicator():
    global recoil_window
    if recoil_window:
        try:
            recoil_window.withdraw()
        except:
            pass

def show_rapid_fire_indicator():
    global rapid_fire_window
    if rapid_fire_window:
        try:
            rapid_fire_window.deiconify()
            rapid_fire_window.attributes('-topmost', True)
        except:
            pass

def hide_rapid_fire_indicator():
    global rapid_fire_window
    if rapid_fire_window:
        try:
            rapid_fire_window.withdraw()
        except:
            pass

def show_crosshair():
    global crosshair_window
    if crosshair_window:
        try:
            crosshair_window.deiconify()
            crosshair_window.attributes('-topmost', True)
        except:
            pass

def hide_crosshair():
    global crosshair_window
    if crosshair_window:
        try:
            crosshair_window.withdraw()
        except:
            pass

def check_capslock():
    global aim_active, running
    while running:
        try:
            new_state = is_capslock_on()
            if new_state != aim_active:
                aim_active = new_state
                # Utiliser after_idle pour mettre à jour l'interface depuis le thread principal
                if root:
                    root.after_idle(update_interface)
        except:
            pass
        time.sleep(0.1)

def is_f5_pressed():
    return ctypes.windll.user32.GetKeyState(VK_F5) & 0x8000 != 0

def is_f6_pressed():
    return ctypes.windll.user32.GetKeyState(0x75) & 0x8000 != 0  # 0x75 est le code pour F6

def check_f5_key():
    global rapid_fire_active, running
    last_state = False
    while running:
        try:
            current_state = is_f5_pressed()
            # Détecter quand la touche F5 est appuyée puis relâchée (front descendant)
            if last_state and not current_state:
                # Basculer l'état du Rapid Fire
                rapid_fire_active = not rapid_fire_active
                # Mettre à jour l'interface depuis le thread principal
                if root:
                    root.after_idle(update_interface)
            last_state = current_state
        except:
            pass
        time.sleep(0.1)

def check_f6_key():
    global crosshair_active, running
    last_state = False
    while running:
        try:
            current_state = is_f6_pressed()
            # Détecter quand la touche F6 est appuyée puis relâchée (front descendant)
            if last_state and not current_state:
                # Basculer l'état du Crosshair
                crosshair_active = not crosshair_active
                # Mettre à jour l'interface depuis le thread principal
                if root:
                    root.after_idle(update_interface)
            last_state = current_state
        except:
            pass
        time.sleep(0.1)

def update_interface():
    global aim_active, selected_weapon, rapid_fire_active, crosshair_active
    
    try:
        # Mise à jour du label de statut
        if aim_active:
            status_label.config(text="STATUT: ACTIF", foreground=ACTIVE_RED)
            show_recoil_indicator()  # Montrer le rectangle rouge
        else:
            status_label.config(text="STATUT: INACTIF", foreground=INACTIVE_BLUE)
            hide_recoil_indicator()  # Cacher le rectangle rouge
        
        # Gestion du rapid fire indicator
        if rapid_fire_active:
            rapid_fire_button.config(text="Rapid Fire: ON (F5)", bg=ACTIVE_RED, fg="white")
            show_rapid_fire_indicator()  # Montrer le rectangle jaune
        else:
            rapid_fire_button.config(text="Rapid Fire: OFF (F5)", bg="#444444", fg=LIGHT_GRAY)
            hide_rapid_fire_indicator()  # Cacher le rectangle jaune
        
        # Mise à jour de la valeur de correction et effet
        weapon_info = PUBG_WEAPONS.get(selected_weapon, PUBG_WEAPONS["Défaut"])
        weapon_recul = weapon_info["recul"]
        
        correction_value_label.config(
            text=f"{selected_weapon} | Force: {weapon_recul}"
        )
        
        base_val = weapon_recul / 20
        effect_text = f"Conversion: {base_val:.2f} pixels par tick"
        
        # Ajuster le texte en fonction de la résolution
        if selected_resolution == "2K":
            effect_text += f" (x1.5 = {base_val*1.5:.2f} pixels)"
        elif selected_resolution == "4K":
            effect_text += f" (x2.5 = {base_val*2.5:.2f} pixels)"
            
        effect_label.config(text=effect_text)

        # Mise à jour du bouton Crosshair
        if crosshair_active:
            crosshair_button.config(text="Crosshair: ON (F6)", bg=ACTIVE_RED, fg="white")
            show_crosshair()
        else:
            crosshair_button.config(text="Crosshair: OFF (F6)", bg="#444444", fg=LIGHT_GRAY)
            hide_crosshair()
            
        # Mise à jour des boutons d'armes
        for btn in weapon_buttons:
            weapon_name = btn.cget("text")
            if weapon_name == selected_weapon:
                category = PUBG_WEAPONS[weapon_name]["category"]
                color = CATEGORY_COLORS[category]
                btn.config(bg=HIGHLIGHT_COLOR, fg="white")
            else:
                category = PUBG_WEAPONS[weapon_name]["category"]
                color = CATEGORY_COLORS[category]
                btn.config(bg="#444444", fg=color)

        # Mise à jour des boutons de résolution
        for btn in resolution_buttons:
            res_name = btn.cget("text")
            if res_name == selected_resolution:
                btn.config(bg=HIGHLIGHT_COLOR, fg="white")
            else:
                btn.config(bg="#444444", fg=LIGHT_GRAY)
                
    except Exception as e:
        pass

def close_application():
    global running
    running = False
    root.destroy()

def toggle_aim():
    # Maintenant uniquement ferme l'application
    close_application()

def toggle_rapid_fire():
    global rapid_fire_active
    rapid_fire_active = not rapid_fire_active
    update_interface()  # Met à jour l'interface graphique

def toggle_crosshair():
    global crosshair_active
    crosshair_active = not crosshair_active
    update_interface()  # Met à jour l'interface graphique

def select_weapon(weapon_name):
    global selected_weapon
    selected_weapon = weapon_name
    update_interface()

def select_resolution(res_name):
    global selected_resolution
    selected_resolution = res_name
    # Recréer l'indicateur avec les nouvelles dimensions
    recreate_indicator()
    update_interface()

def recreate_indicator():
    global recoil_window, rapid_fire_window
    
    # Fermer les fenêtres existantes
    if recoil_window:
        try:
            recoil_window.destroy()
        except:
            pass
            
    if rapid_fire_window:
        try:
            rapid_fire_window.destroy()
        except:
            pass
    
    # Créer de nouveaux indicateurs avec les dimensions de la résolution sélectionnée
    create_indicator()
    
    # Mettre à jour l'interface pour appliquer les états actuels
    update_interface()

def create_gui():
    global status_label, toggle_button, running
    global correction_value_label, weapon_buttons, effect_label, resolution_buttons
    global rapid_fire_button, crosshair_button
    
    # Fenêtre principale avec couleur de fond très sombre
    main_root = tk.Tk()
    main_root.title("Brain Assist - PUBG Pro")
    main_root.geometry("1600x900")  # Taille initiale un peu plus petite
    main_root.configure(bg='#121212')  # Couleur presque noire
    # Rendu redimensionnable
    main_root.resizable(True, True)
    
    # Configurer le style pour tous les widgets
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#121212')  # Très sombre
    style.configure('TLabel', background='#121212', foreground=LIGHT_GRAY)
    style.configure('TButton', background=DARK_GRAY, foreground='white', borderwidth=1)
    
    # Frame principal avec poids pour redimensionnement
    main_frame = ttk.Frame(main_root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    main_root.grid_columnconfigure(0, weight=1)
    main_root.grid_rowconfigure(0, weight=1)

    # Colonne de gauche pour les infos et contrôles
    left_frame = ttk.Frame(main_frame, padding=10)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Colonne de droite pour la sélection d'armes
    right_frame = ttk.Frame(main_frame, padding=10)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # === COLONNE DE GAUCHE ===

    # Titre avec pyfiglet (converti en label)
    ascii_title = pyfiglet.figlet_format("PUBG ASSIST", font="small")
    title_label = tk.Label(left_frame, text=ascii_title, font=("Courier", 10),
                          justify=tk.LEFT, bg='#121212', fg="white")
    title_label.pack(pady=5)

    ascii_title = pyfiglet.figlet_format("V 1 . 1", font="big")
    title_label = tk.Label(left_frame, text=ascii_title, font=("Courier", 5),
                          justify=tk.LEFT, bg='#121212', fg="yellow")
    title_label.pack(pady=5)

    # SECTION: Informations sur l'état du programme
    status_frame = ttk.Frame(left_frame)
    status_frame.pack(pady=10, fill=tk.X)

    status_label = ttk.Label(status_frame, 
                           text="STATUT: INACTIF", 
                           font=("Arial", 20, "bold"),
                           foreground=INACTIVE_BLUE)
    status_label.pack(pady=2)

    # SECTION: Contrôles pour Rapid Fire et Crosshair
    controls_frame = ttk.Frame(left_frame)
    controls_frame.pack(pady=5, fill=tk.X)

    rapid_fire_button = tk.Button(controls_frame,
                                text="Rapid Fire: OFF (F5)",
                                font=("Arial", 10, "bold"),
                                command=toggle_rapid_fire,
                                bg="#444444", fg=LIGHT_GRAY,
                                bd=0, padx=10, pady=5)
    rapid_fire_button.pack(fill=tk.X, pady=5)

    crosshair_button = tk.Button(controls_frame,
                               text="Crosshair: OFF (F6)",
                               font=("Arial", 10, "bold"),
                               command=toggle_crosshair,
                               bg="#444444", fg=LIGHT_GRAY,
                               bd=0, padx=10, pady=5)
    crosshair_button.pack(fill=tk.X, pady=5)

    # SECTION: Sélection de résolution
    resolution_frame = ttk.Frame(left_frame)
    resolution_frame.pack(pady=5, fill=tk.X)

    resolution_label = ttk.Label(resolution_frame, 
                               text="SÉLECTION DE RÉSOLUTION:", 
                               font=("Arial", 9, "bold"),
                               foreground="#FF9900")
    resolution_label.pack(pady=5)

    resolution_buttons_frame = ttk.Frame(resolution_frame)
    resolution_buttons_frame.pack(fill=tk.X)

    resolution_buttons = []
    for res_name in ["1080p", "2K", "4K"]:
        btn = tk.Button(resolution_buttons_frame, 
                      text=res_name, 
                      command=lambda r=res_name: select_resolution(r),
                      font=("Arial", 9, "bold"),
                      bg="#444444", fg=LIGHT_GRAY,
                      bd=0, padx=5, pady=5)
        btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        resolution_buttons.append(btn)

    # SECTION: Informations sur le comportement
    standard_info_frame = ttk.Frame(left_frame)
    standard_info_frame.pack(pady=10, fill=tk.X)

    standard_info = ttk.Label(standard_info_frame, 
                            text="Made by BrainZap", 
                            font=("Arial", 20, "bold"),
                            foreground="#FF2200")
    standard_info.pack(pady=2)

    standard_desc = ttk.Label(standard_info_frame, 
                           text="Cette application ajuste la compensation en fonction de l'arme sélectionnée.\nLes valeurs affichées correspondent à la force de compensation pour chaque arme.")
    standard_desc.pack(pady=2)

    # Bouton de fermeture - Style personnalisé pour un bouton plus visible
    toggle_button = tk.Button(left_frame, text="FERMER", command=close_application,
                            font=("Arial", 12, "bold"), bd=0,
                            bg="#FF2200", fg="white",
                            activebackground="#FF2200", activeforeground="white",
                            padx=50, pady=20,
                            relief="raised",
                            borderwidth=2)
    toggle_button.pack(pady=10)

    # Crédit



    credit_label = ttk.Label(left_frame, 
                            text="https://discord.gg/VekAbJWPTY", 
                            font=("Arial", 15, "bold"),
                            foreground="yellow")  # Ou foreground="#FFFF00"
    credit_label.pack(pady=5)

    credit_label = ttk.Label(left_frame, 
                           text="PUBG ASSIST PRO EDITION / V 1.0 / 15.03.2025", 
                           font=("Arial", 11),
                           foreground=LIGHT_GRAY)
    credit_label.pack(pady=5)

    credit_label = ttk.Label(left_frame, 
                           text="V 1.1 / 16.03.2025", 
                           font=("Arial", 11),
                           foreground=LIGHT_GRAY)
    credit_label.pack(pady=5)

    # === COLONNE DE DROITE ===
    # Section de sélection d'arme PUBG
    weapons_label = ttk.Label(right_frame, 
                            text="Arme sélectionnée:", 
                            font=("Arial", 20, "bold"),
                            foreground="#FF9900")
    weapons_label.pack(pady=5)

    correction_value_label = ttk.Label(right_frame, 
                                     text=f"{selected_weapon} | Force: {PUBG_WEAPONS[selected_weapon]['recul']}", 
                                     font=("Arial", 20, "bold"),
                                     foreground="red")
    correction_value_label.pack(pady=2)

    # Label pour l'effet de conversion en pixels
    effect_label = ttk.Label(right_frame, 
                           text="Conversion: 2.00 pixels par tick", 
                           font=("Arial", 12),
                           foreground="#77CCFF")
    effect_label.pack(pady=2)

    # Organisation des boutons d'armes par catégorie
    categories = {
        "AR": "FUSILS D'ASSAUT (AR)",
        "DMR": "FUSILS DE DÉSIGNATION (DMR)",
        "SR": "FUSILS DE PRÉCISION (SR)",
        "SMG": "MITRAILLETTES (SMG)",
        "LMG": "MITRAILLEUSES LÉGÈRES (LMG)",
        "SG": "FUSILS À POMPE (SG)",
        "PISTOL": "PISTOLETS",
        "Defaut": "PERSONNALISÉ"
    }

    # Créer un dictionnaire pour organiser les armes par catégorie
    weapons_by_category = {}
    for weapon, info in PUBG_WEAPONS.items():
        cat = info["category"]
        if cat not in weapons_by_category:
            weapons_by_category[cat] = []
        weapons_by_category[cat].append(weapon)

    # Trier les catégories dans un ordre spécifique
    ordered_categories = ["Défaut", "AR", "SMG", "DMR", "SR", "SG", "LMG", "PISTOL"]

    # Pour une meilleure expérience avec le redimensionnement, utiliser un Canvas avec scrollbar
    # Cela permettra de faire défiler si la fenêtre est trop petite mais affichera tout si elle est grande
    weapons_canvas_frame = ttk.Frame(right_frame)
    weapons_canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    weapons_canvas = tk.Canvas(weapons_canvas_frame, bg='#121212', highlightthickness=0)
    weapons_scrollbar = ttk.Scrollbar(weapons_canvas_frame, orient="vertical", command=weapons_canvas.yview)
    weapons_scrollable_frame = ttk.Frame(weapons_canvas)

    # Configure le frame intérieur pour être ajusté à la taille du canvas
    weapons_scrollable_frame.bind(
        "<Configure>",
        lambda e: weapons_canvas.configure(scrollregion=weapons_canvas.bbox("all"))
    )

    # Crée une fenêtre dans le canvas qui contient le frame
    weapons_canvas.create_window((0, 0), window=weapons_scrollable_frame, anchor="nw")
    weapons_canvas.configure(yscrollcommand=weapons_scrollbar.set)

    # Place le canvas et la scrollbar
    weapons_canvas.pack(side="left", fill=tk.BOTH, expand=True)
    weapons_scrollbar.pack(side="right", fill="y")

    # Parcourir les catégories dans l'ordre
    weapon_buttons = []
    for category in ordered_categories:
        if category in weapons_by_category and weapons_by_category[category]:
            # Titre de la catégorie
            category_label = ttk.Label(weapons_scrollable_frame,
                                     text=categories.get(category, category),
                                     font=("Arial", 12, "bold"),
                                     foreground=CATEGORY_COLORS[category])
            category_label.pack(pady=(10, 5), anchor='w')
            
            # Cadre pour les boutons de cette catégorie
            cat_frame = ttk.Frame(weapons_scrollable_frame)
            cat_frame.pack(fill=tk.X, padx=5)
            
            # Créer une grille de boutons (3 par ligne)
            cat_weapons = weapons_by_category[category]
            
            current_row = 0
            current_col = 0
            
            for weapon in cat_weapons:
                color = CATEGORY_COLORS[category]
                btn = tk.Button(cat_frame,
                              text=weapon,
                              command=lambda w=weapon: select_weapon(w),
                              bg="#444444",
                              fg=color,
                              bd=0, padx=5, pady=5,
                              width=13,
                              font=("Arial", 9, "bold"))
                btn.grid(row=current_row, column=current_col, padx=3, pady=3, sticky='w')
                weapon_buttons.append(btn)
                
                current_col += 1
                if current_col >= 6:
                    current_col = 0
                    current_row += 1

    # Ajouter des gestionnaires d'événements de redimensionnement pour adapter l'interface
    def on_frame_configure(event):
        weapons_canvas.configure(scrollregion=weapons_canvas.bbox("all"))

    def on_canvas_configure(event):
        # Modifier la largeur de la fenêtre dans le canvas pour s'adapter au redimensionnement
        weapons_canvas.itemconfig(
            weapons_canvas.find_withtag("all")[0],
            width=event.width
        )

    weapons_scrollable_frame.bind("<Configure>", on_frame_configure)
    weapons_canvas.bind("<Configure>", on_canvas_configure)
    
    # Configurer une fonction pour activer/désactiver la scrollbar en fonction de la taille
    def update_scrollbar_visibility(event=None):
        canvas_height = weapons_canvas.winfo_height()
        frame_height = weapons_scrollable_frame.winfo_reqheight()
        
        if frame_height <= canvas_height:
            # Cacher la barre de défilement si tout le contenu est visible
            weapons_scrollbar.pack_forget()
        else:
            # Afficher la barre de défilement si nécessaire
            weapons_scrollbar.pack(side="right", fill="y")
    
    # Lier la fonction aux événements de configuration
    weapons_canvas.bind("<Configure>", update_scrollbar_visibility)
    weapons_scrollable_frame.bind("<Configure>", update_scrollbar_visibility)

    return main_root





# Programme principal
def main():
    global root, running, selected_resolution
    
    try:
        root = create_gui()
        
        # Créer les indicateurs et le crosshair
        create_indicator()
        create_crosshair()

        # Initialiser l'interface
        update_interface()
        
        # Après l'initialisation, marquer la résolution sélectionnée par défaut
        for btn in resolution_buttons:
            if btn.cget("text") == selected_resolution:
                btn.config(bg=HIGHLIGHT_COLOR, fg="white")
        
        # Lancer les threads de surveillance
        aim_thread = threading.Thread(target=mouse_control, daemon=True)
        capslock_thread = threading.Thread(target=check_capslock, daemon=True)
        f5_thread = threading.Thread(target=check_f5_key, daemon=True)
        f6_thread = threading.Thread(target=check_f6_key, daemon=True)
        rapid_fire_thread = threading.Thread(target=rapid_fire_control, daemon=True)
        
        aim_thread.start()
        capslock_thread.start()
        f5_thread.start()
        f6_thread.start()
        rapid_fire_thread.start()
        
        # Démarrer la boucle principale
        root.mainloop()
        
    except Exception as e:
        running = False
    
    finally:
        running = False

if __name__ == "__main__":
    main()
