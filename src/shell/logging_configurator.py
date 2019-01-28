import logging
import logging.handlers


class LoggingConfigurator:

    def __init__(self, logging_config, is_debugging_enabled=False, log_path_override=None):
        self._logging_config = logging_config
        self._is_debugging_enabled = is_debugging_enabled
        self._log_path_override = log_path_override

    def configure_logging(self):
        logger = logging.getLogger()

        log_level = self._determine_log_level()
        log_path = self._determine_log_path()
        is_logging_possible = self._logging_config.enabled and (
            log_path is not None) and (self._logging_config.max_size_bytes > 0)

        logger.setLevel(log_level)

        # If debugging is enabled, log to the command line on DEBUG level by all means.
        if self._is_debugging_enabled:
            logger.addHandler(logging.StreamHandler())
        elif not is_logging_possible:
            logger.addHandler(logging.NullHandler())
            logger.propagate = False

        # If path is set, log to file.
        if is_logging_possible:
            logger.addHandler(logging.handlers.RotatingFileHandler(
                filename=log_path,
                maxBytes=self._logging_config.max_size_bytes,
                backupCount=3))

    def _determine_log_level(self) -> int:
        if self._is_debugging_enabled:
            return logging.DEBUG

        if self._logging_config.level == 'critical':
            return logging.CRITICAL
        if self._logging_config.level == 'debug':
            return logging.DEBUG
        if self._logging_config.level == 'info':
            return logging.INFO
        if self._logging_config.level == 'warning':
            return logging.WARNING

        return logging.ERROR

    def _determine_log_path(self) -> str:
        if self._log_path_override is not None and self._log_path_override != '':
            return self._log_path_override
        if self._logging_config.path is not None and self._logging_config.path != '':
            return self._logging_config.path

        return None
