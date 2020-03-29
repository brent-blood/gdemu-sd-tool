#!/usr/bin/env python3

"""A tool for manipulating SD cards intended for Sega Dreamcasts modded
with GDemu replacments for their GDrom drives. See README.md"""

import sys
import argparse
import os
import os.path
import json
import shutil
import zipfile

def print_err(message):
    """write a message to stderr"""
    print(message, file=sys.stderr)

class Gst:
    """Manage SD cards"""

    def __init__(self, mnt, manifest, verbose):
        """constructor"""
        self.mnt = mnt
        self.manifest = manifest
        self.verbose = verbose
        self.max_slot = 1
        self.data = {}

    def debug(self, message):
        """write a message when verbose output requested"""
        if self.verbose:
            print(message)

    def parse_manifest(self):
        """Convert JSON to python datastructure"""
        with open(self.manifest) as json_file:
            self.data = json.load(json_file)

        self.debug("Checking format of manifest")
        if 'slots' not in self.data:
            print_err(f"'slots' must be defined")
            sys.exit(1)

        slot_num = 1
        for game in self.data['slots']:
            self.debug(f"testing slot {slot_num} for required keys")
            if 'src' not in game:
                print_err(f"'src' not defined for slot {slot_num}")
                sys.exit(1)
            if 'name' not in game:
                print_err(f"'name' not defined for slot {slot_num}")
                sys.exit(1)
            self.debug(f"testing if file for slot {slot_num} exists")
            if not os.path.isfile(game['src']):
                print_err(f"file does not exist: {game['src']}")
                sys.exit(1)

            slot_num = slot_num + 1
        # the last increment in the loop moves it one greater than the number
        # of games in the file, but slot 01 is always GDmenu so it's actually
        # correct so no need to adjust.
        self.max_slot = slot_num
        self.debug(f"Last slot will be {self.max_slot}")

    def create_directories(self):
        """Create directories for all slots"""
        for slot in range(1, self.max_slot + 1):
            # The GDemu docs say that slots 0-9 should be zero filled and
            # anything larger just uses its natural length. This fits that.
            slot_dir = f"{slot:02}"
            self.debug(f"Creating dir: {self.mnt}/{slot_dir}")
            os.mkdir(f"{self.mnt}/{slot_dir}")

    def install_gdmenu(self):
        """Install GDmenu onto mount point"""
        self.debug("Copying GDmenu files")
        shutil.copy('./gdmenu/GDEMU.ini', f"{self.mnt}/")
        # GDmenu is just another slot to GDemu - so it follows the same
        # naming rules.
        shutil.copyfile('./gdmenu/GDmenu_v0.6.cdi', f"{self.mnt}/01/disc.cdi")

    def copy_files(self):
        """dump out internal datastructure"""
        for slot in range(2, self.max_slot + 1):
            # see comment above for why this format is used.
            slot_dir = f"{slot:02}"
            # the datastructure is 0-indexed _and_ doesn't account for GDmenu
            # being in slot 01 so it's necessary to adjust backwards by 2
            game = self.data['slots'][slot - 2]
            self.debug(f"Copying {game['name']} to {self.mnt}/{slot_dir}")

            with zipfile.ZipFile(game['src']) as archive:
                for file in archive.namelist():
                    archive.extract(file, f"{self.mnt}/{slot_dir}")
                    if file.endswith(".gdi"):
                        shutil.move(f"{self.mnt}/{slot_dir}/{file}",
                                    f"{self.mnt}/{slot_dir}/disc.gdi")
            with open(f"{self.mnt}/{slot_dir}/name.txt", "w+") as name_file:
                name_file.write(f"{game['name']}\n")

def main():
    """entrypoint for the program"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--manifest', required=True,
        help='JSON manifest describing desired image layout')
    parser.add_argument(
        '-t', '--target', required=True,
        help='Filesystem target directory for mounted SD card')
    parser.add_argument(
        "-v", "--verbose", action='store_true', help="Enable verbose output")
    args = parser.parse_args()

    gst = Gst(mnt=args.target, manifest=args.manifest, verbose=args.verbose)
    gst.parse_manifest()
    gst.create_directories()
    gst.install_gdmenu()
    gst.copy_files()

if __name__ == "__main__":
    main()
