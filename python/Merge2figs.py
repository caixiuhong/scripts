from PIL import Image
from PIL import ImageDraw,ImageFont
import sys,os
def Merge2Figs(fig1, fig2, newfig):
    '''
    fig1: file of old figure 1
    fig2: file of old figure 2
    newfig: file of new merged figure
    '''

    images = [Image.open(x) for x in [fig1, fig2]]
    labels=['A','B']
    labels_pos=[0, 200]
    fontsize = 160
    font = ImageFont.truetype("arial.ttf", fontsize)

    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))
    draw= ImageDraw.Draw(new_im)

    x_offset = 0
    for i, im in enumerate(images):
        #print(x_offset)
        new_im.paste(im, (x_offset, 0))
        draw.text((x_offset+labels_pos[i], 50),  # Coordinates
                  labels[i] ,  # Text
                  (0, 0, 0),
                  font=font)
        x_offset += im.size[0]


    new_im.save(newfig, quality =300)

    return



if __name__=='__main__':
    if len(sys.argv) < 4:
        print("./ms_agg.py sheet_name")
        sys.exit()
    else:
        Merge2Figs(sys.argv[1], sys.argv[2], sys.argv[3])