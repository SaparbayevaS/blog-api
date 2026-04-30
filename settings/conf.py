from decouple import config, Csv

BLOG_SECRET_KEY = config('BLOG_SECRET_KEY', default='super-secret')
BLOG_DEBUG = config('BLOG_DEBUG', default=True, cast=bool)

BLOG_ALLOWED_HOSTS = config(
    'BLOG_ALLOWED_HOSTS',
    cast=Csv(),
    default='127.0.0.1,localhost'
)

BLOG_REDIS_URL = config(

    'BLOG_REDIS_URL',

    default='redis://redis:6379/1'

)

BLOG_ENV_ID = config('BLOG_ENV_ID', default='local')