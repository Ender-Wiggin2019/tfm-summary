import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    EMAIL_ACCOUNT = "albert.huang@sf-dsc.com"
    EMAIL_PWD = "zbxcgtwtxwqwgdfy"

    PG_IP = 'digital4monitortest.ci7x9sxxlk6g.rds.cn-north-1.amazonaws.com.cn'
    PG_PORT = 5432
    PG_USER = 'postgres'
    PG_PWD = 'Welcome+2021'
    PG_DB = 'diap_ar'
    PG_SCHEMA = 'public'
    TARGET_TABLE = 'estimate_tfm'
