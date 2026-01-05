init python:
    import ctypes
    from ctypes import wintypes
    import time
    import random
    import threading
    import subprocess

    # Cette fonction sert à lancer le mouvement "en arrière-plan"
    def move_window_async(x, y, duration):
        # On crée un Thread (un fil d'exécution parallèle)
        t = threading.Thread(target=window_move_smooth, args=(x, y, duration))
        t.daemon = True # Permet au thread de se couper si on ferme le jeu
        t.start()
    
    # On charge les outils Windows
    user32 = ctypes.windll.user32
    
    # --- CONSTANTES WINDOWS (Ne pas toucher) ---
    SWP_NOSIZE = 0x0001
    SWP_NOZORDER = 0x0004
    SWP_NOMOVE = 0x0002
    SWP_FRAMECHANGED = 0x0020
    GWL_STYLE = -16
    WS_POPUP = 0x80000000 # Style sans bordure
    WS_THICKFRAME = 0x00040000
    WS_CAPTION = 0x00C00000 # Style avec bordure
    LWA_COLORKEY = 0x00000001
    GWL_EXSTYLE = -20
    WS_EX_LAYERED = 0x00080000
    SC_CLOSE = 0xF060
    MF_BYCOMMAND = 0x00000000
    MF_ENABLED = 0x00000000
    MF_GRAYED = 0x00000001
    MF_DISABLED = 0x00000002

    # Récupérer l'ID de la fenêtre du jeu
    def get_hwnd():
        return user32.GetActiveWindow()

    # --- FONCTION 1 : BOUGER LA FENÊTRE ---
    def set_window_pos(x, y):
        hwnd = get_hwnd()
        # 0, 0, 0, 0 sont la taille (ignorés grâce à SWP_NOSIZE)
        user32.SetWindowPos(hwnd, 0, int(x), int(y), 0, 0, SWP_NOSIZE | SWP_NOZORDER)

    # --- FONCTION 2 : FAIRE TREMBLER LA FENÊTRE ---
    def shake_window(duration=1.0, intensity=10):
        hwnd = get_hwnd()
        # On récupère la position actuelle pour pouvoir y revenir
        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        start_x = rect.left
        start_y = rect.top
        
        end_time = time.time() + duration
        while time.time() < end_time:
            # Calcul d'une position aléatoire
            dx = random.randint(-intensity, intensity)
            dy = random.randint(-intensity, intensity)
            set_window_pos(start_x + dx, start_y + dy)
            time.sleep(0.02) # Petite pause pour que ce soit visible
            
        # Remet la fenêtre à sa place
        set_window_pos(start_x, start_y)

    # --- FONCTION 3 : RENDRE TRANSPARENT (CHROMA KEY) ---
    # Cette fonction va rendre INVISIBLE une couleur précise (ex: le magenta)
    # Ce qui permet de voir le bureau derrière
    def set_window_transparent(color_key=0xFF00FF): # Magenta par défaut
        hwnd = get_hwnd()
        
        # 1. Enlever les bordures (Mode Popup)
        style = user32.GetWindowLongA(hwnd, GWL_STYLE)
        user32.SetWindowLongA(hwnd, GWL_STYLE, style & ~WS_CAPTION)
        
        # 2. Activer le mode "Layered" (pour la transparence)
        ex_style = user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongA(hwnd, GWL_EXSTYLE, ex_style | WS_EX_LAYERED)
        
        # 3. Définir la couleur qui doit disparaître
        # Note : Windows utilise le format BGR, pas RGB. Donc 0xFF00FF (Magenta) reste pareil.
        user32.SetLayeredWindowAttributes(hwnd, color_key, 0, LWA_COLORKEY)

    # --- FONCTION 4 : RESTAURER LA FENÊTRE ---
    def reset_window():
        hwnd = get_hwnd()
        # Remettre les bordures
        style = user32.GetWindowLongA(hwnd, GWL_STYLE)
        user32.SetWindowLongA(hwnd, GWL_STYLE, style | WS_CAPTION)
        # Désactiver la transparence
        ex_style = user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
        user32.SetWindowLongA(hwnd, GWL_EXSTYLE, ex_style & ~WS_EX_LAYERED)


    # ... (Garde tes imports ctypes et user32 ici) ...

    # Variable pour stocker les raccourcis clavier qu'on va supprimer temporairement
    old_fullscreen_keys = []

    # --- FONCTION 5 : FORCER LE MODE FENÊTRÉ ---
    def force_windowed_mode():
        # Si le joueur est en plein écran
        if preferences.fullscreen:
            # On le passe en faux
            preferences.fullscreen = False
            # On force le moteur à appliquer le changement tout de suite
            renpy.display.interface.set_fullscreen(False)
            
            # Petite pause technique pour laisser Windows redessiner la fenêtre
            # Sinon on risque d'essayer de rendre transparent une fenêtre qui n'est pas encore prête
            import time
            time.sleep(0.2) 

    # --- FONCTION 6 : BLOQUER LE PLEIN ÉCRAN ---
    def lock_fullscreen():
        global old_fullscreen_keys
        # On sauvegarde les touches actuelles (Alt+Enter, F, etc.)
        old_fullscreen_keys = config.keymap['toggle_fullscreen']
        # On vide la liste des touches : le joueur ne peut plus changer de mode
        config.keymap['toggle_fullscreen'] = []

    # --- FONCTION 7 : DÉBLOQUER LE PLEIN ÉCRAN ---
    def unlock_fullscreen():
        global old_fullscreen_keys
        # On remet les touches comme avant
        if old_fullscreen_keys:
            config.keymap['toggle_fullscreen'] = old_fullscreen_keys
    # --- FONCTION : CHANGER LE TITRE ---
    def set_window_title(text):
        try:
            hwnd = get_hwnd()
            # On utilise la version Unicode (W) pour accepter les accents et emojis
            user32.SetWindowTextW(hwnd, text)
        except Exception as e:
            print(f"Erreur changement titre: {e}")

    # --- BONUS : EFFET "TYPEWRITER" DANS LA BARRE ---
    # Écrit le titre lettre par lettre (animation)
    def type_window_title_async(text, delay=0.1):
        def _anim():
            current_str = ""
            for char in text:
                current_str += char
                set_window_title(current_str)
                time.sleep(delay)
        
        # On lance ça en arrière-plan pour ne pas bloquer le jeu
        t = threading.Thread(target=_anim)
        t.daemon = True
        t.start()


