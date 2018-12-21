"""def readConfig(configPath):
    config = {}
    with open(configPath, 'r') as file:
        for line in file:
            params = line.split()
            config[params[0]] = [params[1], int(params[2])]
    return config"""

def parse_cfg(cfgpath):
    cfg = {}
    with open(cfgpath, 'r') as cfgfile:
        for line in cfgfile:
            (role, host, port) = line.split()
            cfg[role] = (host, int(port))
    return cfg


