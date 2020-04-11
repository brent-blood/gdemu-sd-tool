"""Base DC ROM class"""

class BaseRomHandler:
    """Base DC Rom class"""

    def __init__(self, src, archive):
        """Constructor"""
        self.src = src
        self.archive = archive

        # cached filename of the critical image file within the archive
        self.image_file = self.archive.get_image_filename()
        self.file_mapping = {}
        self.file_obj = None

    def get_filenames(self):
        """return the filename of image's critical file"""
        raise NotImplementedError

    def open(self, filename):
        """Return a file-like object corresponding to the image file"""
        if self.file_obj is not None:
            raise AssertionError("Cannot open file twice")

        return self.archive.open(self.file_mapping[filename])

    def close(self):
        """Close a previously opened file-like object"""
        if self.file_obj is not None:
            self.file_obj.close()
            self.file_obj = None
