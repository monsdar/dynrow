import logbook
log = logbook.Logger("ErgStatsFactory")

try:
    import pyerg
    from pyerg_adapter.ErgStats import ErgStats
    log.debug("using pyerg")
except:
    from PyRow.ErgStats import ErgStats
    log.debug("using pyrow")

