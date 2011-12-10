#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      psi
#
# Created:     10/12/2011
# Copyright:   (c) psi 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from PIL import Image, ImageDraw;
import box_util;

class BoxDetect(object):
    def __init__(self, image, supportLine):
        self.supportLine = supportLine;
        self.__image = image;
        self.image = None;
        self.debugImage= None;
    def analyze(self):
        w,h = self.__image.size;
        minSize = w / 4;
        pa, pb = self.supportLine;
        width = pb[0]-pa[0]
        if width < minSize:
            fix = (minSize - width) / 2;
            vec = [pa[0]-fix, pa[1], pb[0]+fix, pa[1]];
        else:
            vec = [pa[0], pa[1], pb[0], pa[1]];
        extended = 1;
        while extended > 0:
            extended = 0;
            extended += box_util.updateBox(self.__image, vec, ( 0,  0,  0,  1));
            extended += box_util.updateBox(self.__image, vec, (-1,  0,  0,  0));
            extended += box_util.updateBox(self.__image, vec, ( 0, -1,  0,  0));
            extended += box_util.updateBox(self.__image, vec, ( 0,  0,  1,  0));
        self.debugImage = self.__image.copy();
        vec[2]+=1;
        vec[3]+=1;
        self.image = self.__image.crop(vec);
        draw = ImageDraw.Draw(self.debugImage);
        draw.rectangle(vec, outline="#ff0000");
        del draw;

    def getImage(self):
        return self.image;
    def getDebugImage(self):
        return self.debugImage;



