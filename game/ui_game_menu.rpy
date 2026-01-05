## Écran du menu de jeu ########################################################
##
## Ceci présente la structure commune de base d'un écran du menu de jeu. Il est appelé en lui passant le titre de l'écran, et il affiche l'arrière-plan, le titre et la navigation.
##
## Le paramètre de défilement peut être None, ou "viewport" ou "vpgrid". Cet écran est destiné à être utilisé avec un ou plusieurs enfants, qui sont transclus (placés) à l'intérieur de l'écran.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
        on "show" action Function(rpc_update_menu, title)
        # null
    else:
        add gui.game_menu_background
        on "show" action Function(rpc_update_menu, title)
        on "hide" action Function(rpc_restore_game)

    frame:
        # On applique un style différent selon si on est au menu ou en jeu
        style "game_menu_content_frame"

        if scroll == "viewport":
            
            viewport:
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                side_yfill True

                vbox:
                    spacing spacing
                    xalign 0.5
                    transclude

        elif scroll == "vpgrid":
            vpgrid:
                cols 1
                yinitial yinitial
                scrollbars "vertical"
                mousewheel True
                draggable True
                pagekeys True
                side_yfill True
                spacing spacing
                transclude

        else:
            transclude

    # --- MODIFICATIONS ICI ---

    # 1. ON A SUPPRIMÉ LA LIGNE "use navigation"
    # Cela empêche la liste des boutons de s'afficher dans les sous-menus.

    # 2. ON MODIFIE LE BOUTON RETOUR
    textbutton _("Retour"):
        style "return_button"

        if main_menu:
            # Si on est au menu principal, retour au titre
            action ShowMenu("main_menu")
        else:
            # Si on est en jeu, retour au MENU PAUSE (votre hub)
            action ShowMenu("pause_menu")

    label title

    # GESTION DU CLIC DROIT / ECHAP
    if main_menu:
        # Au menu principal : Retour à l'écran titre
        key "game_menu" action ShowMenu("main_menu")
    else:
        # En jeu : Retour au HUB (Pause Menu)
        key "game_menu" action ShowMenu("pause_menu")

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

# # Ce style hérite du cadre normal, mais force le fond à être transparent
# style game_menu_outer_frame_transparent is game_menu_outer_frame:
#     background None
#     # Si tu as une image overlay (genre des engrenages ou un cadre fin), tu peux la laisser ici.
#     # Mais surtout pas de Solid("#000000") !

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True
# 1. On équilibre les marges pour que ce soit symétrique
style game_menu_content_frame:
    # Avant c'était : left 60, right 30. Le décalage venait de là.
    left_margin 45
    right_margin 45
    top_margin 15

# 2. On s'assure que la boite de défilement (Viewport) est elle-même centrée
style game_menu_viewport:
    xsize 1380
    xalign 0.5 # Ajout crucial pour le centrage horizontal

# 3. (Optionnel) Ajustement de la barre de défilement pour qu'elle ne colle pas trop
style game_menu_vscrollbar:
    unscrollable gui.unscrollable
    xoffset 10 # Décale légèrement la barre vers la droite si elle gêne

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45

