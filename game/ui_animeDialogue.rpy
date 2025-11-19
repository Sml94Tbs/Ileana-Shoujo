screen say_anime(who, what):
    style_prefix "anime"
    window:
        id "window"
        vbox:
            xalign 0.5
            yalign 1.0
            # On affiche le nom du perso en petit au-dessus si nécessaire
            # (Optionnel : supprimez ce bloc 'if' si vous ne voulez jamais voir le nom)
            if who is not None:
                text who:
                    id "who"
                    xalign 0.5 
                    text_align 0.5
                    size 24 # Plus petit que le texte normal
                    outlines [ (2, "#000000", 0, 0) ] # Contour noir

            # Le texte du dialogue (le sous-titre)
            text what:
                id "what"
                xalign 0.5
                text_align 0.5

style anime_window:
    # Positionnement
    xalign 0.5
    xfill True
    yalign 0.93 # Juste un peu au-dessus du bas de l'écran
    ysize None # On laisse la taille s'adapter au texte
    
    # IMPORTANT : Pas d'image de fond (la fameuse textbox)
    background None

style anime_dialogue:
    # Le style du texte
    xalign 0.5
    text_align 0.5
    size 40 # Taille du texte (ajustez selon vos besoins)
    color "#ffffff" # Texte blanc
    
    # Le secret des sous-titres lisibles : Le contour (Outline)
    # (Épaisseur, Couleur, Décalage X, Décalage Y)
    outlines [ (3, "#000000", 0, 0), (1, "#000000", 2, 2) ]
    
    # Police d'écriture (optionnel, mettez votre font ici)
    # font "fonts/anime_font.ttf"
    ## Affiche le dialogue avec une animation de type « machine à écrire »