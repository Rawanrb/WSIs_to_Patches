import tiles
import slide
import util
import math
import matplotlib.pyplot as plt
import multiprocessing
import openslide
import os
import matplotlib
matplotlib.use('TkAgg')

#slides = [1,2,8,10,14]
slide_num = 10
count = 0

#if scale factor is 16 and above make this true
scale_up = False

#this scale factor is for the pre-processing of mask and wsi
slide.SCALE_FACTOR = 16

#this number will be divided by the scale factor according to the required level 
tiles.ROW_TILE_SIZE = 224
tiles.COL_TILE_SIZE = 224

slide.MASK_DIR = os.path.join(slide.BASE_DIR,"Annotations", "pngs","Tumour")



#step 1
#save the info of wsi done for once
#slide.xlsx_name = os.path.join(slide.BASE_DIR,'Slide_Patch_Info.xlsx')
#slide.sheet_name = 'Sheet1'
# slide.slide_info(display_all_properties=True)

#step 2
#get the image from wsi to apply filter 
# import tensorflow as tf
# with tf.device('/device:GPU:0'):
	#slide.training_slide_to_image(slide_num) #delete the filtered imag
#slide.singleprocess_training_slides_to_images() # for all wsi images at once


#Step 3
import tensorflow as tf
tf.debugging.set_log_device_placement(True)

with tf.device('/device:GPU:0'):
	try:
		#to save the info of tiles
		slide_filepath = slide.get_training_slide_path(slide_num)
		wsi_slide = slide.open_slide(slide_filepath)
		slide.xlsx_name = os.path.join(slide.BASE_DIR,'patches_'+ str(slide_num).zfill(3) +'.xlsx')
		slide.sheet_name = "Sheet1"

		tile_summary = tiles.dynamic_tiles(slide_num)

		tiles.NUM_TOP_TILES =  tile_summary.count # to change how many tiles we want to access default value is 100 in tiles file
		top_tiles = tile_summary.top_tiles()
		top_tiles = sorted(top_tiles, key=lambda t: t.tissue_percentage, reverse=True)



		for t in top_tiles:
			count += 1
			if scale_up:#in case you want top tiles from different level

				slide.SCALE_FACTOR = 2
				level = wsi_slide.get_best_level_for_downsample(slide.SCALE_FACTOR)

				x, y = t.o_c_s, t.o_r_s
				w, h = t.o_c_e - t.o_c_s, t.o_r_e - t.o_r_s

				w = math.floor(w / slide.SCALE_FACTOR)
				h = math.floor(h / slide.SCALE_FACTOR)

				tile_region = wsi_slide.read_region((x, y), level, (w, h)) # read the required region
				pil_img = tile_region.convert("RGB") #convert from RGBA to RGB
				np_tile = util.pil_to_np_rgb(pil_img) 

				patch_path = slide.get_patch_path(t,count, slide.SCALE_FACTOR,w,h)

			else: #in case you want top tiles from level 0
				np_tile = t.get_np_tile()
				print(t.tissue_percentage)
				slide.SCALE_FACTOR = 1 
				patch_path = slide.get_patch_path(t,count, slide.SCALE_FACTOR,t.o_c_e - t.o_c_s,t.o_r_e - t.o_r_s) # where to save patches

			patch = util.np_to_pil(np_tile)

			dir = os.path.dirname(patch_path)
			if not os.path.exists(dir):
				os.makedirs(dir)
			
			patch.save(patch_path)
			#if count > 2000:# when patch numbers more than 2000
			#	break
		# 	#plt.imshow(patch)
		# 	#plt.show()

	except RuntimeError as e:
	  print(e)



