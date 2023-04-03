from logging.handlers import TimedRotatingFileHandler
from logging.config import fileConfig
import inspect, os, logging, sys

FORMATTER = logging.Formatter("%(levelname)-6s- %(name)s - %(asctime)s - message=%(message)s - line=%(lineno)-4d")
FORMATTER_EXTENDED = logging.Formatter("%(levelname)-6s- %(name)s - %(asctime)s - message=%(message)s - function=%(funcName)s line=%(lineno)-4d - call_trace=%(pathname)s")

if not os.path.isdir(os.path.join(os.getcwd(), "logs")):
    os.mkdir(os.path.join(os.getcwd(), "logs"))


def get_log_level():
    log_level = os.getenv("LOG_LEVEL")
    if log_level == None or log_level.upper() not in ["DEBUG", "INFO", "ERROR", "EXCEPTION"]:
        log_level = "DEBUG"
    log_level = log_level.upper()
    return log_level

# get the filepath to the importer
def caller_name():
    frame=inspect.currentframe()
    frame=frame.f_back.f_back
    code=frame.f_code
    return os.path.relpath(code.co_filename)

# def file_handler():
#     handler = TimedRotatingFileHandler(os.path.join("logs", "api.log"), "midnight", 1, 1, "utf-8")
#     handler.setFormatter(FORMATTER)
# def file_handler_extended():
#     handler = TimedRotatingFileHandler(os.path.join("logs", "api_extended.log"), "midnight", 1, 1, "utf-8")
#     handler.setFormatter(FORMATTER_EXTENDED)

# def get_console_handler():
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setFormatter(FORMATTER)
#     return console_handler

# get logger
def get_logger(name: str = None):
    if not name:
        name = caller_name().rstrip(".py").replace("/", ".").replace("\\",".")
    
    file = os.path.abspath(os.path.join("logger", "logging.conf"))
    fileConfig(file, disable_existing_loggers=False)
    logger = logging.getLogger(name)
    logger.setLevel(get_log_level())
    return logger