# Définir l'image "transparente" (qui sera en fait magenta)
image bg transparent = Solid("#FF00FF")


init python:
    import math

    # --- 1. OBTENIR LA TAILLE DE L'ÉCRAN ---
    # Nécessaire pour savoir où sont les coins de l'écran du joueur
    def get_screen_metrics():
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        return width, height

    # --- 2. FONCTIONS DE MOUVEMENT ---
    
    # SAUT INSTANTANÉ (Glitch / Téléportation)
    # Positions possibles : "center", "top_left", "top_right", "bottom_left", "bottom_right"
    def window_jump_to(position_name="center"):
        screen_w, screen_h = get_screen_metrics()
        
        # On suppose une taille de fenêtre par défaut (ex: 1280x720)
        # Ajuste ceci selon config.screen_width dans options.rpy
        win_w = config.screen_width
        win_h = config.screen_height
        
        target_x, target_y = 0, 0

        if position_name == "center":
            target_x = (screen_w - win_w) / 2
            target_y = (screen_h - win_h) / 2
        elif position_name == "top_left":
            target_x = 0
            target_y = 0
        elif position_name == "top_right":
            target_x = screen_w - win_w
            target_y = 0
        elif position_name == "bottom_left":
            target_x = 0
            target_y = screen_h - win_h
        elif position_name == "bottom_right":
            target_x = screen_w - win_w
            target_y = screen_h - win_h
            
        set_window_pos(int(target_x), int(target_y))

    # GLISSADE FLUIDE (Cinématique)
    # Déplace la fenêtre d'un point A vers B en 'duration' secondes
    def window_move_smooth(target_x, target_y, duration=0.5):
        hwnd = get_hwnd()
        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        
        start_x = rect.left
        start_y = rect.top
        
        start_time = time.time()
        
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            if elapsed >= duration:
                break
                
            # Calcul de la progression (0.0 à 1.0)
            t = elapsed / duration
            # Formule "SmoothStep" pour que ce soit doux au début et à la fin
            t_smooth = t * t * (3 - 2 * t) 
            
            new_x = start_x + (target_x - start_x) * t_smooth
            new_y = start_y + (target_y - start_y) * t_smooth
            
            set_window_pos(int(new_x), int(new_y))
            
            # Petite pause pour ne pas figer le jeu complètement
            # Note: Le jeu sera "en pause" pendant le mouvement
            time.sleep(0.01) 
            
        set_window_pos(int(target_x), int(target_y))

    # LE "KICK" (Rebond sur le Beat)
    # Fait sauter la fenêtre vers le haut et retomber, parfait pour les rythmes
    def window_kick(intensity=50, duration=0.2):
        hwnd = get_hwnd()
        rect = ctypes.wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        
        base_x = rect.left
        base_y = rect.top
        
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                break
            
            # Utilise une courbe Sinus pour monter et descendre
            progress = elapsed / duration
            offset_y = -math.sin(progress * math.pi) * intensity 
            
            set_window_pos(base_x, int(base_y + offset_y))
            time.sleep(0.01)
            
        set_window_pos(base_x, base_y)

    # --- GESTION DES BORDURES WINDOWS ---
    def set_borders(visible=True):
        hwnd = get_hwnd()
        style = user32.GetWindowLongA(hwnd, GWL_STYLE)
        
        if visible:
            new_style = style | WS_CAPTION | WS_THICKFRAME
        else:
            new_style = style & ~WS_CAPTION & ~WS_THICKFRAME
            
        user32.SetWindowLongA(hwnd, GWL_STYLE, new_style)
        
        # --- LA LIGNE CORRIGÉE EST ICI ---
        rect = wintypes.RECT() 
        # ---------------------------------
        
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        
        user32.SetWindowPos(hwnd, 0, 0, 0, width, height+1, SWP_NOMOVE | SWP_NOZORDER)
        user32.SetWindowPos(hwnd, 0, 0, 0, width, height, SWP_NOMOVE | SWP_NOZORDER)


    # Fonction pour agrandir la fenêtre progressivement
    def window_expand_to_fullscreen_logic(duration):
        try:
            hwnd = get_hwnd()
            screen_w, screen_h = get_screen_metrics()
            
            # On part de la taille ACTUELLE de la fenêtre
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            start_w = rect.right - rect.left
            start_h = rect.bottom - rect.top
            
            start_time = time.time()
            
            while True:
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    break
                    
                # Calcul du pourcentage (0.0 à 1.0)
                t = elapsed / duration
                # Lissage (Ease Out) pour que ça ralentisse à la fin
                t = 1 - math.pow(1 - t, 3)
                
                # Interpolation (Lerp)
                current_w = start_w + (screen_w - start_w) * t
                current_h = start_h + (screen_h - start_h) * t
                
                # Calcul pour garder la fenêtre centrée
                pos_x = (screen_w - current_w) / 2
                pos_y = (screen_h - current_h) / 2
                
                # APPLICATION : On change la taille ET la position
                # Note : On N'UTILISE PAS SWP_NOSIZE ni SWP_NOMOVE car on veut tout changer
                user32.SetWindowPos(
                    hwnd, 0, 
                    int(pos_x), int(pos_y), 
                    int(current_w), int(current_h), 
                    SWP_NOZORDER | SWP_SHOWWINDOW
                )
                
                time.sleep(0.010) # 60 FPS environ
                
        except Exception as e:
            # En cas d'erreur, on l'affiche dans la console (Shift+O) pour debug
            print("Erreur dans le thread d'expansion: " + str(e))

