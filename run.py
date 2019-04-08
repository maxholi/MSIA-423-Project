import argparse
import logging.config
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-penny-lane")

from src.add_songs import create_db, add_track


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("artist", default="Britney Spears", description="Artist of song to be added")
    sb_create.add_argument("title", default="Radar", description="Title of song to be added")
    sb_create.add_argument("album", default="Circus", description="Album of song being added.")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("artist", default="Emancipator", description="Artist of song to be added")
    sb_ingest.add_argument("title", default="Minor Cause", description="Title of song to be added")
    sb_ingest.add_argument("album", default="Dusk to Dawn", description="Album of song being added")
    sb_ingest.set_defaults(func=add_track)

    args = parser.parse_args()
    args.func(args)
