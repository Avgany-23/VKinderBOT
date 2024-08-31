from vk_bot.menu_button import filters_menu
import unittest
import json


class TestFiltersMenu(unittest.TestCase):
    def test_check_button(self):
        result_menu = json.loads(filters_menu().get_keyboard())
        self.assertEqual(len(result_menu['buttons']), 4, 'Кол-во строк кнопок должно быть 4')
        for i, (row, excepted, label) in enumerate(zip(result_menu['buttons'],
                                                       [5, 3, 1, 1],
                                                       ['Возраст:',
                                                        'Пол:',
                                                        'Статус: нажать для получения информации',
                                                        'Город: нажать для получения информации']), 1):
            with self.subTest(i):
                self.assertEqual(len(row), excepted, f'На строке {i} должно быть {excepted} кнопок')
                self.assertEqual(row[0]['action']['label'], label,
                                 f'На строке {i} должен быть фильтр {label}')
