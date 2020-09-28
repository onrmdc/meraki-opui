from logging.handlers import SysLogHandler
import logging
from time import gmtime, strftime
import os


LOG_SERVER = None
DATE_FORMAT = "[%a, %d/%b/%Y %H:%M:%S +0000]"
NAME_FORMAT = "%Y%m%d.log"


def send_wr_log(log_message):
    if LOG_SERVER:
        syslogger = logging.getLogger('SyslogLogger')
        syslogger.setLevel(logging.INFO)
        log_handler = SysLogHandler(address=(LOG_SERVER, 514))
        syslogger.addHandler(log_handler)
        syslogger.basicConfig(format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")
        syslogger.info(log_message)

    # write to a log file
    log_date = strftime(DATE_FORMAT, gmtime())
    log_line = "{} - {}".format(log_date, log_message)
    log_filename = "/project/logs/{}".format(strftime(NAME_FORMAT, gmtime()))
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)
    with open(log_filename, "a") as f:
        f.write("\n" + log_line)