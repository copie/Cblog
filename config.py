import os
basedir = os.path.abspath(os.path.dirname(__name__))


class Config():
    SECRET_KEY = os.environ.get(
        "SECRET_KEY") or "ed076287532e86365e841e92bfc50d8c"
    MAIL_SUBJECT_PREFIX = '[copie]'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.exmail.qq.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'cblog@copie.cn')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '!1s=NsxFsKR0aq&S')
    MAIL_SENDER = os.environ.get('MAIL_USERNAME', 'cblog@copie.cn')
    ADMIN_EMAIL = os.environ.get('FLASKY_ADMIN', 'cblog@copie.cn')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
