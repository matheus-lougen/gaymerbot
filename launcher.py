#!/usr/bin/env python

import os
import time
import click
import logging
import asyncio
import platform

import discord

from gaymerbot import Client
from gaymerbot.modules import Logger
from gaymerbot.modules import Config


def setup_logging(debug):
    logger = Logger()
    logger.setup_formatters()
    log = logger.setup_logger('main', debug_mode=debug, file_level=logging.INFO, stream_level=logging.INFO)
    logger.setup_logger('twitch', debug_mode=debug, file_level=logging.INFO, stream_level=logging.INFO)
    logger.setup_logger('commands', debug_mode=debug, file_level=logging.INFO, stream_level=logging.INFO)
    logger.setup_logger('extensions', debug_mode=debug, file_level=logging.INFO, stream_level=logging.INFO)
    logger.setup_logger('discord', file_level=logging.INFO, stream_level=logging.INFO)
    logger.setup_logger('discord.https', file_level=logging.WARNING, stream_level=logging.WARNING)
    return log


@click.group(invoke_without_command=True)
@click.option('--debug', is_flag=True, help='Launch with debug mode')
def main(debug):
    initial_extensions = (
        'gaymerbot.extensions.Events',
        'gaymerbot.extensions.RoleSelector',
        'gaymerbot.extensions.UserCommands',
        'gaymerbot.extensions.AdminCommands',
        'gaymerbot.extensions.DeveloperCommands'
        'gaymerbot.extensions.TwitchIntegrations',
    )
    log = setup_logging(debug)
    start_time = time.time()
    config_path = './data/config.yaml'
    config = Config(config_path)
    log.debug(f'Discord.py version [{discord.__version__}]')
    log.debug(f'Python version [{platform.python_version()}]')
    log.debug(f'OS information [{platform.system()} {platform.release()} ({os.name})]')
    client = Client(start_time, config, initial_extensions)
    asyncio.run(run_bot(client, config))


async def run_bot(client, config):
    async with client:
        await client.start(config.token)


if __name__ == '__main__':
    main()
