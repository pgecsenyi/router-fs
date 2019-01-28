import sys

from multiprocessing import Process

from fuse import FUSE

from domain import exceptions
from shell.argument_parser import ArgumentParser
from shell.config_manager import ConfigManager
from shell.logging_configurator import LoggingConfigurator
from shell.proxy_factory import ProxyFactory


def run():
    try:
        argument_parser = ArgumentParser(sys.argv)
        if not argument_parser.parse():
            return

        config = _load_or_generate_configuration(argument_parser)

        _configure_logging(config, argument_parser)

        proxy_factory = ProxyFactory()
        proxies = proxy_factory.create_proxies(config.volumes)
        _run_fuse(proxies, argument_parser)
    except exceptions.ArgumentParserException:
        argument_parser.print_help()
        sys.exit(1)
    except exceptions.ConfigManagerException as exception:
        print(str(exception))
        sys.exit(2)
    except exceptions.InvalidConfigException as exception:
        print(F'Configuration is invalid. {exception}')
        sys.exit(2)


def _load_or_generate_configuration(argument_parser):
    config_manager = ConfigManager(argument_parser.config_file_path)

    if argument_parser.is_config_generation_requested:
        config = config_manager.generate_sample_configuration()
        config_manager.save(config)
        print(
            F'Configuration file successfully generated to {argument_parser.config_file_path}.')
        sys.exit(0)

    return config_manager.load()


def _configure_logging(config, argument_parser):
    logging_configurator = LoggingConfigurator(
        config.logging,
        argument_parser.is_debugging_enabled,
        argument_parser.log_file_path)
    logging_configurator.configure_logging()


def _run_fuse(proxies, argument_parser):
    if argument_parser.is_debugging_enabled and len(proxies) == 1:
        FUSE(
            proxies[0].fuse_fs,
            proxies[0].mount_point,
            nothreads=True,
            foreground=True)
    else:
        for proxy in proxies:
            _start_fuse_process(proxy)


def _start_fuse_process(proxy):
    named_args = _get_named_args(proxy)
    proc = Process(
        target=FUSE,
        args=(proxy.fuse_fs, proxy.mount_point),
        kwargs=named_args)
    proc.start()


def _get_named_args(proxy):
    return {
        'nothreads': True,
        'foreground': True,
        'allow_other': proxy.allow_other
    }
