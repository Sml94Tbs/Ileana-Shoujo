init python:
    import ctypes
    from ctypes import wintypes
    import time
    import random
    import threading

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