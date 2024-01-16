# Global Settings for the project
# COOKIE: For authenticate connection
# PATH: Program output storage path
# USER_AGENT_POOL: Crawler agent random pool

import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, 'web', 'static')
OUTPUT_PATH = os.path.join(ROOT_PATH, 'output')

if __name__ == '__main__':
    print(ROOT_PATH)
    print(OUTPUT_PATH)
