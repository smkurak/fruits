# ============================================
# РЕЕСТР ДЕВУШЕК
# ============================================
# Единый источник правды: имя, стиль реплик, спрайты, локация.
# Чтобы добавить новую девушку — один register_girl(...) здесь плюс
# game/characters/<id>.rpy с лейблами <id>_stage1..N (см. nana.rpy).

init python:

    class Girl(object):
        def __init__(self, id, name, fruit, emoji, color, outline,
                     flaw, growth, stage_thresholds, sprite_thresholds,
                     sprite_stub, bg, unlock_day=1, favorite_item=None):
            self.id = id
            self.name = name
            self.fruit = fruit
            self.emoji = emoji
            self.flaw = flaw          # дизайн-referencе: изъян персонажа
            self.growth = growth      # дизайн-referencе: к чему растёт
            # [(мин. affection, номер стадии диалога), ...] по возрастанию
            self.stage_thresholds = stage_thresholds
            # [(мин. affection, суффикс спрайта), ...] по возрастанию
            self.sprite_thresholds = sprite_thresholds
            self.sprite_stub = sprite_stub  # "chars/nana/nana"
            self.bg = bg
            self.unlock_day = unlock_day
            self.favorite_item = favorite_item  # id из ITEMS (game/exploration.rpy) или None
            self.say = Character(name, image=id, who_color=color,
                                  who_outlines=[outline])

    GIRLS = {}

    def register_girl(**kwargs):
        girl = Girl(**kwargs)
        GIRLS[girl.id] = girl
        return girl

    def _stage_from_thresholds(value, thresholds):
        result = thresholds[0][1]
        for threshold, stage in thresholds:
            if value >= threshold:
                result = stage
        return result

    def get_stage_index(girl_id):
        girl = GIRLS[girl_id]
        return _stage_from_thresholds(get_affection(girl_id), girl.stage_thresholds)

    def get_sprite_suffix(girl_id):
        girl = GIRLS[girl_id]
        return _stage_from_thresholds(get_affection(girl_id), girl.sprite_thresholds)

    def girl_completed(girl_id):
        girl = GIRLS[girl_id]
        return get_stage_index(girl_id) >= girl.stage_thresholds[-1][1]

    def get_affection(girl_id):
        return affection.get(girl_id, 0)

    def add_affection(girl_id, amount):
        affection[girl_id] = get_affection(girl_id) + amount

    def set_flag(name):
        relationship_flags.add(name)

    def has_flag(name):
        return name in relationship_flags

    # Чтобы игрок не мог второй раз подряд ткнуть тот же вариант ответа в
    # рамках одной стадии: каждый вариант помечается использованным после
    # выбора и пропадает из меню (см. "if choice_open(...)" на пунктах
    # menu в game/characters/*.rpy). Когда использованы все варианты —
    # набор сбрасывается, чтобы меню не осталось пустым.
    def _choice_key(girl_id, stage, idx):
        return "%s_stage%d_choice%d_used" % (girl_id, stage, idx)

    def choice_open(girl_id, stage, idx):
        return not has_flag(_choice_key(girl_id, stage, idx))

    def use_choice(girl_id, stage, idx):
        set_flag(_choice_key(girl_id, stage, idx))

    def reset_choices_if_exhausted(girl_id, stage, count):
        keys = [_choice_key(girl_id, stage, i) for i in range(count)]
        if all(k in relationship_flags for k in keys):
            for k in keys:
                relationship_flags.discard(k)

    # Найденные на прогулке предметы (game/exploration.rpy) — тоже просто
    # флаги, без экрана инвентаря. Дарится только "любимый" предмет
    # девушки (Girl.favorite_item), проверяется в visit_router.
    def has_item(item_id):
        return has_flag("has_item_%s" % item_id)

    def give_item(item_id):
        set_flag("has_item_%s" % item_id)

    def has_gift_ready(girl_id):
        girl = GIRLS[girl_id]
        return girl.favorite_item and has_item(girl.favorite_item)

    def use_favorite_item(girl_id):
        girl = GIRLS[girl_id]
        relationship_flags.discard("has_item_%s" % girl.favorite_item)
        add_affection(girl_id, 20)


