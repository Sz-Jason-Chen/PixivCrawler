class ArtworkUnavailableError(Exception):
    def __str__(self):
        return "No access to artwork text."


class ImageFilesNotFoundError(Exception):
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def __str__(self):
        return f"No image files found in {self.folder_path}."


class PageReturnError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"Error message: {self.message}"

