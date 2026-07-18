# ========================
# СЦЕНЫ С НАНОЙ
# ========================
# Точка входа — общий label visit_router в game/characters.rpy,
# который выставляет current_girl/n и прыгает сюда по стадии.

# ----------------------------------------
# ПЕРВЫЙ ВИЗИТ / СТАДИЯ 1 (affection 0–14)
# ----------------------------------------

label nana_stage1:
    scene bg nana with fade
    play music "audio/music/nana_music_10.mp3" fadein 2.0

    show nana at center with dissolve

    $ _first_visit = not has_flag("nana_stage1_seen")
    $ set_flag("nana_stage1_seen")

    if _first_visit:
        "Она стоит у самой кромки воды, скрестив руки на груди, и даже не поворачивается на звук шагов."
        n "…Ну вот. Новый 'смотритель'. Спорим, надолго тебя не хватит."
    else:
        n "...Опять ты тут ошиваешься. Ладно, что на этот раз?"

    $ reset_choices_if_exhausted("nana", 1, 4)

    menu:
        "Я здесь, чтобы помочь. Всем вам." if choice_open("nana", 1, 0):
            $ use_choice("nana", 1, 0)
            $ add_affection("nana", 6)
            n "Помочь? Смешно. Посмотрим, насколько тебя хватит."

        "Ты выглядишь… необычно." if choice_open("nana", 1, 1):
            $ use_choice("nana", 1, 1)
            $ add_affection("nana", 8)
            n "Ха. Прямолинейный. Хотя бы не врёшь."

        "Я могу уйти, если мешаю." if choice_open("nana", 1, 2):
            $ use_choice("nana", 1, 2)
            $ add_affection("nana", 3)
            n "...Оставайся. Всё равно скучно одной."

        "Могла бы быть и повежливее." if choice_open("nana", 1, 3):
            $ use_choice("nana", 1, 3)
            $ add_affection("nana", -3)
            n "Повежливее? Может, ещё чаю с печеньем подать?"

    if _first_visit:
        n "Слушай сюда, 'смотритель'. Я не фрукт, который сам падает в руки."

    # Проверяем, достигли ли новой стадии
    if get_affection("nana") >= 15:
        $ renpy.notify("✨ Нана стала чуть мягче. Шипы немного притупились.")
    else:
        $ renpy.notify("Нана держится колюче, но кажется... не прочь поговорить снова.")

    hide nana with dissolve
    jump return_to_map


# ----------------------------------------
# ВТОРОЙ ВИЗИТ / СТАДИЯ 2 (affection 15–34)
# ----------------------------------------

label nana_stage2:
    scene bg nana with fade
    play music "audio/music/nana_music_20.mp3" fadein 2.0

    show nana at center with dissolve

    $ _first_visit = not has_flag("nana_stage2_seen")
    $ set_flag("nana_stage2_seen")

    if _first_visit:
        "Прошло несколько дней. Нана всё ещё держится, но её шипы стали заметно короче."
        n "Опять ты... Настойчивый."
    else:
        n "...Соскучился, что ли? Ладно, не тяни."

    $ reset_choices_if_exhausted("nana", 2, 4)

    menu:
        "Ты выглядишь мягче. Это идёт тебе." if choice_open("nana", 2, 0):
            $ use_choice("nana", 2, 0)
            $ add_affection("nana", 10)
            n "Не льсти. Хотя... спасибо."

        "Я пришёл, потому что думал о тебе." if choice_open("nana", 2, 1):
            $ use_choice("nana", 2, 1)
            $ add_affection("nana", 12)
            n "Думал обо мне? Интересно... и что же ты думал?"

        "Просто хотел узнать, как ты." if choice_open("nana", 2, 2):
            $ use_choice("nana", 2, 2)
            $ add_affection("nana", 7)
            n "Как я? Никто раньше не спрашивал. Странное чувство."

        "Признай, ты уже скучаешь по мне, когда меня нет." if choice_open("nana", 2, 3):
            $ use_choice("nana", 2, 3)
            $ add_affection("nana", -4)
            n "Не льсти себе. У меня и без тебя дел хватает."

    if _first_visit:
        n "Твои старания заметны... Но не думай, что я сразу позволю себя трогать."

    if get_affection("nana") >= 35:
        $ renpy.notify("✨ Нана раскрывается. Кожа стала заметно глаже.")
    else:
        $ renpy.notify("Нана немного теплее. Продолжай.")

    hide nana with dissolve
    jump return_to_map


