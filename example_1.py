import colorama

from coreX import Core, TerminalScreen, Engine

colorama.init()


# Create core
# - width and height corresponds to terminal size
# - resolution - number of channel colors -> 2**resolution. 8 is max
core = Core(width=80, height=40, resolution=6, rgb=True)
core.table = u"■"

# create Pipeline
# media - link or path to image/YTvideo, or generator returning images
tube = Engine(
    media="https://i.pinimg.com/originals/85/40/06/8540061a1f9a7249949ce72fe822a71f.jpg",
    core=core,
)

# clean screen
TS = TerminalScreen()
TS.init_clean()

# push image through pipeline and returns True if succesful
if tube.propagate():
    # move cursor to 0,0 in terminal for quick override
    TS.fast_clean()

    # Flush result into terminal
    tube.render()