init python:
    def expand_window_async(duration=3.0):
        t = threading.Thread(target=window_expand_to_fullscreen_logic, args=(duration,))
        t.daemon = True
        t.start()

init python:
    import random

    # Variable pour contrôler la boucle
    glitch_title_active = False

    # --- LA FONCTION QUI TOURNE EN FOND ---
    def _glitch_title_loop(base_text, intensity=0.05):
        global glitch_title_active
        hwnd = get_hwnd()
        
        while glitch_title_active:
            # On reconstruit la phrase lettre par lettre
            # en choisissant pile ou face pour la majuscule
            new_title = ""
            for char in base_text:
                if random.choice([True, False]):
                    new_title += char.upper()
                else:
                    new_title += char.lower()
            
            # On applique le titre
            try:
                user32.SetWindowTextW(hwnd, new_title)
            except:
                break # Arrête si la fenêtre est fermée
            
            # Pause très courte (l'intensité du glitch)
            time.sleep(intensity)

    # --- COMMANDES POUR LE JEU ---
    
    def start_title_glitch(text="RUN"):
        global glitch_title_active
        # Si un glitch tourne déjà, on ne fait rien pour éviter les bugs
        if glitch_title_active:
            return

        glitch_title_active = True
        # On lance le thread
        t = threading.Thread(target=_glitch_title_loop, args=(text,))
        t.daemon = True
        t.start()

    def stop_title_glitch():
        global glitch_title_active
        # On dit à la boucle de s'arrêter
        glitch_title_active = False
        
        # Petite pause pour être sûr que le thread a fini
        time.sleep(0.1)
        
        # On remet le titre normal du jeu (défini dans options.rpy)
        set_window_title(config.window_title)

    def set_close_button_enabled(enabled=True):
        hwnd = get_hwnd()
        # On récupère le menu système (là où il y a Fermer, Réduire, Agrandir)
        h_menu = user32.GetSystemMenu(hwnd, False)
        
        if enabled:
            flag = MF_ENABLED
        else:
            flag = MF_DISABLED | MF_GRAYED
            
        # On applique le changement au bouton "Fermer" (SC_CLOSE)
        user32.EnableMenuItem(h_menu, SC_CLOSE, MF_BYCOMMAND | flag)
