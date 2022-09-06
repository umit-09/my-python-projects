import numpy as np
from PIL import Image

GREYSCALE = False
img_name = 'image.png'

# Read in the image, convert to greyscale.
img = Image.open(img_name)
if GREYSCALE:
    img = img.convert('L')

width, height = img.size
new_width = int(input("new width > "))
new_height = int(height * new_width / width)
img = img.resize((new_width, new_height), Image.ANTIALIAS)
samples = int(input("enter samples > "))

def get_new_val(old_val, nc):
    """
    Get the "closest" colour to old_val in the range [0,1] per channel divided
    into nc values.

    """

    return np.round(old_val * (nc - 1)) / (nc - 1)

# For RGB images, the following might give better colour-matching.
#p = np.linspace(0, 1, nc)
#p = np.array(list(product(p,p,p)))
#def get_new_val(old_val):
#    idx = np.argmin(np.sum((old_val[None,:] - p)**2, axis=1))
#    return p[idx]

def fs_dither(img, nc):
    """
    Floyd-Steinberg dither the image img into a palette with nc colours per
    channel.

    """

    arr = np.array(img, dtype=float) / 255

    for ir in range(new_height):
        for ic in range(new_width):
            # NB need to copy here for RGB arrays otherwise err will be (0,0,0)!
            old_val = arr[ir, ic].copy()
            new_val = get_new_val(old_val, nc)
            arr[ir, ic] = new_val
            err = old_val - new_val
            # In this simple example, we will just ignore the border pixels.
            if ic < new_width - 1:
                arr[ir, ic+1] += err * 7/16
            if ir < new_height - 1:
                if ic > 0:
                    arr[ir+1, ic-1] += err * 3/16
                arr[ir+1, ic] += err * 5/16
                if ic < new_width - 1:
                    arr[ir+1, ic+1] += err / 16
        print("%",int((100*ir)/new_height))

    carr = np.array(arr/np.max(arr, axis=(0,1)) * 255, dtype=np.uint8)
    return Image.fromarray(carr)


print('sample =', samples)
dim = fs_dither(img, samples)
dim.save('dimg-{}.png'.format(samples))
print("sample:",samples,"finished")