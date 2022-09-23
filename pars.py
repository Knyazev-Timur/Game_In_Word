import requests


class Parsing:
    """
    Класс обрабатывает выбранное слово, получает список возможных субслов с внешнего ресурса и формирует словарь
    """

    def __init__(self, choice_word):
        self.choice_word = choice_word

    def get_subwords(self):
        """ Получает субслова с https://slogislova.ru/iz_bukv/ и возвращает словарь {слово:список субслов}"""

        url = f'https://anagram.poncy.ru/words.html?inword={self.choice_word}&answer_type=3&nouns=true'
        answer = requests.get(url)
        html_file = answer.text.split()

        subword_helphref = [item.strip('</a></div>').lower() for item in html_file if 'id="helphref' in item]

        subwords = [subword_helphref[i].strip(f'id="helphref{i}">') for i in range(len(subword_helphref))
                    if self.choice_word not in subword_helphref[i]
                    and len(subword_helphref[i].strip(f'id="helphref{i}">')) >= 2]

        return {'word': self.choice_word, 'subwords': subwords}
