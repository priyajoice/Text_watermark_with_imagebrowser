from PIL import Image, ImageFont, ImageDraw
from matplotlib import font_manager
import glob
import os
from image_browser import SlideShowGUI

# changing the default text font for watermarking text
font = font_manager.FontProperties(family='Gabriola', weight='bold')
file_font = font_manager.findfont(font)


# Getting the text font size based on the image size
def find_font_size(text, font, txt_image, image_width):
    target_width_ratio = 0.5
    tested_font_size = 30
    tested_font = ImageFont.truetype(font, tested_font_size)

    edit_img = ImageDraw.Draw(txt_image)
    _, _, w_t, _ = edit_img.textbbox((0, 0), text, tested_font)

    # print(w_t)
    estimated_font_size = tested_font_size / (w_t / image_width) * target_width_ratio
    return round(estimated_font_size)


# Saving watermarked image to output folder
def save_image(output_image, path):
    filename = os.path.basename(path)
    if filename.split(".")[-1] != "png":
        output_image = output_image.convert('RGB')
        output_image.save("watermarked_images/watermark_" + filename)
    else:
        output_image.save("watermarked_images/watermark_" + filename)


# Watermarking the raw images from the input folder
def watermark_image(path):
    # Opening Image & Creating New Text Layer
    load = Image.open(path).convert("RGBA")
    txt = Image.new("RGBA", load.size, (255, 255, 255, 0))

    # Get size of image
    img_width, img_height = load.size
    # print(load.size)

    # Creating Text and text font size
    text = "www.darsha.com"
    text_font_size = find_font_size(text, file_font, txt, img_width)
    # print(text_font_size)

    # setting the font-family and text-font-size and Creating Draw Object
    text_font = ImageFont.truetype(file_font, text_font_size)
    edit_image = ImageDraw.Draw(txt)

    # Positioning Text
    _, _, w, h = edit_image.textbbox((0, 0), text, text_font)
    wm_position = img_width - w - img_width * 0.025, img_height - h - img_height * 0.025  # (330, 450)
    # print(wm_position)

    # Applying Text
    edit_image.text(wm_position, text=text, fill=(255, 255, 255, 80), font=text_font)
    # Combine the image with text watermark
    out_img = Image.alpha_composite(load, txt)
    return out_img


if __name__ == "__main__":
    # Getting all the list of images from the input folder
    image_path = glob.glob("images/*.*")
    print("Watermarking started !!!")

    # For each image from the input folder, watermark is applied
    wm_img = list(map(watermark_image, image_path))
    # Saving the watermarked image in output folder
    save_img = list(map(save_image, wm_img, image_path))

    print("Watermarking Completed !!!")

    # Getting the list of watermarked images from output folder
    watermarked_image_path = glob.glob("watermarked_images/*.*")

    # Display the watermarked images using Tkinter GUI
    img_browser = SlideShowGUI(watermarked_image_path)
