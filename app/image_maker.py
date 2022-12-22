import glob
import random
import os
from PIL import Image
import glob
import application

GRID_SIZE=300
ROW=2
COLUMN=2
PADDING=100
PADDING_CELLS=5
PADDING_COLOR="white"
PADDING_CELL_COLOR="white"

IMG_PATH=".\\static\\ANIMEIMAGES\\*"
SAVE_PATH=".\\static\\image.jpg"
DELETE_IMAGES=False




def init():
  global coord_list
  global type
  coord_list = []
  type = ""
  global height
  height = int(GRID_SIZE + (GRID_SIZE / 2))
  #Get image list
  global img_list
  img_list=glob.glob(IMG_PATH)
  global images
  images=[x for x in img_list]
  print(img_list)

  #Final image
  global new_im
  new_im = Image.new('RGB', (COLUMN*GRID_SIZE, ROW*height))

def make_type():
  # 2 resize types
  num = random.randint(0, 1)
  if num == 1:
    return "big"
  else:
    return "small"
def append_coord(i, j, type):
  coord_list.append((i, j))
  if type == "big":
    coord_list.append((i, j + 1))
    coord_list.append((i + 1, j))
    coord_list.append((i + 1, j + 1))
def check_coord(i, j, type):
  # Check taken coord
  if type == "big":
    if (i, j) not in coord_list and (i + 1, j + 1) not in coord_list and (i + 1, j) not in coord_list and (
            i, j + 1) not in coord_list and j != COLUMN - 1 and i != ROW - 1:

      return True
    else:
      return False
  elif type == "small":
    if (i, j) not in coord_list:
      return True
    else:
      return False

def add_padding(pil_img, PADDING, color):
  width, height = pil_img.size
  new_width = width + PADDING + PADDING
  new_height = height + PADDING + PADDING
  result = Image.new(pil_img.mode, (new_width, new_height), color)
  result.paste(pil_img, (PADDING, PADDING))
  return result
def delete_images():

  print("Images deleted")
  files = glob.glob(IMG_PATH)
  print(files)
  for f in files:
    os.remove(f)
def main():
  #Makes grid
  y_offset = 0
  i=0
  while i < ROW:
    j = 0
    x_offset = 0
    while j < COLUMN:
      #Big or small
      type=make_type()

      # Check coord
      if not check_coord(i, j, type):
        if type == "big":
          continue
        if type == "small":
          j+=1

          x_offset += GRID_SIZE
          continue
      if len(images) == 0:
        print("not enough images")
        break
      # Takes images
      random.shuffle(images)
      image=images[-1]
      im=Image.open(image)
      padded_image = add_padding(im, PADDING_CELLS, PADDING_CELL_COLOR)
      print(im)

      if type == "big":
        new_image=padded_image.resize((int(GRID_SIZE * 2), int(height * 2)))
      elif type == "small":
        new_image=padded_image.resize((int(GRID_SIZE), int(height)))

      print(new_image.size)
      #Paste image
      print(coord_list)
      print(x_offset,y_offset)
      new_im.paste(new_image, (x_offset,y_offset))
      append_coord(i,j,type)
      images.remove(image)
      if type == "big":
        j+=2
        x_offset += GRID_SIZE*2

      else:
        j+=1
        x_offset += GRID_SIZE

    i+=1
    y_offset+=height

  #Add general padding
  add_padding(new_im, PADDING,PADDING_COLOR).save(SAVE_PATH)

  #Delete images
  if DELETE_IMAGES:
    delete_images()

if __name__=="__main__":
  init()
  main()

