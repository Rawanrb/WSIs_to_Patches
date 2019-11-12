import os
import tiles
import slide
import filters
import util
import numpy as np

#First change slide SRC_TRAIN_EXT & DEST_TRAIN_DIR to tif


slide.SRC_TRAIN_DIR = os.path.join(slide.BASE_DIR, "5_pilot_wsi")
slide.DEST_TRAIN_DIR = os.path.join(slide.BASE_DIR, "wsi_masks")



slide.SCALE_FACTOR = 32
slide.training_slide_to_image(1)
filters.produce_image_mask(1, display=False, save=True)
# slide.training_slide_to_image(2)
# filters.produce_image_mask(2, display=False, save=True)
# slide.training_slide_to_image(8)
# filters.produce_image_mask(8, display=False, save=True)
# slide.training_slide_to_image(10)
# filters.produce_image_mask(10, display=False, save=True)
# slide.training_slide_to_image(14)
# filters.produce_image_mask(14, display=False, save=True)


#slide.xlsx_name = os.path.join(slide.BASE_DIR,'Slide_Patch_Info.xlsx')
#slide.sheet_name = 'Sheet2'
#slide.mask_info()
