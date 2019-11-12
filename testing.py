slide_filepath = slide.get_training_slide_path(slide_num)
wsi_slide = slide.open_slide(slide_filepath)
slide.SCALE_FACTOR = 2
x,y = (10000,20000)
w,h = (448,448)
level = wsi_slide.get_best_level_for_downsample(slide.SCALE_FACTOR)

tile_region = wsi_slide.read_region((x, y), 0, (w, h))
pil_img = tile_region.convert("RGB")
np_tile = util.pil_to_np_rgb(pil_img)
patch = util.np_to_pil(np_tile)

plt.imshow(patch)
plt.show()

w = math.floor(w / slide.SCALE_FACTOR)  # use round?
h = math.floor(h / slide.SCALE_FACTOR)  # use round?
		
		#x, y = slide.large_to_small_mapping ((x, y), (o_w, o_h))
#x = math.floor(x / slide.SCALE_FACTOR)
#y = math.floor(y / slide.SCALE_FACTOR)


tile_region = wsi_slide.read_region((x, y), level, (w, h))
pil_img = tile_region.convert("RGB")
np_tile = util.pil_to_np_rgb(pil_img)
patch = util.np_to_pil(np_tile)

plt.imshow(patch)
plt.show()


# #Step 5

# # slide_num = 21

# slide.SCALE_FACTOR = 32
# row_tile_size = 224
# col_tile_size = 224



# slide_filepath = slide.get_training_slide_path(slide_num)
# wsi_slide = slide.open_slide(slide_filepath)
# level = 32
# score = 1
# count = 0

# slide_dimensions = wsi_slide.level_dimensions[5]#the  place of the level  5 = 32
# print(slide_dimensions)
# h = slide_dimensions[0]
# w = slide_dimensions[1]
# #num_row_tiles, num_col_tiles = tiles.get_num_tiles(h, w, row_tile_size, col_tile_size)
# #tile_indices = tiles.get_tile_indices(h, w, row_tile_size, col_tile_size)


# xlsx_name = "patches_21.xlsx"
# sheet_name ="Sheet1"
# import openpyxl
# wb = openpyxl.load_workbook(xlsx_name)
# sheet = wb[sheet_name]



# patch = wsi_slide.read_region((497, 1148), 32, (row_tile_size,col_tile_size))

# patch = patch.convert("RGB")
# patch_path = slide.get_patch_path(slide_num,score,count)

# plt.imshow(patch)
# plt.show()

# for row in sheet.iter_rows(min_row=2, values_only=True):

# 	count +=1
# 	pixel_row = row[11]
# 	pixel_col = row[12]


# 	patch = wsi_slide.read_region((pixel_row, pixel_col), level, (row_tile_size,col_tile_size))

# 	patch = patch.convert("RGB")
# 	patch_path = slide.get_patch_path(slide_num,score,count)
# 	patch.save(patch_path)

#Step 3 #if you are using dynamic_tile no need for this step as the filtering will be on the fly
#apply filter to get apply masks later and get patches done for once for wsi and many for tifs
# import tensorflow as tf
# with tf.device('/device:GPU:0'):
# # 	filters.apply_filters_to_image(slide_num)
# 	filters.singleprocess_apply_filters_to_images(save=True, display=False, html=True, image_num_list=None)



# from PIL import Image

# png = Image.read(patch)
# png.load() # required for png.split()

# background = Image.new("RGB", png.size, (255, 255, 255))
# background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

# background.save('foo.jpg', 'JPEG', quality=80)

# plt.imshow(background)
# plt.show()

 # xlsx_name = "SlideInfo.xlsx"
 # sheet_name ="Sheet1"
 # import openpyxl
 # wb = openpyxl.load_workbook(xlsx_name)
 # sheet = wb.get_sheet_by_name(sheet_name)
#Step 3 #if you are using dynamic_tile no need for this step as the filtering will be on the fly
#apply filter to get apply masks later and get patches done for once for wsi and many for tifs
# import tensorflow as tf
# with tf.device('/device:GPU:0'):
# # 	filters.apply_filters_to_image(slide_num)
# 	filters.singleprocess_apply_filters_to_images(save=True, display=False, html=True, image_num_list=None)
