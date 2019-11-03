import os
import urllib

import cv2
import numpy as np
import pafy
import requests


class Image:
    """
    Image download helpers
    """

    def url_to_image(self, url):
        resp = urllib.request.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        imageRGB = image.copy()
        image = image.mean(axis=2)
        return image, imageRGB

    def local_to_image(self, path):
        image = cv2.imread(path, 0)
        imageRGB = cv2.imread(path, 1)
        return image, imageRGB


class DataLoader(Image):
    """
    Very stupid decision maker
    """

    VIDEO = ["mp4", "wmv", "avi", "mkv"]
    STREAM = ["youtube.com"]
    IMAGE = ["jpg", "png", "bmp"]
    IS_URL = ["http", ".com"]

    def __call__(self, media):

        method = "local"
        data_type = ""
        for url_types in self.IS_URL:
            if url_types in media and "youtube.com" in media:
                method = "net"
                data_type = "video"
                break
            if url_types in media and "youtube.com" not in media:
                method = "net"
                data_type = "image"
                break

        if data_type == "":
            if any(media.endswith(formt) for formt in self.IMAGE):
                data_type = "image"

            if any(media.endswith(formt) for formt in self.VIDEO):
                data_type = "video"

        return self.generator(method, data_type, media)

    def generator(self, method, data_type, media):
        """Create image generators
        
        Args:
            method (str): net/local
            data_type (str): image or video
            media (str): medium - link, path
        
        Returns:
            TYPE: Description
        """
        if data_type == "image":
            return self.image(method, media)
        if data_type == "video":
            return self.stream(method, media)

    def image(self, method, media):
        if method == "net":
            image, imageRGB = self.url_to_image(media)
            yield image, imageRGB
        if method == "local":
            image = cv2.imread(media, 0)
            imageRGB = cv2.imread(media, 1)
            yield image, imageRGB

    def stream(self, method, media):
        """Simple stream
        
        Args:
            method (str): above
            media (str): above
        
        Yields:
            image/rgbimage: return both images
        """
        if method == "net":
            vPafy = pafy.new(media)
            play = vPafy.getbest(preftype="webm")
            streams = vPafy.streams
            # for s in streams:
            #    print(s)
            capture = cv2.VideoCapture(play.url)

        if method == "local":
            capture = cv2.VideoCapture(media)

        while capture.isOpened():
            ret, image = capture.read()
            yield image.mean(axis=2), image
