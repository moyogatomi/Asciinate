import colorama

from coreX import Core, TerminalScreen, Engine

colorama.init()


core = Core(width=80, height=40, resolution=6, rgb=True)
core.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"

tube = Engine(media="https://www.youtube.com/watch?v=HbsPgGpfKpU", core=core)


TS = TerminalScreen()
TS.init_clean()

while tube.propagate():
    TS.fast_clean()
    tube.render()

    # If you have video, set up fps for smoothness
    tube.sleep(fps=25)
