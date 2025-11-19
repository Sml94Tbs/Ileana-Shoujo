
## Écran des menus rapides #####################################################
##
## Les menus rapides sont affichés dans le jeu pour permettre un accès rapide à certaines fonctions.

screen quick_menu():

    ## Assure qu'il apparaît au-dessus des autres screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("Retour") action Rollback()
            textbutton _("Historique") action ShowMenu('history')
            textbutton _("Avance rapide") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Sauvegarde") action ShowMenu('save')
            textbutton _("Sauvegarde R.") action QuickSave()
            textbutton _("Chargement R.") action QuickLoad()
            textbutton _("Préf.") action ShowMenu('preferences')


## Ce code garantit que le menu d’accès rapide sera affiché dans le jeu, tant que le joueur n’aura pas explicitement demandé à cacher l’interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")

