"""Base class for all Dreamcast ROM file formats"""

import os

from .base_archive import BaseArchive
from .gdi_rom_handler import GdiRomHandler
from .cdi_rom_handler import CdiRomHandler

class DirectoryArchive(BaseArchive):
    """Base class for all Dreamcast ROM file formats"""
    def __init__(self, src, name):
        """constructor"""
        super().__init__(src, name)
        self.fileobj = None

    def determine_rom_format(self):
        """Determine the type of the archive by looking at its files"""

        # pylint: disable=fixme
        # TODO: modify the format handler classes to give hints as to how
        # to recognize the critical files that they look for and replace this
        # code with some that uses that
        for entity in os.listdir(self.src):
            ext = os.path.splitext(entity)[1]
            if ext == ".cdi":
                self.image_file = entity
                self.handler = CdiRomHandler(self.src, self)
                return
            elif ext == ".gdi":
                self.image_file = entity
                self.handler = GdiRomHandler(self.src, self)
                return

        # if we got this far, we couldn't determine the type of image from
        # the contents of the zip file, so no point in continuing. Let the
        # user fix it.
        raise ValueError(f"ROM format could not be determined for {self.src}")

    def get_filenames(self):
        """Return a list of all files in the top level of the directory"""
        return os.listdir(self.src)

    def open(self, filename):
        """Return a fileobject corresponding to the requested file"""
        self.fileobj = open(f"{self.src}/{filename}", "rb")
        return self.fileobj

    def close(self):
        """close previously opened file"""
        if self.fileobj is not None:
            self.fileobj.close()
