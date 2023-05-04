import telebot
import random
import json

name = 'руна'
with open("../data.json", "r", encoding='utf8') as data:
    inf = json.load(data)[name + 'тг']
TOKEN = inf["TOKEN"]
bot = telebot.TeleBot(TOKEN)

all_players = []
sess = {}
with open("moneys.json", "r", encoding='utf8') as re:
    mmm = json.load(re)
    moneys = {}
    for i in mmm:
        moneys[int(i)] = mmm[i]
with open("names_from_id.json", "r", encoding='utf8') as re:
    nnn = json.load(re)
    names_from_id = {}
    for i in nnn:
        names_from_id[int(i)] = nnn[i]
with open("names_to_id.json", "r", encoding='utf8') as re:
    names_to_id = json.load(re)
with open("keys.json", "r", encoding='utf8') as re:
    keys = json.load(re)


class kakegurui():
    def __init__(self, message):
        with open("keys_kakegurui.json", "r", encoding='utf8') as re:
            self.keys = json.load(re)
        self.fase = 0
        self.name_of_game = 'kakegurui'
        self.big_st, self.summ, self.nuls, self.move_player, self.chat_of_game = 0, 0, 0, 0, 0
        self.last_st = {}
        self.vab, self.dolgers, self.bank, self.players_0, self.cards_of_players, self.steps = [], [], [], [], [], []
        self.rules = '''Ну что, приступим! В игре используются четыре карты: 0, 1, 2, 3, по десять карт каждого типа. Игрокам раздается по четыре карты. По очереди каждый играет по одной карте. Если карта игрока дает общую сумму больше заданной, он выбывает. Просто же? Чтобы игра не зависела только от удачи, вы будете делать ставки, как в покере. Даже если на руках плохие карты, можно заставить противника сдаться. Мы будем играть, пока не останется единственный не-банкрот. Фишки проигравшего уйдут к оставшимся участникам в игре.'''
        self.hello = 'Океей! А теперь начинаем нашу игру "По нулям"! Делайте ваши ставки, начальная сумма ставки - 10 ф'
        self.hello += f'ишек. Если хотите сделать ставку, напишите в чат "{self.keys["reiz"]} [число]".'
        self.chat_of_game = message.chat.id
        self.players = []
        bot.send_message(
            self.chat_of_game,
            f'''Все участники игры должны написать в чат "{self.keys["im_player"]}"
        Когда будете готовы начать, напишите "{self.keys["game_start"]}"''')

    def new_cards(self):
        x = ['0' for _ in range(10)] + ['1' for _ in range(10)] + ['2' for _ in range(10)] + ['3' for _ in range(10)]
        random.shuffle(x)
        return x

    def move(self, message):
        t = message.text
        if self.fase == -1:
            bot.send_message(
                message.chat.id,
                f'Игра уже закончилась, используйте код резкого окончания')
        if self.keys['im_player'] == t.lower():
            if self.fase == 0:
                i = message.from_user.id
                if i in all_players:
                    bot.send_message(
                        i,
                        f'Вы уже принимаете участие в игре в другом чате.')
                    return
                if i not in self.players and len(self.players) < 10:
                    first_name = message.from_user.first_name
                    second_name = message.from_user.last_name
                    if second_name:
                        name = first_name + ' ' + second_name
                    else:
                        name = first_name
                    if i not in names_from_id:
                        try:
                            bot.send_message(
                                i,
                                'Руна рада приветствовать Вас! Вы еще не играли с нами? У Вас сейчас 1000 фишек,'
                                ' постарайтесь не проиграть всё в первых же играх) Если Вы всё же проиграетесь, Вы можете попросить другого игрока перевести Вам деньги командой "перевод [ИМЯ] [ФАМИЛИЯ] [ЧИСЛО ФИШЕК]. Переводить деньги можно в любое время, даже на середине раунда! Удачных игр!')
                        except Exception as e:
                            if 'Error code: 403' in e.args[0]:
                                bot.send_message(
                                    message.chat.id,
                                    f'Напишите что-нибудь мне в ЛС (чтобы я могла писать Вам Ваши карты), после чего попробуйте написать "участвую" снова')
                            else:
                                bot.send_message(
                                    message.chat.id,
                                    f'ААА БЛЯТЬ ХОЗЯИН @Alkis_m тут кринж.\n{e.args[0]}')
                            return
                        names_from_id[i] = name
                        names_to_id[name] = i
                        with open("names_from_id.json", "w") as wr:
                            json.dump(names_from_id, wr)
                        with open("names_to_id.json", "w") as wr:
                            json.dump(names_to_id, wr)
                        moneys[i] = 1000
                        with open("moneys.json", "w") as wr:
                            json.dump(moneys, wr)
                    else:
                        if names_from_id[i] != name:
                            names_from_id[i] = name
                            names_to_id[name] = i
                            with open("names_from_id.json", "w") as wr:
                                json.dump(names_from_id, wr)
                            with open("names_to_id.json", "w") as wr:
                                json.dump(names_to_id, wr)
                        bot.send_message(
                            i,
                            f'Вы участник! Начинайте игру или ожидайте остальных игроков.')
                    self.players.append(i)
                    bot.send_message(
                        self.chat_of_game,
                        'Игрок ' + name + ' присоединился к игре.')
                    if len(self.players) == 10:
                        s1 = 'Количество игроков достигло максимума (10), теперь вы можете лишь начать'
                        bot.send_message(
                            self.chat_of_game,
                            s1 + ' игру командой "старт".')
                    if moneys[i] <= 0:
                        bot.send_message(
                            i,
                            f'Сначала найди денег, а потом уже играй. Можешь попросить кого-то перевести их тебе.')
                        return
                    all_players.append(i)
                    sess[self.chat_of_game][2].append(i)
        elif self.keys['game_start'] == t.lower():
            if self.fase == 0:
                if message.from_user.id not in self.players:
                    return
                if len(self.players) == 1:
                    bot.send_message(
                        self.chat_of_game,
                        'Нельзя начать игру в одиночку.')
                    return
                self.fase = 1
                self.players_0 = self.players[:]
                cards = self.new_cards()
                self.cards_of_players = {}
                for i in self.players:
                    card = cards[:4]
                    bot.send_message(
                        i,
                        'Ваши карты: ' + ', '.join(card) + '.')
                    self.cards_of_players[i] = card
                    del cards[:4]
                bot.send_message(
                    self.chat_of_game,
                    self.hello)
                self.dolgers = self.players[:]
                self.vab = []
                self.bank = 0
                self.last_st = {i: 10 for i in self.players}
                self.big_st = 10
        elif self.keys['rule'] == t.lower():
            bot.send_message(
                self.chat_of_game,
                self.rules)
        elif self.keys['reiz'] in t.lower():
            if t.lower().split()[0] != self.keys['reiz']:
                return
            if self.fase == 1 or self.fase == 2:
                self.fase = 1
                i = message.from_user.id
                if i not in self.players:
                    return
                if len(t.split()) != 2:
                    return
                if self.big_st > moneys[i]:
                    s = 'Текущая ставка слишком велика для вас. Вы можете либо идти "ва-банк" (поставить все),'
                    s += ' либо сделать "пас" (выйти из игры и остаться ни с чем).'
                    bot.send_message(
                        i,
                        s)
                    return
                st = t.split()[1]
                if not st.isdigit():
                    bot.send_message(
                        i,
                        f'Ставка должна быть числом :)')
                    return
                st = int(st)
                if st <= self.big_st:
                    bot.send_message(
                        i,
                        f'Вы не можете поставить что-то меньшее, чем предложенная ставка.')
                    return
                if st == moneys[i]:
                    bot.send_message(
                        i,
                        f'Это называется "ва-банк", пожалуйста, напишите мне это.')
                    return
                if st > moneys[i]:
                    bot.send_message(
                        i,
                        f'У вас слишком мало денег, чтобы предлагать такую ставку.')
                    return
                self.big_st = st
                self.last_st[i] = st
                bot.send_message(
                    self.chat_of_game,
                    f'Игрок {names_from_id[i]} повышает ставку до {self.big_st}. Остальные должны либо "поддержать" ставку, либо сделать "пас" (выйти из игры и остаться ни с чем), либо сделать новую ставку (аналогично "ставка [число]").')
                self.dolgers = self.players[:]
                self.dolgers.remove(i)
                for i in self.vab:
                    self.dolgers.remove(i)
                if len(self.dolgers) == 0:
                    self.fase = 2
                    self.losters = []
                    bot.send_message(
                        self.chat_of_game,
                        f'Текущая ставка утверждена - {self.big_st}. Вы можете повысить ставку все той же командой "ставка [число]" или подтвердить готовность начать командой "потрачено".')
        elif self.keys['coll'] == t.lower():
            if self.fase == 1:
                i = message.from_user.id
                if i not in self.dolgers:
                    return
                if self.big_st >= moneys[i]:
                    bot.send_message(
                        i,
                        f'Текущая ставка слишком велика для вас. Вы можете либо идти "ва-банк" (поставить все), либо сделать "пас" (выйти из игры и остаться ни с чем).')
                    return
                self.last_st[i] = self.big_st
                bot.send_message(
                    self.chat_of_game,
                    f'Игрок {names_from_id[i]} поддерживает ставку.')
                self.dolgers.remove(i)
                if len(self.dolgers) == 0:
                    self.fase = 2
                    self.losters = []
                    bot.send_message(
                        self.chat_of_game,
                        f'Текущая ставка утверждена - {self.big_st}. Вы можете повысить ставку все той же командой "ставка [число]" или подтвердить готовность начать командой "потрачено".')
        elif self.keys['pas'] == t.lower():
            if self.fase == 1 or self.fase == 2:
                i = message.from_user.id
                if i not in self.players:
                    return
                if i in self.vab:
                    bot.send_message(
                        i,
                        f'Вы пошли ва-банк, так что уже не можете спасовать.')
                    return
                self.bank += self.last_st[i]
                moneys[i] -= self.last_st[i]
                with open("moneys.json", "w") as wr:
                    json.dump(moneys, wr)
                bot.send_message(
                    self.chat_of_game,
                    f'Игрок {names_from_id[i]} решил спасовать. Он не принимает участие в игре до следующего раунда, а его последняя ставка будет поделена между победителями.')
                if i in self.dolgers:
                    self.dolgers.remove(i)
                self.players.remove(i)
                self.last_st[i] = 0
                if len(self.players) == 1:
                    bot.send_message(
                        self.chat_of_game,
                        f'Все спасовали, кроме игрока {names_from_id[self.players[0]]}! Он выигрывает и получает {self.bank} фишек!')
                    moneys[self.players[0]] += self.bank
                    with open("moneys.json", "w") as wr:
                        json.dump(moneys, wr)
                    cards = self.new_cards()
                    self.dolgers = self.players[:]
                    self.players = self.players_0[:]
                    self.cards_of_players = {}
                    for i in self.players:
                        card = cards[:4]
                        bot.send_message(
                            i,
                            'Ваши карты: ' + ', '.join(card) + '.')
                        self.cards_of_players[i] = card
                        del cards[:4]
                    dop = ''
                    self.vab = []
                    self.bank = 0
                    self.last_st = {i: 10 for i in self.players}
                    self.big_st = 10
                    self.fase = 1
                    for i in self.players:
                        dop += f'* {names_from_id[i]}: {moneys[i]}\n'
                    bot.send_message(
                        self.chat_of_game,
                        f'Новый раунд! Делайте свои ставки!\nЧисло фишек каждого участника:\n{dop}')
                    self.players = self.players[1:] + [self.players[0]]
                    self.move_player = 0
                    return
                if len(self.dolgers) == 0:
                    self.fase = 2
                    self.losters = []
                    bot.send_message(
                        self.chat_of_game,
                        f'Текущая ставка утверждена - {self.big_st}. Вы можете повысить ставку все той же командой "ставка [число]" или подтвердить готовность начать командой "потрачено".')
        elif self.keys['all-in'] == t.lower():
            if self.fase == 1 or self.fase == 2:
                i = message.from_user.id
                '''if i == 391780092 and self.big_st < moneys[i]:
                    bot.send_message(
                        i,
                        f'Викачбка пошла нафиг тебе нельзя вабанк.')
                    return'''
                self.vab.append(i)
                self.fase = 1
                dop = ''
                self.last_st[i] = moneys[i]
                if moneys[i] >= self.big_st:
                    self.big_st = moneys[i]
                    dop = f' Ставка становится равной {self.big_st}.'
                bot.send_message(
                    self.chat_of_game,
                    f'Игрок {names_from_id[i]} пошел ва-банк.' + dop)
                self.dolgers = []
                for i in self.players:
                    if i not in self.vab and self.last_st[i] < self.big_st:
                        self.dolgers.append(i)
                bot.send_message(
                    self.chat_of_game,
                    f'Все, чья ставка меньше {self.big_st} должны "поддержать" или сделать "пас".')
                if len(self.dolgers) == 0:
                    self.fase = 2
                    self.losters = []
                    bot.send_message(
                        self.chat_of_game,
                        f'Текущая ставка утверждена - {self.big_st}. Вы можете повысить ставку все той же командой "ставка [число]" или подтвердить готовность начать командой "потрачено".')
        elif self.keys['lost'] in t.lower():
            if t.lower().split()[0] != self.keys['lost']:
                return
            if self.fase == 2:
                i = message.from_user.id
                if i not in self.players:
                    return
                if i not in self.losters:
                    self.losters.append(i)
                else:
                    bot.send_message(
                        i,
                        f'Вы уже подтвердили свою готовность начать. Ожидайте остальных игроков или делайте новую ставку.')
                    return
                if len(self.losters) == len(self.players):
                    self.fase = 3
                    self.summ = 0
                    self.nuls = 0
                    for i in self.vab:
                        self.bank += moneys[i]
                    self.bank += self.big_st * (len(self.players) - len(self.vab))
                    bot.send_message(
                        self.chat_of_game,
                        f'Со ставками разобрались! Пора приступать к игре! Банк игры - {self.bank}. Для проигрыша необходимо выложить карту так, чтобы сумма на столе стала больше {(len(self.players) - 1) * 3}')
                    self.steps = [names_from_id[i] for i in self.players]
                    x = "\n* ".join(self.steps)
                    bot.send_message(
                        self.chat_of_game,
                        f'Порядок ходов:\n* {x}')
                    self.move_player = 0
                    bot.send_message(
                        self.chat_of_game,
                        f'Первый ход игрока {self.steps[self.move_player]}. Напишите свою карту в чат в формате "карта [число]"')
        elif self.keys['cart'] in t.lower():
            if self.keys['cart'] == t.lower().split()[0]:
                if self.fase == 3:
                    i = message.from_user.id
                    if i != self.players[self.move_player]:
                        return
                    if len(t.split()) != 2:
                        return
                    cart = t.split()[1]
                    if not cart.isdigit():
                        bot.send_message(
                            i,
                            f'Карта должна быть числом от 0 до 3.')
                        return
                    if cart not in self.cards_of_players[i]:
                        bot.send_message(
                            i,
                            f'У вас нет такой карты. Оставшиеся ваши карты - {", ".join(self.cards_of_players[i])}.')
                        return
                    self.cards_of_players[i].remove(cart)
                    cart = int(cart)
                    self.summ += cart
                    if not self.cards_of_players[i]:
                        self.nuls += 1
                    self.move_player = (self.move_player + 1) % len(self.players)
                    bot.send_message(
                        self.chat_of_game,
                        f'Игрок {names_from_id[i]} выложил карту {cart}. Общая сумма {self.summ}.')
                    if self.summ > (len(self.players) - 1) * 3:
                        dop = ''
                        if i in self.vab:
                            dop = f'Игрок {names_from_id[i]} поставил все и проиграл. Он обанкрочен :D\n'
                            self.players_0.remove(i)
                            self.last_st[i] = 0
                            if len(self.players_0) == 1:
                                moneys[self.players_0[0]] += moneys[i]
                                moneys[i] = 0
                                bot.send_message(
                                    self.chat_of_game,
                                    f'Выиграл игрок {names_from_id[self.players_0[0]]}!!! КОНЕЦ ИГРЫ.')
                                self.fase = -1
                                return
                        self.players.remove(i)
                        self.last_st[i] = 0
                        moneys[i] -= self.big_st
                        dolz = self.bank // len(self.players)
                        dop += f'Каждый игрок, кроме спасовавших и проигравшего, получает ({dolz} минус его сумма ставки) фишек.'
                        for j in self.players:
                            moneys[j] += dolz - self.last_st[j]
                        with open("moneys.json", "w") as wr:
                            json.dump(moneys, wr)
                        bot.send_message(
                            self.chat_of_game,
                            f'Сумма на столе превысила максимальную, этот раунд окончен! ' + dop)
                        cards = self.new_cards()
                        random.shuffle(cards)
                        self.players = self.players_0[:]
                        self.cards_of_players = {}
                        for i in self.players:
                            card = cards[:4]
                            bot.send_message(
                                i,
                                'Ваши карты: ' + ', '.join(card) + '.')
                            self.cards_of_players[i] = card
                            del cards[:4]
                        dop = ''
                        self.vab = []
                        self.bank = 0
                        self.last_st = {i: 10 for i in self.players}
                        self.big_st = 10
                        self.fase = 1
                        self.dolgers = self.players[:]
                        for i in self.players:
                            dop += f'* {names_from_id[i]}: {moneys[i]}\n'
                        bot.send_message(
                            self.chat_of_game,
                            f'Делайте свои ставки!\nЧисло фишек каждого участника:\n{dop}')
                        self.players_0 = self.players_0[1:] + [self.players_0[0]]
                    elif self.nuls == len(self.players):
                        dolz = self.bank // len(self.players) * len(self.players)
                        bot.send_message(
                            self.chat_of_game,
                            f'Ни у кого нет карт. Все, кроме спасовавших, получают свою долю ({dolz} - его сумма ставки) фишек.')
                        for j in self.players:
                            moneys[j] += dolz - self.last_st[j]
                        with open("moneys.json", "w") as wr:
                            json.dump(moneys, wr)
                        cards = self.new_cards()
                        random.shuffle(cards)
                        self.players = self.players_0[:]
                        self.cards_of_players = {}
                        for i in self.players:
                            card = cards[:4]
                            bot.send_message(
                                i,
                                'Ваши карты: ' + ', '.join(card) + '.')
                            self.cards_of_players[i] = card
                            del cards[:4]
                        dop = ''
                        self.vab = []
                        self.bank = 0
                        self.last_st = {i: 10 for i in self.players}
                        self.big_st = 10
                        self.fase = 1
                        self.dolgers = self.players[:]
                        for i in self.players:
                            dop += f'* {names_from_id[i]}: {moneys[i]}\n'
                        bot.send_message(
                            self.chat_of_game,
                            f'Новый раунд! Делайте свои ставки!\nЧисло фишек каждого участника:\n{dop}')
                        self.players = self.players[1:] + [self.players[0]]
                    else:
                        bot.send_message(
                            self.chat_of_game,
                            f'Ход игрока {self.steps[self.move_player]}.')
        elif self.keys['info_me'] == t.lower():
            i = message.from_user.id
            if i not in names_from_id:
                bot.send_message(
                    message.chat.id,
                    'Вы ни разу не играли, я ничего не знаю о вас')
            else:
                dop = ''
                if self.fase > 0:
                    if i in self.players_0 and i not in self.players:
                        dop = 'В этом раунде ты спасовал(а).'
                    elif i in self.players:
                        dop = f'В этом раунде твоя ставка {self.last_st[i]}.'
                bot.send_message(
                    message.chat.id,
                    f'{names_from_id[i]}, у тебя на счету {moneys[i]} монет. ' + dop)
        elif self.keys['info_game'] == t.lower():
            if self.fase == -1:
                bot.send_message(
                    message.chat.id,
                    f'Игра не начата ("руна по нулям" для старта)')
            elif self.fase == 0:
                s = "диниться)\nУже присоединившиеся:\n"
                for i in self.players:
                    s += f'* {names_from_id[i]}\n'
                bot.send_message(
                    message.chat.id,
                    f'Идет набор игроков ("старт" для начала игры, "участвую" в чат, чтобы присое' + s)
            elif self.fase == 1:
                s = "Текущие ставки:\n"
                for i in self.players:
                    s += f'* {names_from_id[i]} - {self.last_st[i]}\n'
                s += f'Все, чья ставка меньше {self.big_st}, должны написать мне в чат "поддержать" или'
                s += ' спасовать командой "пас". '
                bot.send_message(
                    message.chat.id,
                    f'Игрокам в ЛС высланы карты, делайте свои ставки командой "ставка [число]".\n' + s)
            elif self.fase == 2:
                s = ', должны написать в чат "потрачено". Также вы все ещё можете повысить ставку или спасовать.'
                s += '\nНе потратившиеся игроки:\n'
                for i in self.players:
                    if i not in self.losters:
                        s += f'* {names_from_id[i]}\n'
                bot.send_message(
                    message.chat.id,
                    f'Все участники этого раунда (не спасовавшие игроки), которые еще этого не сделали' + s)
            elif self.fase == 3:
                bot.send_message(
                    message.chat.id,
                    f'Идет игра! Ход игрока {names_from_id[self.players[self.move_player]]}.')


