from engine import Engine
from util import DATABASE

if __name__ == "__main__":
    DATABASE.connect()
    engine = Engine()
    engine.run()    