# command-line arguments for DynRow

import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', default="Nils", help="user NAME for user boat name")  # --name <name on user boat>
    return parser.parse_args()


# name = player's name (always present)
args = parse_args()
