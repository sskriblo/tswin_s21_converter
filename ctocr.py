'''
Created on Aug 5, 2013
source code from:
http://craiget.com/extracting-table-data-from-pdfs-with-ocr/
my page with info:
https://docs.google.com/document/d/10UH7dH13te816lPPZARTfG3oK5eXq__W78q5viXgjrU/edit?usp=sharing

use PILLOW instead of PIL:
sudo pip uninstall PIL
sudo pip install pillow -U

tesseract install procedure:
sudo apt-get install tesseract-ocr
Russian language:
sudo apt-get install tesseract-ocr-rus

ToDo:
1. find two tables at one page and split to two pages
2. find index at field - done

Release History:
R0.1 2013-08-07 Initial Release. Works with Russian, INDEX chatched well
R0.2 2013-08-09 Fix bug for PIL library (PIL import was wrong)
R0.3 
R0.4

'''
from PIL import Image, ImageOps

###############################################################################
#import Image, ImageOps
import subprocess, sys, os, glob
import time
from time import sleep

RELEASE = 0.4

# minimum run of adjacent pixels to call something a line
H_THRESH = 300
V_THRESH = 300

     
def get_hlines(pix, w, h):
    """Get start/end pixels of lines containing horizontal runs of at least THRESH black pix"""
    hlines = []
    for y in range(h):
        x1, x2 = (None, None)
        black = 0
        run = 0
        for x in range(w):
####            if pix[x,y] == (0,0,0):
            if pix[x,y] == (0,255):
                black = black + 1
                if not x1: x1 = x
                x2 = x
            else:
                if black > run:
                    run = black
                black = 0
        if run > H_THRESH:
            hlines.append((x1,y,x2,y))
    return hlines
 
def get_vlines(pix, w, h):
    """Get start/end pixels of lines containing vertical runs of at least THRESH black pix"""
    vlines = []
    for x in range(w):
        y1, y2 = (None,None)
        black = 0
        run = 0
        for y in range(h):
###            if pix[x,y] == (0,0,0):
            if pix[x,y] == (0,255):
                black = black + 1
                if not y1: y1 = y
                y2 = y
            else:
                if black > run:
                    run = black
                black = 0
        if run > V_THRESH:
            vlines.append((x,y1,x,y2))
    return vlines
 
def get_cols(vlines):
    """Get top-left and bottom-right coordinates for each column from a list of vertical lines"""
    cols = []
    for i in range(1, len(vlines)):
        if vlines[i][0] - vlines[i-1][0] > 1:
            cols.append((vlines[i-1][0],vlines[i-1][1],vlines[i][2],vlines[i][3]))
    return cols
 
def get_rows(hlines):
    """Get top-left and bottom-right coordinates for each row from a list of vertical lines"""
    rows = []
    for i in range(1, len(hlines)):
        if hlines[i][1] - hlines[i-1][3] > 1:
            rows.append((hlines[i-1][0],hlines[i-1][1],hlines[i][2],hlines[i][3]))
    return rows         
 
def get_cells(rows, cols):
    """Get top-left and bottom-right coordinates for each cell usings row and column coordinates"""
    cells = {}
    for i, row in enumerate(rows):
        cells.setdefault(i, {})
        for j, col in enumerate(cols):
            x1 = col[0]
            y1 = row[1]
            x2 = col[2]
            y2 = row[3]
            cells[i][j] = (x1,y1,x2,y2)
    return cells
 
