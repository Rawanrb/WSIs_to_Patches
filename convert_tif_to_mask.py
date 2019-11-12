import os
import tiles
import slide
import filters
import util
import numpy as np

#First change slide SRC_TRAIN_EXT & DEST_TRAIN_DIR to tif

slide.SRC_TRAIN_DIR = os.path.join(slide.BASE_DIR, "Annotations","tif","Tumour")
slide.DEST_TRAIN_DIR = os.path.join(slide.BASE_DIR, "Annotations","pngs","Tumour")

slide.SRC_TRAIN_EXT = "tif"


slide.SCALE_FACTOR = 16
slide.training_slide_to_image(1)
slide.training_slide_to_image(2)
slide.training_slide_to_image(8)
slide.training_slide_to_image(10)
slide.training_slide_to_image(14)


#slide.xlsx_name = os.path.join(slide.BASE_DIR,'Slide_Patch_Info.xlsx')
#slide.sheet_name = 'Sheet2'
#slide.mask_info()
