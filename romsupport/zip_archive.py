"""Handle zip archives containing Dreamcast ROM images"""

import os
import zipfile

from .base_archive import BaseArchive
from .gdi_rom_handler import GdiRomHandler
from .cdi_rom_handler import CdiRomHandler

class ZipArchive(BaseArchive):
    """Class for handling zip files"""

    def __init__(self, src, name):
        """constructor"""
        super().__init__(src, name)
        # hold a reference to an opened archive
        self.archive = None

    def determine_rom_format(self):
        with zipfile.ZipFile(self.src) as archive:
            # iterate over the files in the zip archive, checking each one
            # to determine what it contains.
            for file in archive.namelist():
                ext = os.path.splitext(file)[1]
                if ext == ".gdi":
                    self.image_file = file
                    self.handler = GdiRomHandler(self.src, self)
                    return
                elif ext == ".cdi":
                    self.image_file = file
                    self.handler = CdiRomHandler(self.src, self)
                    return
                else:
                    # nothing special to do in this case - it's just a file
                    # that is uninteresting to this code
                    pass

        # if we got this far, we couldn't determine the type of image from
        # the contents of the zip file, so no point in continuing. Let the
        # user fix it.
        raise ValueError(f"ROM format could not be determined for {self.src}")

    def get_filenames(self):
        """Return a list of all files in the top level of the archive. These
        names may need translated to what GDemu expects still."""
        with zipfile.ZipFile(self.src) as archive:
            return archive.namelist()

    def open(self, filename):
        """return a file-like object for filename"""
        self.archive = zipfile.ZipFile(self.src)
        return self.archive.open(filename, "r")

    def close(self):
        """close a previously opened archive"""
        if self.archive is not None:
            self.archive.close()
