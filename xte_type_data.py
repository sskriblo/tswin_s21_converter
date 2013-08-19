# -*- coding: utf-8 -*-
"""
Программа для набора данных (только цифр) в карточке S-21.

Утилиты:
xdotool getmouselocation - определяет положение мышки
xte 'mousemove 508 339' 'mouseclick 1' - позиционирует на Сентябрь@Книги в верхней половине
xte 'mousemove 509 734' 'mouseclick 1' - позиционирует на Сентябрь@Книги в нижней половине
sleep 3 && xte 'key 6' 'key Tab' 'key 7' 'key Tab' 'key 8' - набирает цифры в клетках из bash

Алгоритм и аргументы:
    - path_work - рабочая директория, полный путь к ней;
    - path_temp - рабочая для временных файлов, полный путь к ней;
    - name - ФИО - для создания файла и печати ФИО в карточках;
    - position=[0,1,2,3] - номер карточки в файле. Отсчет идет с нуля, слева 
    направо, сверху вниз. Служит для позиционирования при вводе данных;
    Данные записываются в карточку с номером "position".
    - year - служебный год - две цифры, которые впечатываются в графе "год" рядом с данными;
    - data - список данных - цифры с Сентября@Книги далее Сентябрь@Из.Б, по Август@Из.Б. 
        Если цифра равна нулю, то она не печатается. Всего длина списка 6*12+72 элемента. 
        При выводе учесть, что есть еще 7-ая колонка - "примечание", ее надо проскочить.
        Еще учесть позицию position. Сделать специальный алгоритм перепрыгивания в нужную позицию.
    
Перед запуском PDF карточка должна быть открыта в прогрмаме PDF-XChange-Viewer 
на полный экран и затем закрыта. Это обеспечит открывание на полный экран в автоматическом режиме.
    
Формат утилиты:
def type_data(path_temp, path_work, name, position, data, year,  pdfxviewer):

"""
import subprocess, sys, os, glob, time

XTE_POSITION_UP = "xte 'mousemove 472 230' 'mouseclick 1' "
XTE_POSITION_DOWN = "xte 'mousemove 469 628' 'mouseclick 1' "
TAB = 'key Tab'
###############################################################################
def    positioning(position):
    """
    position = 0 - левая верхняя таблица
    position = 1 - правая верхняя таблица
    position = 2 - левая нижняя таблица
    position = 3 - правая верхняя таблица
    position % 2 == 0 - четная - левая таблица
    position % 2 == 1 - нечетная - правая таблица
    position > 1 - нижняя;  position < 2 - верхняя
    """
    if position == 0:
        cmd = "xte 'mousemove 508 339' 'mouseclick 1' "
        subprocess.call([cmd], shell=True)
        res = "LEFT"
    elif position == 1:
        cmd = "xte 'mousemove 508 339' 'mouseclick 1' "
        subprocess.call([cmd], shell=True)
        res = "RIGHT"
    elif position == 2:
        cmd = "xte 'mousemove 509 734' 'mouseclick 1' "
        subprocess.call([cmd], shell=True)
        res = "LEFT"
    elif position == 3:
        cmd = "xte 'mousemove 509 734' 'mouseclick 1' "
        subprocess.call([cmd], shell=True)
        res = "RIGHT"
    return res
    
###############################################################################
def tab_skip(number):
    for i in range (number):
        cmd = "xte 'usleep 100000' 'key Tab'"
        subprocess.call([cmd], shell=True)
    
###############################################################################
def type_digit(data, side):   
    if side == "RIGHT":
        tab_skip(7) # шесть колонок с цифрами и примечание

    data_list = data.split("\t")
    for month in range(12):
        for i in range (6):
            try:                
                digit = int( data_list[(month*6) + i].strip() )
            except ValueError: # if empty data
                digit = 0
            if digit == 0:
                cmd = "xte 'usleep 100000' 'key Tab'"
                subprocess.call([cmd], shell=True)
            else:
                cmd = "xte 'usleep 100000' 'str %s' 'key Tab'" %(digit)
                subprocess.call([cmd], shell=True)
        tab_skip(8) # шесть колонок с цифрами и два примечания
      
    cmd = "xte  'usleep 100000' 'mousemove 100 200' 'mouseclick 1' "
    subprocess.call([cmd], shell=True)
    cmd = "xte  'usleep 100000' 'keydown Control_L' 'key s' 'keyup Control_L' " # CNTRL-S - save file
    subprocess.call([cmd], shell=True)
    cmd = "xte  'sleep 2' 'keydown Alt_L' 'key F4' 'keyup Alt_L' " # Exit
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
def type_data(path_temp, path_work, name, position, data, year, pdfxviewer):
    cmd = "wine %s '%s' &" %(pdfxviewer,  name)
    subprocess.call([cmd], shell=True)
    time.sleep(8)
    windows_focus(name)
    side = positioning(position)
    type_digit(data, side)  
#        cmd = "wmctrl -c %s " %(name) 
#        subprocess.call([cmd], shell=True)
###############################################################################
if __name__ == '__main__':
    PATH_TEMP =     '/home/sskriblo/s21-ocr_work/temp'
    PATH_WORK =     '/home/sskriblo/s21-ocr_work'
    PDFXVIWER = '/home/sskriblo/s21-ocr_work/PDFX_Vwr_Port/PDFXCview.exe'
    
    name = u'ПЕТЯ.pdf'
    """
    data  = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10,11,12],
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10,11,12],
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10,11,12],
        [1, 2, 3, 4, 5, 6],
        [0, 0, 0, 0,0,0],
        [0, 0, 0, 0, 0, 0],
        [7, 8, 9, 10,11,12],
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10,11,12],
    ]  
    """
    data  = [
        1, 2, 3, 4, 5, 6,
        7, 8, 9, 10,11,12,
        1, 2, 3, 4, 5, 6,
        7, 8, 9, 10,11,12,
        1, 2, 3, 4, 5, 6,
        7, 8, 9, 10,11,12,
        1, 2, 3, 4, 5, 6,
        0, 0, 0, 0,0,0,
        0, 0, 0, 0, 0, 0,
        7, 8, 9, 10,11,12,
        1, 2, 3, 4, 5, 6,
        7, 8, 9, 10,11,12,
    ]    

    type_data(PATH_TEMP, PATH_WORK, name, 0, data, 'year', PDFXVIWER)



###############################################################################
###############################################################################
###############################################################################
