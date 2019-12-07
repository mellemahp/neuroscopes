"""SOME INFO

"""
# start import # 

# end imports #
class Config: 
    A_CONFIG_VARIABLE_1 = 1
    A_CONFIG_VARIABLE_2 = 2


class DevConfig(Config): 
    DEBUG = True


config = { 
    'dev': DevConfig,
    'prod': None,
    'default': DevConfig
}