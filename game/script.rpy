# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"
# Variable pour savoir si le joueur a le droit de sortir




# Déclarez les personnages utilisés dans le jeu.
define e = Character('Eileen', color="#c8ffc8")
define nv = Character('Ileana' ,kind=nvl, color="#ffc8c8")
define narrator = nvl_narrator
define a = Character(None, screen="say_anime", what_prefix="{cps=0}", what_suffix="{/cps}")
default current_act = 1
default current_scene = "Introduction"
image ok = "sfx/01 A.jpg"
# Le jeu commence ici
label start:
    $ rpc_update_game(current_act, current_scene)
    $ quick_menu = False
    hide screen main_menu_effects
    stop music fadeout 2.0
    with dissolve_all_scene
    window hide
    pause 1.0
    show text "MSSML Present"
    with dissolve
    pause (5)
    scene black with dissolve_all_scene
    pause 0.5
    window auto
    $ quick_menu = True


    $ start_title_glitch("RUN RUN RUN")
    e "Vous venez de créer un nouveau jeu Ren'Py."

    $ stop_title_glitch()

    e "Après avoir ajouté une histoire, des images et de la musique, vous pourrez le présenter au monde entier !"

    $ quick_menu = False

    scene white

    a 'Bonne chance pour votre projet de jeu !'

    a "Si la phrase est vraiment très longue, elle devrait se centrer parfaitement et rester lisible grâce au contour noir épais."

    scene ok

    $ set_window_title("Sonic.exe")

    # 2. Messages cryptiques
    $ set_window_title("AIDE MOI")
    pause 1.0
    $ set_window_title("IL EST DERRIERE TOI")
    pause 1.0

    $ type_window_title_async("DON'T LOOK...", 0.2)

    $ quick_menu = True

    e "yes"

    show anneko at t_center

    "Anneko" "Et là je suis tout près !"

    show anneko at t_left
    
    $ type_window_title_async("DON'T LOOK...", 0.2)


    "Anneko" "Coucou"

    show anneko at t_right

    

    "Anneko" "Je suis là !"

    show anneko at t_center_close

    "Anneko" "Je suis toute proche !"

    show anneko at t_left_close

    $ set_window_title("")

    narrator "The End."
    narrator "Je ne pense que cela soit du à une erreu de ta partujguguyyfgufffttyfrtytfyftyftftfyfytftyftftyfftyftfyfyttrtrtrtrturyturytrutyrutyrutyrutryutryutry"
    narrator "Je ne pense que cela soit du à une erreu de ta part"
    narrator "Il me faudrait surment un endroit ou amener ces ames égaréés"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    $ gui.nvl_bg_bool = False
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    scene white
    $ set_window_title(config.window_title)
    $ gui.nvl_bg_bool = True
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"

    "Anneko" "Il se passe quoi ?"

    # --- EFFET 1 : TREMBLEMENT ---
    "Anneko" "La fenêtre... elle tremble !"
    $ current_scene = "Coucou Toi!"
    $ rpc_update_game(current_act, current_scene)
    show anneko at t_center
    $ force_windowed_mode()
    $ lock_fullscreen()

    "Anneko" "C'est bizarre..."
    "Anneko" "Est-ce que tu vois mon vrai visage ?"
    $ shake_window(2.0, 20) # Tremble pendant 2 sec, intensité 20px

    scene bg transparent

    "Anneko" "Ahhh ! Mon visage a disparu !"

    $ set_window_transparent(0xFF00FF)

    "Anneko" "Je suis libre !"

    $ reset_window()

    "Anneko" "Merci de m'avoir libérée !"

    $ unlock_fullscreen()

    "Anneko" "C'est revenu"
    "Anneko" "Voilà, tout est normal."

    jump meta_event
    return

