from vk_bot.utils import (
    choose_plural,
    calculate_age,
    filter_age,
    format_for_filters_users,
)
import unittest


class TestChoosePlural(unittest.TestCase):
    def test_work_function(self):
        """Проверка на правильность склонения слов"""
        declensions = ('яблоко', 'яблока', 'яблок')

        for i, (count, res) in enumerate(zip([1, 2, 5, 100, 603],
                                             [
                                                 '1 яблоко',
                                                 '2 яблока',
                                                 '5 яблок',
                                                 '100 яблок',
                                                 '603 яблока',
                                             ])):
            with self.subTest(i):
                result = choose_plural(count, declensions)
                result_ = str(result[0]) + ' ' + str(result[1])
                self.assertRegex(result_, r'\d{1,3} яблок[оа]?')
                self.assertEqual(result_, res)

    def test_type_params(self):
        self.assertRaises(TypeError, choose_plural, '1', ('яблоко', 'яблока', 'яблок'))

    def test_none(self):
        self.assertIsNotNone(choose_plural(1, ('яблоко', 'яблока', 'яблок')))


class TestFiltersFunc(unittest.TestCase):
    def test_calculate_age_true(self):
        for i, (birthday, expected) in enumerate([
            ('21.02.2001', 23),
            ('13.10.1999', 24),
            ('13.10.1984', 39),
            ('03.12.1231', 792)
        ], 1):
            with self.subTest(i):
                result = calculate_age(birthday)
                self.assertEqual(expected, result)
                self.assertNotEqual(expected + 1, result)
                self.assertIsInstance(result, int, 'Результат должен быть типом int')

    def test_calculate_age_with_wrongs_arguments(self):
        for i, birthday in enumerate([
            '2001',
            '13.10.-1',
            '.10.1984',
            '03.12.21231',
            2001,
            (13, 19, 2005)
        ], 1):
            with self.subTest(i):
                error = TypeError
                if i <= 4:
                    error = ValueError
                with self.assertRaises(error):
                    calculate_age(birthday)

    def test_filter_age(self):
        for i, (birthday, expected) in enumerate(
            [
                ('03.12.1988', (35, 40)),
                ('03.12.1987', (35, 100)),
                ('03.12.1999', (24, 29)),
                ('03.12.1788', (35, 40)),
            ], 1
        ):
            with self.subTest(i):
                if i <= 3:
                    self.assertEqual(filter_age(birthday), expected)
                else:
                    self.assertNotEqual(filter_age(birthday), expected)

    def test_format_for_filters_users(self):
        for i, (info, expected) in enumerate([
            ({'id_user': 'id_user', 'sex': 1, 'age_from': 'age', 'age_to': 'age', 'bdate': '03.12.1987',
             'city_id': 'city_id', 'city_title': 'city_title', 'relation': 'relation'},
             {'id_user': 'id_user', 'sex': 2, 'age_from': 35, 'age_to': 100,
              'city_id': 'city_id', 'city_title': 'city_title', 'relation': 'relation'}),
            ({'id_user': '123123', 'sex': 1, 'age_from': 'age', 'age_to': 'age', 'bdate': '03.12.1987',
              'city_id': 'city_id', 'city_title': 'city_title', 'relation': 'relation'},
             {'id_user': 'id_user', 'sex': 2, 'age_from': 35, 'age_to': 100,
              'city_id': 'city_id', 'city_title': 'city_title', 'relation': 'relation'}),
            ({'id_user': '123123', 'sex': 1, 'age_from': 'age', 'age_to': 'age', 'bdate': '03.12.1987',
              'city_id': 'city_id', 'city_title': 'city_title', 'relation': 'relation'},
             {'id_user': 'id_user', 'sex': 2, 'age_from': 35, 'age_to': 100,
              'city_id': 'city_id', 'city_title': 'city_title'})
        ], 1):
            with self.subTest(i):
                if i == 1:
                    self.assertEqual(format_for_filters_users(info), expected)
                if i == 2:
                    self.assertNotEqual(format_for_filters_users(info), expected,
                                        'Значения ключей id_user не должны совпадать')
                if i == 3:
                    self.assertNotEqual(format_for_filters_users(info), expected,
                                        'Ключ relation должен отсутствовать в результате')
