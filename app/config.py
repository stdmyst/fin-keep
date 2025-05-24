# Config class that keeps values from env.

import os


class Config():
    def __init__(self):
        env: dict = os.environ
        
        self.example = env.get('example', None)


if __name__ == '__main__':
    c = Config()
    print(c.__dict__)