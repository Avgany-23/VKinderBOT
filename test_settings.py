DATABASES_TEST = {
    'postgresql': {
        'NAME': 'postgresql',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
        'BD_NAME': 'vk_test',
    },
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 1,
        'decode_responses': True,
        'charset': "utf-8",
    }
}

DT_POSTGRESQL = DATABASES_TEST['postgresql']
PATH_TEST_POSTGRESQL = (f"{DT_POSTGRESQL['NAME']}://{DT_POSTGRESQL['USER']}:{DT_POSTGRESQL['PASSWORD']}@"
                        f"{DT_POSTGRESQL['HOST']}:{DT_POSTGRESQL['PORT']}/{DT_POSTGRESQL['BD_NAME']}")