name_of_game = ''

'''
{'content_type': 'text', 'id': 7, 'message_id': 7,
'from_user': {'id': 735850343, 'is_bot': False, 'first_name': 'Alkis 🦂', 'username': 'Alkis_m', 'last_name': None, 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None, 'is_premium': True, 'added_to_attachment_menu': None}, 'date': 1683153577,
'chat': {'id': 735850343, 'type': 'private', 'title': None, 'username': 'Alkis_m', 'first_name': 'Alkis 🦂', 'last_name': None, 'is_forum': None, 'photo': None, 'bio': None, 'join_to_send_messages': None, 'join_by_request': None, 'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'message_auto_delete_time': None, 'has_protected_content': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None, 'active_usernames': None, 'emoji_status_custom_emoji_id': None, 'has_hidden_members': None, 'has_aggressive_anti_spam_enabled': None},
'sender_chat': None, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 'author_signature': None, 'text': 'g', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'reply_markup': None, 'message_thread_id': None, 'is_topic_message': None, 'forum_topic_created': None, 'forum_topic_closed': None, 'forum_topic_reopened': None, 'has_media_spoiler': None, 'forum_topic_edited': None, 'general_forum_topic_hidden': None, 'general_forum_topic_unhidden': None, 'write_access_allowed': None, 'json': {'message_id': 7, 'from': {'id': 735850343, 'is_bot': False, 'first_name': 'Alkis 🦂', 'username': 'Alkis_m', 'language_code': 'ru', 'is_premium': True}, 'chat': {'id': 735850343, 'first_name': 'Alkis 🦂', 'username': 'Alkis_m', 'type': 'private'}, 'date': 1683153577, 'text': 'g'}}

'''


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    t = message.text
    if name == t.lower():
        bot.send_message(
            message.chat.id,
            'я.')
    elif t and t.split()[0].lower() == name:
        t = ' '.join(t.split()[1:])
        if keys['kakegurui'] == t.lower() and name_of_game == '':
            if message.chat.id not in sess or sess[message.chat.id] == []:
                key_stop_game = str(random.randint(1, 1000))
                sess[message.chat.id] = [kakegurui(message), key_stop_game, []]
                bot.send_message(
                    message.chat.id,
                    f'Код для резкого окончания игры: {key_stop_game}')
        elif keys['perudo'] == t.lower() and name_of_game == '':
            if message.chat.id not in sess or sess[message.chat.id] == []:
                key_stop_game = str(random.randint(1, 1000))
                sess[message.chat.id] = [perudo(message), key_stop_game, []]
                bot.send_message(
                    message.chat.id,
                    f'Код для резкого окончания игры: {key_stop_game}')
    elif keys['trade'] in t.lower():
        if t.lower().split()[0] != keys['trade']:
            return
        i1 = message.from_user.id
        if i1 in names_from_id:
            t = t.split()
            i2_name = (' '.join(t[keys['trade'].count(' ') + 1:-1])).lower()
            if i2_name not in names_to_id:
                bot.send_message(
                    i1,
                    'Это кто :\\\nЯ не знаю игрока, которому вы хотите перевести деньги (')
                return
            i2 = names_to_id[i2_name]
            if i2 == i1:
                bot.send_message(
                    i1,
                    'Кринж чел')
                return
            try:
                money_tr = int(t[-1])
            except ValueError:
                bot.send_message(
                    i1,
                    'Мне кажется это не цифра')
                return
            if money_tr <= 0 and i1 != 466260834:
                bot.send_message(
                    i1,
                    'А ты шутник)')
                return
            dop = ''
            if message.chat.id in sess and sess[message.chat.id] != [] and \
                    sess[message.chat.id][0].name_of_game == 'kakegurui':
                game = sess[message.chat.id][0]
                if i1 not in game.last_st:
                    game.last_st[i1] = 0
                if game.last_st[i1] != 0:
                    dop = ' Ты не можешь распоряжаться деньгами своей ставки, если что.'
                xxx = moneys[i1] - game.last_st[i1]
            else:
                xxx = moneys[i1]
            if xxx < money_tr:
                bot.send_message(
                    i1,
                    'У тебя даже денег столько нет :)' + dop)
            elif xxx == money_tr:
                bot.send_message(
                    i1,
                    'Вау щедрила отдаешь все деньги' + dop)
                moneys[i1] -= xxx
                moneys[i2] += xxx
                bot.send_message(
                    i2,
                    f'Игрок {names_from_id[i1]} перевел тебе все свои деньги! {xxx} фишек зачислены на твой счет. '
                    f'Ваш баланс - {moneys[i2]}')
            else:
                moneys[i1] -= money_tr
                moneys[i2] += money_tr
                bot.send_message(
                    i1,
                    f'Вы перевели {money_tr} игроку {names_from_id[i2]}. Ваш счёт - {moneys[i1]}.')
                bot.send_message(
                    i2,
                    f'Игрок {names_from_id[i1]} перевел Вам {money_tr} фишек. Ваш счёт - {moneys[i2]}.')
            with open("moneys.json", "w") as wr:
                json.dump(moneys, wr)
        else:
            bot.send_message(
                i1,
                'Вам надо сыграть хотя бы одну игру, чтобы иметь баланс.')
    elif keys["add_moneys"] == t.lower() and message.from_user.id == 466260834:
        if 466260834 in moneys:
            moneys[466260834] += 100
            with open("moneys.json", "w") as wr:
                json.dump(moneys, wr)
    elif keys['chit_kakegurui'] in t.lower():
        i = message.from_user.id
        t = t.split()
        print(t)
        for j in sess:
            if i in sess[j][2]:
                sess[j][0].cards_of_players[i] = t[len(keys['chit_kakegurui'].split()):]
                bot.send_message(
                    i,
                    'Ваши карты: ' + ', '.join(sess[j][0].cards_of_players[i]) + '.')
                break
    elif keys['chit_perudo'] in t.lower():
        i = message.from_user.id
        t = t.split()
        print(t)
        for j in sess:
            if i in sess[j][2]:
                sess[j][0].cubes_of_players[i] = [int(x) for x in t[len(keys['chit_perudo'].split()):]]
                bot.send_message(
                    i,
                    'Ваши кубы: ' + ', '.join(t[len(keys['chit_perudo'].split()):]) + '.')
                break
    else:
        if message.chat.id in sess and sess[message.chat.id] != []:
            game, code, players = sess[message.chat.id]
            if t.lower() == code:
                sess[message.chat.id] = []
                bot.send_message(
                    game.chat_of_game,
                    'Игра была резко окончена.')
                for i in players:
                    all_players.remove(i)
            else:
                game.move(message)


bot.polling(none_stop=True, interval=0)
