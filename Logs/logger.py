import logging


class logger:
    def __init__(self, name, filename, formatter):
        self.logger = logging.getLogger(name)
        self.fileHandler = logging.FileHandler(filename)
        formatter = logging.Formatter(formatter, '%B %d, %Y. %H:%M:%S')
        self.fileHandler.setFormatter(formatter)
        self.logger.addHandler(self.fileHandler)

    def get_logger(self):
        return self.logger

    def close_logger(self):
        self.fileHandler.close()

    def write_log(self, level, message, extra=None):

        if extra is None:
            extra = {}

        if level == 20:
            self.logger.setLevel(logging.INFO)
            self.logger.info(message, extra=extra)
        elif level == 30:
            self.logger.setLevel(logging.WARNING)
            self.logger.warning(message, extra=extra)
        elif level == 40:
            self.logger.setLevel(logging.ERROR)
            self.logger.error(message, extra=extra)
