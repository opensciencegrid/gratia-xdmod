
"""
Library for synchronizing Gratia job accounting with XDMoD.

This library will connect to the Gratia database, query for
job records, do a little bit of data modificaiton and insert
the record in the XDMoD database.

"""

import os
import time
import random
import logging
import optparse
import ConfigParser

import xdmod
import gratia
import locking
import transaction

log = None

MAX_ITERATIONS = 30

def parse_opts():

    parser = optparse.OptionParser(conflict_handler="resolve")
    parser.add_option("-c", "--config", dest="config",
                      help="Location of the configuration file.",
                      default="/etc/gratia-xdmod.cfg")
    parser.add_option("-v", "--verbose", dest="verbose",
                      default=False, action="store_true",
                      help="Increase verbosity.")
    parser.add_option("-s", "--cron", dest="cron",
                      type="int", default=0,
                      help = "Called from cron; cron interval (adds a random sleep)")
    
    opts, args = parser.parse_args()

    if not os.path.exists(opts.config):
        raise Exception("Configuration file, %s, does not exist." % \
            opts.config)

    return opts, args


def config_logging(cp, opts):
    global log
    log = logging.getLogger("gratia_xdmod")

    # log to the console
    # no stream is specified, so sys.stderr will be used for logging output
    console_handler = logging.StreamHandler()

    # default log level - make logger/console match
    # Logging messages which are less severe than logging.WARNING will be ignored
    log.setLevel(logging.WARNING)
    console_handler.setLevel(logging.WARNING)

    if opts.verbose: 
        log.setLevel(logging.DEBUG)
        console_handler.setLevel(logging.DEBUG)

    # formatter
    formatter = logging.Formatter("[%(process)d] %(asctime)s %(levelname)7s:  %(message)s")
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    log.debug("Logger has been configured")


def main():
    opts, args = parse_opts()
    cp = ConfigParser.ConfigParser()
    cp.read(opts.config)
    config_logging(cp, opts)

    if opts.cron > 0:
        random_sleep = random.randint(1, opts.cron)
        log.info("gratia-xdmod called from cron; sleeping for %d seconds." % \
            random_sleep)
        time.sleep(random_sleep)

    lockfile = cp.get("transaction", "lockfile")
    locking.exclusive_lock(lockfile)
   
    iteration = 0
    job_count = 1
    while job_count > 0 and iteration < MAX_ITERATIONS:

        iteration = iteration + 1

        last_dbid = xdmod.get_last_dbid(cp)

        log.debug("Starting from DBID %d" % last_dbid)

        jobs = gratia.query_gratia(cp, last_dbid)

        job_count = 0
        for job in jobs:
            log.debug("Processing job: %s" % str(job))
            
            if not xdmod.add(cp, job):
                log.fatal("Fatal error inserting thew job in the XDMoD database - exiting!")
                return 1
            
            job_count += 1

    return 0

