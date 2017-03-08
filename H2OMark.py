#Import Libraries
from __future__ import print_function
import os, sys
import PIL
from PIL import Image, ExifTags

#Check Folder Existance and Create it
if not os.path.exists('Output'):
    os.makedirs('Output')

#success counter
success = 0

#files counter
files_n = 1
#Check for all files on the folder for processing
for filename in os.listdir('Images'):
    print(" ")
    print(str(files_n) + " - Processing file: " + filename + "...")
    #Image
    img = Image.open('Images/' + filename)

    #Check for EXIFTags --> Camera Information --> Orientation of Camera
    for orientation in ExifTags.TAGS.keys() :
        if ExifTags.TAGS[orientation]=='Orientation' : break
    exif=dict(img._getexif().items())

    #Check for EXIFTags --> Camera Information --> Orientation of Camera
    if   exif[orientation] == 3 :
        img=img.rotate(180, expand=True)
    elif exif[orientation] == 6 :
        img=img.rotate(270, expand=True)
    elif exif[orientation] == 8 :
        img=img.rotate(90, expand=True)

    #Image dimensions
    img_width = img.size[0]
    img_height = img.size[1]

    #Vertical or Horizontal?
    if img_width >= img_height:
        #Watermark horizontal
        watermark = Image.open('Fluid/Watermark.png')
        #Banner horizontal
        banner = Image.open('Fluid/Banner.png')
    elif img_width < img_height:
        #Watermark vertical
        watermark = Image.open('Fluid/Watermark_Vertical.png')
        #Banner vertical
        banner = Image.open('Fluid/Banner_Vertical.png')
        #Adjusting Vertical Banner
        basewidth = 3672
        wpercent = (basewidth/float(banner.size[0]))
        hsize = int(float(banner.size[1])*float(wpercent))
        banner = banner.resize((basewidth,hsize), PIL.Image.ANTIALIAS)

    #Banner dimensions
    ban_width = banner.size[0]
    ban_height = banner.size[1]

    #Watermark dimensions
    water_width = watermark.size[0]
    water_height = watermark.size[1]

    #Pasting Watermark into Image
    box_wm = (0, 0, water_width, water_height)
    img.paste(watermark, box_wm, mask = watermark)

    #Pasting Banner into Image
    box_ban = (0,img_height - ban_height, ban_width, img_height)
    img.paste(banner, box_ban, mask = banner)

    #Generate Output file
    output_file = 'Output/' + filename.split('.')[0] + '_H2OMarked.png'
    img.save(output_file, "PNG")
    #Count successes and
    success += 1
    print(filename + " H2Omarked sucessfully!")
    files_n += 1
print("----------------------------------------------")
print(" ")
print(str(success) + " of " + str(len(os.listdir('Images'))) + " images H2Omarked sucessfully!")
