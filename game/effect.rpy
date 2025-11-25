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



# Remplace le bloc précédent par ça si tu as l'image :
image gradient_texture = "gui/gradient_overlay.png"

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
    # Récupération de la couleur de la route (définie dans votre python init)
    $ current_col = get_theme_color()

    # --- Étape 1 : Fond noir/sombre pour l'overlay ---
    # Ajoute un rectangle noir sur toute la zone pour assombrir le fond.
    # L'opacité (alpha 0.8) rend le noir semi-transparent.
    # add Solid("#000000") alpha 0.8
    # --- Étape 2 : L'effet de dégradé Accordéon ---
    # On ajoute le dégradé lumineux (gradient_texture) qui a le mouvement.
    # Il est important de spécifier où il se trouve (alignement en bas).
    # --- Ton code de dégradé et particules ---
    add "four_band_gradient":
    # Aligné en bas et centré
        xalign 0.5 
        yalign 1.0
        matrixcolor TintMatrix(current_col)
        at accordion_effect
        blend "add"

    # --- Étape 3 : Les particules (qui doivent être au-dessus du fond noir) ---
    # Nous les laissons ici, car elles sont déjà au-dessus du fond noir
    for p in particle_data:
        add "particle_texture":
            xalign p["x"] 
            zoom p["size"]
            matrixcolor TintMatrix(current_col)
            at particle_move(p["speed"], p["delay"])
            blend "add"

# On définit la forme géométrique du dégradé en 4 bandes
image four_band_gradient:
    # On définit la taille globale de l'image
    ysize 600
    
    # --- BANDE 1 : La plus haute (Très transparente) ---
    contains:
        Solid("#ffffff3b")
        xsize config.screen_width 
        ysize 600
        alpha 0.1
        yalign 1.0 # Collé en bas
        
    # --- BANDE 2 : Moyenne haute ---
    contains:
        Solid("#ffffff44")
        xsize config.screen_width 
        ysize 450
        alpha 0.3
        yalign 1.0

    # --- BANDE 3 : Moyenne basse ---
    contains:
        Solid("#ffffff7c")
        xsize config.screen_width 
        ysize 300
        alpha 0.5
        yalign 1.0

    # --- BANDE 4 : La plus basse (Très opaque) ---
    contains:
        Solid("#ffffffc7")
        xsize config.screen_width 
        ysize 150
        alpha 0.8
        yalign 1.0
    # --- LA TOUCHE FINALE : LE FLOU ---
    # Cette ligne s'applique au résultat final des "contains" ci-dessus.
    # Une valeur entre 20 et 50 donnera un résultat très doux.
    blur 70

transform accordion_effect:
    yalign 1.0 # L'animation part du bas
    xalign 0.5
    
    # On commence un peu petit
    yzoom 0.8 alpha 0.8
    
    parallel:
        # Effet d'étirement vertical (Accordéon)
        ease 4.0 yzoom 1.2 # S'étire vers le haut
        ease 4.0 yzoom 0.8 # Se rétracte
        repeat
    parallel:
        # Légère variation d'intensité globale
        ease 3.0 alpha 1.0
        ease 5.0 alpha 0.7
        repeat