# ----------------------------------------
# ТРЕТИЙ ВИЗИТ / СТАДИЯ 3 (affection 35–59)
# ----------------------------------------

label nana_stage3:
    scene bg nana with fade
    play music "audio/music/nana_music_30.mp3" fadein 2.0
    show nana at center with dissolve

    $ _first_visit = not has_flag("nana_stage3_seen")
    $ set_flag("nana_stage3_seen")

    if _first_visit:
        "Нана стоит у воды. Она уже не прячется за шипами — их почти не осталось."
        n "Долго шёл сюда. Я уже думала — не придёшь сегодня."
    else:
        n "...Знала, что вернёшься. Садись, если хочешь."

    $ reset_choices_if_exhausted("nana", 3, 4)

    menu:
        "Я всегда прихожу, когда обещаю." if choice_open("nana", 3, 0):
            $ use_choice("nana", 3, 0)
            $ add_affection("nana", 12)
            n "...Да. Я это заметила."

        "Без тебя здесь скучно." if choice_open("nana", 3, 1):
            $ use_choice("nana", 3, 1)
            $ add_affection("nana", 14)
            n "Хм. Я тоже... скучала. Не говори никому."

        "Хочу узнать тебя лучше." if choice_open("nana", 3, 2):
            $ use_choice("nana", 3, 2)
            $ add_affection("nana", 10)
            n "Лучше? Ты уже знаешь меня лучше всех. Это пугает немного."

        "Может, хватит уже играть в недотрогу?" if choice_open("nana", 3, 3):
            $ use_choice("nana", 3, 3)
            $ add_affection("nana", -5)
            n "...Отойди. Не всё происходит по твоему расписанию."

    if _first_visit:
        n "...Не уходи сразу. Ещё немного побудь здесь."

    if get_affection("nana") >= 60:
        $ renpy.notify("✨ Нана полностью раскрылась. Что-то изменилось между вами.")
    else:
        $ renpy.notify("Нана смотрит тебе вслед дольше обычного.")

    hide nana with dissolve
    jump return_to_map


# ----------------------------------------
# ФИНАЛЬНАЯ СЦЕНА (affection 60+)
# ----------------------------------------

label nana_stage4:
    scene bg nana with fade
    play music "audio/music/nana_music_30.mp3" fadein 2.0

    show nana at center with dissolve

    $ _first_visit = not has_flag("nana_stage4_seen")
    $ set_flag("nana_stage4_seen")

    if _first_visit:
        "Вечер. Пляж пустой. Нана не прячет взгляд и не отходит — впервые сама делает шаг ближе."
        n "…Ну что, смотритель. Долго я держалась, да? Сама решила, что хватит."
    else:
        n "...Что, снова хочешь побыть рядом? Я не против."

    $ reset_choices_if_exhausted("nana", 4, 4)

    menu:
        "Ты красивая. По-настоящему." if choice_open("nana", 4, 0):
            $ use_choice("nana", 4, 0)
            $ add_affection("nana", 15)
            n "...Дурак. Почему от тебя это звучит иначе, чем от других."

        "Можно я прикоснусь?" if choice_open("nana", 4, 1):
            $ use_choice("nana", 4, 1)
            $ add_affection("nana", 12)
            n "...Только потому что это ты. Больше ни для кого."

        "Я хочу быть рядом с тобой." if choice_open("nana", 4, 2):
            $ use_choice("nana", 4, 2)
            $ add_affection("nana", 18)
            n "Рядом... да. Это я могу позволить."

        "Долго же ты сопротивлялась." if choice_open("nana", 4, 3):
            $ use_choice("nana", 4, 3)
            $ add_affection("nana", -6)
            n "...Прибавь эти слова к списку того, что лучше было не говорить."

    if _first_visit:
        n "...Не смей останавливаться."

    hide nana with dissolve
    $ renpy.notify("🍍 Нана полностью раскрылась перед тобой. Сад снова дышит.")
    jump return_to_map
