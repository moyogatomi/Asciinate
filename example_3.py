import colorama

from coreX import Core, TerminalScreen, Engine

colorama.init()

TS = TerminalScreen()

core = Core(resolution=6, rgb=True)

core.adapt_size = TS.adapt(ratio=1.2, width_multier=2.5)
core.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"

# Show fps to see if stream can be handled smoothly
tube = Engine(
    media="https://www.youtube.com/watch?v=HbsPgGpfKpU", core=core, show_fps=True
)


TS.init_clean()

while tube.propagate():
    TS.fast_clean()
    tube.render()

    # If you have video, set up fps for smoothness
    tube.sleep(fps=25)
