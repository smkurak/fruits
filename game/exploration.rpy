# ============================================
# ПРОГУЛКА ПО ОСТРОВУ
# ============================================
# Лёгкая замена мини-игре/инвентарю: без экрана вещей и без отдельного
# движка. Каждая прогулка гарантированно даёт один предмет из ITEMS —
# просто флаг has_item_<id> (хелперы — в characters.rpy). Если предмет
# совпадает с favorite_item текущей девушки, при следующем визите к ней
# visit_router предложит подарить его (см. <id>_gift_offer в
# game/characters/<id>.rpy).
#
# Чтобы добавить нового персонажа с любимым предметом — достаточно
# добавить пункт в ITEMS и favorite_item=... в register_girl(...).

init python:
    ITEMS = {
        "seashell": {
            "found": "ракушка",
            "gift": "ракушку",
        },
        "moss_stone": {
            "found": "мшистый камешек",
            "gift": "мшистый камешек",
        },
    }

label explore_island:
    $ visits_today += 1

    scene expression "bg/island_map.jpg" with fade

    $ _flavor = renpy.random.choice([
        "Ты бредёшь вдоль берега без особой цели, разглядывая всё, что выносит прибой.",
        "Тропинка уводит тебя дальше обычного маршрута, вглубь острова.",
        "Ты решаешь обойти остров с той стороны, где раньше не бывал.",
    ])

    "[_flavor]"

    $ _item_id = renpy.random.choice(list(ITEMS.keys()))
    $ _found_name = ITEMS[_item_id]["found"]
    $ give_item(_item_id)

    "Среди камней и песка ты замечаешь кое-что и подбираешь: [_found_name]."

    $ renpy.notify("Найдено: %s" % _found_name)

    jump return_to_map
