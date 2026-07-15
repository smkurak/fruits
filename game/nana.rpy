# ========================
# СЦЕНЫ С НАНОЙ
# ========================

# Роутер визитов — определяет, какую сцену показать
label nana_visit_router:
    $ visits_today += 1

    if nana_affection >= 60:
        jump nana_undress
    elif nana_affection >= 35:
        jump nana_third_meeting   # ← было nana_second_meeting
    elif nana_affection >= 15:
        jump nana_second_meeting  # ← добавить этот порог
    else:
        jump nana_first_meeting


# ----------------------------------------
# ПЕРВЫЙ ВИЗИТ / СТАДИЯ 1 (affection 0–14)
# ----------------------------------------

label nana_first_meeting:
    scene bg pineapple_beach with fade
    play music "audio/music/nana_music_10.mp3" fadein 2.0

    show nana at center with dissolve

    n "…Ну вот. Ещё один 'смотритель'. Как будто предыдущие были лучше."

    menu:
        "Я здесь, чтобы помочь. Всем вам.":
            $ nana_affection += 6
            n "Помочь? Смешно. Посмотрим, насколько тебя хватит."

        "Ты выглядишь… необычно.":
            $ nana_affection += 8
            n "Ха. Прямолинейный. Хотя бы не врёшь."

        "Я могу уйти, если мешаю.":
            $ nana_affection += 3
            n "...Оставайся. Всё равно скучно одной."

    n "Слушай сюда, 'смотритель'. Я не фрукт, который сам падает в руки."

    # Проверяем, достигли ли новой стадии
    if nana_affection >= 15:
        $ renpy.notify("✨ Нана стала чуть мягче. Шипы немного притупились.")
    else:
        $ renpy.notify("Нана держится колюче, но кажется... не прочь поговорить снова.")

    hide nana with dissolve
    jump nana_return_to_map


# ----------------------------------------
# ВТОРОЙ ВИЗИТ / СТАДИЯ 2 (affection 15–34)
# ----------------------------------------

label nana_second_meeting:
    scene bg pineapple_beach with fade
    play music "audio/music/nana_music_20.mp3" fadein 2.0

    show nana at center with dissolve

    "Прошло несколько дней. Нана всё ещё держится, но её шипы стали заметно короче."

    n "Опять ты... Настойчивый."

    menu:
        "Ты выглядишь мягче. Это идёт тебе.":
            $ nana_affection += 10
            n "Не льсти. Хотя... спасибо."

        "Я пришёл, потому что думал о тебе.":
            $ nana_affection += 12
            n "Думал обо мне? Интересно... и что же ты думал?"

        "Просто хотел узнать, как ты.":
            $ nana_affection += 7
            n "Как я? Никто раньше не спрашивал. Странное чувство."

    n "Твои старания заметны... Но не думай, что я сразу позволю себя трогать."

    if nana_affection >= 35:
        $ renpy.notify("✨ Нана раскрывается. Кожа стала заметно глаже.")
    else:
        $ renpy.notify("Нана немного теплее. Продолжай.")

    hide nana with dissolve
    jump nana_return_to_map


# ----------------------------------------
# ТРЕТИЙ ВИЗИТ / СТАДИЯ 3 (affection 35–59)
# ----------------------------------------

label nana_third_meeting:
    scene bg pineapple_beach with fade
    play music "audio/music/nana_music_30.mp3" fadein 2.0
    show nana at center with dissolve

    "Нана стоит у воды. Она уже не прячется за шипами — их почти не осталось."

    n "Долго шёл сюда. Я уже думала — не придёшь сегодня."

    menu:
        "Я всегда прихожу, когда обещаю.":
            $ nana_affection += 12
            n "...Да. Я это заметила."

        "Без тебя здесь скучно.":
            $ nana_affection += 14
            n "Хм. Я тоже... скучала. Не говори никому."

        "Хочу узнать тебя лучше.":
            $ nana_affection += 10
            n "Лучше? Ты уже знаешь меня лучше всех. Это пугает немного."

    n "...Не уходи сразу. Ещё немного побудь здесь."

    if nana_affection >= 60:
        $ renpy.notify("✨ Нана полностью раскрылась. Что-то изменилось между вами.")
    else:
        $ renpy.notify("Нана смотрит тебе вслед дольше обычного.")

    hide nana with dissolve
    jump nana_return_to_map


# ----------------------------------------
# ФИНАЛЬНАЯ СЦЕНА (affection 60+)
# ----------------------------------------

label nana_undress:
    scene bg pineapple_beach with fade
    play music "audio/music/nana_music_30.mp3" fadein 2.0

    show nana at center with dissolve

    "Вечер. Пляж пустой. Нана ждёт тебя — впервые без колючей защиты."

    n "…Ну что. Доволен? Смотри, до чего ты меня довёл."

    menu:
        "Ты красивая. По-настоящему.":
            $ nana_affection += 15
            n "...Дурак. Почему от тебя это звучит иначе, чем от других."

        "Можно я прикоснусь?":
            $ nana_affection += 12
            n "...Только потому что это ты. Больше ни для кого."

        "Я хочу быть рядом с тобой.":
            $ nana_affection += 18
            n "Рядом... да. Это я могу позволить."

    n "...Не смей останавливаться."

    hide nana with dissolve
    $ renpy.notify("🍍 Нана полностью раскрылась перед тобой. Сад снова дышит.")
    jump nana_return_to_map


# ----------------------------------------
# ВОЗВРАТ НА КАРТУ
# ----------------------------------------

label nana_return_to_map:
    call screen island_map
    return
