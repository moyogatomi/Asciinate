import colorama
import cv2
import numpy as np

from coreX import Core, TerminalScreen, Engine

def generator_wave():
	size_axes = np.arange(100)/10
	x,y = np.meshgrid(size_axes,size_axes)
	for z in range(200):
		grayscale_frame = np.uint8(255*np.clip((np.sin(np.sin(z/50)*x+z/50)+np.sin(np.sin(z/50)*y+z/50)),0,255))
		rgb_frame = cv2.cvtColor(grayscale_frame,cv2.COLOR_GRAY2RGB)
		rgb_frame[:,:,0]=255*np.sin(np.sin(z/50))
		rgb_frame[:,:,1]=255*np.sin(np.cos(z/50))
		yield grayscale_frame, rgb_frame

media_generator= generator_wave()



colorama.init()

TS = TerminalScreen()

core = Core(resolution=6, rgb=True)

core.adapt_size = TS.adapt(ratio=0.9, width_multier=2.5)
core.table = u" . . . ....:.:.::::::;;;;;======+=+++|+|+|+||||i|iiiiililllIIvIvvvvvnvnnnnooo2o2222S2SSSSXXXXZZZZZZ#Z#Z#####mmBmBmWBWWBWWWWQQQ"

# Show fps to see if stream can be handled smoothly
tube = Engine(
    media=media_generator, core=core, show_fps=True
)


TS.init_clean()

while tube.propagate():
    TS.fast_clean()
    tube.render()

    # If you have video, set up fps for smoothness
    tube.sleep(fps=25)
