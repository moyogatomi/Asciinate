from tqdm import tqdm
import numpy as np
from sty import fg, bg, ef, rs, RgbFg
import os

class Content:
    

    @property
    def table(self):
        self._table_size = ((256/len(self._table)))
        return self._table

    @table.setter
    def table(self, value):
        
        self._table = value
        self.d3 = self.create_container()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = (int(value[0]), int(value[1]))

    def content_mask(self):
        return np.zeros(shape=self.size)

    def create_container(self):
        image_mask = self.content_mask()
        self.indexes = np.where(image_mask==0)
        d3 = np.chararray(
            shape=[image_mask.shape[0], image_mask.shape[1], len(self.table)],
            unicode=True,
        )

        indexes = np.where(image_mask == 0)
        for i in range(d3.shape[-1]):
            d3[:, :, i] = self.table[i]

        return d3

    def revert_table(self):
        temp_table = list(self._table)[::-1]
        self.table = temp_table



class RGB:
    def __init__(self):
        self.cube = self.load_cube()
    @staticmethod
    def create_cube(resolution = 2):
        res = 2**resolution
        
        print(f'Resolution {resolution} generates RGB file with {(2**7)**3} colors')
        if resolution>=7:
            print(
                "\x1b[38;2;0;255;250m Need to create RGB memory file. Expected size: 300mb \x1b[39m"
            )
        cube = np.chararray(shape=[res, res, res], itemsize=19)
        cube = cube.astype("|S19")
        
        rd = int(256/(2**resolution))
        for x in tqdm(range(res)):
            for y in range(res):
                for z in range(res):
                
                    fg.set_style("colorr", RgbFg(z*rd, y*rd, x*rd))
                    cube[x, y, z] = fg.colorr.replace("38", "38")
        np.save(f"color_{resolution}.npy", cube.astype("|S19"))
        return cube.astype("<U19")

    @staticmethod
    def load_cube(resolution=2):

        files = os.listdir("./")
        if f"color_{resolution}.npy" in files:
            cube = np.load(f"color_{resolution}.npy")
            return cube.astype("<U19")

        else:
            return RGB.create_cube(resolution=resolution)