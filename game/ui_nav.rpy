################################################################################
## Screens du menu principal et du menu de jeu
################################################################################

## Écran de navigation #########################################################
##
## Cet écran est disponible dans le menu principal et dans le menu de jeu. Il fournit l’accès aux autres menus et permet le démarrage du jeu.

label intro_transition:
    hide screen main_menu_effects
    $ quick_menu = False
    stop music fadeout 2.0
    scene black with Fade(1.5, 0.0, 1.0)
    pause 0.5
    jump start
    return

screen navigation():

    if main_menu:
        text [config.version]:
            align (0.0, 1.0)
            offset (10, -10)
    vbox:
        style_prefix "navigation"

        # xpos gui.navigation_xpos
        yalign 0.9
        xalign 0.5
        yoffset -100

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("NOUVELLE PARTIE") action Start("intro_transition")
            textbutton _("CONTINUER") action ShowMenu("load")
            textbutton _("CONFIGURATION") action ShowMenu("preferences")
            textbutton _("QUITTER") action Quit(confirm=True)

        else:
            spacing gui.navigation_spacing
            xalign 0.5
            yalign 0.7

            textbutton _("Historique") action ShowMenu("history")

            


        if _in_replay:

            textbutton _("Fin de la rediffusion") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Menu principal") action MainMenu()

            textbutton _("Sauvegarde") action ShowMenu("save")

            textbutton _("Charger") action ShowMenu("load")

            textbutton _("Configuration") action ShowMenu("preferences")
            if renpy.variant("pc"):

                ## Le bouton pour quitter est banni sur iOS et inutile sur Android et sur le Web.
                textbutton _("Quitter le jeu") action Quit(confirm=not main_menu)

        # textbutton _("À propos") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## L'aide n’est ni nécessaire ni pertinente sur les appareils mobiles.
            textbutton _("Aide") action ShowMenu("help")


style navigation_button is gui_button
style navigation_button_text is empty

style navigation_button_text:
    font gui.interface_font
style navigation_vbox:
    xalign 0.5
    yalign 0.9
style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    xalign 0.5
    font gui.interface_text_font
    size 30
    idle_color "#ffffff"
    hover_background "animated_glow"
    idle_background None
    hover_color "#ff81ca"
    selected_color "#ffcc00"
    outlines [ (2, "#000000", 0, 0) ]
    properties gui.text_properties("navigation_button")
