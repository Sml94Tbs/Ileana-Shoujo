
## Écran d'aide ################################################################
##
## Cet écran fournit des informations sur les touches et les boutons de souris. En interne, il utilise d’autres écrans (keyboard_help, mouse_help et gamepad_help) pour afficher une aide dédiée.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Aide"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Clavier") action SetScreenVariable("device", "keyboard")
                textbutton _("Souris") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Manette") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Entrée")
        text _("Avance dans les dialogues et active l’interface (effectue un choix).")

    hbox:
        label _("Espace")
        text _("Avance dans les dialogues sans effectuer de choix.")

    hbox:
        label _("Flèches directionnelles")
        text _("Permet de se déplacer dans l’interface.")

    hbox:
        label _("Echap.")
        text _("Ouvre le menu du jeu.")

    hbox:
        label _("Ctrl")
        text _("Fait défiler les dialogues tant que la touche est pressée.")

    hbox:
        label _("Tab")
        text _("Active ou désactive les «sauts des dialogues».")

    hbox:
        label _("Page Haut")
        text _("Retourne au précédent dialogue.")

    hbox:
        label _("Page Bas")
        text _("Avance jusqu'au prochain dialogue.")

    hbox:
        label "H"
        text _("Cache l’interface utilisateur.")

    hbox:
        label "S"
        text _("Prend une capture d’écran.")

    hbox:
        label "V"
        text _("Active la {a=https://www.renpy.org/l/voicing}{size=24}vocalisation automatique{/size}{/a}.")

    hbox:
        label "Shift+A"
        text _("Ouvre le menu d'accessibilité.")


screen mouse_help():

    hbox:
        label _("Bouton gauche")
        text _("Avance dans les dialogues et active l’interface (effectue un choix).")

    hbox:
        label _("Bouton central")
        text _("Cache l’interface utilisateur.")

    hbox:
        label _("Bouton droit")
        text _("Ouvre le menu du jeu.")

    hbox:
        label _("Molette vers le haut")
        text _("Retourne au précédent dialogue.")

    hbox:
        label _("Molette vers le bas")
        text _("Avance jusqu'au prochain dialogue.")


screen gamepad_help():

    hbox:
        label _("Bouton R1\nA/Bouton du bas")
        text _("Avance dans les dialogues et active l’interface (effectue un choix).")

    hbox:
        label _("Gâchettes gauche")
        text _("Retourne au précédent dialogue.")

    hbox:
        label _("Bouton R1")
        text _("Avance jusqu'au prochain dialogue.")

    hbox:
        label _("Boutons directionnels, stick gauche")
        text _("Permet de se déplacer dans l’interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Ouvre le menu du jeu.")

    hbox:
        label _("Y/Bouton du haut")
        text _("Cache l’interface utilisateur.")

    textbutton _("Calibrage") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0

