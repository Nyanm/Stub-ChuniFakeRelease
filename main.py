import base64
from os import path, remove
import sys
from PIL import Image, ImageDraw, ImageFont
import time
from traceback import format_exc
import __bg

"""
Using PIL coordinate system (x, y)
"""
jk_pos, jk_size = (735, 319), 450
color_white = (245, 245, 245)
font_path = 'C:/Windows/Fonts/msyhbd.ttc'

test_mode = 0

if test_mode:
    local_dir = path.dirname(path.abspath(__file__)).replace('\\', '/')
else:
    local_dir = path.dirname(path.abspath(sys.executable)).replace('\\', '/')

if __name__ == '__main__':

    try:
        bg_str = __bg.__bg
        bg_data = base64.b64decode(bg_str)
        temp = open(local_dir + '/temp.png', 'wb')
        temp.write(bg_data)
        temp.close()

        bg = Image.open(local_dir + '/temp.png')
        bg_x = bg.width
        try:
            jk_path = sys.argv[1].replace('\\', '/')

        except IndexError:
            input('Drag the jacket image to this exe file directly to generate fake release.\n'
                  'The file name of the jacket should be like {song name}@{author name}.png(jpg)\n'
                  'Example: 春告胡蝶@BlackY feat. Risa Yuzuki.png \n'
                  'Close this window and have a try.\n')
            sys.exit(1)

        jk_name = jk_path.split('/')[-1]
        jk_name = path.splitext(jk_name)[-2]
        name, artist = '', ''
        for index in range(len(jk_name)):
            if jk_name[index] == '@':
                artist = jk_name[index + 1:]
                break
            name += jk_name[index]

        jk = Image.open(jk_path)
        jk_x, jk_y = jk.size
        if jk_x > jk_y:
            jk = jk.crop(((jk_x - jk_y) // 2, 0, (jk_x + jk_y) // 2), jk_y)
        elif jk_y > jk_x:
            jk = jk.crop((0, (jk_y - jk_x) // 2, jk_x, (jk_y + jk_x) // 2))
        if jk_x != 450:
            jk = jk.resize((jk_size, jk_size))
        bg.paste(jk, box=jk_pos)

        pen = ImageDraw.Draw(bg)
        font_name = ImageFont.truetype(font_path, 34, encoding='utf-8')
        font_art = ImageFont.truetype(font_path, 25, encoding='utf-8')


        def draw_center(text, pos_y, __font):
            offset = __font.getsize(text)[0] // 2
            pen.text((bg_x // 2 - offset, pos_y), text, color_white, font=__font)


        draw_center(name, 788, font_name)
        draw_center(artist, 865, font_art)

        bg.save(local_dir + '/FakeRelease_%s.png' % jk_name)
        input('Plot successfully, close this window to continue.')
        remove(local_dir + '/temp.png')
        time.sleep(0.1)

    except Exception:
        input(format_exc())

# pyinstaller -i bard.ico -F main.py
