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