
## Écran « À propos... » #######################################################
##
## Cet écran présente le générique, les crédits et les informations de copyright relatives au jeu et à Ren’Py.
##
## Il n’y a rien de spécial sur cet écran. Par conséquent, il sert aussi d’exemple pour créer un écran personnalisé.

screen about():

    tag menu

    ## Cette déclaration concerne l’écran game_menu. L’élément vbox est ensuite inclus dans la fenêtre de l'écran game_menu.
    use game_menu(_("À propos"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about est généralement initialisé dans le fichier options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Conçu avec {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size

