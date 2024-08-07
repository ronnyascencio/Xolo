import os
def checkPath(path):
    if os.path.exists(path):
        return path
    return None
