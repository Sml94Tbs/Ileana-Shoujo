init python:
    import random

    # 1. Configuration des Thèmes
    # C'est ici que tu ajoutes tes routes. Plus besoin de toucher au code complexe après.
    theme_config = {
        "default":  {"color": "#ffffff", "intensity": 0.5}, # Blanc neutre
        "alice":    {"color": "#ffb7b2", "intensity": 0.7}, # Rose doux
        "combat":   {"color": "#ff3333", "intensity": 0.8}, # Rouge vif
        "mystere":  {"color": "#a29bfe", "intensity": 0.6}, # Violet
    }

    # Variable persistante pour savoir quelle route est active (par défaut "default")
    if persistent.menu_theme is None:
        persistent.menu_theme = "default"

    # 2. Fonction pour récupérer la couleur actuelle
    def get_theme_color():
        theme = theme_config.get(persistent.menu_theme, theme_config["default"])
        return Color(theme["color"])

    # 3. Générateur de positions aléatoires pour les particules (Pro Tip)
    # On génère une liste de positions fixes au démarrage pour éviter que
    # les particules ne sautent partout à chaque rafraîchissement d'écran.
    particle_data = []
    for i in range(40): # 40 particules
        d = {
            "x": random.random(),      # Position X (0.0 à 1.0)
            "speed": random.randint(4, 8), # Vitesse (secondes pour monter)
            "size": random.uniform(0.5, 1.0), # Taille variable
            "delay": random.uniform(0.0, 5.0) # Délai de départ
        }
        particle_data.append(d)

# Une particule : Un cercle blanc flou
image particle_texture:
    Text("•", size=50, color="#fff") # Un simple point texte
    alpha 0.8
    blur 4 # On le floute pour faire "lumière"

# Le dégradé : Un rectangle qui va du transparent au blanc
image gradient_texture:
    # Transforme un Solid blanc en dégradé vertical
    Solid("#ffffff")
    ysize 500 # Hauteur du dégradé
    alpha 0.0 # Commence transparent
    # Masque alpha pour créer le dégradé (bas opaque -> haut transparent)
    # (Note: Si tu as une image PNG de dégradé, utilise-la ici à la place)
    # mask "gui/gradient_mask.png"

# Mouvement d'une particule (Bas -> Haut)
transform particle_move(speed, delay):
    subpixel True  # Mouvement ultra-fluide
    yalign 1.1     # Commence sous l'écran
    alpha 0.0      # Invisible au début
    
    # Attend un peu avant de partir (pour ne pas qu'elles partent toutes ensemble)
    pause delay
    
    parallel:
        # Mouvement vers le haut
        easeout speed yalign -0.1 
    parallel:
        # Gestion de l'opacité (Apparaît -> Disparaît)
        easein 1.0 alpha 0.6
        pause (speed - 2.0)
        easeout 1.0 alpha 0.0
    
    repeat # Recommence à l'infini

# Effet Accordéon (Respiration)
transform accordion_effect:
    yalign 1.0 # Collé en bas
    # xfill True # Prend toute la largeur
    
    parallel:
        # Respiration de la hauteur (Zoom vertical)
        ease 4.0 yzoom 1.2
        ease 4.0 yzoom 0.8
        repeat
    parallel:
        # Respiration de l'intensité (Alpha)
        ease 3.0 alpha 0.6
        ease 5.0 alpha 0.3
        repeat

screen main_menu_effects():
    # Zorder bas pour être tout au fond
    zorder -100 
    
    # PAS DE 'tag menu' ICI ! C'est le secret.

    $ current_col = get_theme_color()

    # --- Ton code de dégradé et particules ---
    add "gradient_texture":
        at accordion_effect
        matrixcolor TintMatrix(current_col) 
        blend "add"

    for p in particle_data:
        add "particle_texture":
            xalign p["x"] 
            zoom p["size"]
            matrixcolor TintMatrix(current_col)
            at particle_move(p["speed"], p["delay"])
            blend "add"