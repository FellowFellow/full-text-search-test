import os
import sys
from dataclasses import MISSING

from dotenv import load_dotenv

sys.path.append(".")

from logger import get_logger
logger = get_logger()

load_dotenv(".env")



# get version number from version.txt
try:
    with open("version.txt", "r") as file:
        VERSION = file.readline().strip("\n")
except Exception:
    VERSION = "latest"


class EnvError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        logger.exception(message)
        super().__init__(*args)



class MissingEnvError(EnvError):
    pass


class EnvTypeError(EnvError):
    pass


class URL:
    def __init__(self, url):
        self.url = url
        if not self.url.endswith("/"):
            self.url += "/"
        if "http" not in self.url or "://" not in self.url:
            raise EnvTypeError(f"Invalid url formatting for url: {self.url}")


def env(env_name: str, env_type: type = str, default_value: str = MISSING):
    """
    This function is used to get the environment variable.

    Args:
        env_name (str): Name of the environment variable.
        env_type (type, optional): Type of the environment variable. Defaults to str.

    Raises:
        MissingEnvError: If the environment variable is missing this error is raised
        EnvTypeError: If the environment variable has the wrong type this error is raised

    Returns:
        env (env_type): The environment variable.
    """

    var = os.getenv(env_name)
    if not var and default_value is not MISSING:
        # print(f"{env_name} not found. Using default value: {default_value}")
        var = default_value
    if not var and default_value is MISSING:
        raise MissingEnvError(message=f"the env {env_name} is missing")

    try:
        if env_type is bool and type(var) is not bool:
            var = eval(var)
        elif env_type is not str:
            var = env_type(var)
            if env_type is URL:
                var = var.url
        else:
            var = str(var)

    # needed for env_type check
    except TypeError:
        raise EnvTypeError(
            f"The env {env_name} should be type {env_type} but is {type(var)}"
        )
    # needed if eval has a faulty value
    except NameError:
        raise EnvTypeError(
            f"The env {env_name} should be type {env_type} but is {type(var)}"
        )

    return var


DB_URI = env("SQLALCHEMY_DATABASE_URI")
