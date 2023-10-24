"""Dreamcast ROM Class"""

import os.path
from os import mkdir
import shutil

import romsupport

class Rom:
    """Dreamcast ROM Class"""

    def __init__(self, src, name):
        """Constructor"""
        self.src = src
        self.name = name
        self.archive = self.determine_archive_type()
        self.handler = self.archive.get_handler()

    def determine_archive_type(self):
        """Determine the type of archive and return a proper handler"""
        if os.path.isdir(self.src):
            return romsupport.DirectoryArchive(self.src, self.name)
        elif os.path.splitext(self.src)[1] == ".zip":
            return romsupport.ZipArchive(self.src, self.name)
        else:
            raise ValueError(f"unhandled ROM file format: {self.src}")

    def translate_rom(self, dst_dir):
        """Initiate copying and transforming ROM contents to destination."""
        if hasattr(self, 'skip') and self.skip is True:
            print(f"skipping rom {self.name}")
            return
        elif hasattr(self, 'skip') and self.skip is False:
            shutil.rmtree(dst_dir)
            mkdir(dst_dir)
        print(f"translating rom {self.name}")
        # get a list of all the files to copy and loop over them
        for filename in self.handler.get_filenames():
            print(f"Copying {filename} to {dst_dir}")
            # get a file-like obj for the src to copy from ...
            with self.handler.open(filename) as src_file:
                # and copy it to the dst
                with open(f"{dst_dir}/{filename}", "wb") as dst_file:
                    shutil.copyfileobj(src_file, dst_file)

        # also make a file with the ROM's name in it
        with open(f"{dst_dir}/name.txt", "w") as name_file:
            name_file.write(self.name)
