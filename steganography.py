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

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    # print(pixels[(100,100)])
    flag = 0
    for i in range(x_size):
        for j in range(y_size):
            # print(bin(red_array[i,j]))
            if bin(red_array[i,j])[-1] == "1":
                pixels[i,j] = 255
                decoded_image.putpixel((i,j),(255,255,255))
                flag = 1
            else:
                pixels[i,j] = 0
                decoded_image.putpixel((i,j),(0,0,0))
    # decoded_image2 = Image.fromarray(pixels)
    # print(flag)
    decoded_image.save("images/decoded_image.png")
    # decoded_image2.save("images/decoded_image2.png")

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    image_text.save("test3.png")
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    base_image = Image.open(template_image)
    #Split into multiple channel
    red_channel = base_image.split()[0]
    # print(red_channel[1,1])
    red_array = red_channel.load()
    blue_channel = base_image.split()[1]
    blue_array = blue_channel.load()
    green_channel = base_image.split()[2]
    green_array = green_channel.load()
    
    new_image = Image.new("RGB", base_image.size)
    
    x_size = base_image.size[0]
    y_size = base_image.size[1]

    flag = 0
    text_image = write_text(text_to_encode,base_image.size)
    pix_chan_1 = text_image.split()[0]
    pix = pix_chan_1.load()
    
    for i in range(x_size):
        for j in range(y_size):
            # print(bin(red_array[i,j]))
            if pix[i,j] == 0: #if it's BLACK
                #mod2 it, subtract from self to get least significant to 0
                red_val = red_array[i,j]
                red_array[i,j] = red_val - red_val%2
            else: # it's probably white
            #bitwise or red channel and 1 - turns least significant digit to 1
                red_array[i,j] = red_array[i,j]|1
                flag = 1
                
            new_image.putpixel((i,j),(red_array[i,j],blue_array[i,j],green_array[i,j]))
    
    print(flag)
    new_image.save("images/new_image.png")

if __name__ == '__main__':
    print("Decoding the image...")
    # decode_image()
    decode_image("images/new_image.png")

    print("Encoding the image...")
    encode_image("Happy Birthday, Celina!")