def ocr_cell(im, cells, x, y):
    """Return OCRed text from this cell"""
    fbase = PATH_TEMP + "/%d-%d" % (x, y)
    ftif = "%s.tif" % fbase
    ftxt = "%s.txt" % fbase
    cmd = "tesseract -l rus -psm 7 %s %s" % (ftif, fbase)
    # extract cell from whole image, grayscale (1-color channel), monochrome
    region = im.crop(cells[x][y])
    region = ImageOps.grayscale(region)
    region = region.point(lambda p: p > 200 and 255)
    # determine background color (most used color)
    histo = region.histogram()
    if histo[0] > histo[255]: bgcolor = 0
    else: bgcolor = 255
    # trim borders by finding top-left and bottom-right bg pixels
    pix = region.load()
    x1,y1 = 0,0
    x2,y2 = region.size
    x2,y2 = x2-1,y2-1
    while pix[x1,y1] != bgcolor:
        x1 += 1
        y1 += 1
    while pix[x2,y2] != bgcolor:
        x2 -= 1
        y2 -= 1
    # save as TIFF and extract text with Tesseract OCR
    trimmed = region.crop((x1,y1,x2,y2))
    trimmed.save(ftif, "TIFF")
    subprocess.call([cmd], shell=True, stderr=subprocess.PIPE)
    lines = [l.strip() for l in open(ftxt).readlines()]
    if len(lines) == 0:
        return "0"
    else:
        return lines[0]

###############################################################################
# ported from get_cells() - only for one field - Phone. This fiel contains INDEX
def get_index(im, cells, field="NAME"):
    try:  # if bottom page is empty, neet escape !!
        square_0 = cells[0][0]
    except KeyError:
        return "EMPTY"
#    print "cell 0 before shift: ", square_0
    if field == "NAME":
        phone_field = (square_0[0] - 110, square_0[1] - 450, square_0[2] + 650, square_0[3] - 420) #(x1,y1,x2,y2)
    elif field == "INDEX":
        phone_field = (square_0[0] + 110, square_0[1] - 220, square_0[2] + 50, square_0[3] - 220)
    else:
        print "Wrong option for get_index() , STOP !!"
        sys.exit(1)
#    print "after shift to phone field: ", phone_field
    
    """Return OCRed text from this cell"""
    fbase = PATH_TEMP + "/index_field"
    ftif = "%s.tif" % fbase
    ftxt = "%s.txt" % fbase
    cmd = "tesseract -l rus -psm 7 %s %s" % (ftif, fbase)
    # extract cell from whole image, grayscale (1-color channel), monochrome
    region = im.crop(phone_field)
    region = ImageOps.grayscale(region)
    region = region.point(lambda p: p > 200 and 255)
    # determine background color (most used color)
    histo = region.histogram()
    if histo[0] > histo[255]: bgcolor = 0
    else: bgcolor = 255
    # trim borders by finding top-left and bottom-right bg pixels
    pix = region.load()
    x1,y1 = 0,0
    x2,y2 = region.size
    x2,y2 = x2-1,y2-1
    while pix[x1,y1] != bgcolor:
        x1 += 1
        y1 += 1
    while pix[x2,y2] != bgcolor:
        x2 -= 1
        y2 -= 1
    # save as TIFF and extract text with Tesseract OCR
    trimmed = region.crop((x1,y1,x2,y2))
    trimmed.save(ftif, "TIFF")
    subprocess.call([cmd], shell=True, stderr=subprocess.PIPE)
    lines = [l.strip() for l in open(ftxt).readlines()]
    if len(lines) == 0:
        return "EMPTY"
    else:
        return lines[0]
###############################################################################
###############################################################################
def cut_half_page(im, page):
    width, height = im.size
    box_top = (0, 0, width, height/2) # (left, upper, right, lower)
    box_bottom = (0, height/2, width, height) # (left, upper, right, lower)
    if page == 0:
        region_top = im.crop(box_top)
        region_top.save("halph_page_file.png", "PNG" )
    else:
        region_bottom = im.crop(box_bottom)
        region_bottom.save("halph_page_file.png", "PNG" )
    im = Image.open("halph_page_file.png")
    return im

###############################################################################

def get_image_data(filename, page):
    """Extract textual data[rows][cols] from spreadsheet-like image file"""  
    im = Image.open(filename)
