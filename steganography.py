"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap
import numpy

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    red_array = red_channel.load()
    blue_channel = encoded_image.split()[1]
    blue_array = blue_channel.load()
    green_channel = encoded_image.split()[2]
    green_array = green_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("L", encoded_image.size)
    pixels = decoded_image.load()
    # print(pixels[(100,100)])
    flag = 0
    for i in range(x_size):
        for j in range(y_size):
            # print(bin(red_array[i,j]))
            #The +4s in this make sure that the binary representation have multiple digits
            #rather than being 0b0 or 0b1
            red_bin =  bin(red_array[i,j]+4)[-2:] 
            blue_bin = bin(blue_array[i,j]+4)[-2:] 
            green_bin = bin(green_array[i,j]+4)[-2:]
            print(red_bin+blue_bin+green_bin)
            binlum = red_bin+blue_bin + green_bin + "00"
            lum = int(binlum,base = 2)
            decoded_image.putpixel((i,j),lum)


    decoded_image.save("images/decoded_image.png")

def prep_encoding_image(encoding_image="images/kittens.jpg",image_size = (800,600)):
    """Prepares an image for encoding by making it the right size and turning
    it greyscale

    encoding_image:  The image you want encoded in the other image
    image_size:  Size of the resulting image.  Is a tupble (x_size,y_size)
    """
    enc_image = Image.open(encoding_image)
    modified_enc_image = enc_image.copy()
    enc_x = modified_enc_image.size[0]
    enc_y = modified_enc_image.size[1]
    main_x = image_size[0]
    main_y = image_size[1]
    
    x_scale = main_x/enc_x
    y_scale = main_y/enc_y
    
    scale_factor = 1
    
    # Finds the scale factor to multiply the image by to get it so that the
    # encoded image gets scaled to the correct size and fits entirely in
    # the main image
    if y_scale< x_scale:
        scale_factor = y_scale
    else:
        scale_factor = x_scale
    print(scale_factor)
    im_x = int(numpy.floor(enc_x*scale_factor))
    im_y = int(numpy.floor(enc_y*scale_factor))
    modified_enc_image = modified_enc_image.resize((im_x,im_y)).convert('L')
    #resize and greyscale
    modified_enc_image.save("images/modified_enc_image.png")
    return modified_enc_image

def split_bin(num_to_split):
    first_two = num_to_split//64
    second_two = (num_to_split%64)//16
    third_two = (num_to_split%16)//4
    return (first_two,second_two,third_two)

def encode_image(image_to_encode="images/kittens.jpg", template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    base_image = Image.open(template_image)
    #Split into multiple channels
    red_channel = base_image.split()[0]
    red_array = red_channel.load()
    blue_channel = base_image.split()[1]
    blue_array = blue_channel.load()
    green_channel = base_image.split()[2]
    green_array = green_channel.load()
    
    x_size = base_image.size[0]
    y_size = base_image.size[1]
    #setup new image
    new_image = Image.new("RGB", base_image.size)


    preped_image = prep_encoding_image(image_to_encode,base_image.size)
    #gets luminance values from image
    pix_chan = preped_image.split()[0] #
    pix = pix_chan.load()
    #gets size of image that needs to be modified
    x_size_changing = preped_image.size[0]
    y_size_changing = preped_image.size[1]
    
    for i in range(x_size):
        out_of_range = False
        if i>=x_size_changing:
            #if we're past where the encoding image stops:
            out_of_range = True
        for j in range(y_size):
            print(i,j)
            print(preped_image.size)
            if j>=y_size_changing:
                #if we're past where the encoding image stops:
                out_of_range = True
            
            #fill in back with black if out of range
            if out_of_range:
                luminance_split = (0,0,0)
            else:
                luminance = pix[i,j]
                luminance_split = split_bin(luminance)
            
            #set red value to two most significant digits, then green, then blue
            #mod4 it, subtract from self to get 2 least significant to 0
            red_val = red_array[i,j]
            red_array[i,j] = red_val - red_val%4  +luminance_split[0]
            blue_val = blue_array[i,j]
            blue_array[i,j] = blue_val - blue_val%4  +luminance_split[1]
            green_val = green_array[i,j]
            green_array[i,j] = green_val - green_val%4  +luminance_split[2]
            
            new_image.putpixel((i,j),(red_array[i,j],blue_array[i,j],green_array[i,j]))
    new_image.save("images/new_image.png")

if __name__ == '__main__':
    # print("Decoding the image...")
    # decode_image()
    decode_image("images/new_image.png")

    print("Encoding the image...")
    # encode_image("Happy Birthday, Celina!  I love you so much <3")
    # prep_encoding_image()
    # split_bin(200)
    # encode_image()