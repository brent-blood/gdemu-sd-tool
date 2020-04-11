"""Dreamcast GDI ROM image handler"""

import os.path
import io
import shlex

from .base_rom_handler import BaseRomHandler

class GdiRomHandler(BaseRomHandler):
    """Class for GDI files"""

    def __init__(self, src, archive):
        """constructor"""
        super().__init__(src, archive)
        # the contents of the GDI need patched to meet GDemu requirements
        self.translated_gdi = ""
        self.map_names()

    def map_names(self):
        """Find and walk the GDI file in the archive and map the names of
        files in the archive"""

        self.translated_gdi = ""

        # add a mapping for the GDI file itself with static name
        self.file_mapping['disc.gdi'] = self.image_file

        # retrieve the file contents and crack it open
        with self.archive.open(self.image_file) as gdi:
            # the first line contains an integer for the number of track files
            files_in_archive = int(gdi.readline())
            self.translated_gdi += f"{files_in_archive}\n"

            # there should be a line for each file, slurp in those lines ...
            filenum = 0
            while filenum < files_in_archive:
                filenum = filenum + 1
                line = gdi.readline().decode()
                # split it by spaces but preserve quoted strings
                fields = shlex.split(line)

                # the 4th field in these lines appears to be the filename
                ext = os.path.splitext(fields[4])[1]
                # map the mentioned files to what GDemu expects
                patched = f"track{filenum:02}{ext}"
                self.file_mapping[patched] = fields[4]

                # overwrite the original name with the new patched name
                # and add it to the translated data
                fields[4] = patched
                self.translated_gdi += f"{' '.join(fields)}\n"

    def open(self, filename):
        """Translate the gdi file, or retrieve the mapped file as is"""
        if filename == 'disc.gdi':
            return io.BytesIO(self.translated_gdi.encode())

        return self.archive.open(self.file_mapping[filename])

    def get_filenames(self):
        """Return the name of the translated files within the archive"""
        if self.file_mapping is None:
            self.map_names()

        return self.file_mapping.keys()