#    im = Image.open(open(filename, 'rb'))

    # code for divided page not ready yet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # looking for top text line Y coordinate.
    h_im = cut_half_page(im, page)

    pix = h_im.load()
    width, height = h_im.size

    
    hlines = get_hlines(pix, width, height)
    sys.stderr.write("%s: hlines: %d\n" % (filename, len(hlines)))
    vlines = get_vlines(pix, width, height)
    sys.stderr.write("%s: vlines: %d\n" % (filename, len(vlines)))
    rows = get_rows(hlines)
    sys.stderr.write("%s: rows: %d\n" % (filename, len(rows)))
    cols = get_cols(vlines)
    sys.stderr.write("%s: cols: %d\n" % (filename, len(cols)))
    cells = get_cells(rows, cols)

    # add my code - looking for INDEX at Phone Field
    index = get_index(h_im, cells, "NAME")
        
    data = []
    for row in range(len(rows)):
        data.append([ocr_cell(h_im,cells, row, col) for col in range(len(cols))])
    return data, "NAME " + index
 
def split_pdf(filename):
    """Split PDF into PNG pages, return filename"""    
    prefix = filename[:-4]
    cmd_1 = "convert -density 600 %s"   % (filename)
    cmd_2 = "/%s-%%d.png" % (prefix)
    cmd = cmd_1 + " " + PATH_TEMP + cmd_2
    subprocess.call([cmd], shell=True)
    return [f for f in glob.glob(os.path.join(PATH_TEMP, '%s*' % prefix))]
 
def extract_pdf(filename,f):
    """Extract table data from pdf"""
    pngfiles = split_pdf(filename)
    sys.stderr.write("Pages: %d\n" % len(pngfiles))
    # extract table data from each page
    data = []
    for pngfile in pngfiles:
        pngdata, index = get_image_data(pngfile, page=0)
        f.write("\n" + index + "\n")
        print (index + "\n")
        first_line_flag = True
        for d in pngdata:
            data.append(d)
            if first_line_flag == True: # first line should be removed
                first_line_flag = False
            else:
                for i in range(len(d)):
                    f.write(d[i] + "\t")
        # remove temp files for this page
        cmd = "rm %s"  %(PATH_TEMP + '/*.tif')
        subprocess.call([cmd], shell=True)        
        cmd = "rm %s"  %(PATH_TEMP + '/*.txt')
        subprocess.call([cmd], shell=True)  

        pngdata, index = get_image_data(pngfile, page=1)
        f.write("\n" + index + "\n")
        print (index + "\n")
        first_line_flag = True
        for d in pngdata:
            data.append(d)
            if first_line_flag == True: # first line should be removed
                first_line_flag = False
            else:
                for i in range(len(d)):
                    f.write(d[i] + "\t")
        # remove temp files for this page
        cmd = "rm %s"  %(PATH_TEMP + '/*.tif')
        subprocess.call([cmd], shell=True)        
        cmd = "rm %s"  %(PATH_TEMP + '/*.txt')
        subprocess.call([cmd], shell=True)     
        
    # remove split pages
    cmd = "rm %s"  %(PATH_TEMP + '/*')
    subprocess.call([cmd], shell=True)        

    return data

    
###############################################################################
###############################################################################
if __name__ == '__main__':
    PATH_TEMP =     '/home/sskriblo/s21-ocr_work/temp'
    PATH_WORK =     '/home/sskriblo/s21-ocr_work'    
    if len(sys.argv) != 2:
        print "Usage: ctocr.py FILENAME"
        exit()
    start_time = time.time()
    print start_time

    f = open(PATH_WORK + '/s21-ocr.txt', 'w')

    # split target pdf into pages
    filename = sys.argv[1]
    data = extract_pdf(filename,f)
#    s21_report(data)
    for row in data:
        print "\t".join(row)       
       
    stop_time = time.time()
    print stop_time
    print "Total Time (seconds) = ", stop_time - start_time
    f.close()

        