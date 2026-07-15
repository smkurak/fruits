# ============================================
# ОПРЕДЕЛЕНИЯ (самое начало файла)
# ============================================

define n = Character(
    "Нана",
    image="nana",
    who_color="#FFBB5C",
    who_outlines=[(2, "#4A2C00", 0, 0)]
)

# Переменные прогресса
default nana_affection = 0
default current_day = 1
default visits_today = 0

# Фоны
image bg pineapple_beach = "bg/pineapple_beach.jpg"
image bg island_map = "bg/island_map.jpg"

define config.fade_music = 1.0

# Спрайты Наны — пороги снижены для ощутимого прогресса
# Стадия 1 (шипастая):  0–14
# Стадия 2 (полу-гладкая): 15–34
# Стадия 3 (гладкая):   35+
image nana = ConditionSwitch(
    "nana_affection < 15", "chars/nana/nana_10.png",
    "nana_affection < 35", "chars/nana/nana_20.png",
    "True",                "chars/nana/nana_30.png"
)


# ============================================
# ИГРА
# ============================================

label start:
    $ nana_affection = 0
    $ current_day = 1
    $ visits_today = 0
    call screen intro_screen
    call screen island_map
    return


# ============================================
# СМЕНА ДНЯ
# ============================================

label next_day:
    $ current_day += 1
    $ visits_today = 0

    if current_day > 7:
        jump game_ending

    $ renpy.notify("День [current_day]. Новый день — новые возможности.")
    call screen island_map
    return


# ============================================
# ФИНАЛ (заглушка)
# ============================================

label game_ending:
    "Прошло семь дней. Сад снова наполнился жизнью..."
    # Финальная сцена — в разработке
    return
