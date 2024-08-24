import logging
from flask import has_request_context, request


class SingletonLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._logger = logging.getLogger('blog_system')
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler('blog_system.log')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def _log_with_request_info(self, level, message):
        if has_request_context():
            message = f"{request.remote_addr} - {request.method} {request.url} - {message}"
        getattr(self._logger, level)(message)

    def debug(self, message):
        self._log_with_request_info('debug', message)

    def info(self, message):
        self._log_with_request_info('info', message)

    def warning(self, message):
        self._log_with_request_info('warning', message)

    def error(self, message):
        self._log_with_request_info('error', message)

    def critical(self, message):
        self._log_with_request_info('critical', message)


logger = SingletonLogger()