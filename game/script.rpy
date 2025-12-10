# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"

# Déclarez les personnages utilisés dans le jeu.
define e = Character('Eileen', color="#c8ffc8")
define nv = Character('Ileana' ,kind=nvl, color="#ffc8c8")
define narrator = nvl_narrator
define a = Character(None, screen="say_anime", what_prefix="{cps=0}", what_suffix="{/cps}")

image ok = "sfx/01 A.jpg"
# Le jeu commence ici
label start:
    $ quick_menu = False
    hide screen main_menu_effects
    stop music fadeout 2.0
    with dissolve_all_scene
    window hide
    pause 1.0
    show text "MSSML Present"
    with dissolve
    pause (5)
    scene black with dissolve_all_scene
    pause 0.5
    window auto
    $ quick_menu = True

    e "Vous venez de créer un nouveau jeu Ren'Py."

    e "Après avoir ajouté une histoire, des images et de la musique, vous pourrez le présenter au monde entier !"

    $ quick_menu = False

    scene white

    a 'Bonne chance pour votre projet de jeu !'

    a "Si la phrase est vraiment très longue, elle devrait se centrer parfaitement et rester lisible grâce au contour noir épais."

    scene ok

    $ quick_menu = True

    e "yes"

    show anneko at t32


    "Anneko" "Coucou"

    show anneko

    "Anneko" "Je suis là !"

    narrator "The End."
    narrator "Je ne pense que cela soit du à une erreu de ta partujguguyyfgufffttyfrtytfyftyftftfyfytftyftftyfftyftfyfyttrtrtrtrturyturytrutyrutyrutyrutryutryutry"
    narrator "Je ne pense que cela soit du à une erreu de ta part"
    narrator "Il me faudrait surment un endroit ou amener ces ames égaréés"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    $ gui.nvl_bg_bool = False
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"
    scene white
    $ gui.nvl_bg_bool = True
    narrator "Viens a moi jeune"
    narrator "Viens a moi jeune"

    return
