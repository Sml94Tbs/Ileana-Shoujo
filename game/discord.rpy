init python:
    # On importe la librairie qu'on vient de copier
    from pypresence import Presence
    import time

    # --- CONFIGURATION ---
    # Remplace par TON Application ID (copié à l'étape 1)
    DISCORD_CLIENT_ID = "1451267253403254826" 
    
    # Le nom de l'image que tu as uploadée dans Art Assets
    LARGE_IMAGE_KEY = "icon_large" 
    
    rpc_client = None
    start_time = time.time() # Pour afficher "Joue depuis 00:10"

    # Fonction pour démarrer la connexion
    def init_discord_rpc():
        global rpc_client
        try:
            rpc_client = Presence(DISCORD_CLIENT_ID)
            rpc_client.connect()
        except Exception as e:
            print(f"Discord RPC non disponible : {e}")
            rpc_client = None

    # Fonction pour mettre à jour le statut
    def update_discord(act_number, scene_name):
        global rpc_client
        if rpc_client:
            try:
                rpc_client.update(
                    state=f"Scène : {scene_name}",      # Ligne du bas
                    details=f"Acte {act_number}",       # Ligne du haut
                    large_image=LARGE_IMAGE_KEY,        # Ton logo
                    large_text="Nom du Jeu",            # Texte au survol de l'image
                    start=start_time                    # Le timer
                )
            except:
                # Si la connexion saute, on essaie de relancer doucement ou on ignore
                pass
