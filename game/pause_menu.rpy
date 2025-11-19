
init:
    transform flou_leger:
        blur 10

screen pause_menu():
    tag menu
    modal True  # Semi-transparent black background
    style_prefix "game_menu"
    add Solid("#000000aa")
    # add gui.game_menu_background at flou_leger

    # 2. On affiche votre navigation existante
    # Elle s'affichera exactement comme vous l'avez configurée dans screen navigation()
    use navigation