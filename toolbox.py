def readConfig(configPath):
    config = {}
    with open(configPath, 'r') as file:
        for line in file:
            params = line.split()
            config[params[0]] = [params[1], int(params[2])]
    return config


