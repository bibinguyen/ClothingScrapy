from configparser import ConfigParser

def GetConfig(section):
    fileName= "Config.ini"
    parser = ConfigParser(inline_comment_prefixes= "#")
    parser.optionxform = str
    parser.read(fileName)
    cfg = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            cfg[param[0]] = param[1]
    return cfg
