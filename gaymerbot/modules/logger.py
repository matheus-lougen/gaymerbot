import logging
import colorlog
import functools
from logging import handlers


class Logger:
    def __init__(
        self,
        date_format='%d-%m-%Y %H:%M:%S',
        file_format='%(asctime)s %(name)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
        stream_format='%(light_green)s%(asctime)s%(reset)s %(red)s%(name)s%(reset)s %(bold)s%(log_color)s%(levelname)-4s%(reset)s %(yellow)s[%(filename)s:%(lineno)d]%(reset)s %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        },
    ):

        self.date_format = date_format
        self.file_format = file_format
        self.stream_format = stream_format
        self.log_colors = log_colors

    def setup_formatters(self):
        # Create a built-in formatter for the file output
        self.file_formatter = logging.Formatter(self.file_format, datefmt=self.date_format, style='%')
        # Create a colored stream formatter for the terminal output
        self.stream_formatter = colorlog.ColoredFormatter(
            self.stream_format,
            datefmt=self.date_format,
            style='%',
            log_colors=self.log_colors,
        )

    def setup_logger(
        self,
        name: str,
        debug_mode: bool = False,
        file_level=logging.NOTSET,
        stream_level=logging.NOTSET,
    ):

        # Set file and stream level to debug if debug mode is on
        if debug_mode is True:
            file_level = logging.DEBUG
            stream_level = logging.DEBUG

        # Get logger
        log = logging.getLogger(name)

        # Set the default logger level
        log.setLevel(logging.DEBUG)
        # Setup a timed rotated file handler, wich uses a file for logging for a especified period of time
        file_handler = handlers.TimedRotatingFileHandler(f'data/logs/{name}.log', when='D')
        # Setup a stream handler for the terminal output
        stream_handler = logging.StreamHandler()
        # Set each formatter to it's handler
        stream_handler.setFormatter(self.stream_formatter)
        file_handler.setFormatter(self.file_formatter)

        # Set the handlers logging level
        file_handler.setLevel(file_level)
        stream_handler.setLevel(stream_level)
        # Set the handlers to listen to the loggeer
        log.addHandler(stream_handler)
        log.addHandler(file_handler)

        log.debug(f'Sucessfully created new logger, name: {name} debug_mode: {debug_mode}')

        return log

    @classmethod
    def get_logger(self, name):
        # return a log instance based on it's name
        return logging.getLogger(name)

    def exception_catcher(self, logger_name: str = 'main'):
        def pre_run(func):
            log = logging.getLogger(logger_name)

            @functools.wraps(func)
            def runner(*args, **kwargs):
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    log.exception(e)

            return runner

        return pre_run


@Logger.exception_catcher('main')
def main():
    logger = Logger()
    logger.setup_handlers(name='supremelogger.logs')
    logger.setup_formatters()
    main_log = logger.setup_logger(
        'main',
        debug_mode=True,
        file_level=logging.INFO,
        stream_level=logging.INFO,
    )
    https_log = logger.setup_logger(
        'https',
        debug_mode=False,
        file_level=logging.WARNING,
        stream_level=logging.WARNING,
    )

    main_log.debug('this is a DEBUG message')
    main_log.info('this is a INFO message')
    main_log.warning('this is a WARNING message')
    main_log.error('this is a ERROR message')
    main_log.critical('this is a CRITICAL message')

    https_log.debug('this is a https DEBUG message')
    https_log.info('this is a https INFO message')
    https_log.warning('this is a https WARNING message')
    https_log.error('this is a https ERROR message')
    https_log.critical('this is a https CRITICAL message')

    main_log.info('Testing exception catcher decorator')
    print(10 / 0)


if __name__ == '__main__':
    main()
