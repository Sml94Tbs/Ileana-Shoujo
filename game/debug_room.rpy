init python:
    # ---------------------------------------------------------
    # 1. LA CONFIGURATION (C'est ici que tu ajoutes tes persos)
    # ---------------------------------------------------------
    
    all_chars_data = {
        # --- PERSONNAGE 1 : ALICE ---
        "Anneko": {
            "Base": ["anneko"], # Le tag de base (ex: 'show anneko')
            "Outfit": ["schoolA", "casual", "sport"],
            "Yeux": ["normal", "happy", "angry"],
            "Bouche": ["smile", "pout"]
        },
        
        # --- PERSONNAGE 2 : BOB (Exemple) ---
        "itsuka": {
            "Base": ["itsuka"],
            "Outfit": ["school", "swimsuit"],
            "Yeux": ["normal", "surprised", "scared"]
        },

        # --- PERSONNAGE 3 : EILEEN (Exemple) ---
        "Eileen": {
            "Base": ["eileen"],
            "Mood": ["vhappy", "happy", "neutral", "concerned"]
        }
    }
    
    # ---------------------------------------------------------
    # 2. LA LOGIQUE (Ne touche pas à ça)
    # ---------------------------------------------------------
    
    # On définit le premier perso de la liste comme celui par défaut
    active_char_name = list(all_chars_data.keys())[0]

    # On initialise les choix par défaut pour TOUS les persos d'un coup
    # Structure : global_selections["Alice"]["Tenue"] = "uniform"
    global_selections = {}
    
    for c_name, c_data in all_chars_data.items():
        global_selections[c_name] = {k: v[0] for k, v in c_data.items()}

    def set_active_char(name):
        global active_char_name
        active_char_name = name
        renpy.restart_interaction()

    def update_char_option(group, value):
        global_selections[active_char_name][group] = value
        renpy.restart_interaction() 

    def get_current_image_string():
        # Récupère les choix du perso ACTIF
        my_choices = global_selections[active_char_name]
        
        # Construit la commande
        cmd = [my_choices["Base"]] # Le tag de base (ex: "alice")
        
        for group, val in my_choices.items():
            if group != "Base":
                cmd.append(val)
        
        return " ".join(cmd)

# ---------------------------------------------------------
# 3. L'ÉCRAN
# ---------------------------------------------------------
screen sprite_tester():
    modal True
    tag menu
    
    # Fond
    add Solid("#333") 
    
    # Le Sprite (S'affiche selon le perso actif)
    add get_current_image_string():
        align (0.65, 1.0)
        zoom 1.0         
    
    # Panneau Latéral
    frame:
        align (0.0, 0.0)
        xsize 500 
        ysize config.screen_height
        background Solid("#000000E6") 
        padding (20, 20)
        
        vbox:
            spacing 20
            
            text "DEBUG ROOM" size 40 color "#ffcc00" xalign 0.5 font gui.name_text_font
            
            # --- ZONE 1 : SÉLECTEUR DE PERSONNAGE ---
            label "PERSONNAGE :" text_color "#fff" text_size 18
            
            hbox:
                box_wrap True
                spacing 10
                xfill True
                
                for char_name in all_chars_data.keys():
                    button:
                        action Function(set_active_char, char_name)
                        # Bleu si actif, Gris sinon
                        background (Solid("#00d4ff") if active_char_name == char_name else Solid("#444"))
                        padding (15, 10)
                        xminimum 80
                        
                        text char_name:
                            align (0.5, 0.5)
                            color ("#000" if active_char_name == char_name else "#fff")
                            bold True
            
            null height 10
            add Solid("#ffffff44", ysize=2) # Ligne de séparation
            null height 10

            # --- ZONE 2 : LES ATTRIBUTS DU PERSO ACTIF ---
            vpgrid:
                cols 1
                spacing 20
                draggable True
                mousewheel True
                scrollbars "vertical"
                xfill True
                
                vbox:
                    spacing 20
                    # On boucle seulement sur les données du perso actif
                    for group, options in all_chars_data[active_char_name].items():
                        if group != "Base": 
                            vbox:
                                spacing 5
                                text group color "#00d4ff" size 24 bold True
                                
                                hbox:
                                    box_wrap True
                                    spacing 5
                                    xfill True
                                    
                                    for opt in options:
                                        button:
                                            action Function(update_char_option, group, opt)
                                            # Jaune si sélectionné
                                            background (Solid("#ffcc00") if global_selections[active_char_name][group] == opt else Solid("#444"))
                                            padding (10, 5)
                                            xminimum 80 
                                            
                                            text opt:
                                                align (0.5, 0.5)
                                                color ("#000" if global_selections[active_char_name][group] == opt else "#fff")
                                                size 16

    # Bouton Retour
    textbutton "RETOUR":
        align (1.0, 0.05)
        offset (-20, 0)
        action Return()
        padding (20, 10)
        background "#ff0055"
        text_color "#fff"