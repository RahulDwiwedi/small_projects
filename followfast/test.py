from PIL import Image,ImageEnhance
import pytesseract



im= Image.open("cropped.png",'r')
im = im.convert('RGB')
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(3)
# im = im.convert('1')
print (im)
im.show()
# im.save('temp2.jpg')

#use tesseract library to extract text from
text = pytesseract.image_to_string(im,config='-psm 6')

print ("Text:"+text)