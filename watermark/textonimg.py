from PIL import Image, ImageDraw, ImageFont

image = Image.open('s.jpg')
width, height = image.size

draw = ImageDraw.Draw(image)
text = "watermark"

font = ImageFont.truetype('arial.ttf', 72)
textwidth, textheight = draw.textsize(text, font)

# calculate the x,y coordinates of the text
margin = 5
x = width - textwidth - margin
y = height - textheight - margin

# draw watermark in the bottom right corner
draw.text((x, y), text, font=font)

image.save('s.jpg')
