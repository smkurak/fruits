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
                     sprite_stub, bg, unlock_day=1):
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

    def get_affection(girl_id):
        return affection.get(girl_id, 0)

    def add_affection(girl_id, amount):
        affection[girl_id] = get_affection(girl_id) + amount

    def set_flag(name):
        relationship_flags.add(name)

    def has_flag(name):
        return name in relationship_flags


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
    )


# Спрайты по реестру — ConditionSwitch на каждую девушку.
# ConditionSwitch берёт первое истинное условие, поэтому пороги проверяем
# от большего к меньшему (иначе самый низкий порог "съест" все остальные).
init python:
    for _girl in GIRLS.values():
        _cases = []
        for _threshold, _suffix in reversed(_girl.sprite_thresholds):
            _cases.append("get_affection('%s') >= %d" % (_girl.id, _threshold))
            _cases.append("%s_%s.png" % (_girl.sprite_stub, _suffix))
        renpy.image(_girl.id, ConditionSwitch(*_cases))


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
    jump expression "%s_stage%d" % (current_girl, get_stage_index(current_girl))


label return_to_map:
    call screen island_map
    return
