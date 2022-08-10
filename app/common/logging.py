from logging import FileHandler, getLogger

logger = getLogger('default')


class Utf8FileHandler(FileHandler):
    """
    A handler class which writes formatted logging records to disk files with utf-8 encoding.
    """

    def __init__(self, filename, mode='a', encoding=None, delay=False):
        super().__init__(filename, mode, 'utf-8', delay)
