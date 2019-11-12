import os
import tiles
import slide
import filters
import util
import numpy as np
import numpy as np
import openslide
from openslide import OpenSlideError

#General Information that can be modified according to the need

#KIND = "ADI"
#KIND = "BACK"
#KIND = "DEB"
#KIND = "LYM"
#KIND = "MUC"
#KIND = "MUS"
#KIND = "NORM"
KIND = "STR"
#KIND = "TUM"
PARTITION = "valid"
BASE_DIR = os.path.join(os.sep, "media", "bialab","7c33ac31-d9d1-4f8d-aed4-ef4049a63dc2","tialab_rawan","Datasets","kather")
SRC_DIR = os.path.join(BASE_DIR, PARTITION,KIND)
SRC_EXT = "tif"
DEST_TRAIN_EXT = "png"
DEST_TRAIN_DIR = os.path.join(BASE_DIR,PARTITION, KIND + "_" + DEST_TRAIN_EXT)
START_INDEXING = 1





dirFiles = os.listdir(SRC_DIR)
#sort the files according to their names
dirFiles.sort()
#go through all files
for filename in dirFiles:
	original = SRC_DIR +'/' +filename 
	slide = openslide.open_slide(original)
	level = slide.get_best_level_for_downsample(1)
	whole_slide_image = slide.read_region(
        (0, 0), 0, slide.level_dimensions[level])
	whole_slide_image = whole_slide_image.convert("RGB")
	newName =  KIND + '_'+str(START_INDEXING).zfill(5) + '.'+ DEST_TRAIN_EXT
	image_path = os.path.join(DEST_TRAIN_DIR,newName)
	whole_slide_image.save(image_path)
	START_INDEXING +=1

	print(START_INDEXING)

