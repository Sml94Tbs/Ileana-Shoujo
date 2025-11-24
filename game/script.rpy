# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"

# Déclarez les personnages utilisés dans le jeu.
define e = Character('Eileen', color="#c8ffc8")
define a = Character(None, screen="say_anime", what_prefix="{cps=0}", what_suffix="{/cps}")

image ok = "sfx/01 A.jpg"
# Le jeu commence ici
label start:
    window hide
    stop music fadeout 1.0
    scene black with None
    pause 1.0
    show text "MSSML Present"
    with dissolve
    pause (5)
    scene black with fade
    pause 1.0
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

    return
