class NoSuchTableException(Exception):
    """Table is not exist"""
    pass


class DataBaseAccessDeniedException(Exception):
    """Database access denied"""
    pass


class RootDirAccessDeniedException(Exception):
    """Root Dir access denied"""
    pass
