import gc

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

# slides = [1,2,8,10,14]
slide_num = 1
count = 0
# checkpoint_dir = "/media/bialab/7c33ac31-d9d1-4f8d-aed4-ef4049a63dc2/tialab_rawan/Datasets/Checkpoints/TNBC_Dataset/ResNet50/3/"
checkpoint_name = "model_TNBC_Dataset_ResNet50_3_epoch_20.hdf5"
# model_path = os.path.join(checkpoint_dir, checkpoint_name)
model_path = checkpoint_name

# this scale factor is for the pre-processing of mask and wsi
slide.SCALE_FACTOR = 32

#how many patches per batch to feed to the prediction algorithm
batch_size = 64

# this number will be divided by the scale factor according to the required level
tiles.ROW_TILE_SIZE = 224
tiles.COL_TILE_SIZE = 224
slide.SRC_TRAIN_DIR = os.path.join(slide.BASE_DIR, "5_pilot_wsi")

slide.MASK_DIR = os.path.join(slide.BASE_DIR, "Annotations", "pngs", "Tumour")
slide.FILTER_DIR = os.path.join(slide.BASE_DIR,"5_masks")

# step 1
# save the info of wsi done for once
# slide.xlsx_name = os.path.join(slide.BASE_DIR,'Slide_Patch_Info.xlsx')
# slide.sheet_name = 'Sheet1'
# slide.slide_info(display_all_properties=True)

# step 2
# get the image from wsi to apply filter
# import tensorflow as tf
# with tf.device('/device:GPU:0'):
# slide.training_slide_to_image(slide_num) #delete the filtered imag
# slide.singleprocess_training_slides_to_images() # for all wsi images at once

# no need for this one
#import filters
#slide.training_slide_to_image(1)
#import filters
#filters.apply_filters_to_image(1)
#tiles.summary_and_tiles(1, display=True, save_summary=True, save_data=False, save_top_tiles=True)


# # Step 3

import tensorflow as tf
import tensorflow.keras.models as tf_keras
import numpy as np
#

with tf.device('/device:GPU:0'):
    try:
        # to save the info of tiles
        slide_filepath = slide.get_training_slide_path(slide_num)
        wsi_slide = slide.open_slide(slide_filepath)
        scale_up = False

        upsampled_patches = []


        tile_summary = tiles.dynamic_tiles(slide_num)

        #tiles.NUM_TOP_TILES = tile_summary.high + tile_summary.medium + tile_summary.low  # to change how many tiles we want to access default value is 100 in tiles file
        tiles.NUM_TOP_TILES = 10000
        top_tiles = tile_summary.top_tiles()
        top_tiles = sorted(top_tiles, key=lambda t: t.tissue_percentage, reverse=True)
        img_path = slide.get_filter_image_result(slide_num)
        np_img = slide.open_image_np(img_path)
        model = tf_keras.load_model(model_path)

        for t in top_tiles:
            count += 1
            if scale_up:  # in case you want top tiles from different level
                slide.SCALE_FACTOR = 2
                level = wsi_slide.get_best_level_for_downsample(slide.SCALE_FACTOR)

                x, y = t.o_c_s, t.o_r_s
                w, h = t.o_c_e - t.o_c_s, t.o_r_e - t.o_r_s

                w = math.floor(w / slide.SCALE_FACTOR)
                h = math.floor(h / slide.SCALE_FACTOR)

                tile_region = wsi_slide.read_region((x, y), level, (w, h))  # read the required region
                pil_img = tile_region.convert("RGB")  # convert from RGBA to RGB
                np_tile = util.pil_to_np_rgb(pil_img)

                patch_path = slide.get_patch_path(t, count, slide.SCALE_FACTOR, w, h)

            else:  # in case you want top tiles from level 0
                np_tile = t.get_np_tile()
                patch = util.np_to_pil(np_tile)
                patch = np.array(patch.getdata(),np.uint8).reshape(patch.size[1], patch.size[0], 3)/255
                upsampled_patches.append(patch)

            if count%batch_size == 0:
                batch = np.array(upsampled_patches)
                from util import Time
                t = Time()
                probs = model.predict(batch)
                print("%-20s | Time: %-14s  Name: %s", str(t.elapsed()), str(count))
                i = 0
                max_indices = np.argmax(probs, axis=1) #to get the index of max value to know the class

                for t in top_tiles[slice(count-batch_size-1,count-1)]:
                    t.prob = max(probs[i]) * 100
                    if max_indices[i]==0:
                        t.tissue_percentage = 100
                    elif max_indices[i]==1:
                        t.tissue_percentage = 70
                    elif max_indices[i]==2:
                        t.tissue_percentage = 0

                    i += 1

                upsampled_patches = []  # to clear the list

            for t in top_tiles[slice(count - 1,tiles.NUM_TOP_TILES)]:
                t.tissue_percentage = 0



        #batch = np.array(upsampled_patches)
        #model = tf_keras.load_model(model_path)
        #probs = model.predict(batch)

        img_path = slide.get_filter_image_result(slide_num)
        np_img = slide.open_image_np(img_path)

        tiles.generate_tile_summaries(tile_summary, np_img, save_summary=True)

    # dir = os.path.dirname(patch_path)
    # if not os.path.exists(dir):
    #     os.makedirs(dir)

    # patch.save(patch_path)
    # patch = plt.imread(patch_path)

    except RuntimeError as e:
        print(e)



