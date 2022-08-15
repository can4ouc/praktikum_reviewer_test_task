# оптимальнее будет импортировать только необходимые методы из библиотеки
import datetime as dt


# здесь и дале хотелось бы увидеть небольшой docstring класса
class Record:
    # здесь и далее хотелось увидеть аннотацию типов
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            # можно просто по умолчанию использовать это значение в параметре класса
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # не стоит именновать переменную с большой буквы, тем более у нас так назван класс выше
        for Record in self.records:
            # лучшек вынести вызов функции в константу до цикла
            if Record.date == dt.datetime.now().date():
                # можем использовать конструкцию +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # это можно объединить все в одно условие
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Комментарий к функции лучше писать в docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # лучше дать более логическое название переменной
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # можем оставить только return, так как в любом случае вернем это значение, если не выполнится первый if
        else:
            # скобки здесь не нужны
            return('Хватит есть!')


class CashCalculator(Calculator):
    # можно создать число с плавающей точкой в таком формате USD_RATE = 60.
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # имена параметров должны быть в формате snake_case (маленькими буквами)
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # было бы прикольно сделать из этих условие mapping, где вся логика соотношений будет храниться в словаре
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # эта условие лишнее, так как все равно ничего не меняем
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        # новое условие для читаемости можно разделить пробелом
        if cash_remained > 0:
            # скобочки также не нужны
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # можем оставить просто return
        elif cash_remained < 0:
            # лучше использовать f строки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # не стоит переопределять метод, так как мы никак не дополняем логику
    def get_week_stats(self):
        super().get_week_stats()

# не хватает конструкции if __name__ == ‘__main__’, в которой ,например, можно было б написать пару тестиков
