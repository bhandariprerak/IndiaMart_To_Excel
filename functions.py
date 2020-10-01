import os
import re


def monthyear(date) :
    dmy = re.findall('[A-Z 0-9]+',date)
    excelfilename = dmy[1]+'-'+dmy[2]
    return excelfilename

def path(filename) :
    parent_dir = 'C:/IndiaMart Excel/'
    path = os.path.join(parent_dir,filename)
    return path
