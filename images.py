from PIL import Image


def show_color_rgb(rgb: tuple):
    image = Image.new("RGB", [64, 64], rgb)
    image.save("rgb.jpeg", "JPEG")
    return "rgb.jpeg"
