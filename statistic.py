class Statistic:
    """
    Обрабатывает статистику, получает данные об играх ранее, суммирует с текущими данными
    """


    def __init__(self, user_name, statistics):
        self.user_name = user_name
        self.score = 0
        self.games = 0
        self.words_composed = 0
        self.statistics = statistics

    def __repr__(self):
        return f'user_name: {self.user_name}, games {self.games}, ' \
               f'words_composed: {self.words_composed}, score: {self.score} '

    def __del__(self):
        return

    def add_statistics(self, new_statistic):
        self.statistics = new_statistic

    def add_score(self, points):
        self.score += points

    def add_words_composed(self, words_used):
        self.words_composed += words_used

    def add_games(self, games):
        self.games += games

    def get_name(self):
        return self.user_name

    def get_score(self):
        return self.score

    def get_games(self):
        self.games += 1
        return self.games

    def get_words_composed(self):
        return self.words_composed

    def get_statistics(self):
        return self.statistics
