import hashlib
import os

hasher = hashlib.sha256
BLOCKSIZE = 65536

def create_filehash(path):
    """
    Return Base64 hash of file at path
    """
    h = hasher()
    with open(path, "rb") as f:
        buf = f.read(BLOCKSIZE)
        while len(buf) > 0:
            h.update(buf)
            buf = f.read(BLOCKSIZE)
    return h.digest().encode("base64").strip().strip("=")

def filedata(path):
    return {
        "filehash": create_filehash(path),
        "filesize": os.stat(path).st_size,
    }
