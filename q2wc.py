#!/usr/bin/python3
"""

q2wc
Quixel to World Creator 2
Batch-generate WC2 texture XML descriptor files

Copyright (c) 2019 J. Hipps (@yellowcrescent)
https://ycnrg.org/

License: MIT

"""

__version__ = '0.1.0'
__date__ = 'Dec 15 2019'

import json
import logging
import os
import uuid
from argparse import ArgumentParser
from time import time
from xml.dom import minidom
from xml.etree import ElementTree


logger = logging.getLogger('q2wc')
NODE_UUID = uuid.uuid1()
Q_WCVERSION = "2.0"
Q_PUBLISHER = "Quixel Megascans"
Q_WEBSITE = "https://quixel.com/megascans/"
USE_EXR = False


def setup_logging(clevel=logging.INFO, flevel=logging.DEBUG, logfile=None):
    """configure logging using standard logging module"""
    logger.setLevel(logging.DEBUG)

    con = logging.StreamHandler()
    con.setLevel(clevel)
    con_format = logging.Formatter("%(levelname)s: %(message)s")
    con.setFormatter(con_format)
    logger.addHandler(con)

    if logfile:
        try:
            flog = logging.handlers.WatchedFileHandler(logfile)
            flog.setLevel(flevel)
            flog_format = logging.Formatter("[%(asctime)s] %(name)s: %(levelname)s: %(message)s")
            flog.setFormatter(flog_format)
            logger.addHandler(flog)
        except Exception as e:
            logger.warning("Failed to open logfile %s: %s", logfile, str(e))

def parse_cli():
    """parse CLI options with argparse"""
    aparser = ArgumentParser(description="Quixel to World Creator 2 descriptor generator")
    aparser.set_defaults(basedir=None, logfile=None, loglevel=logging.INFO)

    aparser.add_argument("basedir", action="store", nargs=1, metavar="BASEPATH", help="Base path to Quixel library")
    aparser.add_argument("--debug", "-d", action="store_const", dest="loglevel", const=logging.DEBUG, help="Show debug messages")
    aparser.add_argument("--logfile", "-l", action="store", metavar="LOGPATH",
                         help="Path to output logfile [default: %(default)s]")
    aparser.add_argument("--version", "-V", action="version", version="%s (%s)" % (__version__, __date__))
    return aparser.parse_args()

def scan_library(basepath, deref=False):
    """
    Scans the Quixel library at @basepath recursively,
    optionally following symlinks if @deref is True
    """
    assets = {}

    logger.debug("Scanning %s", basepath)
    for tdir, dlist, flist in os.walk(basepath, followlinks=deref):
        # find json files in current dir
        jlist = [x for x in flist if x.endswith('.json')]

        for tjson in jlist:
            rpath = os.path.realpath(os.path.join(tdir, tjson))
            logger.debug("parsing %s", rpath)
            try:
                with open(rpath) as f:
                    tdata = json.load(f)
            except Exception as e:
                logger.error("Failed to read file [%s]: %s", rpath, str(e))
                continue
            if tdata.get('id'):
                assets[rpath] = tdata
                logger.debug("got asset: %s", tdata['id'])
            else:
                logger.debug("skipping file [%s], not an asset", rpath)

    return assets

def write_descriptors(assets):
    """
    Write XML descriptors
    @assets is a dict containing parsed JSON of each asset
    """
    s_ok = 0
    s_fail = 0

    for tpath, tass in assets.items():
        tdir = os.path.dirname(tpath)
        tout = {}
        tout['taglist'] = ' '.join(tass['tags'] + tass['categories'])
        tout['desc'] = tass['name'] + '(' + tass['id'] + ')'
        tout['guid'] = str(uuid.uuid5(NODE_UUID, tass['id']))
        tout['time'] = int(time() * 100000000)
        tout['preview'] = tass['id'] + '_Preview.png'

        # find maps that are present
        for tmap in tass['maps']:
            mpath = os.path.join(tdir, tmap['uri'])
            if os.path.exists(mpath):
                if tmap['type'] == 'image/x-exr' and not USE_EXR:
                    continue
                tout['map_' + tmap['type']] = tmap['uri']

        if write_xml(tdir, tout):
            s_ok += 1
        else:
            s_fail += 1

    return (s_ok, s_fail)

def write_xml(fpath, asset):
    """
    Write new Description.xml at @fpath
    Pass in @asset dict
    """
    xdata = ElementTree.Element('WorldCreator', Version=Q_WCVERSION)
    xtextures = ElementTree.SubElement(xdata, 'Textures', Preview=asset['preview'], Tags=asset['tags'],
                                       Publisher=Q_PUBLISHER, Website=Q_WEBSITE, Guid=asset['guid'])
    ElementTree.SubElement(xtextures, 'Diffuse', File=asset['map_albedo'], Time=asset['time'])
    ElementTree.SubElement(xtextures, 'Normal', File=asset['map_normal'], Time=asset['time'])
    ElementTree.SubElement(xtextures, 'Displacement', File=asset['map_displacement'], Time=asset['time'])

    try:
        outfile = os.path.join(fpath, 'Description.xml')
        with open(outfile, 'w') as f:
            f.write(minidom.parseString(ElementTree.tostring(xdata)).toprettyxml())
            logger.debug("wrote file: %s", outfile)
            return True
    except Exception as e:
        logger.error("Failed to write XML file [%s]: %s", outfile, str(e))
        return False

def _main():
    """
    Entry point
    """
    args = parse_cli()
    setup_logging(args.loglevel, logfile=args.logfile)

    logger.info("Scanning library...")
    assets = scan_library(args.basedir)

    logger.info("Found %d assets", len(assets))
    logger.info("Writing XML descriptors...")
    s_ok, s_fail = write_descriptors(assets)

    logger.info("Wrote %d files, %d failed", s_ok, s_fail)
    logger.info("Complete.")

if __name__ == '__main__':
    _main()
