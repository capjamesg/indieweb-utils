import requests
from PIL import Image
from ..constants import USER_AGENT


def reduce_image_size(url=None, image_data=None, pil_image=None, reduction_size=0.5, height=None, width=None):
    """
    Reduce the size of an image. Returns a PIL.Image object. Useful for creating images for use in HTML source sets.

    :param url: The URL of the image (optional).
    :type url: str
    :param image_data: The image data in bytes (optional).
    :type image_data: bytes
    :param pil_image: The PIL.Image object (optional).
    :type pil_image: PIL.Image
    :param reduction_size: The scale factor by which to reduce the image, expressed as a number between 0 and 1. (i.e. 0.5 = 50%)
    :type reduction_size: float
    :returns: The reduced image data.
    :rtype: PIL.Image

    Example:

    .. code-block:: python

        from indieweb_utils.images import reduce_image_size

        reduced_image_data = reduce_image_size(image_data)


    """
    if not url and not image_data and not pil_image:
        raise Exception("Please provide either a URL, image data, or a PIL.Image object.")

    if url:
        image_data = requests.get(url, headers={"User-Agent": USER_AGENT}).content
        image = Image.open(image_data)

    if image_data:
        image = Image.open(image_data)

    if pil_image:
        image = pil_image

    if not reduction_size and not height and not width:
        raise Exception("Please provide either a reduction size, height, or width.")

    if height and width:
        return image.thumbnail((width, height))

    return image.thumbnail((image.size[0] * reduction_size, image.size[1] * reduction_size))
