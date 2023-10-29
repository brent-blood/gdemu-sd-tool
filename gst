#!/usr/bin/env python3

"""A tool for manipulating SD cards intended for Sega Dreamcasts modded
with GDemu replacments for their GDrom drives. See README.md"""

import sys
import argparse
import os
import os.path
import json
import shutil

import romsupport


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

        # place GDmenu in the first slot
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.slots = [romsupport.Rom(f'{script_dir}/gdmenu', 'GDmenu')]

    def debug(self, message):
        """write a message when verbose output requested"""
        if self.verbose:
            print(message)

    def parse_manifest(self):
        """validate manifest and build image list"""
        with open(self.manifest) as json_file:
            manifest = json.load(json_file)

        self.debug("Checking format of manifest")
        if 'slots' not in manifest:
            print_err(f"'slots' must be defined")
            sys.exit(1)

        for game in manifest['slots']:
            self.debug(f"testing slot for required keys")
            if 'src' not in game:
                print_err(f"'src' not defined for slot")
                sys.exit(1)
            if 'name' not in game:
                print_err(f"'name' not defined for slot")
                sys.exit(1)

            src = game['src']
            name = game['name']

            self.slots.append(romsupport.Rom(src, name))

    def create_directories(self):
        """Create directories for all slots"""
        for slot in range(1, len(self.slots) + 1):
            # The GDemu docs say that slots 0-9 should be zero filled and
            # anything larger just uses its natural length. This fits that.
            slot_dir = f"{slot:02}"
            self.debug(f"Creating dir: {self.mnt}/{slot_dir}")
            try:
                os.mkdir(f"{self.mnt}/{slot_dir}")
            except FileExistsError:
                # Read the the 'name.txt' file in the existing directory and check if the name matches
                # the name of the ROM we're trying to copy. If it does, skip the folder. If it doesn't,
                # set skip to False so that the folder is deleted and recreated.
                translated_slot = slot - 1
                try:
                    with open(f"{self.mnt}/{slot_dir}/name.txt") as name_file:
                        name = name_file.readline().rstrip()
                        if self.slots[translated_slot].name == name:
                            self.slots[translated_slot].skip = True
                        else:
                            print_err(f"Slot {slot} already contains {name}, while the manifast has {self.slots[slot].name}")
                            self.slots[translated_slot].skip = False
                except FileNotFoundError:
                    # If there's no 'name.txt' file, set skip to False so that the folder is deleted and recreated.
                    self.slots[translated_slot].skip = False

    def copy_files(self):
        """Copy GDEMU ini and invoke appropriate copy routine from each slot"""

        # Copy ini file for GDEMU to the root of the target directory.
        # This file is included with the script in the dcmenu subdirectory
        # so act relative to the script's location.
        script_dir = os.path.dirname(os.path.realpath(__file__))
        shutil.copy(f'{script_dir}/gdmenu/GDEMU.ini', f"{self.mnt}/")

        # Each ROM container class has its own routine for copying files
        for index, slot in enumerate(self.slots):
            slot.translate_rom(f"{self.mnt}/{index+1:02}")

    def copy_manifest(self):
        """Place a copy of the manifest file onto the SD card"""
        shutil.copyfile(self.manifest, f"{self.mnt}/manifest.json")


def add_game(manifest, name, src):
    if name is None:
        print_err("Name must be specified with -n")
        sys.exit(1)
    if os.path.isfile(src) is False:
        print_err(f"{src} is not a file or does not exist")
        sys.exit(1)
    with open(manifest, 'r+') as json_file:
        manifest = json.load(json_file)
        manifest['slots'].append({'name': name, 'src': src})
        json_file.seek(0)
        json.dump(manifest, json_file, indent=4)
        json_file.truncate()


def main():
    """entrypoint for the program"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m', '--manifest', required=True,
        help='JSON manifest describing desired image layout')
    parser.add_argument(
        '-t', '--target', required=False,
        help='Filesystem target directory for mounted SD card')
    parser.add_argument(
        "-v", "--verbose", action='store_true', help="Enable verbose output")
    parser.add_argument(
        '-a', '--add', required=False,
        help='File to be added to the manifest')
    parser.add_argument(
        '-n', '--name', required=False,
        help='Name of the game to be added to the manifest'
    )
    args = parser.parse_args()

    if args.target is None and args.add is None:
        print_err("Either -t or -a must be specified")
        sys.exit(1)

    if args.target is not None:
        gst = Gst(mnt=args.target, manifest=args.manifest, verbose=args.verbose)
        gst.parse_manifest()
        gst.copy_manifest()
        gst.create_directories()
        gst.copy_files()
    if args.add is not None:
        add_game(args.manifest, args.name, args.add)


if __name__ == "__main__":
    main()
