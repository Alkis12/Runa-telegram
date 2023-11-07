'''
class perudo():
    def __init__(self):
        with open("keys_perudo.json", "r", encoding='utf8') as re:
            self.keys = json.load(re)
        self.move_player = 0
        self.count = 0
        self.nominal = 0
        self.is_maputo = False
        self.fase = 0
        self.vab, self.players_0, self.cubes_of_players, self.steps = [], [], [], []
        self.rules = 'пу пу пу чекните правила в википедии по запросу "перудо"'
        self.hello = 'Океей! А теперь начинаем нашу игру в пиратские кости!'
        self.chat_of_game = event.obj.message['peer_id']
        self.players = []
        self.lol = []
        self.variants1 = 'единица единицы единиц'
        self.variants2 = 'двойка двойки двоек'
        self.variants3 = 'тройка тройки троек'
        self.variants4 = 'четверка четверки четверок'
        self.variants5 = 'пятерка пятерки пятерок'
        self.variants6 = 'шестерка шестерки шестерок'
        vk.messages.send(
            peer_id=self.chat_of_game,
            message=f'''Все участники игры должны написать в чат "{self.keys["im_player"]}"
        Когда будете готовы начать, напишите "{self.keys["game_start"]}"''',
            random_id=random.randint(0, 2 ** 64))

    def move(self, event):
        t = event.obj.message['text']
        if self.fase == -1:
            vk.messages.send(
                peer_id=event.obj.message['peer_id'],
                message=f'Игра уже закончилась, используйте код резкого окончания',
                random_id=random.randint(0, 2 ** 64))
        if self.keys['im_player'] == t.lower():
            if self.fase == 0:
                i = event.obj.message['from_id']
                if i in all_players:
                    vk.messages.send(
                        peer_id=i,
                        message=f'Вы уже принимаете участие в игре в другом чате.',
                        random_id=random.randint(0, 2 ** 64))
                    return
                if i not in self.players and len(self.players) < 10:
                    if i not in names:
                        if i in self.lol:
                            vk.messages.send(
                                peer_id=i,
                                message='Руна рада приветствовать Вас! Вы еще не играли с нами? У Вас сейчас 1000 фишек'
                                        ', которые вы можете тратить в различных играх) Если Вы проиграетесь, Вы можете'
                                        ' попросить другого игрока перевести Вам деньги командой "перевод [ИМЯ] [ФАМИЛИ'
                                        'Я] [ЧИСЛО ФИШЕК]. Переводить деньги можно в любое время, даже на середине раун'
                                        'да! Удачных игр!',
                                random_id=random.randint(0, 2 ** 64))
                            self.lol.remove(i)
                            response = vk.users.get(user_ids=i)
                            first_name = response[0]['first_name']
                            second_name = response[0]['last_name']
                            names[i] = first_name + ' ' + second_name
                            names1[(first_name + ' ' + second_name).lower()] = i
                            with open("names0.json", "w") as wr:
                                json.dump(names, wr)
                            with open("names1.json", "w") as wr:
                                json.dump(names1, wr)
                            moneys[i] = 1000
                            with open("moneys.json", "w") as wr:
                                json.dump(moneys, wr)
                        else:
                            vk.messages.send(
                                peer_id=event.obj.message['peer_id'],
                                message=f'Напишите что-нибудь мне в ЛС (чтобы я могла писать Вам Ваши кубы), после чего попробуйте написать "участвую" снова',
                                random_id=random.randint(0, 2 ** 64))
                            self.lol.append(i)
                            return
                    else:
                        vk.messages.send(
                            peer_id=i,
                            message=f'Вы участник! Начинайте игру или ожидайте остальных игроков.',
                            random_id=random.randint(0, 2 ** 64))
                    self.players.append(i)
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message='Игрок ' + names[i] + ' присоединился к игре.',
                        random_id=random.randint(0, 2 ** 64))
                    if len(self.players) == 6:
                        s1 = 'Количество игроков достигло максимума (6), теперь вы можете лишь начать'
                        vk.messages.send(
                            peer_id=self.chat_of_game,
                            message=s1 + ' игру командой "старт".',
                            random_id=random.randint(0, 2 ** 64))
                    all_players.append(i)
                    sess[self.chat_of_game][2].append(i)
        elif self.keys['rule'] == t.lower():
            vk.messages.send(
                peer_id=self.chat_of_game,
                message=self.rules,
                random_id=random.randint(0, 2 ** 64))
        elif self.keys['game_start'] == t.lower():
            if self.fase == 0:
                if event.obj.message['from_id'] not in self.players:
                    return
                if len(self.players) == 1:
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message='Нельзя начать игру в одиночку.',
                        random_id=random.randint(0, 2 ** 64))
                    return
                self.fase = 1
                random.shuffle(self.players)
                self.players_0 = self.players[:]
                self.cubes_of_players = {}
                self.count_of_cubes = {}
                for i in self.players:
                    cubes = [random.randint(1, 6) for i in range(5)]
                    vk.messages.send(
                        peer_id=i,
                        message='Ваши кубы: ' + ', '.join([str(x) for x in cubes]) + '.',
                        random_id=random.randint(0, 2 ** 64))
                    self.cubes_of_players[i] = cubes
                    self.count_of_cubes[i] = 5
                vk.messages.send(
                    peer_id=self.chat_of_game,
                    message=self.hello,
                    random_id=random.randint(0, 2 ** 64))
                self.steps = [names[i] for i in self.players]
                x = "\n* ".join(self.steps)
                vk.messages.send(
                    peer_id=self.chat_of_game,
                    message=f'Порядок ходов:\n* {x}',
                    random_id=random.randint(0, 2 ** 64))
                self.move_player = 0
                self.count = 0
                self.nominal = 0
                self.is_maputo = False
                vk.messages.send(
                    peer_id=self.chat_of_game,
                    message=f'Первый ход игрока {self.steps[self.move_player]}. Напишите свою ставку в чат в формате "ставка [количество(числом)] [номинал]" (например, "ставка 2 тройки")',
                    random_id=random.randint(0, 2 ** 64))
        elif self.keys['info_game'] == t.lower():
            if self.fase == -1:
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=f'Игра не начата ("руна перудо" для старта)',
                    random_id=random.randint(0, 2 ** 64))
            elif self.fase == 0:
                s = "диниться)\nУже присоединившиеся:\n"
                for i in self.players:
                    s += f'* {names[i]}\n'
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=f'Идет набор игроков ("старт" для начала игры, "участвую" в чат, чтобы присое' + s,
                    random_id=random.randint(0, 2 ** 64))
            elif self.fase == 1:
                vk.messages.send(
                    peer_id=event.obj.message['peer_id'],
                    message=f'Идет игра! Ход игрока {names[self.players[self.move_player]]}. Число кубов на столе: {sum([i for i in self.count_of_cubes.values()])}.',
                    random_id=random.randint(0, 2 ** 64))
        elif self.keys['cubes'] in t.lower():
            if self.keys['cubes'] == t.lower().split()[0]:
                if self.fase == 1:
                    i = event.obj.message['from_id']
                    if i != self.players[self.move_player]:
                        return
                    if len(t.split()) != 3:
                        return
                    count, nominal = t.split()[1:]
                    if not count.isdigit():
                        vk.messages.send(
                            peer_id=i,
                            message=f'Количество кубов должно быть числом.',
                            random_id=random.randint(0, 2 ** 64))
                        return
                    count = int(count)
                    if nominal not in self.variants1 + self.variants2 + self.variants3 + self.variants4 + self.variants5 + self.variants6:
                        vk.messages.send(
                            peer_id=i,
                            message=f'Я не знаю такого номинала кубов. Проверьте, возможно Вы ошиблись.',
                            random_id=random.randint(0, 2 ** 64))
                        return
                    else:
                        if nominal in self.variants1:
                            nominal = 1
                        elif nominal in self.variants2:
                            nominal = 2
                        elif nominal in self.variants3:
                            nominal = 3
                        elif nominal in self.variants4:
                            nominal = 4
                        elif nominal in self.variants5:
                            nominal = 5
                        elif nominal in self.variants6:
                            nominal = 6
                    if not self.is_maputo:
                        if self.nominal == 0:
                            if nominal == 1:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Нельзя начинать игру с единиц.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            self.count = count
                            self.nominal = nominal
                            self.move_player = (self.move_player + 1) % len(self.players)
                            vk.messages.send(
                                peer_id=self.chat_of_game,
                                message=f'Ход игрока {self.steps[self.move_player]}.',
                                random_id=random.randint(0, 2 ** 64))
                            return
                        if count < self.count and nominal != 1:
                            if self.nominal == 1:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Нельзя понижать число кубов.',
                                    random_id=random.randint(0, 2 ** 64))
                            else:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Нельзя понижать число кубов (если не уходишь в единицы).',
                                    random_id=random.randint(0, 2 ** 64))
                            return
                        if count <= self.count and nominal == 1:
                            if count != self.count // 2 + int(bool(self.count % 2)):
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Когда уходишь в единицы, число кубов становится в два раза меньше (с округлением в большую сторону).',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            else:
                                self.count = count
                                self.nominal = nominal
                                self.move_player = (self.move_player + 1) % len(self.players)
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Ход игрока {self.steps[self.move_player]}.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                        if count == self.count:
                            if nominal < self.nominal:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Нельзя понижать номинал, если не увеличиваешь количество.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            elif nominal == self.nominal:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Это же просто дублирование ставки прошлого игрока, так нельзя)',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            else:
                                self.count = count
                                self.nominal = nominal
                                self.move_player = (self.move_player + 1) % len(self.players)
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Ход игрока {self.steps[self.move_player]}.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                        if count > self.count and self.nominal == 1 and nominal == 1:
                            self.count = count
                            self.nominal = nominal
                            self.move_player = (self.move_player + 1) % len(self.players)
                            vk.messages.send(
                                peer_id=self.chat_of_game,
                                message=f'Ход игрока {self.steps[self.move_player]}.',
                                random_id=random.randint(0, 2 ** 64))
                            return
                        if count > self.count and self.nominal == 1 and nominal != 1:
                            if count != self.count * 2 + 1:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Когда выходишь из единиц, число кубов становится в два раза больше плюс один.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            else:
                                self.count = count
                                self.nominal = nominal
                                self.move_player = (self.move_player + 1) % len(self.players)
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Ход игрока {self.steps[self.move_player]}.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                        if count > self.count and self.nominal != 1 and nominal == 1:
                            vk.messages.send(
                                peer_id=self.chat_of_game,
                                message=f'В единицы можно уйти, лишь уменьшив число кубов.',
                                random_id=random.randint(0, 2 ** 64))
                            return
                        elif count > self.count and self.nominal != 1 and nominal != 1:
                            self.count = count
                            self.nominal = nominal
                            self.move_player = (self.move_player + 1) % len(self.players)
                            vk.messages.send(
                                peer_id=self.chat_of_game,
                                message=f'Ход игрока {self.steps[self.move_player]}.',
                                random_id=random.randint(0, 2 ** 64))
                            return
                    else:
                        if self.nominal == 0:
                            self.count = count
                            self.nominal = nominal
                            self.move_player = (self.move_player + 1) % len(self.players)
                            vk.messages.send(
                                peer_id=self.chat_of_game,
                                message=f'Ход игрока {self.steps[self.move_player]}.',
                                random_id=random.randint(0, 2 ** 64))
                            return
                        if count < self.count:
                            vk.messages.send(
                                peer_id=self.chat_of_game,
                                message=f'Во время Мапуто нельзя понижать число кубов никаким образом.',
                                random_id=random.randint(0, 2 ** 64))
                            return
                        if count == self.count:
                            if nominal < self.nominal:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Нельзя понижать номинал.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            elif nominal == self.nominal:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Это же просто дублирование ставки прошлого игрока, так нельзя)',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            else:
                                self.count = count
                                self.nominal = nominal
                                self.move_player = (self.move_player + 1) % len(self.players)
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Ход игрока {self.steps[self.move_player]}.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                        if count > self.count:
                            if nominal < self.nominal:
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Во время Мапуто нельзя понижать номинал даже при увеличении количества.',
                                    random_id=random.randint(0, 2 ** 64))
                                return
                            else:
                                self.count = count
                                self.nominal = nominal
                                self.move_player = (self.move_player + 1) % len(self.players)
                                vk.messages.send(
                                    peer_id=self.chat_of_game,
                                    message=f'Ход игрока {self.steps[self.move_player]}.',
                                    random_id=random.randint(0, 2 ** 64))
        elif self.keys['lie'] == t.lower():
            if self.fase == 1:
                i = event.obj.message['from_id']
                if i != self.players[self.move_player]:
                    return
                if self.nominal == 0:
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message=f'Ваш ход первый, кому Вы собираетесь не верить? Делайте ставку.',
                        random_id=random.randint(0, 2 ** 64))
                    return
                coco = 0
                s = 'Кубы всех игроков:\n'
                for j in self.players:
                    s += f'{names[j]}: {", ".join([str(x) for x in self.cubes_of_players[j]])};\n'
                    for k in self.cubes_of_players[j]:
                        if (not self.is_maputo and k == 1) or k == self.nominal:
                            coco += 1
                if self.is_maputo:
                    self.is_maputo = False
                vk.messages.send(
                    peer_id=self.chat_of_game,
                    message=s,
                    random_id=random.randint(0, 2 ** 64))
                if coco < self.count:
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message=f'На столе лишь {coco} кубов этого номинала. Вы оказались правы! Предыдущий игрок сбрасывает куб.',
                        random_id=random.randint(0, 2 ** 64))
                    self.move_player -= 1
                    if self.move_player == -1:
                        self.move_player = len(self.players) - 1
                else:
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message=f'На столе целых {coco} кубов этого номинала! Вы ошиблись и лишаетесь одного куба.',
                        random_id=random.randint(0, 2 ** 64))
                mo = self.move_player
                imo = names1[self.steps[mo].lower()]
                self.count_of_cubes[imo] -= 1
                if self.count_of_cubes[imo] == 1:
                    self.is_maputo = True
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message=f'У одного из игроков остался один куб. Объявляется специальный раунд МАПУТО!!!',
                        random_id=random.randint(0, 2 ** 64))
                if self.count_of_cubes[imo] == 0:
                    vk.messages.send(
                        peer_id=self.chat_of_game,
                        message=f'У игрока {self.steps[mo]} не осталось кубов. Он выбывает(',
                        random_id=random.randint(0, 2 ** 64))
                    self.steps.remove(names[imo])
                    self.players.remove(imo)
                    if self.move_player == len(self.players):
                        self.move_player = 0
                    if len(self.players) == 1:
                        vk.messages.send(
                            peer_id=self.chat_of_game,
                            message=f'Остался лишь один игрок с кубами! Побеждает {names[self.players[0]]}! Игра окончена. Введите код резкого окончания игры.',
                            random_id=random.randint(0, 2 ** 64))
                        self.fase = -1
                        return
                for i in self.players:
                    cubes = [random.randint(1, 6) for i in range(self.count_of_cubes[i])]
                    vk.messages.send(
                        peer_id=i,
                        message='Ваши кубы: ' + ', '.join([str(x) for x in cubes]) + '.',
                        random_id=random.randint(0, 2 ** 64))
                    self.cubes_of_players[i] = cubes
                self.count = 0
                self.nominal = 0
                vk.messages.send(
                    peer_id=self.chat_of_game,
                    message=f'Ход игрока {self.steps[self.move_player]}.',
                    random_id=random.randint(0, 2 ** 64))
'''