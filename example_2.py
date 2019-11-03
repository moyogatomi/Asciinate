import colorama

from coreX import Core, TerminalScreen, Engine

colorama.init()


TS = TerminalScreen()

# hardcore width and height (Doesnt correspond to pixels, but terminal sizes)
core = Core(width=140, height=40, resolution=6)

core.table = u"■"

tube = Engine(
    media="https://www.nasa.gov/sites/default/files/cygx1_ill.jpg",
    core=core,
)


TS.init_clean()

if tube.propagate():
	
    TS.fast_clean()
    tube.render()
