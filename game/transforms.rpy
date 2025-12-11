# Animation de pulsation pour la lueur
transform glow_pulse:
    # On centre l'image par rapport au bouton
    xalign 0.5
    yalign 0.5
    
    # L'animation commence ici
    alpha 0.0 # Commence invisible
    easein 0.3 alpha 0.6 # Apparaît rapidement (60% d'opacité)
    
    block: # Boucle infinie
        ease 1.0 alpha 0.3 # Diminue l'intensité
        ease 1.0 alpha 0.6 # Réaugmente l'intensité
        repeat
# Si vous n'avez pas d'image (Version Test avec un rectangle généré) :
# On crée un rectangle blanc, flou sur les bords (Frame)
image animated_glow = At(Frame(Solid("#ffcc00"), 10, 10), glow_pulse)

define dissolve = Dissolve(0.25)

define dissolve_all_scene = MultipleTransition([
    False,
    Dissolve(1.0),
    Solid("#000000"),
    Pause(0.5),
    Solid("#000000"),
    Dissolve(1.25),
    True 
])

define dissolve_half_scene = MultipleTransition([
    Solid("#000000"),
    Pause(1.0),
    Solid("#000000"),
    Dissolve(1.0),
    True
])

# 1. On garde ton code technique (le moteur)
transform tcommon(x_pos, z_zoom):
    yanchor 1.0 subpixel True
    on show:
        ypos 1.03
        zoom z_zoom * 0.95 alpha 0.00
        xcenter x_pos yoffset -20
        easein .25 yoffset 0 zoom z_zoom * 1.00 alpha 1.00
    on replace:
        alpha 1.00
        parallel:
            easein .25 xcenter x_pos zoom z_zoom

# 2. On crée les "Presets" (Les positions fixes)
# C'est ICI que tu règles tes zooms et positions une fois pour toutes.

# -- Positions Standards (Zoom 1.0) --
transform t_center:
    tcommon(0.5, 1.0) # 0.5 = Centre (plus besoin de 640/1280)

transform t_left:
    tcommon(0.2, 1.0) # Un peu à gauche

transform t_right:
    tcommon(0.8, 1.0) # Un peu à droite

# -- Positions "Close Up" (Gros plan / Zoom) --
transform t_center_close:
    tcommon(0.5, 1.3) # Zoom à 130%

transform t_left_close:
    tcommon(0.25, 1.3)