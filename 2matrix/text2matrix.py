from PIL import Image, ImageDraw, ImageFont

def make_unicode(inp):
    if type(inp) != type('1'):
        inp =  inp.decode('utf-8')
    return inp

def text2matrix(id, text, size, fon):
    unicode_text = make_unicode(text)
    font = ImageFont.truetype(fon, size, encoding="unic")
    text_width, text_height = font.getsize(unicode_text)
    canvas = Image.new('RGB', (text_width, text_height), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 0), unicode_text, 'black', font)
    canvas.save(r"2matrix\\" + str(id) + ".png", "PNG")
    # canvas.show()
    return None

text2matrix(13, "No 9", 20, "arial.ttf")