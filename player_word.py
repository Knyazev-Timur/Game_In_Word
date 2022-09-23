import requests


class PlayerWord:
    """
    Обработка слова введенного пользователем, проверка на существование, как имени существительного
    """

    def __init__(self, word):
        self.word = word

    def verify_language(self):
        for symbol in self.word.strip():
            if 1039 < ord(symbol) < 1106:
                continue
            else:
                return False
        return True

    def verify_word(self):

        url = f'http://www.gramota.ru/slovari/dic/?bts=x&word={self.word}'
        answer = requests.get(url)
        html_file = answer.text.split()

        for i in range(len(html_file) - 1):
            if 'слово' in html_file[i] and 'отсутствует' in html_file[i + 1]:
                return False
        return True
