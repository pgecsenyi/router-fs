import getopt

from domain import exceptions


class ArgumentParser:

    def __init__(self, arguments):
        self._application_name = ''
        self._arguments = arguments
        self._config_file_path = None
        self._is_config_generation_requested = False
        self._is_debugging_enabled = False
        self._log_file_path = None

    @property
    def config_file_path(self):
        return self._config_file_path

    @property
    def is_config_generation_requested(self):
        return self._is_config_generation_requested

    @property
    def is_debugging_enabled(self):
        return self._is_debugging_enabled

    @property
    def log_file_path(self):
        return self._log_file_path

    def parse(self):
        self._application_name, parameters = self._arguments[0], self._arguments[1:]

        try:
            shortopts = 'c:dhil:'
            longopts = ['config=', 'debug', 'help', 'install', 'log-path=']
            opts, _ = getopt.getopt(parameters, shortopts, longopts)
        except getopt.GetoptError as ex:
            raise exceptions.ArgumentParserException(ex)

        for opt, arg in opts:
            if opt in ('-c', '--config'):
                self._config_file_path = arg
            elif opt in ('-d', '--debug'):
                self._is_debugging_enabled = True
            elif opt in ('-h', '--help'):
                self.print_help()
                return False
            elif opt in ('-i', '--install'):
                self._is_config_generation_requested = True
            elif opt in ('-l', '--log-path'):
                self._log_file_path = arg

        if not self._is_config_generation_requested and self._config_file_path == '':
            raise exceptions.ArgumentParserException(
                'Configuration file path must be provided.')

        return True

    def print_help(self):
        print('python {0} <options>'.format(self._application_name))
        print('')
        print('  -c, --config     The path of the configuration file.')
        print('  -d, --debug      Start the program in debug mode.')
        print('  -h, --help       Print this help and exit.')
        print('  -i, --install    Generate a sample configuration file and exit.')
        print('  -l, --log-path   The path of the log file.')
        print('')
