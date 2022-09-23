from colorama import Fore, Style

class BasicWord:
    """ Класс - обрабатывает выбранное слово и список субслов """

    def __init__(self, choice_word, subwords, words_dictonary):
        """
        создает экземпляр с полями:
        self.word - выбранное слов
        self.ubwords - список субслов
        """
        self.word = choice_word
        self.subwords = subwords
        self.text = None
        self.words_dictonary = words_dictonary #считывается весь словарь, чтоб можно было проверить слово на наличие
                                               # в словаре если оно отсутствует в списке subwords

    def __repr__(self):
        return f'(word={self.word}, subwords={self.subwords}, слов в words_dictonary = {len(self.words_dictonary)})'

    def __del__(self):
        return

    def get_len_subwords(self):
        return len(self.subwords)

    def get_verify_answer(self, user_word):
        """ Проверяет введенное пользователем слово на длину и наличие в списке subwords"""
        if len(user_word) < 2:
            self.text = f'{Fore.LIGHTWHITE_EX}слишком короткое слово{Style.RESET_ALL}'
            return False
        elif user_word.strip().lower() not in self.subwords:
            self.text = f'{Fore.LIGHTRED_EX}неверно{Style.RESET_ALL}'
            return False
        else:
            return True

    def get_text(self):
        return self.text

    def get_word(self):
        return self.word

    def words_for_dictonaty(self, words_dictonary):
        self.words_dictonary = words_dictonary

    def get_words_dictonary(self):
        return self.words_dictonary
