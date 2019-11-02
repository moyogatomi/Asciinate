from coreX import Core, TerminalScreen, Engine
import colorama
colorama.init()


core = Core(width=80,height=40,resolution=6)
core.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"
tube = Engine(media = 'https://www.nasa.gov/sites/default/files/cygx1_ill.jpg', core = core)


TS = TerminalScreen()
TS.init_clean()

if tube.propagate():
    TS.fast_clean()
    tube.render()

