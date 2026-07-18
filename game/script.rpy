# ============================================
# ОПРЕДЕЛЕНИЯ (самое начало файла)
# ============================================
# Персонажи (Character, спрайты, пороги отношений) — в game/characters.rpy
# и game/characters/*.rpy. Здесь только общеигровые переменные и фоны.

# Переменные прогресса
default current_day = 1
default visits_today = 0
define MAX_VISITS_PER_DAY = 2

# Фоны генерируются автоматически из реестра GIRLS (game/characters.rpy)
# как "bg <id>", напр. "bg nana", "bg ivi".

define config.fade_music = 1.0


# ============================================
# ИГРА
# ============================================

label start:
    $ affection = {}
    $ relationship_flags = set()
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
# ДОМ ИГРОКА
# ============================================

label player_house:
    call screen player_house
    call screen island_map
    return


# ============================================
# ФИНАЛ (заглушка)
# ============================================

label game_ending:
    "Прошло семь дней. Сад снова наполнился жизнью..."
    # Финальная сцена — в разработке
    return
