from PIL import Image


def watermark(image, mask, name):
    image = Image.open(image).convert("RGBA")
    mask = Image.open(mask).convert("RGBA")

    bg_w, bg_h = image.size
    img_w, img_h = mask.size

    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

    image.paste(mask, offset, mask)
    image.save(name + ".png", format="png")


for i in range(1, 6):
    image = "s.jpg"
    mask = "bg" + str(i) + ".png"
    name = "test" + str(i)
    watermark(image, mask, name)
