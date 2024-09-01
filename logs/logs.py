import logging


def create_logger(name, level, filename):
    """Функция для создания лог-ера с заданными именем, уровнем и файлом"""
    format_log = logging.Formatter(
        '\n\n'
        '%(name)s\n'
        'Уровень лога: %(levelname)s\n'
        'Время: %(asctime)s\n'
        'Сообщение: %(message)s',
        datefmt='%H:%M:%S'
    )

    handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
    handler.setFormatter(format_log)

    logger = logging.getLogger(f'Лог - {name}')
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Базовые логи
logger_base = create_logger('base_logger', logging.INFO, r'logs\logs_base.log')

# Логи о критических ошибках
logger_error = create_logger('critical_logger', logging.ERROR, r'logs\logs_error.log')

# Логи о начале старта работы бота
logger_starts_program = create_logger('starts_logger', logging.INFO, r'logs\starts_program.log')

