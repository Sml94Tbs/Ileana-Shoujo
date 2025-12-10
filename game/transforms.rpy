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

transform tcommon(x=640, z=0.80):
    yanchor 1.0 subpixel True
    on show:
        ypos 1.03
        zoom z*0.95 alpha 0.00
        xcenter x yoffset -20
        easein .25 yoffset 0 zoom z*1.00 alpha 1.00
    on replace:

        alpha 1.00
        parallel:
            easein .25 xcenter x zoom z*1.00
        parallel:
            easein .15 yoffset 0 ypos 1.03

transform t41:
    tcommon(200)
transform t42:
    tcommon(493)
transform t43:
    tcommon(786)
transform t44:
    tcommon(1080)
transform t31:
    tcommon(240)
transform t32:
    tcommon(640)
transform t33:
    tcommon(1040)
transform t21:
    tcommon(400)
transform t22:
    tcommon(880)
transform t11:
    tcommon(640)

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