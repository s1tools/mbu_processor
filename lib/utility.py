#!/usr/bin/python
########################################################################
# Copyright (C) 2016 SERCO SpA                                         #
# Gianluca Sabella gianluca.sabella@gmail.com                          #
# Giovanna Palumbo giovanna.palumbo@serco.com                          #
#                                                                      #
# This file is part of OCN to BURF Processor Project                   #
#                                                                      #
# OCN to BURF Processor project can not be copied and/or distributed   #
# without the express permission of the authors.                       #
########################################################################

        
def indentXML(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indentXML(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
