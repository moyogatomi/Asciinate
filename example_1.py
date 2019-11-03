import colorama

from coreX import Core, TerminalScreen, Engine

colorama.init()


TS = TerminalScreen()


# Create core
# - width and height corresponds to terminal size
# - resolution - number of channel colors -> 2**resolution. 8 is max
core = Core(resolution=6, rgb=False)

#
# Adapt image size for terminal
core.adapt_size = TS.adapt(ratio=0.75)

# define ascii table. This one is actually default
core.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"

# revert table
#core.revert_table()


# create Pipeline
# media - link or path to image/YTvideo, or generator returning images
tube = Engine(
    media="https://i.pinimg.com/originals/85/40/06/8540061a1f9a7249949ce72fe822a71f.jpg",
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