# Нана — ананас
init python:
    register_girl(
        id="nana", name="Нана", fruit="ананас", emoji="🍍",
        color="#FFBB5C", outline=(2, "#4A2C00", 0, 0),
        flaw="Колючесть", growth="Доверие",
        stage_thresholds=[(0, 1), (15, 2), (35, 3), (60, 4)],
        sprite_thresholds=[(0, "10"), (15, "20"), (35, "30")],
        sprite_stub="chars/nana/nana",
        bg="bg/pineapple_beach.jpg",
        favorite_item="seashell",
    )

# Иви — киви
init python:
    register_girl(
        id="ivi", name="Иви", fruit="киви", emoji="🥝",
        color="#8BC34A", outline=(2, "#33691E", 0, 0),
        flaw="Замкнутость", growth="Открытость",
        stage_thresholds=[(0, 1), (15, 2), (35, 3), (60, 4)],
        sprite_thresholds=[(0, "10"), (15, "20"), (35, "30")],
        sprite_stub="chars/ivi/ivi",
        bg="bg/kiwi_forest.jpg",
        favorite_item="moss_stone",
    )


# Спрайты и фоны по реестру — генерируются для каждой девушки.
# Если файла ещё нет на диске (арт не готов) — подставляется плейсхолдер
# Ren'Py вместо падения игры; как только реальный файл появится по тому
# же пути, лишний код трогать не надо.
#
# ConditionSwitch берёт первое истинное условие, поэтому пороги проверяем
# от большего к меньшему (иначе самый низкий порог "съест" все остальные).
# Самый нижний порог всегда "True" (а не ">= 0"), иначе отрицательный
# affection (после рискованного выбора в меню) не попадает ни в одно
# условие, и ConditionSwitch падает с "could not choose a displayable".
init python:
    for _girl in GIRLS.values():
        _cases = []
        _thresholds_desc = list(reversed(_girl.sprite_thresholds))
        for _i, (_threshold, _suffix) in enumerate(_thresholds_desc):
            _path = "%s_%s.png" % (_girl.sprite_stub, _suffix)
            _is_lowest = (_i == len(_thresholds_desc) - 1)
            _cases.append("True" if _is_lowest else "get_affection('%s') >= %d" % (_girl.id, _threshold))
            _cases.append(_path if renpy.loadable(_path) else Placeholder("girl", full=True))
        renpy.image(_girl.id, ConditionSwitch(*_cases))

        renpy.image(
            "bg %s" % _girl.id,
            _girl.bg if renpy.loadable(_girl.bg) else Placeholder("bg"),
        )


# ============================================
# ОТНОШЕНИЯ И ФЛАГИ
# ============================================

default affection = {}
default relationship_flags = set()
default current_girl = None
# Реальный спикер подставляется в visit_router перед каждой сценой;
# None здесь только чтобы статический анализ (lint) не ругался на "n".
default n = None


# ============================================
# ВИЗИТЫ — ОБЩАЯ ОБВЯЗКА ДЛЯ ВСЕХ ДЕВУШЕК
# ============================================

label visit_router:
    $ visits_today += 1
    $ n = GIRLS[current_girl].say

    if has_gift_ready(current_girl):
        jump expression "%s_gift_offer" % current_girl

    jump expression "%s_stage%d" % (current_girl, get_stage_index(current_girl))


label gift_offer_continue:
    jump expression "%s_stage%d" % (current_girl, get_stage_index(current_girl))


label return_to_map:
    call screen island_map
    return


# ============================================
# DEBUG: СИМПАТИЯ НА ЭКРАНЕ
# ============================================
# Показывает affection всех девушек в углу поверх любого экрана —
# удобно смотреть, как меняются цифры прямо во время диалога.
# Только в режиме разработки (config.developer == True при запуске из
# SDK/launcher, False в собранном билде) — игрок в релизе это не увидит.

screen debug_affection():
    zorder 101
    frame:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 20
        background Frame("#00000088", 12, 12)
        padding (14, 10)
        vbox:
            spacing 2
            text "DEBUG" size 16 color "#FF8888" bold True
            for _girl in GIRLS.values():
                text "%s: %d" % (_girl.name, get_affection(_girl.id)) size 16 color "#FFFFFF"

init python:
    if config.developer:
        config.overlay_screens.append("debug_affection")
