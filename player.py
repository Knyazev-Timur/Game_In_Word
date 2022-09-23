from colorama import Fore, Style

class Player:
    """ Класс - работает с данными пользователя """

    def __init__(self, user_name, used_words, score=0, statistic=None):
        """
        создает экземпляр с полями:
        self.gamer -  имя пользователя
        self.used_words - использованные слова
        """
        self.gamer = user_name
        self.used_words = used_words
        self.text = None
        self.score = score
        self.statistic = statistic

    def __repr__(self):
        return f'(Gamer={self.gamer}, Used words={self.used_words})'

    def __del__(self):
        return

    def get_used_words(self, user_word):
        self.used_words.add(user_word)

    def get_len_used_word(self):
        return len(self.used_words)

    def get_verify_word(self, user_word):
        """
        Проверяет наличие введенного слова во множестве,
        добавляет слово во множество, возвращает bool
        """
        if user_word.strip().lower() in self.used_words:
            self.text = f'{Fore.LIGHTWHITE_EX}уже использовано{Style.RESET_ALL}'
            return False
        else:
            self.get_used_words(user_word)
            self.text = f'{Fore.LIGHTGREEN_EX}верно{Style.RESET_ALL}'
            return True

    def add_statistic(self, statistic):
        self.statistic = statistic

    def get_text(self):
        return self.text

    def add_score(self, user_word):
        self.score += len(user_word)

    def get_score(self):
        return self.score

    def get_name(self):
        return self.gamer

    def get_statistic(self):
        return self.statistic
