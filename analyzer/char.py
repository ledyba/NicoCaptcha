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
import math;

class CharDetect(object):
    CHARACTERS = 5; #入れ知恵：Captchaは五文字。
    def __init__(self, image, resizedSize):
        self.resizedSize = resizedSize;
        self.__image = image;
        self.width, self.height = self.__image.size;
        self.images = None;
        self.debugImage = None;

    def analyze(self):
        self.statics = self.createStatics();
        self.emptyLines = self.detectEmptyLines(self.statics["black"]);
        if len(self.emptyLines) >= CharDetect.CHARACTERS-1:
            emptyLines = self.emptyLines[:];
            emptyLines.sort(lambda x,y : -cmp(x[1],y[1]));
            print emptyLines;
            self.divLines = emptyLines[0:CharDetect.CHARACTERS-1];
        else:
            self.divLines = self.detectChar(self.emptyLines, CharDetect.CHARACTERS-1-len(self.emptyLines), self.statics);
        self.debugImage = self.debugImage.resize((self.width*3, self.height*3));
        self.divImage();
    def extendImg(self, image):
        w,h = image.size;
        print w,h
        vec = [0, h/2-1, w-1, h/2+1]
        box_util.updateBox(image, vec, ( 0,  0,  0,  1));
        box_util.updateBox(image, vec, ( 0, -1,  0,  0));
        image = image.crop(vec);
        w,h = image.size;
        max_ = max(w,h)
        extended = Image.new("RGBA", (max_, max_), (255,255,255,255))
        extended.paste(image, ((max_-w)/2, (max_-h)/2), image);
        return extended.resize((self.resizedSize,self.resizedSize), Image.BILINEAR);

    def divImage(self):
        nowX = 0
        images = [];
        self.divLines.sort();
        for split in self.divLines:
            img = self.extendImg(self.__image.crop((nowX, 0, split[0], self.height)));
            images.append(img);
            nowX = split[0]+split[1];
        images.append(self.extendImg(self.__image.crop((nowX, 0, self.width, self.height))));
        return images;

    def createStatics(self):
        statics = {
            "black":[],
            "delta":[]
        }
        for x in xrange(0, self.width):
            hasLast = x <= 0;
            black = 0;
            delta = 0;
            for y in xrange(0, self.height):
                r,g,b,a = self.__image.getpixel((x,y));
                pix = 1-((r+g+b) / 3.0 / 255.0);
                if pix > 0.1:
                    black+=1;
                if x > 0:
                    r,g,b,a = self.__image.getpixel((x-1,y));
                    pixLast = 1-((r+g+b) / 3.0 / 255.0);
                    if pix > 0.1 and pixLast <= 0.1 or pix <= 0.1 and pixLast > 0.1:
                        delta+=1;
            statics["black"].append(black);
            statics["delta"].append(delta);
        return statics;

    def detectEmptyLines(self, blackData):
        lastBlack = blackData[0];
        emptyLines = [];
        contCnt = 0;
        for x in xrange(1,self.width):
            black = blackData[x];
            if lastBlack == black:
                contCnt += 1;
            else:
                if lastBlack == 0:
                    emptyLines.append((x-contCnt-1, contCnt));
                contCnt = 0;
            lastBlack = black;
        self.debugImage = self.__image.copy();
        draw = ImageDraw.Draw(self.debugImage);
        for line in emptyLines:
            x = line[0] + line[1]/2;
            draw.line([(x, 0),(x, self.height)], fill="#00ffff", width=1);
        return emptyLines;

    def detectChar(self, emptyLines, left, statics):
        draw = ImageDraw.Draw(self.debugImage);
        blackData = statics["black"];
        deltaData = statics["delta"];
        # 空白だけでは区切れない！
        block = self.width/5;
        splitList = [];
        for x in xrange(max(self.width/10,5),min(self.width*9/10, self.width-5)):
            #情報量を計算
            changedP = float(deltaData[x-1]+deltaData[x]+deltaData[x+1])/self.height/3;
            sameP = 1-changedP;
            assert changedP <= 1.0 and changedP >= 0.0
            if changedP > 0.95 or changedP < 0.05:
                infoSize = 0;
            else:
                infoSize = -(changedP * math.log(changedP, 2) + sameP * math.log(sameP, 2))
            addFlag = True
            distances = [x, self.width-x]
            for emp in emptyLines:
                center = emp[0]+emp[1]/2;
                dist = abs(x-center);
                distances.append(dist);
                if dist < block:
                    addFlag = False;
                    break;
            distances.sort();
            d = (distances[1]+distances[0])/float(distances[1]-distances[0]+1);
            if addFlag:#情報量が大きくなって、かつ黒が少ない場所が文字の境目
                splitList.append((infoSize * d, blackData[x], x));
        splitList.sort();
        splitLines = []
        for i in xrange(0, left):
            maxInfo = splitList[len(splitList)-1][0];
            maxList = [];
            for item in splitList[len(splitList)/2:]:
                info, black, x = item;
#                if abs(maxInfo-info) < 0.15:
                maxList.append((black, x));
            maxList.sort();
            maxItem = maxList[0]
            splitLines.append(maxItem);
            print "line:", maxItem
            #近隣を削除
            newList = []
            for item in splitList:
                if abs(item[2]-maxItem[1]) >= block*3/4:
                    newList.append(item);
            splitList = newList;
        #デバッグ用
        for line in splitLines:
            x = line[1];
            draw.line([(x, 0),(x, self.height)], fill="#ff00ff", width=1);
        #draw.line(infoLst, fill="#FF8B4D", width=1);
        #draw.line(blackLst, fill="#00ff00", width=1);
        emptyLines = emptyLines[:];
        for line in splitLines:
            emptyLines.append((line[1],0));
        return emptyLines;

    def getDivLine(self):
        return self.divLines;
    def getDebugImage(self):
        return self.debugImage;