label meta_event:
    
    e "Je vais essayer de sortir d'ici..."

    # --- ÉTAPE COMMUNE : Forcer le mode fenêtré ---
    # On le fait dans les deux cas, car même pour le placeholder, 
    # c'est plus stylé si la fenêtre n'est pas en plein écran.
    $ force_windowed_mode()
    $ lock_fullscreen()
    
    # Petit bruitage tech
    play sound "audio/glitch.ogg"


    # --- BIFURCATION : Vrai Hack vs Placeholder ---
    
    if persistent.allow_transparent_window:
        # === PLAN A : LA TOTALE (Pour les bons PC) ===
        scene bg transparent
        $ set_window_transparent(0xFF00FF)
        
        e "Tu me vois sur ton bureau ?"

    else:
        # === PLAN B : LE PLACEHOLDER (Pour ton CPU) ===
        # Au lieu de rendre transparent, on affiche une image qui "imite" un bureau ou un glitch
        scene bg placeholder_desktop with Dissolve(0.2)
        
        e "Je prends le contrôle de ton écran !"


    # --- MOUVEMENT DE FENÊTRE (Fonctionne souvent même avec un petit CPU) ---
    # Tu peux laisser ça actif même en mode placeholder pour garder l'immersion
    
    $ shake_window(1.0, 10)
    
    if persistent.allow_transparent_window:
        e "Je suis libre !"
    else:
        e "Je suis partout !"


    # --- DÉPLACEMENT (Optionnel) ---
    # Si tu veux que la fenêtre bouge même avec le placeholder :
    e "Je vais me déplacer à gauche."
    $ set_window_pos(100, 100)
    
    # ... dialogue ...


    # --- RETOUR A LA NORMALE ---
    
    # Important : On appelle reset_window() dans TOUS les cas par sécurité
    $ reset_window() 
    
    scene bg classroom
    $ unlock_fullscreen()

    e "Retour à la réalité."
    jump dance_event
    return

label dance_event:
    
    # Sécurité (toujours !)
    $ force_windowed_mode()
    
    e "Accroche-toi, ça va bouger !"
    
    # --- PHASE 1 : LE BEAT (Bumping) ---
    # Simule les basses de la musique
    
    # Boum !
    $ window_kick(50, 0.2)
    pause 0.2
    # Boum !
    $ window_kick(50, 0.2)
    pause 0.2
    
    # --- PHASE 2 : LES COINS (Teleport) ---
    # Très rapide, effet glitch
    
    $ window_jump_to("top_left")
    pause 0.2
    $ window_jump_to("bottom_right")
    pause 0.2
    $ window_jump_to("top_right")
    pause 0.2
    $ window_jump_to("bottom_left")
    pause 0.2
    
    # Retour au centre
    $ window_jump_to("center")
    
    e "Pas mal non ?"
    
    # --- PHASE 3 : LE SLIDE (Rewrite Style) ---
    # La fenêtre glisse doucement vers le bas de l'écran pour laisser voir le haut
    
    e "Je descends..."
    # On calcule une position un peu plus bas (ex: Y = 500)
    $ window_move_smooth(300, 500, 1.0)
    
    e "Et je remonte !"
    # Retour au centre (ajuste 300, 150 selon ton écran, ou utilise des calculs auto)
    $ window_move_smooth(300, 150, 0.5) 

    

    jump sonic_walk_event

    return


# L'image de la fausse barre
image fake_header_img = "images/fake_header.png"

# Un écran pour l'afficher par-dessus tout le reste (Z-Index élevé)
screen fake_ui_overlay():
    zorder 100
    add "fake_header_img":
        yalign 0.0 # Collé tout en haut
        xalign 0.5

label sonic_walk_event:
    
    scene bg sonic_world
    show sonic walking_anim at center

    e "Attention, je vais briser le 4ème mur..."

    # 1. On affiche la fausse barre (elle apparaît instantanément)
    show screen fake_ui_overlay
    
    # Petite pause pour stabiliser
    $ renpy.pause(0.1, hard=True)

    # 2. On retire la vraie barre Windows
    $ set_borders(False)
    
    e "Regarde bien le haut de la fenêtre."

    # 3. L'ACTION SIMULTANÉE
    
    # A. On lance l'animation de disparition (Ren'Py gère ça tout seul)
    # On crée un "moule" d'animation
    transform fade_out_3s:
        linear 3.0 alpha 0.0

    # B. On lance le mouvement en arrière-plan (via notre nouvelle fonction)
    # Comme c'est async, le jeu ne fige pas !
    $ move_window_async(800, 300, 3.0)

    # C. IMPORTANT : On met une pause de la même durée (3s)
    # C'est cette pause qui permet à Ren'Py de jouer l'animation pendant que la fenêtre bouge
    pause 3.0

    # Une fois fini, on cache l'écran vide
    hide screen fake_ui_overlay

    e "Tu as vu ? Plus de barre de titre !"
    
    # 4. RETOUR À LA NORMALE
    $ set_borders(True)
    
    jump expand_event
    return

