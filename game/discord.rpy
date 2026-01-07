init python:
    from pypresence import Presence
    import time

    # --- CONFIGURATION ---
    DISCORD_CLIENT_ID = "1451267253403254826"
    LARGE_IMAGE_KEY = "icon_large"
    
    rpc_client = None
    start_time = time.time()

    # --- MÉMOIRE DU JEU (Pour se souvenir où on en était) ---
    mem_act = "1"
    mem_scene = "Intro"

    def init_discord_rpc():
        global rpc_client
        try:
            rpc_client = Presence(DISCORD_CLIENT_ID)
            rpc_client.connect()
        except:
            rpc_client = None

    # --- 1. FONCTION POUR LE JEU (Sauvegarde + Affiche) ---
    def rpc_update_game(act, scene):
        global mem_act, mem_scene, rpc_client
        
        # On sauvegarde l'état actuel
        mem_act = act
        mem_scene = scene
        
        if rpc_client:
            try:
                rpc_client.update(
                    details=f"Acte {act}",
                    state=f"Scène : {scene}",
                    large_image=LARGE_IMAGE_KEY,
                    large_text="En Jeu",
                    start=start_time
                )
            except: pass

    # --- 2. FONCTION POUR LES MENUS (Affiche seulement) ---
    def rpc_update_menu(menu_name):
        global rpc_client
        if rpc_client:
            try:
                rpc_client.update(
                    details="Dans les Menus", # Ou juste "En pause"
                    state=menu_name,          # Ex: "Options", "Sauvegardes"
                    large_image=LARGE_IMAGE_KEY,
                    large_text="Menu",
                    start=start_time
                )
            except: pass

    # --- 3. FONCTION DE RESTAURATION (Appelée quand on quitte un menu) ---
    def rpc_restore_game():
        # On réutilise les valeurs sauvegardées dans mem_act/mem_scene
        rpc_update_game(mem_act, mem_scene)