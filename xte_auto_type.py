# -*- coding: utf-8 -*-
"""
Программа для набора текста в карточке S-21.

Утилиты:
xdotool getmouselocation - определяет положение мышки
xte 'mousemove 472 230' 'mouseclick 1' - позиционирует на имя возвещателя в верхней половине
xte 'mousemove 469 628' 'mouseclick 1' - позиционирует на имя возвещателя в нижней половине
sleep 3 && xte 'key 6' 'key Tab' 'key 7' 'key Tab' 'key 8' - набирает цифры в клетках из bash

Алгоритм и аргументы:
    - workingdir - рабочая директория, полный путь к ней;
    - name - ФИО - для создания файла и печати ФИО в карточках;
    - position=[0,1,2,3] - номер карточки в файле. Отсчет идет с нуля, слева 
    направо, сверху вниз. Служит для позиционирования при вводе данных;
    - data - TXT файл с именем ФИО и с данными из OCR модуля. Формат обозначим позднее.
    Данные записываются в карточку с номером "position".
    - year - служебный год - две цифры, которые впечатываются в графе "год" рядом с данными;
    
Перед запуском PDF карточка должна быть открыта в прогрмаме PDF-XChange-Viewer на полный экран.
    
Формат утилиты:
def autotype(name=None, mode=None, position=None, data=None, year=None):
    return res

"""
import subprocess, sys, os, glob, time

XTE_POSITION_UP = "xte 'mousemove 472 230' 'mouseclick 1' "
XTE_POSITION_DOWN = "xte 'mousemove 469 628' 'mouseclick 1' "
TAB = 'key Tab'

###############################################################################
def type_name(name):   
#    xdotool  search "ПЕТЯ"  windowactivate --sync mousemove --window %1 410 205 click 1  type  --delay 1500 П Е Т Я
    
    cmd = "xte 'mousemove 472 230' 'mouseclick 1' "
    subprocess.call([cmd], shell=True)

#    cmd = "xdotool  search 'ПЕТЯ' windowactivate --sync mousemove --window %1 410 205 click 1"
#    subprocess.call([cmd], shell=True)
#    cmd = "xdotool  type  --delay 200 %s " %( " ПП Е Т Я")
#    subprocess.call([cmd], shell=True)

#    cmd = "xte  'sleep 3' 'str %s' 'key Tab' " % (name.encode('utf-8'))
    cmd = "xte 'sleep 1' 'str %s' 'key Tab'  " % (name)
    subprocess.call([cmd], shell=True)
    cmd = "xte 'sleep 1' 'str %s' 'key Tab'  " % (name)
    subprocess.call([cmd], shell=True)

    cmd = "xte  'sleep 1' 'mousemove 469 628' 'mouseclick 1' "
    subprocess.call([cmd], shell=True)

    cmd = "xte 'sleep 1' 'str %s' 'key Tab'  " % (name)
    subprocess.call([cmd], shell=True)
    cmd = "xte  'sleep 1' 'str %s' 'key Tab' " % (name)
    subprocess.call([cmd], shell=True)
    
    cmd = "xte  'sleep 1' 'mousemove 100 200' 'mouseclick 1' "
    subprocess.call([cmd], shell=True)
    cmd = "xte  'sleep 1' 'keydown Control_L' 'key s' 'keyup Control_L' " # CNTRL-S - save file
    subprocess.call([cmd], shell=True)
    cmd = "xte  'sleep 1' 'keydown Alt_L' 'key F4' 'keyup Alt_L' " # Exit
    subprocess.call([cmd], shell=True)
    
###############################################################################    
def windows_focus(name):
    """
http://linux.die.net/man/1/wmctrl
Going to the window with a name containing 'emacs' in it
wmctrl -a emacs

Closing the window with a name containing 'emacs' in it
wmctrl -c emacs
    """    
    cmd = "wmctrl -a %s " %(name)
    subprocess.call([cmd], shell=True)
    
###############################################################################       
def autotype(path_temp, path_work, name, position, data, year, s21_template, pdfxviewer):
    res = 0
    if os.path.isdir(path_temp) and os.path.isdir(path_work) == True:
        pass
#        print "dir exist"
    else: 
        print "directory not exist. EXIT!"
        sys.exit(1)    
    if name == None:
        print "name argument is not exist. EXIT!"
        sys.exit(1)
    if os.path.exists(path_work + '/%s.pdf' % name) == True:
        print "File exist already !!!!!!!!!"
        res = 1
    else:
        print "create new file..."
        # компировать можно ТОЛьКО в рабочую директорию Python !!
        cmd = "cp %s %s" % (path_work+'/'+S21_TEMPLATE, name+".pdf")
        subprocess.call([cmd], shell=True)
        cmd = "wine %s %s" %(pdfxviewer,  name+".pdf &")
        subprocess.call([cmd], shell=True)
        time.sleep(5)
        windows_focus(name)
        type_name(name)  
#        cmd = "wmctrl -c %s " %(name) 
#        sPeterubprocess.call([cmd], shell=True)
    return res
###############################################################################
if __name__ == '__main__':
    PATH_TEMP =     '/home/sskriblo/s21-ocr_work/temp'
    PATH_WORK =     '/home/sskriblo/s21-ocr_work'
    PDFXVIWER = '/home/sskriblo/s21-ocr_work/PDFX_Vwr_Port/PDFXCview.exe'
#    PDFXVIWER_START = 'wine /home/sskriblo/s21-ocr_work/PDFX_Vwr_Port  %s' %(PATH_WORK+'/'+name + '.pdf')
    S21_TEMPLATE = 'S21-.pdf'
    

    name = u'ПЕТЯ'
#    name = chr(0x5F) + chr(0x5F) + u'ПЕТЯ'
#    type_name(name)
#    sys.exit(1)
    autotype(PATH_TEMP, PATH_WORK, name, 1, 'data', 'year', S21_TEMPLATE,PDFXVIWER)



###############################################################################
###############################################################################
###############################################################################
