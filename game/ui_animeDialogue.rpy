screen say_anime(who, what):
    tag say   # Remplace l'écran de dialogue standard
    layer "screens" # S'assure qu'on est au bon niveau

    # --- 1. GESTION DU QUICK MENU ---
    # On force la fermeture du quick_menu dès que cet écran apparaît
    on "show" action Hide("quick_menu")
    on "replace" action Hide("quick_menu")
    
    # (Optionnel) On le réaffiche quand on quitte ce mode, 
    # mais généralement le prochain écran "say" normal s'en charge.
    # on "hide" action Show("quick_menu") 

    window:
        # On n'utilise PAS id "window" pour éviter que Ren'Py n'impose son style bleu
        style "anime_window"

        vbox:
            # On place le conteneur en bas au centre
            xalign 0.5
            yalign 1.0 # Collé au bas de l'écran (le padding du style remontera le texte)
            xfill True # Prend toute la largeur

            # --- LE NOM (WHO) ---
            if who is not None:
                text who:
                    id "who"
                    style "anime_label"

            # --- LE TEXTE (WHAT) ---
            text what:
                id "what"
                style "anime_dialogue"

# ---------------------------------------------------------
# LES STYLES (Boostés pour le look Anime)
# ---------------------------------------------------------

style anime_window is empty:
    # Positionnement global de la zone de texte
    xalign .1
    yalign .8     # Position verticale : 90% vers le bas
    ysize None       # Hauteur automatique
    background None  # TRANSPARENT (Pas de boîte)
    
    # Marges pour que le texte ne touche pas les bords de l'écran
    left_padding 200
    # right_padding 200
    # bottom_padding 50

style anime_label is gui_label:
    # Le Nom du personnage
    xalign 0.5       # Centre l'objet
    text_align 0.5   # Centre le texte dans l'objet
    color "#ffaa00"  # Couleur Or
    size 40          # Assez gros
    outlines [ (3, "#000000", 0, 0) ] # Gros contour noir
    yoffset 10       # Un peu d'espace avant le dialogue

style anime_dialogue is gui_text:
    # Le Sous-titre
    
    # CENTRAGE (Les deux sont obligatoires)
    xalign 0.5       # Centre le bloc de texte au milieu de l'écran
    text_align 0.5   # Centre les lignes de texte (si 2 lignes ou plus)
    layout "subtitle" # Optimise la coupure des phrases pour les sous-titres
    
    # TAILLE ET COULEUR
    color "#ffffff"
    size 65          # Taille cinéma (ajustez à 70 ou 80 si besoin)
    font gui.anime_dialogue_font # Police avec empattement pour le style anime
    
    # CONTOUR TYPE ANIME (Très épais + Ombre portée)
    # (Épaisseur, Couleur, Décalage X, Décalage Y)
    # outlines [ (4, "#000000", 0, 0), (2, "#000000", 2, 2) ]