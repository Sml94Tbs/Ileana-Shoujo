init python:
    # Liste de tuples : ("Titre Affiché", "chemin/du/fichier.ogg")
    jukebox_playlist = [
        ("BGM BoomBap", "audio/bgm/bgm_boombapv4.mp3"),
        ("BGM TrapSoul",   "audio/bgm/bgm_trapsoul.ogg"),
        ("Combat Boss",     "audio/bgm/battle_boss.opus"),
        ("Tristesse",       "audio/bgm/test5.mp3"),
        # Ajoute autant de musiques que tu veux ici !
    ]

    # Une petite fonction pour récupérer le titre et le chemin proprement
    def get_track_info(index):
        # Le modulo (%) permet de boucler (si on dépasse la fin, on revient au début)
        safe_index = index % len(jukebox_playlist)
        return safe_index, jukebox_playlist[safe_index]

screen sound_room():
    tag menu # Remplace le menu actuel
    modal True # Empêche de cliquer en dessous

    # On utilise un fond (tu peux mettre ton effet de particules ici aussi !)
    add Solid("#000000ff")
    # ou : use main_menu_effects 

    # --- VARIABLE DE L'ÉCRAN ---
    # idx = L'index de la musique actuelle dans la liste (0, 1, 2...)
    default idx = 0
    
    # On récupère les infos de la musique actuelle grâce à notre fonction Python
    $ current_idx, (track_title, track_path) = get_track_info(idx)

    # --- LE CONTENEUR CENTRAL ---
    frame:
        style_prefix "soundtest" # On créera ce style plus bas
        xalign 0.5
        yalign 0.5
        
        vbox:
            spacing 20

            label _("SOUND TEST ROOM") xalign 0.5

            # --- LA ZONE DE CONTRÔLE ---
            hbox:
                xalign 0.5
                spacing 40
                yalign 0.5

                # BOUTON PRÉCÉDENT (<)
                textbutton "<":
                    text_size 60
                    # Action composée :
                    # 1. On décrémente l'index
                    # 2. On joue IMMÉDIATEMENT la nouvelle musique correspondante
                    action [
                        SetScreenVariable("idx", idx - 1), 
                        Play("music", get_track_info(idx - 1)[1][1])
                    ]

                # NOM DE LA MUSIQUE (Dynamique)
                frame: # Un petit cadre pour le titre
                    xsize 600
                    ysize 100
                    background None # Ou un fond semi-transparent
                    
                    text track_title:
                        xalign 0.5
                        yalign 0.5
                        size 50
                        color "#ffcc00"
                        # Petite animation pour montrer que ça joue
                        at transform:
                            alpha 0.8
                            linear 1.0 alpha 1.0
                            linear 1.0 alpha 0.8
                            repeat

                # BOUTON SUIVANT (>)
                textbutton ">":
                    text_size 60
                    action [
                        SetScreenVariable("idx", idx + 1), 
                        Play("music", get_track_info(idx + 1)[1][1])
                    ]

            # --- INFOS FICHIER (Optionnel) ---
            # Affiche le vrai nom du fichier en petit en dessous
            text f"Fichier: {track_path}" size 20 color "#888" xalign 0.5

    # BOUTON RETOUR
    textbutton _("Retour"):
        style "return_button"
        # Stop la musique quand on part ? Ou on laisse jouer ?
        action [Stop("music", fadeout=0.5), Return()]

style soundtest_frame:
    xpadding 50
    ypadding 50
    background Solid("#000000aa") # Fond noir semi-transparent

style soundtest_button_text:
    color "#ffffff"
    hover_color "#ffcc00" # Jaune au survol
    outlines [ (2, "#000000", 0, 0) ]