default can_quit_game = True

init python:
    # Cette fonction est appelée par Ren'Py quand le joueur essaie de quitter
    def check_quit_request():
        if can_quit_game:
            return Quit() # Comportement normal (Ouvre le menu "Voulez-vous quitter ?")
        else:
            # Si c'est bloqué, on peut faire parler le perso (voir Bonus plus bas)
            # Ou juste ne rien faire
            return None 

# On remplace l'action par défaut de Ren'Py par la nôtre
define config.quit_action = check_quit_request

init python:
    
    
    # Fonction pour envoyer une notification Windows (Toast)
    def send_windows_notification(title, message):
        # Le code PowerShell magique pour créer une notification native Windows 10/11
        # On utilise le template 'ToastText02' (Titre en gras + Texte en dessous)
        ps_script = f"""
        [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime] | Out-Null
        $Template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
        
        $TextElements = $Template.GetElementsByTagName("text")
        $TextElements[0].AppendChild($Template.CreateTextNode("{title}")) | Out-Null
        $TextElements[1].AppendChild($Template.CreateTextNode("{message}")) | Out-Null
        
        $Notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Ton Nom de Jeu")
        $Notifier.Show([Windows.UI.Notifications.ToastNotification]::new($Template))
        """

        # On exécute ça discrètement (sans fenêtre noire cmd.exe)
        try:
            # CREATE_NO_WINDOW permet de cacher la fenêtre PowerShell
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            subprocess.Popen(
                ["powershell", "-Command", ps_script],
                startupinfo=startupinfo,
                creationflags=0x08000000 # CREATE_NO_WINDOW
            )
        except Exception as e:
            print(f"Impossible d'envoyer la notification: {e}")

    # Variante : Notification avec un délai (pour laisser le temps de minimiser le jeu)
    def notify_delayed(title, message, delay=2.0):
        def _thread():
            time.sleep(delay)
            send_windows_notification(title, message)
        
        t = threading.Thread(target=_thread)
        t.daemon = True
        t.start()
    # --- METHODE 1 : LES ERREURS WINDOWS (Natif) ---
    # Styles : 0=OK, 1=OK/Annuler, 16=Erreur Critique (X Rouge), 32=Question, 48=Attention
    def _show_message_box(title, message, style=16):
        # MessageBoxW est la fonction native de Windows
        # Le dernier paramètre (style) définit l'icône et les boutons
        ctypes.windll.user32.MessageBoxW(0, message, title, style)

    def spawn_error_popup(title="Fatal Error", message="Corrupted Data", style=16):
        # On lance dans un thread pour que le jeu ne se fige pas en attendant le clic "OK"
        t = threading.Thread(target=_show_message_box, args=(title, message, style))
        t.daemon = True
        t.start()

    # --- METHODE 2 : FENÊTRE PERSONNALISÉE (Tkinter) ---
    def _create_custom_window(title, text_content, width=300, height=100, x=None, y=None):
        try:
            root = tk.Tk()
            root.title(title)
            
            # Taille et Position
            if x is None or y is None:
                # Si pas de position, on centre un peu au hasard
                import random
                screen_w, screen_h = get_screen_metrics()
                x = random.randint(100, screen_w - 400)
                y = random.randint(100, screen_h - 400)
            
            root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
            
            # Style "Horreur" (Fond noir, texte rouge)
            root.configure(bg='black')
            label = tk.Label(root, text=text_content, fg='red', bg='black', font=("Arial", 12, "bold"))
            label.pack(expand=True)
            
            # Empêcher le redimensionnement
            root.resizable(False, False)
            
            # On garde la fenêtre ouverte 5 secondes puis on détruit
            root.after(5000, root.destroy)
            
            root.mainloop()
        except:
            pass

    def spawn_custom_black_window(title, message):
        # Script PowerShell pour créer une fenêtre noire effrayante
        # car on ne peut pas utiliser Tkinter dans Ren'Py
        ps_script = f"""
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        
        $form = New-Object System.Windows.Forms.Form
        $form.Text = "{title}"
        $form.BackColor = [System.Drawing.Color]::Black
        $form.Width = 400
        $form.Height = 200
        $form.StartPosition = "CenterScreen"
        $form.FormBorderStyle = "FixedDialog"
        $form.MaximizeBox = $false
        
        $label = New-Object System.Windows.Forms.Label
        $label.Text = "{message}"
        $label.ForeColor = [System.Drawing.Color]::Red
        $label.Font = New-Object System.Drawing.Font("Consolas", 14, [System.Drawing.FontStyle]::Bold)
        $label.AutoSize = $false
        $label.TextAlign = "MiddleCenter"
        $label.Dock = "Fill"
        
        $form.Controls.Add($label)
        $form.ShowDialog() | Out-Null
        """

        def _run():
            try:
                # On cache la fenêtre de commande noire
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                subprocess.Popen(
                    ["powershell", "-Command", ps_script],
                    startupinfo=startupinfo,
                    creationflags=0x08000000
                )
            except: pass

        t = threading.Thread(target=_run)
        t.daemon = True
        t.start()

    def _show_message_box(title, message, style=16):
    # MessageBoxW est la fonction native de Windows
    # Elle affiche une vraie fenêtre système par-dessus le jeu
        ctypes.windll.user32.MessageBoxW(0, message, title, style)

    def spawn_error_popup(title="Fatal Error", message="Corrupted Data", style=16):
        # On lance dans un thread pour que le jeu ne se fige pas en attendant le clic "OK"
        # Si on ne met pas de thread, le jeu s'arrête tant que le joueur n'a pas fermé le popup !
        t = threading.Thread(target=_show_message_box, args=(title, message, style))
        t.daemon = True
        t.start()