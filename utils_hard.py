import json
import random

from colorama import init
from colorama import Fore, Style

import pandas as pd
from basic_word import BasicWord
from pars import Parsing
from player import Player
from player_word import PlayerWord
from statistic import Statistic

init()


def load_words():
    """ Считывает и возвращает словарь """
    with open('russian_nouns.txt', 'r', encoding='UTF-8') as file_words:
        return file_words.read().split()


def add_word(text_word, atribute):
    """ Сохраняет словарь, в случае изменения """
    with open('russian_nouns.txt', atribute, encoding='UTF-8') as file_words:
        file_words.write(text_word)
        file_words.close()


def statistic_load():
    """ Получает данные из файлов .json и возвращает их в виде словаря python"""
    with open('statistic.json', 'r', encoding='UTF-8') as file_json:
        data_dict = json.load(file_json)
        return data_dict


def save_statstic(statistics):
    """ Сохраняет статистику в конце игры """
    with open('statistic.json', 'w', encoding='utf-8') as file_statistic:
        json.dump(statistics, file_statistic)
        file_statistic.close()
        statistic_output(statistics)


def get_start_game():
    """ Стартовая функция, запрос имени игрока,
    создает экземпляр класса Player c полями имя пользователя и уже использованные слова"""

    user_name = input(f'{Fore.LIGHTGREEN_EX}Введите имя игрока\n')
    used_words = set()
    player_data = Player(user_name, used_words)
    statistic_building(player_data)
    primary_output(player_data)


def get_instructions(player_data):
    """ Вывод корокой инструкции, если игрок впервые запустил игру """
    print(Fore.LIGHTWHITE_EX, end='')
    print(f'Приветствую, {Fore.LIGHTGREEN_EX}{player_data.get_name()}!\n'
          f'{Fore.LIGHTWHITE_EX}В этой игре необходимо составлять слова из букв выбранного слова. \n'
          f'Слова должны быть существительными, а за каждую букву в составленном слове будут начисляться баллы.\n'
          f'Успехов в игре!!!')
    return


def main(words_data, player_data):
    """ Получает ввод от пользователя, проверяет ввод на окончание игры,
    получает из классов BasicWord и Player значение bool,
    получает кол-во введеных слов, проверяет есть ли еще не отгаданные сублова.
    """

    user_word = input(f'{Fore.LIGHTWHITE_EX}Введите слово '
                      f'или {Fore.LIGHTRED_EX}stop{Fore.LIGHTWHITE_EX} для завершения\n').lower().strip()

    if user_word.strip().lower() == 'stop':
        the_end(player_data, words_data)

    elif words_data.get_verify_answer(user_word) is False:
        print(words_data.get_text())
        second_output(words_data, player_data)
        main(words_data, player_data)

    elif player_data.get_verify_word(user_word) is False:
        print(player_data.get_text())
        second_output(words_data, player_data)
        main(words_data, player_data)

    elif player_data.get_len_used_word() == words_data.get_len_subwords():
        player_data.add_score(user_word)
        the_end(player_data, words_data)

    else:
        print(player_data.get_text())
        player_data.add_score(user_word)
        second_output(words_data, player_data)
        main(words_data, player_data)


def get_words(word=None):
    """ Получает словарь допустимых слов, выбирает случайный словарь {word:subword},
        создает экземпляр класса BasicWord c полями: выбранное слово, соответсвующие ему субслова.
        Возращает созданный экземпляр класса"""

    words_dictonary = load_words()
    if word is None:
        word = random.choice(words_dictonary)
    choice_words = Parsing(word)
    words = choice_words.get_subwords()
    data_for_game = BasicWord(words.get('word'), words.get('subwords'), words_dictonary)
    return data_for_game


