################################################################################
## Screens du menu principal et du menu de jeu
################################################################################

## Écran de navigation #########################################################
##
## Cet écran est disponible dans le menu principal et dans le menu de jeu. Il fournit l’accès aux autres menus et permet le démarrage du jeu.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Nouvelle partie") action Start()

        else:

            textbutton _("Historique") action ShowMenu("history")

            textbutton _("Sauvegarde") action ShowMenu("save")

        textbutton _("Charger") action ShowMenu("load")

        textbutton _("Préférences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("Fin de la rediffusion") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Menu principal") action MainMenu()

        textbutton _("À propos") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## L'aide n’est ni nécessaire ni pertinente sur les appareils mobiles.
            textbutton _("Aide") action ShowMenu("help")

        if renpy.variant("pc"):

            ## Le bouton pour quitter est banni sur iOS et inutile sur Android et sur le Web.
            textbutton _("Quitter") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")
