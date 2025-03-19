import vk_api, random, requests, time, threading
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# в файле key.py указать токен юзера и токен группы
from key import token_user, token_session

vk_session = vk_api.VkApi(token = token_session)
longpoll = VkBotLongPoll(vk_session, 216149415)
dat = 0

def numCards(cards):
    number = 0
    for card in cards:
        if card.startswith('6'):
            number += 6
        elif card.startswith('7'):
            number += 7
        elif card.startswith('8'):
            number += 8
        elif card.startswith('9'):
            number += 9
        elif card.startswith('1'):
            number += 10
        elif card.startswith('J'):
            number += 2
        elif card.startswith('Q'):
            number += 3
        elif card.startswith('K'):
            number += 4
        else:
            number += 11
    return number

def sender(id, text):
    vk_session.method('messages.send', {'peer_ids' : 2000000000 + id, 'message' : text, 'random_id' : 0})

def deleter(id, cmid):
    vk_session.method('messages.delete', {
        'delete_for_all': 1,
        'peer_id': 2000000000 + id,
        'cmids': cmid,
    })

def edit(id, cmid, text):
    vk_session.method('messages.edit', {
        'message': text,
        'peer_id': 2000000000 + id,
        'conversation_message_id': cmid,
    })

def getHistory(count, id):
    vk_session.method('messages.getHistory', {
        'count': count,
        'peer_id': 2000000000 + id,
        'group_id': 216149415,

    })



def keyboardSender(id, keyboard, text):
    vk_session.method('messages.send', {
        'chat_id': id,
        'random_id': 0,
        'message': text,
        'keyboard': keyboard.get_keyboard()
    })

