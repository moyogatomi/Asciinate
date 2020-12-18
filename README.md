# Asciinate

![](https://github.com/moyogatomi/Asciinate/blob/master/showcase.gif)

## Description

fast transformation of grayscale and rgb images into custom ascii letters

support for youtube stream (not all videos are working)

## Usage

0) have python >= 3.6

1) install requirements (virtualenv)
```bash
pip install -r requirements
```
2) init colorama
```python

import colorama

colorama.init()
```

3) import core and pipeline modules
```python
from coreX import Core, TerminalScreen, Engine
```

4) Create Terminal controller
```python
TS = TerminalScreen()
```

5) Initialize core
```python
# resolution - number of colors in a channel  -> 2**resolution. 8 is max. Use 8 unless you want to carry extra 400mb in RAM
core = Core(resolution=6, rgb=True)

# dont care about image size and leave it to Terminal Controller
core.adapt_size = TS.adapt(ratio=0.75)

# define ascii table. This one is actually default
core.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"

# create Pipeline
# media - link or path to image/YTvideo, or generator returning tuple(grayscale_image,rgb_image)
tube = Engine(
    media="url or path to image/YT stream or generator",
    core=core,
)

# clean screen
TS.init_clean()

# push image through pipeline and returns True if succesful
if tube.propagate():

    # move cursor to 0,0 in terminal for quick override
    TS.fast_clean()

    # Flush result into terminal
    tube.render()
```

### For more use cases checkout examples
