import telegram
import telegram.ext
import os
from fatecalls.character import CharacterList


characters = CharacterList()


if __name__ == "__main__":
    u = telegram.ext.Updater(token=os.environ["TELEGRAM_KEY"])