def get_player_word():
    """ Запрос слова от пользователя, проверка возможности использования введенного слова,
    выбор порядка действия со словарем, если введенное слово отсутствует в словаре """
    while True:
        input_word = input(f'{Fore.LIGHTGREEN_EX}Придумайте слово{Style.RESET_ALL}\n')
        player_word = PlayerWord(input_word.strip().lower())
        data_for_game = get_words(input_word.strip().lower())

        if player_word.verify_language() is False:
            print(f'{Fore.LIGHTWHITE_EX}Пожалуйста, проверьте раскладку клавиатуры')
            continue

        elif len(input_word) < 3 or data_for_game.get_len_subwords() < 2:
            print(f"{Fore.LIGHTWHITE_EX}Из данного слова нельзя составить новые слова.{Style.RESET_ALL}")
            continue

        elif player_word.verify_language() and player_word.verify_word():
            if input_word.strip().lower() not in data_for_game.get_words_dictonary():
                add_word(f'\n{input_word.strip().lower()}', 'a')
            return data_for_game

        else:
            print(f'{Fore.LIGHTWHITE_EX}Я не знаю такого слова.\n')

            while True:
                confirmation = input(f'{Fore.LIGHTGREEN_EX}Хотите добавить слово в словарь '
                                     f'или придумаете другое слово?\n{Style.RESET_ALL}'
                                     f'{Fore.LIGHTBLUE_EX}0{Style.RESET_ALL} - придумать новое слово\n'
                                     f'{Fore.LIGHTBLUE_EX}1{Style.RESET_ALL} - начать игру с текущим словом\n'
                                     f'{Fore.LIGHTBLUE_EX}2{Style.RESET_ALL} - добавить слово в словарь и начать игру\n')

                if confirmation == '0':
                    break

                elif confirmation == '1':
                    data_for_game = get_words(input_word.strip().lower())
                    return data_for_game

                elif confirmation == '2':
                    text_word = f'\n{input_word.strip().lower()}'
                    add_word(text_word, 'a')
                    data_for_game = get_words(input_word.strip().lower())
                    return data_for_game

                else:
                    print(f'{Fore.LIGHTWHITE_EX}Кажется, такого варианта нет.{Style.RESET_ALL}')


def get_elector(question, function_0, function_1):
    """ Выбор действия из 2пунктов """
    while True:
        elector = input(question)

        if elector == '0':
            return function_0()

        elif elector == '1':
            return function_1()

        else:
            print(f'{Fore.LIGHTWHITE_EX}Кажется, такого варианта нет.{Style.RESET_ALL}')


def get_validation(data_for_game, player_data):
    """ Подтверждение выбранного слова перед началом игры """
    while True:
        validation = input(f'{Fore.LIGHTGREEN_EX}Выберите вариант:\n'
                           f'{Fore.LIGHTBLUE_EX}0 {Style.RESET_ALL}- начать игру с выбранным словом\n'
                           f'{Fore.LIGHTBLUE_EX}1 {Style.RESET_ALL}- выбрать новое слово\n'
                           f'{Fore.LIGHTBLUE_EX}2 {Style.RESET_ALL}- удалить слово из словаря\n')
        if validation == '0':
            return
        elif validation == '1':
            primary_output(player_data)
            return
        elif validation == '2':
            word_for_dell = input(f'{Fore.LIGHTGREEN_EX}Введите слово, которое хотите удалить\n')
            if word_for_dell.strip().lower() in data_for_game.get_words_dictonary():
                data_for_game.get_words_dictonary().remove(word_for_dell.strip().lower())
                text_word = '\n'.join(data_for_game.get_words_dictonary())
                add_word(text_word, 'w')
                print(f'{Fore.LIGHTRED_EX}{word_for_dell.strip().upper()}{Style.RESET_ALL} удалено из словаря.')
            else:
                print(f'{Fore.LIGHTWHITE_EX}Такого слова нет в словаре.{Style.RESET_ALL}')
        else:
            print(f'{Fore.LIGHTWHITE_EX}Кажется, такого варианта нет.{Style.RESET_ALL}')


def primary_output(player_data):
    question = f'{Fore.LIGHTGREEN_EX}Выберите вариант:\n' \
               f'{Fore.LIGHTBLUE_EX}0 {Style.RESET_ALL}- выбрать случайное слово из словаря\n' \
               f'{Fore.LIGHTBLUE_EX}1 {Style.RESET_ALL}- выбрать свое слово\n'
    data_for_game = get_elector(question, get_words, get_player_word)
    len_subwords = data_for_game.get_len_subwords()

    print(f'{Fore.LIGHTWHITE_EX}Выбрано слово: {Fore.LIGHTGREEN_EX}{data_for_game.get_word().upper()}\n'
          f'{Fore.LIGHTWHITE_EX}можно составить новых слов: {Fore.LIGHTGREEN_EX}{len_subwords}\n')

    get_validation(data_for_game, player_data)
    main(data_for_game, player_data)


def second_output(words_data, player_data):
    print(f'{Fore.LIGHTWHITE_EX}Вы составили слов: {Fore.LIGHTGREEN_EX}{player_data.get_len_used_word()}'
          f'{Fore.LIGHTWHITE_EX}, набрали очков: {Fore.LIGHTGREEN_EX}{player_data.get_score()}{Fore.LIGHTWHITE_EX}'
          f'\nОсталось составить слов: {Fore.LIGHTGREEN_EX}'
          f'{words_data.get_len_subwords() - player_data.get_len_used_word()} '
          f'{Fore.LIGHTWHITE_EX}из слова {Fore.LIGHTGREEN_EX}{words_data.get_word().upper()}')
    return


