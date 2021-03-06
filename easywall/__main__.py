"""
TODO: Doku
"""
from logging import info
from time import sleep

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from easywall.config import Config
from easywall.easywall import Easywall
from easywall.log import Log
from easywall.rules_handler import RulesHandler
from easywall.utility import delete_file_if_exists

CONFIG_PATH = "config/easywall.ini"


class ModifiedHandler(FileSystemEventHandler):
    """
    TODO: Doku
    """

    def __init__(self, apply: object) -> None:
        self.apply = apply

    def on_created(self, event) -> None:
        """
        TODO: Doku
        """
        if event.src_path.endswith("apply"):
            info("file was created. filename: {}".format(event.src_path))
            self.apply(event.src_path)


class Main(object):
    """
    TODO: Doku
    """

    def __init__(self):
        self.cfg = Config(CONFIG_PATH)

        loglevel = self.cfg.get_value("LOG", "level")
        to_stdout = self.cfg.get_value("LOG", "to_stdout")
        to_files = self.cfg.get_value("LOG", "to_files")
        logpath = self.cfg.get_value("LOG", "filepath")
        logfile = self.cfg.get_value("LOG", "filename")
        self.log = Log(loglevel, to_stdout, to_files, logpath, logfile)

        info("starting easywall")

        self.rules_handler = RulesHandler()
        self.rules_handler.ensure_files_exist()
        self.easywall = Easywall(self.cfg)
        self.event_handler = ModifiedHandler(self.apply)
        self.observer = Observer()
        self.stop_flag = False

        info("easywall has been started")

    def apply(self, filename: str) -> None:
        """
        TODO: Doku
        """
        info("starting apply process from easywall")
        delete_file_if_exists(filename)
        self.easywall.apply()

    def start_observer(self) -> None:
        """
        this function is called to keep the main process running
        if someone is pressing ctrl + C the software will initiate the stop process
        """
        self.observer.schedule(self.event_handler, ".")
        self.observer.start()

        try:
            while not self.stop_flag:
                sleep(2)
        except KeyboardInterrupt:
            info("KeyboardInterrupt received, starting shutdown")
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """
        the function stops all threads and shuts the software down gracefully
        """
        info("starting shutdown")

        self.observer.stop()
        delete_file_if_exists(".acceptance")
        self.observer.join()

        info("shutdown completed")
        self.log.close_logging()


if __name__ == "__main__":
    MAIN = Main()
    MAIN.start_observer()
