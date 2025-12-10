init python:
    # --- CONFIGURATION DE TES SPRITES ---
    # Structure : "Nom du Groupe": ["attribut1", "attribut2", ...]
    
    # Remplis ceci avec TES vrais noms de fichiers/attributs
    anneko_data = {
        "Base": ["anneko"], 
        "Tenue": ["schoolA", "casual", "sport"],
        "Yeux": ["normal", "happy", "angry", "crying"],
        "Bouche": ["smile", "pout", "open"],
        # "Bras": ["bras_long", "bras_croise"] 
    }
    
    # Initialisation
    current_selections = {k: v[0] for k, v in anneko_data.items()}

    def update_selection(group, value):
        current_selections[group] = value
        renpy.restart_interaction() 

    def get_image_string():
        # Construit la chaîne: "alice uniform happy smile"
        cmd = [current_selections["Base"]]
        for group, val in current_selections.items():
            if group != "Base":
                cmd.append(val)
        return " ".join(cmd)

# --- L'ÉCRAN D'ESSAYAGE CORRIGÉ ---
screen sprite_tester():
    modal True
    tag menu
    
    # 1. Fond neutre 
    add Solid("#333") 
    
    # 2. Le Sprite 
    add get_image_string():
        align (0.6, 1.0) # Un peu à droite pour laisser la place au menu
        zoom 1.0         
    
    # 3. Panneau de Contrôle (à gauche)
    frame:
        align (0.0, 0.0)
        xsize 500 # Un peu plus large pour le confort
        ysize config.screen_height
        background Solid("#000000E6") 
        padding (20, 20)
        
        vpgrid:
            cols 1
            spacing 20
            draggable True
            mousewheel True
            scrollbars "vertical"
            xfill True
            
            vbox:
                spacing 30
                
                text "DEBUG ROOM" size 40 color "#ffcc00" xalign 0.5 font gui.name_text_font
                
                # Génération automatique des boutons
                for group, options in anneko_data.items():
                    if group != "Base": 
                        vbox:
                            spacing 10
                            text group color "#00d4ff" size 24 bold True
                            
                            # --- CORRECTION ICI ---
                            # Au lieu de 'grid', on utilise hbox avec box_wrap
                            hbox:
                                box_wrap True  # Permet de passer à la ligne auto
                                spacing 10
                                xfill True
                                
                                for opt in options:
                                    button:
                                        action Function(update_selection, group, opt)
                                        # Couleur jaune si sélectionné, gris sinon
                                        background (Solid("#ffcc00") if current_selections[group] == opt else Solid("#444"))
                                        padding (10, 5)
                                        # Taille minimum pour que ce soit joli
                                        xminimum 100 
                                        
                                        text opt:
                                            align (0.5, 0.5)
                                            color ("#000" if current_selections[group] == opt else "#fff")
                                            size 18

    # 4. Bouton Retour
    textbutton "RETOUR AU JEU":
        align (1.0, 0.05)
        offset (-20, 0)
        action Return()
        padding (20, 10)
        background "#ff0055"
        text_color "#fff"
        text_bold True