def statistic_building(player_data):
    """ Построение первичной статистики, проверка велись ли игры ранее, предложение сброса статистики игрока """
    statistics = statistic_load()
    statistic = [items for items in statistics if items.get('user_name') == player_data.get_name()]
    statistics_data = Statistic(player_data.get_name(), statistics)
    if not statistic:
        get_instructions(player_data)

        player_data.add_statistic(statistics_data)
        return
    else:
        print(f"{Fore.LIGHTWHITE_EX}С возварщением, {Fore.LIGHTGREEN_EX}{player_data.get_name()}"
              f"{Fore.LIGHTWHITE_EX}, продолжим?{Style.RESET_ALL}")

        while True:
            question = input(f'{Fore.LIGHTBLUE_EX}0{Style.RESET_ALL} - продолжить статистику\n'
                             f'{Fore.LIGHTBLUE_EX}1{Style.RESET_ALL} - начать новую\n')
            if question == '0':
                add_statistics(statistic[0], player_data, statistics_data)
                return
            elif question == '1':

                statistics_data.get_statistics().remove(statistic[0])
                player_data.add_statistic(statistics_data)
                return
            else:
                print(f'{Fore.LIGHTWHITE_EX}Кажется, такого варианта нет.{Style.RESET_ALL}')


def add_statistics(statistic, player_data, statistics_data):
    """
    Суммирует игры, полученные очки, с имеющимися ранее
    :param statistic:
    :param player_data:
    :param statistics_data:
    :return:
    """
    statistics_data.add_games(statistic.get('games'))
    statistics_data.add_score(statistic.get('score'))
    statistics_data.add_words_composed(statistic.get('words_composed'))
    player_data.add_statistic(statistics_data)
    statistics_data.get_statistics().remove(statistic)
    return


def statistic_dictonary(player_data):
    """
    Формирует словарь статистики и передает на создания ТОП-10
    :param player_data:
    :return:
    """
    statistic = player_data.get_statistic()
    statistic.add_score(player_data.get_score())
    statistic.add_words_composed(player_data.get_len_used_word())
    statistics_dictonary = {"user_name": player_data.get_name(), "games": statistic.get_games(),
                            "words_composed": statistic.get_words_composed(), "score": statistic.get_score()}
    get_top(player_data, statistics_dictonary)


def get_top(player_data, statistics_dictonary):
    """ Формирует ТОП-10, выводите через dataframe pandas
    :param player_data:
    :param statistics_dictonary:
    :return:
    """
    statistic_data = player_data.get_statistic()
    statistics = statistic_data.get_statistics()
    items = 0
    for i in range(len(statistics)):
        if statistics[items].get('score') > statistic_data.get_score():
            items += 1
            continue
        else:
            break
    statistics.insert(items, statistics_dictonary)
    save_statstic(statistics)


def statistic_output(statistics):
    data = [{'ИГРОК': statistics[i].get('user_name'), 'ИГР': statistics[i].get('games'),
             'СЛОВ': statistics[i].get('words_composed'), 'ОЧКИ': statistics[i].get('score')}
            for i in range(len(statistics)) if i < 10]

    print(f'\t' * 3, f'{Fore.LIGHTBLUE_EX}ТОП-10{Style.RESET_ALL}', end='')
    df = pd.DataFrame(data)
    print(Fore.LIGHTGREEN_EX)
    print(df.rename(index={i: i + 1 for i in range(len(statistics))}))
    print(Style.RESET_ALL)
    question = f'\n{Fore.LIGHTGREEN_EX}Выберите вариант:\n' \
               f'{Fore.LIGHTBLUE_EX}0{Style.RESET_ALL} - выход\n' \
               f'{Fore.LIGHTBLUE_EX}1{Style.RESET_ALL} - новая игра\n'

    get_elector(question, quit, get_start_game)


def the_end(player_data, words_data):
    """ Выводит итоговый результат, передает на формирование статистики """

    print(f'\n{player_data.get_name()}, игра завершена!\n'
          f'Всего можно было составить слов: {words_data.get_len_subwords()}\n'
          f'Вы составили слов: {player_data.get_len_used_word()}\n'
          f'Набрано очков: {player_data.get_score()}\n')
    statistic_dictonary(player_data)
