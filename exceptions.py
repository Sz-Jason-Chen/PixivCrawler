class ArtworkUnavailableError(Exception):
    def __str__(self):
        return "No access to artwork text."


class PageReturnError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Error message: " + self.message
