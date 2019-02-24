import telegram
import telegram.ext
import telegram.error
import time
import os
import re
import typing
from fatecalls.character import CharacterAspects, CharacterApproaches, Character
from fatecalls.aspect import PermanentAspect
from fatecalls.roll import Fate


characters: typing.List[Character] = []

active = {}


def find_character(name: str) -> typing.Optional[Character]:
    for character in characters:
        if character.name.lower() == name.lower():
            return character
    return None


def reply(bot: telegram.Bot, update: telegram.Update, string: str, ignore_escaping=False, disable_web_page_preview=True, **kwargs) -> typing.Optional[telegram.Message]:
    while True:
        try:
            return bot.send_message(update.message.chat.id, string,
                                    parse_mode="HTML",
                                    disable_web_page_preview=disable_web_page_preview)
        except telegram.error.Unauthorized:
            break
        except telegram.error.TimedOut:
            time.sleep(1)
            pass
    return None


def delete_invoking(func):
    def new_func(bot: telegram.Bot, update: telegram.Update, *args, **kwargs):
        while True:
            try:
                bot.delete_message(update.message.chat.id, update.message.message_id)
                return func(bot, update, *args, **kwargs)
            except telegram.error.BadRequest:
                break
            except telegram.error.Unauthorized:
                break
            except telegram.error.TimedOut:
                time.sleep(1)
                pass
        return None
    return new_func


@delete_invoking
def cmd_newchar(bot: telegram.Bot, update: telegram.Update):
    text = update.message.text
    match = re.match(r'/newchar "([A-Za-z0-9 \-\']+)" "([A-Za-z0-9 \-\'!?.,;:]+)" ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)', text)
    if match is None:
        reply(bot, update, '⚠️ Sintassi non valida.\nSintassi: <code>/newchar "(nome)" "(coreaspect)" (careful) (clever) (flashy) (forceful) (quick) (sneaky)</code>')
        return
    name = match.group(1)
    core = match.group(2)
    try:
        careful = int(match.group(3))
        clever = int(match.group(4))
        flashy = int(match.group(5))
        forceful = int(match.group(6))
        quick = int(match.group(7))
        sneaky = int(match.group(8))
    except ValueError:
        reply(bot, update, '⚠️ Un parametro non è un numero.\nSintassi: <code>/newchar "(nome)" "(coreaspect)" (careful) (clever) (flashy) (forceful) (quick) (sneaky)</code>')
        return
    aspects = CharacterAspects(PermanentAspect(core))
    approaches = CharacterApproaches(careful, clever, flashy, forceful, quick, sneaky)
    character = Character(name, aspects, approaches)
    characters.append(character)
    active[update.effective_user.id] = character
    reply(bot, update, f"✅ Personaggio creato!\n{character.telegramify()}")


@delete_invoking
def cmd_active(bot: telegram.Bot, update: telegram.Update):
    name = update.message.text.split(" ", 1)[1]
    user_id = update.effective_user.id
    character = find_character(name)
    if character is None:
        reply(bot, update, '⚠️ Il personaggio specificato non esiste.')
        return
    active[user_id] = character
    reply(bot, update, f'✅ Hai attivato:\n{character.telegramify()}')


def with_selected(func):
    def new_func(bot, update, *args, **kwargs):
        if update.message.reply_to_message:
            user_id = update.message.reply_to_message.from_user.id
        else:
            user_id = update.from_user.id
        try:
            character = active[user_id]
        except KeyError:
            reply(bot, update, '⚠️ Non è stato selezionato nessun personaggio! Selezionane uno con <code>/active (nome)</code>, o rispondendo a un giocatore!')
            return
        return func(bot, update, character, *args, **kwargs)
    return new_func


@delete_invoking
@with_selected
def cmd_show(bot: telegram.Bot, update: telegram.Update, character: Character):
    reply(bot, update, f'ℹ️ Il tuo personaggio:\n{character.telegramify()}')


@delete_invoking
@with_selected
def cmd_careful(bot: telegram.Bot, update: telegram.Update, character: Character):
    roll = Fate(character.approaches.careful)
    reply(bot, update, f'🎲 <b>{character.name}</b> [Careful]\n{roll.telegramify()}')


@delete_invoking
@with_selected
def cmd_clever(bot: telegram.Bot, update: telegram.Update, character: Character):
    roll = Fate(character.approaches.clever)
    reply(bot, update, f'🎲 <b>{character.name}</b> [Clever]\n{roll.telegramify()}')


@delete_invoking
@with_selected
def cmd_flashy(bot: telegram.Bot, update: telegram.Update, character: Character):
    roll = Fate(character.approaches.flashy)
    reply(bot, update, f'🎲 <b>{character.name}</b> [Flashy]\n{roll.telegramify()}')


@delete_invoking
@with_selected
def cmd_forceful(bot: telegram.Bot, update: telegram.Update, character: Character):
    roll = Fate(character.approaches.forceful)
    reply(bot, update, f'🎲 <b>{character.name}</b> [Forceful]\n{roll.telegramify()}')


@delete_invoking
@with_selected
def cmd_quick(bot: telegram.Bot, update: telegram.Update, character: Character):
    roll = Fate(character.approaches.quick)
    reply(bot, update, f'🎲 <b>{character.name}</b> [Quick]\n{roll.telegramify()}')


@delete_invoking
@with_selected
def cmd_sneaky(bot: telegram.Bot, update: telegram.Update, character: Character):
    roll = Fate(character.approaches.sneaky)
    reply(bot, update, f'🎲 <b>{character.name}</b> [Sneaky]\n{roll.telegramify()}')


@delete_invoking
def cmd_clean(bot: telegram.Bot, update: telegram.Update):
    for character in characters:
        character.aspects.other.clean()
    reply(bot, update, f'🌬 Rimossi tutti gli aspetti temporanei da tutti i personaggi.')


if __name__ == "__main__":
    u = telegram.ext.Updater(token=os.environ["TELEGRAM_TOKEN"])
    u.dispatcher.add_handler(telegram.ext.CommandHandler("newchar", cmd_newchar))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("active", cmd_active))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("show", cmd_show))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("careful", cmd_careful))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("clever", cmd_clever))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("flashy", cmd_flashy))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("forceful", cmd_forceful))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("quick", cmd_quick))
    u.dispatcher.add_handler(telegram.ext.CommandHandler("sneaky", cmd_sneaky))
    u.start_polling()
    print("Bot started.")
    u.idle()
