import base64
from fastapi import HTTPException, status


def decode_image(path: str, encoded_image: str):
    with open(path, 'wb') as f:
        try:
            f.write(base64.b64decode(encoded_image.encode("utf-8")))
        except Exception as ex:
            # log the exception
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid image encoding')
