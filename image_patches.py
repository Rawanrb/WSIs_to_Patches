import tiles
import slide
import util
import math
import matplotlib.pyplot as plt
import multiprocessing
import openslide
import glob
import os
import matplotlib
matplotlib.use('TkAgg')

BASE_DIR = os.path.join(os.sep, "media","bialab","7c33ac31-d9d1-4f8d-aed4-ef4049a63dc2", "tialab_rawan","Datasets","CRAG")
SRC_TRAIN_DIR = os.path.join(BASE_DIR, "train")
SRC_TRAIN_Images = os.path.join(SRC_TRAIN_DIR, "Images")
SRC_TRAIN_Annotations = os.path.join(SRC_TRAIN_DIR, "Annotation")
SRC_TRAIN_EXT = "png"
TRAIN_PREFIX = "train_"
MASK_PREFIX = "train_"
SRC_MASK_EXT = "png"

PATCH_DIR = os.path.join(BASE_DIR, "patches")
PATCH_EXT = "png"

ROW_TILE_SIZE = 448
COL_TILE_SIZE = 448


def get_num_training_images():
	num_training_images = len(glob.glob1(SRC_TRAIN_Images, "*." + SRC_TRAIN_EXT))
	return num_training_images

def get_training_image_path(img_num):
	img_path = os.path.join(SRC_TRAIN_Images, TRAIN_PREFIX + str(img_num) + "." + SRC_TRAIN_EXT)
	return img_path

def get_mask_image_path(img_num):
	img_path = os.path.join(SRC_TRAIN_Annotations, MASK_PREFIX + str(img_num) + "." + SRC_MASK_EXT)
	return img_path

def get_patch_path(src_dir,score,count):

    dir = PATCH_DIR
    if not os.path.exists(dir):
        os.makedirs(dir)
    patch_path = os.path.join(dir, get_patch_image_filename(src_dir,score,count))
    return patch_path

def get_patch_image_filename(src_dir,score,count):
  ext = PATCH_EXT
  patch_filename = os.path.join(src_dir,str(score),str(count) + "." + ext)
  return patch_filename

def get_num_tiles(rows, cols, row_tile_size, col_tile_size,overlap_allowed):
	num_row_tiles = math.ceil(rows / math.floor(row_tile_size * overlap_allowed))
	num_col_tiles = math.ceil(cols / math.floor(col_tile_size * overlap_allowed))

	return num_row_tiles, num_col_tiles


def get_tile_indices_without_reflection(rows, cols, row_tile_size, col_tile_size,overlap_allowed = 0.5): 
 # in case I have small patch I can take the patch 
  """
  Obtain a list of tile coordinates (starting row, ending row, starting column, ending column, row number, column number).

  Args:
    rows: Number of rows.
    cols: Number of columns.
    row_tile_size: Number of pixels in a tile row.
    col_tile_size: Number of pixels in a tile column.

  Returns:
    List of tuples representing tile coordinates consisting of starting row, ending row,
    starting column, ending column, row number, column number.
  """
  indices = list()
  num_row_tiles, num_col_tiles = get_num_tiles(rows, cols, row_tile_size, col_tile_size,overlap_allowed)
  for r in range(0, num_row_tiles):
    start_r = math.ceil(r * row_tile_size * overlap_allowed)
    end_r = math.ceil((((r * overlap_allowed) + 1) * row_tile_size) if (r < num_row_tiles - 1) else rows)
    for c in range(0, num_col_tiles):
      start_c = math.ceil(c * col_tile_size * overlap_allowed)
      end_c = math.ceil((((c* overlap_allowed) + 1) * col_tile_size) if (c < num_col_tiles - 1) else cols)

      if((end_c-start_c) < col_tile_size): # in case we reach the end of the image without proper size
      	start_c = math.ceil(abs(start_c - (col_tile_size - (end_c-start_c))))
      	
      if((end_r-start_r) < row_tile_size): # in case we reach the end of the image without proper size
      	start_r = math.ceil(abs(start_r - (row_tile_size - (end_r-start_r))))

      if(end_r <= rows and end_c <= cols ):
      	indices.append((start_r, end_r, start_c, end_c))
  return indices



num_train_images = get_num_training_images()


count = 0

for img_num in range(1, num_train_images):
	img_path = get_training_image_path(img_num)
	np_img = slide.open_image_np(img_path)


	tile_indices = get_tile_indices_without_reflection(np_img.shape[0], np_img.shape[1], ROW_TILE_SIZE, COL_TILE_SIZE, 0.5)


	img_mask_path = get_mask_image_path(img_num)
	np_img_mask = slide.open_image_np(img_mask_path)

	for t in tile_indices:
		r_s, r_e, c_s, c_e= t

		np_tile = np_img[r_s:r_e, c_s:c_e]

		np_tile_mask = np_img_mask[r_s:r_e, c_s:c_e]

		score = tiles.unique_count_app(np_tile_mask) #do not use unique this is not acceptable

		if(score > 0):
			count += 1

			patch = util.np_to_pil(np_tile)

			patch_path = get_patch_path("train",score, count)

			dir = os.path.dirname(patch_path)
			if not os.path.exists(dir):
				os.makedirs(dir)
			patch.save(patch_path)

	
	#print(img_path)
