"""Base class for ROM file encapsulation"""

import sys

class BaseArchive:
    """Base class for ROM file encapsulation"""

    def __init__(self, src, name):
        """constructor"""

        self.src = src
        self.name = name

        # Adjust relative paths to be relative to the executable's location
        if self.src[0] != '/':
            # This is the path relative of the script itself. Use this as the
            # base for any paths that aren't absolute.
            sys_path = sys.path[0]
            self.src = f"{sys_path}/{self.src}"

        # name of 'critical' file in archive for a given format
        self.image_file = None
        # instance of a handler class determined by the archive contents
        self.handler = None
        # sets the handler and image_file instance variables
        self.determine_rom_format()

    def get_name(self):
        """Return the human readable name of this ROM"""
        return self.name

    def get_src(self):
        """Return the ROM's src on the filesystem"""
        return self.src

    def get_image_filename(self):
        """Return the name of the critical file within the archive"""
        return self.image_file

    def get_handler(self):
        """return handler instance"""
        return self.handler

    def determine_rom_format(self):
        """Determine in a manner unique to the file container what type of
        ROM this represents."""
        raise NotImplementedError()

    def get_filenames(self):
        """get list of files in archive"""
        raise NotImplementedError()

    def open(self, filename):
        """Open a file from the archive"""
        raise NotImplementedError()

    def close(self):
        """Close the archive"""
        raise NotImplementedError
