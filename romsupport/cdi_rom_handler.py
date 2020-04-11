"""CDI ROM images"""

import os.path

from .base_rom_handler import BaseRomHandler

class CdiRomHandler(BaseRomHandler):
    """CDI ROM image class"""

    def __init__(self, src, name):
        """constructor"""
        super().__init__(src, name)
        # temporary storage for file-like object references
        self.file_obj = None

        self.map_names()

    def map_names(self):
        """map names from archive to what the handler presents"""
        # loop over each file in archive and preserve the names unless it's
        # the cdi file, in which case name it 'disc.cdi'
        for filename in self.archive.get_filenames():
            if os.path.splitext(filename)[1] == ".cdi":
                self.file_mapping['disc.cdi'] = filename
            else:
                self.file_mapping[filename] = filename

    def get_filenames(self):
        """Return the name of the .cdi file within the archive"""
        filenames = []
        for filename in self.archive.get_filenames():
            if os.path.splitext(filename)[1] == ".cdi":
                filenames.append("disc.cdi")
            else:
                filenames.append(filename)
        return filenames
