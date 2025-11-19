screen pause_menu():
    tag menu
    modal True
    add Solid("#000000cc")  # Semi-transparent black background
    add Blur(10)
    vbox:
        style_prefix "navigation"

        xalign 0.5
        yalign 0.5
        spacing 20
        label "PAUSE":
            xalign 0.5
            text_size 60
            text_color "#ffffff"
        null height 20 # Espace vide

        # --- VOS BOUTONS ---
        textbutton "Reprendre le jeu" action Return()
        
        textbutton "Sauvegarder" action ShowMenu("save")
        textbutton "Charger" action ShowMenu("load")
        
        textbutton "Options" action ShowMenu("preferences")
        textbutton "Mode graphique" action ShowMenu("graphic")
        
        textbutton "Menu Principal" action MainMenu()
        textbutton "Quitter le jeu" action Quit(confirm=True)