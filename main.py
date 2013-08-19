# -*- coding: utf-8 -*-

'''
Внимание, есть фамилия (Зад-на, у которой лишний пробел между фамилией и именем) !!

Файлы S21 находятся в отдельно папке PATH_S21_INPUT Далее ищется нужный файл по имени и копируется 
в текущую папку, где все Python программы. После заполнения этот файл копируется в
другую папку, выходную.

На входе - текстовый файл FILENAME - где результат работы программы ctocr.py. Там есть имена
и данные.

ToDo:
    - "year" еще не реализован;
    - 

Release History:
R0.1 2013-08-07 Initial Release. Works with Russian, INDEX chatched well
R0.2 2013-08-09 Fix bug for PIL library (PIL import was wrong)
R0.3 
R0.4

'''

###############################################################################
#import Image, ImageOps
import subprocess, sys, glob, os
import time
from time import sleep
import xte_type_data

RELEASE = 0.6


###############################################################################
###############################################################################
def search_s21(two_words):
    name1 = two_words[1].strip()
    name2 = two_words[2].strip()  

    res = glob.glob(PATH_S21_INPUT + '/*%s*%s' %( name1,".pdf"))
    if len(res) > 0:
        res = glob.glob(PATH_S21_INPUT + '/*%s*%s' %( name2,".pdf"))
#        print res[0]
        if len(res) > 0:
            return res
        else:
            return None

###############################################################################
if __name__ == '__main__':
    PATH_TEMP =     '/home/sskriblo/s21-ocr_work/temp'    
    PATH_WORK =     '/home/sskriblo/s21-ocr_work'   
    PATH_S21_INPUT =  '/home/sskriblo/s21-ocr_work/s21input'
    PATH_S21_OUTPUT =  '/home/sskriblo/s21-ocr_work/s21output'
    PDFXVIWER = '/home/sskriblo/s21-ocr_work/PDFX_Vwr_Port/PDFXCview.exe'
    
    if len(sys.argv) != 4:
        print "Usage: main.py FILENAME POSITION  YEAR"
        exit()
    filename = sys.argv[1]
    position = int(sys.argv[2])
    year = sys.argv[3]

    start_time = time.time()
    print start_time

    f = open(filename, 'r') 
    lines = f.readlines()
    data_flag = False
    for i in range(len(lines)):
        if data_flag == True:
            data = lines[i]
            data_flag = False
            xte_type_data.type_data(PATH_TEMP, PATH_WORK, short_name, position, data, year, PDFXVIWER)
            print "remove %s file" %(short_name)
            cmd = "mv '%s' %s" % (short_name, PATH_S21_OUTPUT)
            subprocess.call([cmd], shell=True)            
        if lines[i].count("NAME") > 0:
            # next line will be "data" !!
            name = lines[i]
            two_words = name.split(" ")
            if len(two_words) > 2:
                pass # ok

                full_name = two_words[2].strip() + " " + two_words[1].strip()  
                # Ищем имя файла, где бы было имя и фамилия
                res = search_s21(two_words)
                if res != None:
#                    print res[0]
                    # copy s21 to current dir
                    short_name = res[0][ res[0].rfind("/") +1 : ]
                    print "short_name", short_name
                    cmd = "cp '%s' %s" % (res[0], " .")
                    subprocess.call([cmd], shell=True)
                    data_flag = True
                else:
                    print "ERROR: file with name %s not found!!" %(full_name)
            else:
                print "ERROR: name contains one word only?"
            

       
    stop_time = time.time()
    print stop_time
    print "Total Time (seconds) = ", stop_time - start_time
    f.close()

        