label expand_event:
    
    scene bg dark_room
    e "C'est trop étroit ici..."

    # 1. On retire les bordures (OBLIGATOIRE pour un zoom fluide)
    $ set_borders(False)
    
    # Si tu as la fausse barre, cache-la
    hide screen fake_ui_overlay 
    hide screen fake_window_ui

    e "J'ai besoin de plus d'espace."

    # 2. LANCEMENT DU ZOOM
    # On lance l'agrandissement sur 3 secondes
    $ expand_window_async(3.0)
    
    play sound "audio/power_up.ogg" loop
    
    # On attend un tout petit peu plus que la durée (3.1s)
    # Regarde bien ta fenêtre : elle doit grandir physiquement !
    pause 3.1
    
    stop sound fadeout 0.5

    # 3. VERROUILLAGE FINAL
    # Maintenant qu'on fait la taille de l'écran, on active le vrai mode plein écran
    $ preferences.fullscreen = True
    
    # On remet les propriétés de bordure pour la prochaine fois
    $ set_borders(True)

    e "Voilà. Maintenant je contrôle tout l'écran."

    jump trap

    return

# Petite animation de tremblement pour accompagner l'agrandissement
transform shake_anim:
    xoffset 0 yoffset 0
    linear 0.05 xoffset 5
    linear 0.05 xoffset -5
    linear 0.05 yoffset 5
    linear 0.05 yoffset -5
    repeat


label trap:
    e "Je pense qu'on devrait rester ensemble un peu plus longtemps..."
    
    # 1. On grise le bouton X (Effet visuel)
    $ set_close_button_enabled(False)
    
    # 2. On bloque Alt+F4 (Effet logique)
    $ can_quit_game = False
    
    play sound "audio/lock_door.ogg"
    
    e "Voilà. Personne ne sort."
    
    # Le joueur essaie de cliquer sur la croix : elle est grise.
    # Le joueur fait Alt+F4 : rien ne se passe.
    
    pause 2.0
    
    e "Inutile d'insister."
    
    # ... L'histoire continue ...
    
    # 3. LIBÉRATION (Très important de ne pas oublier !)
    $ set_close_button_enabled(True)
    $ can_quit_game = True
    
    e "Allez, tu peux partir maintenant."

    jump notification_event

    return

label notification_event:
    
    e "Je n'aime pas que tu me regardes comme ça."
    e "Arrête de me regarder."

    # 1. On minimise le jeu (Le joueur se retrouve sur son bureau)
    $ renpy.iconify()
    
    # 2. On attend 2 secondes que le joueur soit confus devant son fond d'écran
    pause 2.0
    
    # 3. La notification Windows apparaît en bas à droite
    $ send_windows_notification("Système", "GOOD LUCK")
    
    pause 3.0
    
    # 4. Une deuxième pour la pression
    $ send_windows_notification("Système", "Fichier 'soul.dat' introuvable.")
    
    # Le joueur doit cliquer sur l'icône dans la barre des tâches pour revenir
    # (ou tu peux utiliser window_kick() pour faire clignoter la barre)
    
    pause 2.0
    
    # Quand il revient...
    e "Tu croyais pouvoir t'échapper ?"

    jump popup_event

    return

label popup_event:
    
    e "Je crois qu'il y a un problème avec ton ordinateur..."

    # 1. SIMPLE ERREUR WINDOWS
    # Affiche une boîte de dialogue avec le son d'erreur
    $ spawn_error_popup("System Error", "Le fichier 'hope.chr' est manquant.", 16)
    
    play sound "audio/windows_error_sound.ogg"
    
    e "Tu entends ça ?"
    
    pause 1.0

    # 2. SPAM D'ERREURS (L'effet Virus)
    # On lance 10 fenêtres d'un coup à des endroits aléatoires (Windows gère le placement en cascade)
    python:
        for i in range(5):
            spawn_error_popup("RUN", "DON'T LOOK BEHIND YOU", 48) # 48 = Warning (Triangle Jaune)
            renpy.pause(0.2) # Petite pause entre chaque pour l'effet "mitraillette"
            
    e "C'est incontrôlable !"

    # 3. FENÊTRE PERSONNALISÉE (Contenu Noir/Rouge)
    # Apparaît à une position précise (x=100, y=100 : Coin haut gauche)
    $ spawn_custom_black_window("???", "JE SUIS SORTI")
    
    e "Regarde en haut à gauche de ton écran..."
    
    pause 2.0
    
    e "Ferme-les ! Vite !"

    # 1. Le Popup Windows classique (Gris) - Marche instantanément
    $ spawn_error_popup("Système", "Fichier manquant.", 16)
    
    e "Une erreur Windows..."
    
    # 2. La Fenêtre Horreur (Noire/Rouge via PowerShell)
    # Elle peut mettre 1 seconde à apparaître, le temps que PowerShell se lance
    $ spawn_custom_black_window("???", "JE TE VOIS")
    
    e "C'est quoi cette fenêtre noire ?!"

    return