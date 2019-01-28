import unittest

from domain import exceptions
from shell.argument_parser import ArgumentParser


class ArgumentParserTest(unittest.TestCase):

    def test_argumentparser_complex(self):
        args = ['main.py', '--debug', '--config=config.cfg']

        arg_parser = ArgumentParser(args)
        arg_parser.parse()

        self.assertEqual('config.cfg', arg_parser.config_file_path)
        self.assertTrue(arg_parser.is_debugging_enabled)
        self.assertIsNone(arg_parser.log_file_path)

    def test_argumentparser_config_file(self):
        args1 = ['main.py', '-c', 'test.cfg']
        args2 = ['main.py', '--config', 'test1.cfg']

        arg_parsers = self._run_argumentparser(args1, args2)

        self.assertEqual('test.cfg', arg_parsers[0].config_file_path)
        self.assertEqual('test1.cfg', arg_parsers[1].config_file_path)

    def test_argumentparser_config_file_error(self):
        args = ['main.py', '-c']

        arg_parser = ArgumentParser(args)

        with self.assertRaises(exceptions.ArgumentParserException):
            arg_parser.parse()

    def test_argumentparser_debugging(self):
        args1 = ['main.py']
        args2 = ['main.py', '-d']
        args3 = ['main.py', '--debug']

        arg_parsers = self._run_argumentparser(args1, args2, args3)

        self.assertFalse(arg_parsers[0].is_debugging_enabled)
        self.assertTrue(arg_parsers[1].is_debugging_enabled)
        self.assertTrue(arg_parsers[2].is_debugging_enabled)

    def test_argumentparser_log_file(self):
        args1 = ['main.py']
        args2 = ['main.py', '-l', 'test.log']
        args3 = ['main.py', '--log', 'test1.log']

        arg_parsers = self._run_argumentparser(args1, args2, args3)

        self.assertIsNone(arg_parsers[0].log_file_path)
        self.assertEqual('test.log', arg_parsers[1].log_file_path)
        self.assertEqual('test1.log', arg_parsers[2].log_file_path)

    def test_argumentparser_log_file_error(self):
        args = ['main.py', '--log']

        arg_parser = ArgumentParser(args)

        with self.assertRaises(exceptions.ArgumentParserException):
            arg_parser.parse()

    def _run_argumentparser(self, *argument_lists):
        result = []
        for argument_list in argument_lists:
            argument_parser = ArgumentParser(argument_list)
            argument_parser.parse()
            result.append(argument_parser)

        return result
