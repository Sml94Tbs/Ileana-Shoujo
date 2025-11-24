## Écran du menu principal #####################################################
##
## Utilisé pour afficher le menu principal quand Ren'Py démarre.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

# Ce label spécial est appelé par Ren'Py juste avant le menu principal
label before_main_menu:
    # On affiche l'écran d'effets de manière permanente
    show screen main_menu_effects
    return
screen main_menu():

    ## Ceci assure que tout autre screen de menu est remplacé.
    tag menu

    add gui.main_menu_background

    use main_menu_effects

    ## L'instruction use inclut un autre écran à l'intérieur de celui-ci. Le vrai contenu du menu principal se trouve dans l'écran "navigation".
    use navigation


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)
