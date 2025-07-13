import json
import logging


class IgnoreMinioStatObject(logging.Filter):  # NOSONAR
    def filter(self, record):
        if isinstance(record.msg, AttributeError):
            return 'Could not stat object' not in record.msg.args[0]
        return True


class IgnoreDjangoServer(logging.Filter):  # NOSONAR
    @staticmethod
    def _conditions_to_ignore_log_record(record):
        try:
            msg = str(record.args[0])
            _conditions = (
                '/__debug__/' in msg,
                '/static/' in msg,
                'favicon.ico' in msg,
            )
            return _conditions
        except (IndexError, KeyError):
            return (False,)

    def filter(self, record):
        return not any(self._conditions_to_ignore_log_record(record))


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'level': record.levelname,
            'timestamp': self.formatTime(record, self.datefmt),
            'message': record.getMessage(),
            'logger': record.name,
        }
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_record)
