import os
import sys
import time
import asyncio
import logging
import platform
import argparse

from gaymerbot import GaymerBot
from gaymerbot.modules import Config


try:
    parser = argparse.ArgumentParser(description='Launch the discord bot')
    parser.add_argument("-d", "--debug", type=bool, required=False, help='Enable main logger debug mode')
    parser.add_argument("-dc", "--debugcommands", type=bool, required=False, help='Enable comamnds logger debug mode')
    parser.add_argument("-dd", "--discorddebug", type=bool, required=False, help='Enable discord logger debug mode')
    parser.add_argument("-dhd", "--discordhttpsdebug", type=bool, required=False, help='Enable discord.https logger debug mode')
    args = parser.parse_args()

    # Default all args as False
    if args.debug is None:
        args.debug = False

    if args.discorddebug is None:
        args.discorddebug = False

    if args.discordhttpsdebug is None:
        args.discordhttpsdebug = False

except Exception as e:
    print('An error ocurred while setting up argparse, aborting...')
    print(e)
    sys.exit()


try:
    # Do all logging setup
    from gaymerbot.modules import Logger
    logger = Logger()
    logger.setup_formatters()
    log = logger.setup_logger('main', debug_mode=args.debug, file_level=logging.INFO, stream_level=logging.INFO)
    ticket_log = logger.setup_logger('ticket', debug_mode=args.debug, file_level=logging.WARNING, stream_level=logging.WARNING)
    commands_log = logger.setup_logger('commands', debug_mode=args.debug, file_level=logging.INFO, stream_level=logging.INFO)
    discord_log = logger.setup_logger('discord', debug_mode=args.discorddebug, file_level=logging.INFO, stream_level=logging.INFO)
    discord_https_log = logger.setup_logger('discord.https', debug_mode=args.discordhttpsdebug, file_level=logging.WARNING, stream_level=logging.WARNING)
except Exception as e:
    # If any step on the logging setup fails, abort execution
    print('An error ocurred while trying to setup logging, aborting now...', e)
    sys.exit()


@logger.exception_catcher('main')
def setup(initial_extensions, start_time, config_path):
    try:
        log.debug('Checking discord.py version')
        import discord
    except Exception as e:
        log.critical('An error ocurred while importing the discord library, aborting...')
        log.exception(e)
        sys.exit()
    else:
        log.debug(f'Sucessfull, discord.py version [{discord.__version__}]')

    log.debug(f'Python version [{platform.python_version()}]')
    log.debug(f'OS information [{platform.system()} {platform.release()} ({os.name})]')
    config = Config(config_path)
    client = GaymerBot(start_time, config, initial_extensions)
    asyncio.run(main(client, config))


async def main(client, config):
    async with client:
        await client.start(config.token)

# Extensions to load when the bot turns on
initial_extensions = (
    'gaymerbot.extensions.events',
    'gaymerbot.extensions.user_commands',
    'gaymerbot.extensions.cogs_commands',
    'gaymerbot.extensions.admin_commands'
)


# CLient startup timestamp
start_time = time.time()

config_path = './data/config.yaml'

setup(initial_extensions, start_time, config_path)