def find_string_number(data, required):
    with open(data) as file:
        for num_line, line in enumerate(file):
            if required in line:
                return (num_line)

    return (-1)

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:

            id = event.chat_id
            msg = event.object.message['text'].lower()
            user_id = event.message.from_id
            user = vk_session.method("users.get", {"user_ids": str(user_id)})
            fullname = user[0]['first_name'] + ' ' + user[0]['last_name']

            if msg == '/бот старт':
                user_id = event.message.from_id

                user = vk_session.method("users.get", {"user_ids": str(user_id)})
                fullname = user[0]['first_name'] + ' ' + user[0]['last_name']


                file_path = "data.txt"
                required = str(user_id)



                string_numbers = find_string_number(file_path, required)
                if string_numbers == -1:
                    f = open('data.txt', 'a', encoding='utf-8')
                    f.write(str(user_id) + ' ' + str(fullname) + ' ' + '1000' + ' ' + '0' + '\n')
                    f.close()
                    sender(id, 'Вы успешно зарегистрированы!')
                else:
                    sender(id, 'Вы уже зарегистрированы!')



            elif msg == '/бот инфо':
                user_id = event.message.from_id

                file_path = "data.txt"
                required = str(user_id)





                string_numbers = find_string_number(file_path, required)
                if string_numbers == -1:
                    sender(id, 'Вы ещё не зарегистрированы!')
                else:
                    num = string_numbers
                    f = open('data.txt', encoding='utf-8')
                    data = f.read()
                    line11 = data.split('\n')[num]
                    nom = num + 1
                    kolvo = line11.split()[3]
                    at = int(int(kolvo) * 0.3)
                    name = line11.split()[1] + ' ' + line11.split()[2]
                    f.close()


                    sender(id, f"Регистрационный номер - {nom}\nИмя - {name}\nРоботов - {kolvo}({at} на защите)")

            elif msg == '/бот топ':
                def top_players(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        players = []
                        for line in f:
                            player_data = line.split()
                            player_id = player_data[0]
                            player_name = player_data[1]
                            player_surname = player_data[2]
                            player_score = int(player_data[3])
                            players.append((player_score, player_name, player_surname))

                        players.sort(reverse=True)

                        top_players = []
                        for i, player in enumerate(players[:10]):
                            top_players.append(f"{i + 1}. {player[1]} {player[2]} - {player[0]}\n")

                        return ''.join(top_players)


                sender(id, top_players('data.txt'))

            elif msg.startswith('/бот напасть'):
                user_id = event.message.from_id

                file_path = "data.txt"
                required = str(user_id)




                string_numbers = find_string_number(file_path, required)
                if string_numbers == -1:
                    sender(id, 'Вы ещё не зарегистрированы!')
                else:
                    line_count = sum(1 for line in open('data.txt'))
                    reg = msg.split()
                    if int(len(reg)) < 4:
                        sender(id, 'Ошибка! Указаны неверные значения')
                    else:

                        reg = msg.split()[2]
                        attac = msg.split()[3]
                        s = reg + attac

                        def isint(s):
                            try:
                                int(s)
                                return 1
                            except ValueError:
                                return 0


                        if isint(s) == 0:
                            sender(id, 'Ошибка! Указаны неверные значения')
                        else:
                            if int(reg) > int(line_count) or int(reg) < 1:
                                sender(id, 'Ошибка! Такого регистрационного номера ещё нет')
                            else:
                                reg = int(msg.split()[2])
                                reg = reg - 1
                                attac = int(msg.split()[3])


                                user_id = event.message.from_id

                                file_path = "data.txt"
                                required = str(user_id)




                                string_numbers = find_string_number(file_path, required)
                                if string_numbers == -1:
                                    sender(id, 'Вы ещё не зарегистрированы!')
                                else:
                                    num = string_numbers
                                    f = open('data.txt', encoding='utf-8')
                                    data = f.read()
                                    line11 = data.split('\n')[num]
                                    kolvo = int(int(line11.split()[3]) * 0.5)
                                    defat1 = data.split('\n')[reg]
                                    defat = int(int(defat1.split()[3]) * 0.3)
                                    f.close()

                                    if attac > kolvo:
                                        sender(id, f"Ошибка! У Вас доступно всего {kolvo} роботов для нападения!")
                                    elif attac <= kolvo:
                                        if attac < defat:
                                            sender(id, f"Ошибка! У Вашего противника {defat} роботов в защите! Вы не можете атаковать в меньшинстве")
                                        elif attac >= defat:

                                                x = int((attac / (attac + defat)) * 100)
                                                n = random.randint(1, 100)
                                                if n <= x:

                                                    fin = open("data.txt", "rt", encoding='utf-8')
                                                    data = fin.read()
                                                    data = data.replace(str(line11), str(str(line11.split()[0]) + ' ' + str(line11.split()[1]) + ' ' + str(line11.split()[2]) + ' ' + str(int(line11.split()[3]) + defat) + ' ' + str(line11.split()[4])))
                                                    data = data.replace(str(defat1), str(str(defat1.split()[0]) + ' ' + str(
                                                        defat1.split()[1]) + ' ' + str(defat1.split()[2]) + ' ' + str(
                                                        int(defat1.split()[3]) - defat) + ' ' + str(defat1.split()[4])))
                                                    fin.close()
                                                    fin = open("data.txt", "wt", encoding='utf-8')
                                                    fin.write(data)
                                                    fin.close()

                                                    fin = open("data.txt", encoding='utf-8')
                                                    data = fin.read()
                                                    line11 = data.split('\n')[num]
                                                    kolvo = line11.split()[3]
                                                    defat1 = data.split('\n')[reg]
                                                    defat = defat1.split()[3]
                                                    name = defat1.split()[1] + ' ' + defat1.split()[2]


                                                    sender(id, f"Вы победили в сражении!\n"
                                                               f"Шанс победить был {x}%\n"
                                                               f"Ваши роботы - {kolvo}\n"
                                                               f"Роботы {name} - {defat}")
                                                    fin.close()
                                                else:

                                                    fin = open("data.txt", "rt", encoding='utf-8')
                                                    data = fin.read()
                                                    data = data.replace(str(line11), str(str(line11.split()[0]) + ' ' + str(
                                                        line11.split()[1]) + ' ' + str(line11.split()[2]) + ' ' + str(
                                                        int(line11.split()[3]) - attac) + ' ' + str(line11.split()[4])))
                                                    data = data.replace(str(defat1), str(str(defat1.split()[0]) + ' ' + str(
                                                        defat1.split()[1]) + ' ' + str(defat1.split()[2]) + ' ' + str(
                                                        int(defat1.split()[3]) + attac) + ' ' + str(defat1.split()[4])))
                                                    fin.close()
                                                    fin = open("data.txt", "wt", encoding='utf-8')
                                                    fin.write(data)
                                                    fin.close()

                                                    fin = open("data.txt", encoding='utf-8')
                                                    data = fin.read()
                                                    line11 = data.split('\n')[num]
                                                    kolvo = line11.split()[3]
                                                    defat1 = data.split('\n')[reg]
                                                    defat = defat1.split()[3]
                                                    name = defat1.split()[1] + ' ' + defat1.split()[2]

                                                    sender(id, f"Вы проиграли в сражении!\n"
                                                               f"Шанс победить был {x}%\n"
                                                               f"Ваши роботы - {kolvo}\n"
                                                               f"Роботы {name} - {defat}")
                                                    fin.close()

            elif msg == '/бот помощь':
                sender(id, 'Привет, это чат-игра про роботов. '
                           'Цель игры - нападать на базы других игроков, уничтожать их роботов-защитников, а после из добытого материала собирать '
                           'новых роботов, тем самым увеличивая свою армию. Ты не можешь отправить в атаку больше половины имеющихся у тебя роботов, '
                           'а на защите у тебя стоит стабильно 30% роботов от твоего общего количества, также ты не можешь отправить в атаку меньше роботов чем стоит у противника в защите.\n'
                           'Для начала ты должен зарегистрироваться, для этого используй команду "/бот старт", без неё у тебя ничего не выйдет.\n'
                           'Ты всегда можешь узнать информацию о себе командой "/бот инфо".\n'
                           'Команда "/бот топ" показывает игроков с наибольшим количеством роботов, а также их регистрационный номер для нападения.\n'
                           '"/бот напасть [рег. номер противника] [сколько роботов отправишь в атаку?]" - команда для нападения на другого игрока.\n'
                           'Команда "/бот рандомный противник" дает информацию о случайном противнике для атаки')

            elif msg == '/бот рандомный противник':
                user_id = event.message.from_id

                file_path = "data.txt"
                required = str(user_id)





                string_numbers = find_string_number(file_path, required)
                if string_numbers == -1:
                    sender(id, 'Вы ещё не зарегистрированы!')
                else:
                    with open('data.txt', encoding='utf-8') as file:
                        line = file.readline()
                        list = []
                        while line:
                            kolvo = line.split()[0]
                            list.append(kolvo)

                            line = file.readline()


                file_path = "data.txt"
                required = str(random.choice(list))





                string_numbers = find_string_number(file_path, required)
                if string_numbers == -1:
                    sender(id, 'Вы ещё не зарегистрированы!')
                else:
                    num = string_numbers
                    f = open('data.txt', encoding='utf-8')
                    data = f.read()
                    line11 = data.split('\n')[num]
                    nom = num + 1
                    kolvo = line11.split()[3]
                    at = int(int(kolvo) * 0.3)
                    name = line11.split()[1] + ' ' + line11.split()[2]
                    f.close()

                    sender(id, f"Регистрационный номер - {nom}\nИмя - {name}\nРоботов - {kolvo}({at} на защите)")

            elif msg == '/бот кто гаврик':

                red_id = event.object.message['conversation_message_id']

                mtime = int(time.time())

                file_path = "cooldown.txt"

                required = str(id)

                string_numbers = find_string_number(file_path, required)

                if string_numbers == -1:

                    f = open('cooldown.txt', 'a', encoding='utf-8')

                    f.write(str(id) + ' ' + str(mtime) + '\n')

                    f.close()

                else:

                    num = string_numbers

                    f = open('cooldown.txt', encoding='utf-8')

                    data = f.read()

                    line11 = data.split('\n')[num]

                    time1 = int(line11.split()[1])

                    f.close()

                    if mtime < time1 + 14400:

                        sec = time1 + 14400 - mtime
                        min = 0
                        hour = 0

                        while sec >= 60:
                            sec -= 60
                            min += 1

                        while min >= 60:
                            min -= 60
                            hour += 1

                        sender(id, f"Следующий запуск возможен через {hour}ч {min}мин {sec}сек")

                    else:

                        user_id = event.message.from_id

                        file_path = "data.txt"

                        required = str(user_id)

                        string_numbers = find_string_number(file_path, required)

                        if string_numbers == -1:

                            sender(id, 'Вы ещё не зарегистрированы!')

                        else:

                            f = open('cooldown.txt', encoding='utf-8')

                            data = f.read()

                            line11 = data.split('\n')[num]

                            f.close()

                            fin = open("cooldown.txt", "rt", encoding='utf-8')

                            data = fin.read()

                            data = data.replace(str(line11), str(str(line11.split()[0]) + ' ' + str(mtime)))

                            fin.close()

                            fin = open("cooldown.txt", "wt", encoding='utf-8')

                            fin.write(data)

                            fin.close()

                            with open('data.txt', encoding='utf-8') as file:

                                line = file.readline()

                                list = []

                                while line:
                                    kolvo = line.split()[0]

                                    list.append(kolvo)

                                    line = file.readline()

                            file_path = "data.txt"

                            required = str(random.choice(list))

                            string_numbers = find_string_number(file_path, required)

                            if string_numbers == -1:

                                sender(id, 'Вы ещё не зарегистрированы!')

                            else:

                                num = string_numbers

                                f = open('data.txt', encoding='utf-8')

                                data = f.read()

                                line11 = data.split('\n')[num]

                                name = line11.split()[1] + ' ' + line11.split()[2]

                                f.close()

                                fin = open("data.txt", "rt", encoding='utf-8')
                                data = fin.read()

                                data = data.replace(str(line11), str(str(line11.split()[0]) + ' ' + str(
                                    line11.split()[1]) + ' ' + str(
                                    line11.split()[2]) + ' ' + str(line11.split()[3]) + ' ' + str(
                                    int(line11.split()[4]) + 1)))

                                fin.close()
                                fin = open("data.txt", "wt", encoding='utf-8')
                                fin.write(data)
                                fin.close()

                                id_msg = red_id + 1

                                def search():
                                    sender(id, f"Инициирую поиск гаврика/.")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Инициирую поиск гаврика|..")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Инициирую поиск гаврика\...")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Инициирую поиск гаврика--.")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Инициирую поиск гаврика/..")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Инициирую поиск гаврика|...")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Проверяю данные\.")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Проверяю данные--..")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Проверяю данные/...")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Проверяю данные|.")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Проверяю данные\..")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Проверяю данные--...")
                                    time.sleep(0.2)
                                    edit(id, id_msg, f"Местный гаврик найден - {name}!")


                                thread = threading.Thread(target=search())
                                thread.start()

            elif msg == '/бот топ гавриков':

                def top_players(filename):
                    with open(filename, 'r', encoding='utf-8') as f:
                        players = []
                        for line in f:
                            player_data = line.split()
                            player_name = player_data[1]
                            player_surname = player_data[2]
                            player_score2 = int(player_data[4])
                            players.append((player_score2, player_name, player_surname))

                        players.sort(reverse=True)

                        top_players = []
                        for i, player in enumerate(players[:10]):
                            top_players.append(f"{i + 1}. {player[1]} {player[2]} - {player[0]}\n")

                        return ''.join(top_players)


                sender(id, top_players('data.txt'))

            elif msg.startswith('/бот раздай'):

                user_id = event.message.from_id

                user = vk_session.method("users.get", {"user_ids": str(user_id)})
                fullname = user[0]['first_name'] + ' ' + user[0]['last_name']

                string_numbers = find_string_number("data.txt", str(user_id))
                if string_numbers == -1:
                    sender(id, 'Вы ещё не зарегистрированы!')
                else:
                        if int(len(msg.split())) < 3:
                            sender(id, 'Ошибка! Указаны неверные значения')
                        else:

                            reg = msg.split()[2]

                            def isint(reg):
                                try:
                                    int(reg)
                                    return 1
                                except ValueError:
                                    return 0


                            if isint(reg) == 0:
                                sender(id, 'Ошибка! Указаны неверные значения')
                            else:
                                attac = int(msg.split()[2])

                                num = string_numbers
                                f = open('data.txt', encoding='utf-8')
                                data = f.read()
                                line11 = data.split('\n')[num]
                                kolvo = int(line11.split()[3])
                                f.close()

                                if attac > kolvo:
                                    sender(id, f"Ошибка! У Вас доступно всего {kolvo} роботов для ставки!")
                                elif attac <= kolvo:
                                    file_path1 = "stol.txt"

                                    f = open('koloda.txt', encoding='utf-8')
                                    data = f.read()
                                    spisok = data.split()
                                    f.close()

                                    k1, k2 = random.sample(spisok, 2)
                                    spisok.remove(k1)
                                    spisok.remove(k2)
                                    fin = open("koloda.txt", "rt", encoding='utf-8')
                                    data = fin.read()
                                    data = data.replace(str(k1),
                                                        str(''))
                                    data = data.replace(str(k2),
                                                        str(''))
                                    fin.close()
                                    fin = open("koloda.txt", "wt", encoding='utf-8')
                                    fin.write(data)
                                    fin.close()

                                    string_numbers = find_string_number(file_path1, str(user_id))
                                    if string_numbers == -1:
                                        f = open('stol.txt', 'a', encoding='utf-8')
                                        f.write(str(user_id) + ' ' + str(fullname) + ' ' + f"{attac} {k1},{k2}" + '\n')
                                        f.close()
                                        sender(id, 'Вы добавлены в очередь на игру!')
                                    else:
                                        sender(id, 'Вы уже в очереди на игру!')

                                    f = open('stol.txt', encoding='utf-8')
                                    data = f.read()
                                    line11 = data.split('\n')[0]
                                    f.close()
                                    if int(line11) == 1:
                                        if not fullname in gameMessage:
                                            gameMessage += f"{fullname}:\n{k1}, {k2}\n"
                                        continue
                                    elif int(line11) == 0:
                                        fin = open("stol.txt", "rt", encoding='utf-8')
                                        data = fin.read()
                                        data = data.replace(str(line11),
                                                            str('1'), 1)
                                        fin.close()
                                        fin = open("stol.txt", "wt", encoding='utf-8')
                                        fin.write(data)
                                        fin.close()
                                        keyboard = VkKeyboard(inline=True)
                                        keyboard.add_button('Играть', color=VkKeyboardColor.SECONDARY)

                                        keyboardSender(id, keyboard, 'Игра начнется через 10 секунд.\nУспевай принять участие!\nЖми "Играть"\nДефолтная ставка - 100')

                                        f = open('koloda.txt', encoding='utf-8')
                                        data = f.read()
                                        spisok = data.split()
                                        f.close()

                                        d1, d2 = random.sample(spisok, 2)

                                        spisok.remove(d1)
                                        spisok.remove(d2)
                                        fin = open("koloda.txt", "rt", encoding='utf-8')
                                        data = fin.read()
                                        data = data.replace(str(d1),
                                                            str(''))
                                        data = data.replace(str(d2),
                                                            str(''))
                                        fin.close()
                                        fin = open("koloda.txt", "wt", encoding='utf-8')
                                        fin.write(data)
                                        fin.close()

                                        gameMessage = f"Игра началась!\nДилер:\n{d1}, {d2}\n"
                                        gameMessage += f"{fullname}:\n{k1}, {k2}\n"

                                        def task():
                                            time.sleep(10)

                                            keyboard = VkKeyboard(inline=True)
                                            keyboard.add_button('Добрать', color=VkKeyboardColor.POSITIVE)

                                            keyboardSender(id, keyboard, gameMessage + 'Игра закончится через 15 секунд\nДобирай либо пасуй!')

                                            f = open('stol.txt', encoding='utf-8')
                                            data = f.read()
                                            line11 = data.split('\n')[0]
                                            f.close()
                                            fin = open("stol.txt", "rt", encoding='utf-8')
                                            data = fin.read()
                                            data = data.replace(str(line11),
                                                                str('2'), 1)
                                            fin.close()
                                            fin = open("stol.txt", "wt", encoding='utf-8')
                                            fin.write(data)
                                            fin.close()

                                            time.sleep(15)
                                            fin = open("stol.txt", encoding='utf-8')
                                            lines = fin.readlines()[1:]
                                            fin.close()
                                            sender(id, 'Добирает Дилер...')
                                            cards = [d1, d2]
                                            while numCards(cards) < 17:
                                                f = open('koloda.txt', encoding='utf-8')
                                                data = f.read()
                                                spisok = data.split()
                                                f.close()
                                                p1 = random.sample(spisok, 1)
                                                p1 = str(p1[0])
                                                spisok.remove(p1)
                                                fin = open("koloda.txt", "rt", encoding='utf-8')
                                                data = fin.read()
                                                data = data.replace(str(p1),
                                                                    str(''))
                                                fin.close()
                                                fin = open("koloda.txt", "wt", encoding='utf-8')
                                                fin.write(data)
                                                fin.close()
                                                cards.append(p1)
                                            dilerNumber = numCards(cards)
                                            finalMessage = f"Игра завершена!\nДилер - {numCards(cards)}\n"


                                            for card in cards:
                                                finalMessage += card

                                            finalMessage += '\n'


                                            for line in lines:
                                                line11 = line.split()[4]
                                                cards = line11.split(',')

                                                if dilerNumber > 21:
                                                    if numCards(cards) <= 21:
                                                        value = '✅'
                                                    else:
                                                        value = '🚫'
                                                else:
                                                    if dilerNumber > numCards(cards):
                                                        value = '🚫'
                                                    elif dilerNumber < numCards(cards) <= 21:
                                                        value = '✅'
                                                    elif dilerNumber == numCards(cards):
                                                        value = '♻'
                                                    else:
                                                        value = '🚫'


                                                finalMessage += f"{value} {line.split()[1]} {line.split()[2]} - {numCards(cards)}\n{line.split()[4]}\n"
                                            sender(id, finalMessage)
                                            fin = open("koloda.txt", "wt", encoding='utf-8')
                                            fin.write('6♠ 7♠ 8♠ 9♠ 10♠ J♠ Q♠ K♠ A♠ 6♥ 7♥ 8♥ 9♥ 10♥ J♥ Q♥ K♥ A♥ 6♦ 7♦ 8♦ 9♦ 10♦ J♦ Q♦ K♦ A♦ 6♣ 7♣ 8♣ 9♣ 10♣ J♣ Q♣ K♣ A♣')
                                            fin.close()
                                            fin = open("stol.txt", "wt", encoding='utf-8')
                                            fin.write('0\n')
                                            fin.close()
                                            def task2():
                                                gameMessage = ''
                                                finalMessage = ''
                                            thread = threading.Thread(target=task2)
                                            thread.start()





                                        thread = threading.Thread(target=task)
                                        thread.start()


                                    else:
                                        sender(id, 'Игра уже идет!')


            elif msg == '[club216149415|@bot__obormot] играть':
                f = open('stol.txt', encoding='utf-8')
                data = f.read()
                line11 = data.split('\n')[0]
                f.close()
                if int(line11) == 0:
                    sender(id, 'Чтобы начать игру используйте команду\n /бот раздай [ставка]')
                    continue
                elif int(line11) == 2:
                    sender(id, 'Игра уже идет, дождитесь окончания предыдущей игры')
                    continue
                user_id = event.message.from_id

                user = vk_session.method("users.get", {"user_ids": str(user_id)})
                fullname = user[0]['first_name'] + ' ' + user[0]['last_name']

                file_path = "data.txt"
                required = str(user_id)

                string_numbers = find_string_number(file_path, required)
                if string_numbers == -1:
                    sender(id, 'Вы ещё не зарегистрированы!')
                    continue
                attac = 100

                num = string_numbers
                f = open('data.txt', encoding='utf-8')
                data = f.read()
                line11 = data.split('\n')[num]
                kolvo = int(line11.split()[3])
                f.close()

                if attac > kolvo:
                    sender(id, f"Ошибка! У Вас доступно всего {kolvo} роботов для ставки!")
                elif attac <= kolvo:
                    file_path1 = "stol.txt"

                    f = open('koloda.txt', encoding='utf-8')
                    data = f.read()
                    spisok = data.split()
                    f.close()

                    k1, k2 = random.sample(spisok, 2)
                    spisok.remove(k1)
                    spisok.remove(k2)
                    fin = open("koloda.txt", "rt", encoding='utf-8')
                    data = fin.read()
                    data = data.replace(str(k1),
                                        str(''))
                    data = data.replace(str(k2),
                                        str(''))
                    fin.close()
                    fin = open("koloda.txt", "wt", encoding='utf-8')
                    fin.write(data)
                    fin.close()

                    string_numbers = find_string_number(file_path1, required)
                    if string_numbers == -1:
                        f = open('stol.txt', 'a', encoding='utf-8')
                        f.write(str(user_id) + ' ' + str(fullname) + ' ' + f"{attac} {k1},{k2}" + '\n')
                        f.close()
                        sender(id, 'Вы добавлены в очередь на игру!')
                    else:
                        sender(id, 'Вы уже в очереди на игру!')
                    if not fullname in gameMessage:
                    	gameMessage += f"{fullname}:\n{k1}, {k2}\n"



            elif msg == '[club216149415|@bot__obormot] добрать':
                f = open('stol.txt', encoding='utf-8')
                data = f.read()
                line11 = data.split('\n')[0]
                f.close()
                if int(line11) == 0:
                    sender(id, 'Чтобы начать игру используйте команду\n /бот раздай [ставка]')
                    continue
                elif int(line11) == 1:
                    sender(id, 'Игра ещё не началась')
                    continue

                num = find_string_number('stol.txt', str(user_id))
                if num == -1:
                    sender(id, 'Вы не участвуете в этой игре!')
                    continue

                fin = open("stol.txt", encoding='utf-8')
                data = fin.read()
                line11 = data.split('\n')[num]
                line11 = line11.split()[4]
                cards = line11.split(',')
                fin.close()

                number = numCards(cards)

                if number > 21:
                    sender(id, 'Еблан, ты уже перебрал')
                    continue
                elif number == 21:
                    sender(id, 'Ты уже выиграл!')
                    continue






                f = open('koloda.txt', encoding='utf-8')
                data = f.read()
                spisok = data.split()
                f.close()
                p1 = random.sample(spisok, 1)
                p1 = str(p1[0])
                spisok.remove(p1)
                fin = open("koloda.txt", "rt", encoding='utf-8')
                data = fin.read()
                data = data.replace(str(p1),
                                    str(''))
                fin.close()
                fin = open("koloda.txt", "wt", encoding='utf-8')
                fin.write(data)
                fin.close()

                f = open('stol.txt', encoding='utf-8')
                data = f.read()
                line11 = data.split('\n')[num]
                f.close()
                fin = open("stol.txt", "rt", encoding='utf-8')
                data = fin.read()
                data = data.replace(line11,
                                    line11 + f",{p1}")
                fin.close()
                fin = open("stol.txt", "wt", encoding='utf-8')
                fin.write(data)
                fin.close()
                fin = open("stol.txt", encoding='utf-8')
                data = fin.read()
                line11 = data.split('\n')[num]
                line11 = line11.split()[4]
                fin.close()
                sender(id, f"{fullname}:\n{line11}")


            else:
                if id == 1:

                    if event.object['message']['attachments']:
                        if event.object['message']['attachments'][0]['photo']:
                            def task_photo():

                                vk_session = vk_api.VkApi(token=token_user)
                                vk = vk_session.get_api()

                                photo_url = event.object.message['attachments'][0]['photo']['sizes'][-1]['url']
                                photo_data = requests.get(photo_url).content

                                # загрузка фото на сервер
                                upload_url = vk.photos.getWallUploadServer()['upload_url']
                                response = requests.post(upload_url, files={'photo': ('photo.png', photo_data)}).json()

                                # загруженное фото помещаем в альбом группы
                                photo = vk.photos.saveWallPhoto(**response)[0]

                                image_uri = f"photo{photo['owner_id']}_{photo['id']}"
                                access_key = str(photo['access_key'])

                                if msg == '1':
                                    url = 'https://api.vk.com/method/wall.post'
                                    response = requests.post(url=url, params={'access_token': token_user,
                                                                              'owner_id': -215399830,
                                                                              'from_group': 1,
                                                                              'message': '',
                                                                              'attachments': image_uri,
                                                                              'access_key': access_key,
                                                                              'signed': 0,
                                                                              'v': "5.131"})


                                else:

                                    file1 = open("post.txt", "at", encoding='utf-8')
                                    file1.write(image_uri + ' ' + access_key + '\n')
                                    file1.close()
                                    file1 = open("post.txt", "rt", encoding='utf-8')
                                    list = file1.read()
                                    list = list.split()
                                    file1.close()
                                    if len(list) == 20:
                                        attachments = f"{list[0]}, {list[2]}, {list[4]}, {list[6]}, {list[8]}, {list[10]}, {list[12]}, {list[14]}, {list[16]}, {list[18]}"
                                        keys = f"{list[1]}, {list[3]}, {list[5]}, {list[7]}, {list[9]}, {list[11]}, {list[13]}, {list[15]}, {list[17]}, {list[19]}"

                                        url = 'https://api.vk.com/method/wall.post'
                                        response = requests.post(url=url, params={'access_token': token_user,
                                                                                  'owner_id': -215399830,
                                                                                  'from_group': 1,
                                                                                  'message': '',
                                                                                  'attachments': attachments,
                                                                                  'access_key': keys,
                                                                                  'signed': 0,
                                                                                  'v': "5.131"})
                                        file1 = open("post.txt", "w", encoding='utf-8')
                                        file1.write(' ')
                                        file1.close()


                            thread = threading.Thread(target=task_photo())
                            thread.start()

                        else:
                            continue
                    else:
                        continue
                else:
                    continue



