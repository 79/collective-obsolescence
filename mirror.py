# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import random

start_time = time.time()

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 108

pixel_is_on = [False] * num_pixels
pixel_start_time = [0] * num_pixels
colors = []
for i in range(num_pixels):
    colors.append(random.randint(0, 255))

def add_check_in(numg):
    for i in range(numg):
        key = random.randint(0, num_pixels-1)
        pixel_is_on[key] = True
        pixel_start_time[key] = time.time()

add_check_in(15)

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
        pixel_pin,
        num_pixels,
        brightness=0.01,
        auto_write=False,
        pixel_order=ORDER)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            if pixel_is_on[i] and pixel_start_time[i] != 0:
                pixels[i] = wheel(colors[i])
            else:
                pixels[i] = (0, 0, 0)

    pixels.show()
    #    time.sleep(wait)

def update_start_times():
    ctime = time.time()

    for i in range(num_pixels):
        if (pixel_start_time[i] is 0):
            continue

        elapsed_time = ctime - pixel_start_time[i]
        print(elapsed_time)
        if elapsed_time > 10:
            pixel_is_on[i] = False
            pixel_start_time[i] = 0


while True:
    secs = time.time() - start_time
    print("elapsed: " + str(secs))

    #if random.randint(0, 2) <= 1:
    #    add_check_in(2)


    #update_start_times()
    rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step

    input()
    add_check_in(1)

