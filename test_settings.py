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

PATH_TEST = (f"{DATABASES_TEST['NAME']}://{DATABASES_TEST['USER']}:{DATABASES_TEST['PASSWORD']}@"
             f"{DATABASES_TEST['HOST']}:{DATABASES_TEST['PORT']}/{DATABASES_TEST['BD_NAME']}")
