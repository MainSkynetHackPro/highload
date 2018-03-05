#!/usr/bin/env python
from core.serverManager import ServerManager
from utils.configLoader import load_config

if __name__ == '__main__':
    config = load_config()
    server = ServerManager(config['listen'], config['thread_limit'], config['listen'])
    server.run()
