import os
import random
import sys
import time

import cv2
import numpy as np
import types

from dataloader import DataLoader
from graphics import Content, RGB


class TerminalScreen:
    def init_clean(self):
        try:
            os.system("clear")
        except:
            os.system("cls")

    def fast_clean(self):
        self.move_cursor(0, 0)

    def move_cursor(self, x, y):
        print("\x1b[{};{}H".format(y + 1, x + 1))

    def clear():
        print("\x1b[2J")


class Core(Content, RGB):

    """Core that transforms RGB values into symbols
    and very fastly add colors
    
    Attributes:
        cube (np.array): 3Dim array of colors - color is composed of terminal code for each rgb value
        div_resolution (TYPE): value that helps to build up cube
        rgb (Bool): rgb or black/white output
        shape (TYPE): Description
        size (TYPE): Output size into terminal
        table (str): string of symbols to be used
    """

    def __init__(self, width=30, height=30, resolution=6, rgb=True):
        if not (resolution > 1 and resolution <= 8):
            raise ValueError("resolution between 1-8")

        self.rgb = rgb
        self.size = (width, height)
        # self.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"
        # self.table_ = u"■"
        self.table = u"■"
        self.div_resolution = 256 / (2 ** resolution)
        self.cube = self.load_cube(resolution=resolution)

    def view(self, img):
        return np.int64(img.reshape(img.shape[0] * img.shape[1]))

    def ixs(self, indexes, view):
        return (indexes[0], indexes[1], view)

    def ixsRGB(self, img):
        """
        Create indexes from RGB values
        
        Args:
            img (TYPE): Description
        
        Returns:
            array: indexes that will pull from RGB cube terminal color values
        """
        shap = img.shape[0] * img.shape[1]
        x1 = img[:, :, 0].reshape(shap)
        x2 = img[:, :, 1].reshape(shap)
        x3 = img[:, :, 2].reshape(shap)
        return (x1, x2, x3)

    def resize(self, frame):
        """
        Resize image and scale values according to table size
        
        Args:
            frame (2D array): frame
        
        Returns:
            2D array: unit8 frame
        """
        self.shape = frame.shape[:2]
        if len(frame.shape) == 2:
            frame = frame / self._table_size
        return np.uint8(cv2.resize(frame, (self.size[0], self.size[1])))

    def content_screen(self, frame):
        """
        Exchange grayscale values for table symbols
        Args:
            frame (2D array): Description
        
        Returns:
            array: 1D array of table symbols. Will be reshaped into 2D later
        """
        return self.d3[self.ixs(self.indexes, self.view(frame))]

    def rgb_screen(self, rgb_frame):
        """
        Exchange RGB values for rgb terminal colors
        (see ixsRGB function)
        
        Args:
            rgb_frame (2D array): image
        
        Returns:
            array: 1D chararray of rgb terminal colors
        """
        return self.cube[self.ixsRGB(rgb_frame)]

    def blend(self, frame=None, rgb_frame=None):
        """
        Blend RGB terminal colors with table symbols
        
        Args:
            frame (None, optional): Grayscale image
            rgb_frame (None, optional): RGB image
        
        Returns:
            2D chararray: reshaped chararrays almost ready for flushing
        """
        if frame is not None:
            frame = self.resize(frame)
            if rgb_frame is not None and self.rgb:
                if len(rgb_frame.shape) == 3:
                    rgb_frame = self.resize(rgb_frame / self.div_resolution)

                    return (
                        self.rgb_screen(rgb_frame) + self.content_screen(frame)
                    ).reshape(self.size[1], self.size[0])
                else:
                    return self.content_screen(frame).reshape(
                        self.size[1], self.size[0]
                    )
            else:
                return self.content_screen(frame).reshape(self.size[1], self.size[0])
        else:
            return None

    def _render(self, screen):
        """
        Replacing last column of chararray with new line
        and flushing it into standard output
        
        Args:
            screen (chararray): Charray ready to be flushed
        """
        screen[:, -1] = "\n"
        sys.stdout.buffer.write(screen.encode())
        sys.stdout.flush()


class Engine:
    def __init__(self, media=None, core=None):
        if isinstance(media, str):
            self.media = DataLoader()(media)
        if isinstance(media, types.GeneratorType):
            self.media = media

        self.core = core
        self.screen = None
        self._timestamp = time.time()

    def sleep(self, fps=30):
        """
        FPS controller. Sleep diff time to keepup FPS
        
        Args:
            fps (int, optional): frames per seconds
        """
        diff = 1 / fps - (time.time() - self._timestamp)
        if diff > 0:
            time.sleep(diff)

    def propagate(self):
        """
        Propagate image from generator through chararray generation. Blend table symbols with colors
        
        Returns:
            Bool: True if image was propagated and is ready to be flushed
        """
        try:
            self.last_images = self.media.__next__()
            self.screen = self.core.blend(
                frame=self.last_images[0], rgb_frame=self.last_images[1]
            )
            return True
        except Exception as e:
            print(e)
            return None

    def render(self):
        """
        Flush chararray if is ready and commit time for FPS controller
        """
        if self.screen is not None:
            self.core._render(self.screen)
            self._timestamp = time.time()
