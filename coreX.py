import os
import random
import sys
import time

import cv2
import numpy as np
import types

from dataloader import DataLoader
from graphics import Content, RGB, BasicColors


class TerminalScreen:

    """
    Class that manages terminal window
    """

    def init_clean(self):
        try:
            os.system("clear")
        except:
            os.system("cls")

    def fast_clean(self,x=0,y=0):
        self.move_cursor(x, y)

    def move_cursor(self, x, y):
        print("\x1b[{};{}H".format(y + 1, x + 1))

    def clear():
        print("\x1b[2J")

    def size(self, ratio=1):
        """
        Get terminal size
        
        Args:
            ratio (int, optional): fration of terminal sizes
        
        Returns:
            tuple: width,height multiplied by ratio
        """
        # credits https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
        height, width = os.popen("stty size", "r").read().split()
        return int(width)*ratio, int(height)*ratio

    def adapt(self, ratio=1, width_multier=2.5):
        """
        Experimental size adaptation. Due to the fact that terminal height/width doesnt correspond
        to frame width and height, it may need some refactor
        
        Args:
            ratio (int, optional): Description
            width_multier (float, optional): as is written in description. this value manipulates width
        """
        terminal_height, terminal_width = self.size(ratio=ratio)

        class AutoResizer:
            WIDTH_MULTIER = width_multier

            def __init__(self, terminal_height, terminal_width, ratio):
                self.terminal_height = terminal_height
                self.terminal_width = terminal_width
                self.terminal_ratio = terminal_width / terminal_height
                self.ratio = ratio

            def __call__(self, frame):
                return self.adapt_size(frame.shape)

            def adapt_size(self, shape):
                frame_height, frame_width = shape[0], shape[1]
                frame_ratio = frame_height / frame_width
                # print(frame_ratio ,self.terminal_ratio)
                w_resizer = terminal_width / frame_width
                h_resizer = terminal_height / frame_height
                resizer = min([w_resizer, h_resizer])
                return (
                    int(frame_width * resizer * ratio * self.WIDTH_MULTIER),
                    int(frame_height * resizer * ratio),
                )

        return AutoResizer(terminal_height, terminal_width, ratio)


class Core(Content, RGB):

    """Core that transforms RGB values into symbols
    and very fastly add colors
    
    Attributes:
        adapt_size (class): auto frame resizer
        cube (np.array): 3Dim array of colors - color is composed of terminal code for each rgb value
        div_resolution (TYPE): value that helps to build up cube
        rgb (Bool): rgb or black/white output
        size (TYPE): Output size into terminal
        table (str): string of symbols to be used
    
    Deleted Attributes:
        shape (TYPE): Description
    """

    def __init__(self, width=30, height=30, resolution=6, rgb=True):
        if not (resolution > 1 and resolution <= 8):
            raise ValueError("resolution between 1-8")

        self.rgb = rgb
        self.size = (width, height)
        self.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"
        self.div_resolution = 256 / (2 ** resolution)
        if rgb:
            self.cube = self.load_cube(resolution=resolution)
        self.adapt_size = None
        self._frame_size = (0, 0, 0)

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
            if self.adapt_size is not None:

                if frame.shape != self._frame_size:
                    self.size = self.adapt_size(frame)
                    self.create_container()

                self._frame_size = frame.shape

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
    def __init__(self, media=None, core=None,show_fps = False):
        if isinstance(media, str):
            self.media = DataLoader()(media)
        if isinstance(media, types.GeneratorType):
            self.media = media

        self.core = core
        self.screen = None
        self._timestamp = time.time()
        self.performance = 0
        self.show_fps = show_fps

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
        time_start= time.time()
        try:
            self.last_images = self.media.__next__()
            self.screen = self.core.blend(
                frame=self.last_images[0], rgb_frame=self.last_images[1]
            )
            self.performance = round(1/(time.time()-time_start),2)
            return True
        except Exception as e:
            print(e)
            self.performance = (time.time()-time_start)
            return None
        
    def render(self):
        """
        Flush chararray if is ready and commit time for FPS controller
        """
        if self.screen is not None:
            self.core._render(self.screen)
            self._timestamp = time.time()
        if self.show_fps:
            
            print(f"{BasicColors.WHITE}Calculation performance: --{self.performance}--")
