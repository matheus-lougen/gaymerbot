import os
import sys
import time
import asyncio
import logging
import discord
import platform
import argparse

from gaymerbot import Client
from gaymerbot.modules import Logger
from gaymerbot.modules import Config


try:
    parser = argparse.ArgumentParser(description='Launch the discord bot')
    parser.add_argument("-d", "--debug", type=bool, required=False, help='Enable main logger debug mode')
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


logger = Logger()
logger.setup_formatters()
log = logger.setup_logger('main', debug_mode=args.debug, file_level=logging.INFO, stream_level=logging.INFO)
commands_log = logger.setup_logger('commands', debug_mode=args.debug, file_level=logging.INFO, stream_level=logging.INFO)
discord_log = logger.setup_logger('discord', debug_mode=args.discorddebug, file_level=logging.INFO, stream_level=logging.INFO)
discord_https_log = logger.setup_logger('discord.https', debug_mode=args.discordhttpsdebug, file_level=logging.WARNING, stream_level=logging.WARNING)


@logger.exception_catcher('main')
def setup():
    log.debug(f'Discord.py version [{discord.__version__}]')
    log.debug(f'Python version [{platform.python_version()}]')
    log.debug(f'OS information [{platform.system()} {platform.release()} ({os.name})]')
    initial_extensions = (
        'gaymerbot.extensions.events',
        'gaymerbot.extensions.user_commands',
        'gaymerbot.extensions.developer_commands',
        'gaymerbot.extensions.admin_commands'
    )
    # CLient startup timestamp
    start_time = time.time()

    config_path = './data/config.yaml'
    config = Config(config_path)
    client = Client(start_time, config, initial_extensions)
    asyncio.run(main(client, config))
    # Extensions to load when the bot turns on


async def main(client, config):
    async with client:
        await client.start(config.token)


setup()
