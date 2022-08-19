# Sky Filtering

I do not own the example images.

Run the script by using `python3 sky_filter.py <path to image(s)>`.
Ex. `python3 sky_filter.py images`

In `sky_filter.py`, you can modify the masks on lines 59 - 63 to adjust to your needs. It's a bit of a tradeoff between keeping the antennae and removing visual artifacts from the filtering, but it works with a bit of fine-tuning.

Use the `splitter` function to check RGB or HSV values in your images. This will make the mask tuning process easier.

I did throw this together very quickly. Good luck!
