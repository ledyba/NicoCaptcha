#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math;
from PIL import Image, ImageFilter, ImageDraw;

class Gravity(object):
	def __init__(self, image):
		self.image = image \
					.filter(ImageFilter.MaxFilter) \
					.filter(ImageFilter.MinFilter) \
					.convert("RGBA") \
					;
		self.width, self.height = self.image.size;
		self.debugImage = None;
		self.supportVector = None;
		self.stoneDistance = self.width/2.0;
	def analyze(self):
		self.supportLine = self.calcLine();
		self.supportLine.sort();
		rot = 0.0;
		startPt = self.supportLine[0];
		for pt in self.supportLine[1:]:
			deltaY = pt[1]-startPt[1];
			deltaX = pt[0]-startPt[0];
			rot += math.atan2(deltaY, deltaX);
		rot /= len(self.supportLine)-1;
		self.image = self.image.rotate(math.degrees(rot), Image.BICUBIC)
		self.image = Image.composite(self.image, Image.new("RGBA", self.image.size, (255,255,255,255)), self.image)
		#ポイントもそれにつれて回転
		center = [self.width/2.0, self.height/2.0];
		for i in xrange(0,len(self.supportLine)):
			self.supportLine[i] = [int(val) for val in self.rotatePoint(center, self.supportLine[i], -rot)];

		#中央線を表示
		self.debugImage = self.image.copy();
		draw = ImageDraw.Draw(self.debugImage);
		draw.line([tuple(pt[:2]) for pt in self.supportLine], fill="#ff0000", width=3);
		del draw;
	def rotatePoint(self, centerPt, pt, rotate):
		sin_ = math.sin(rotate);
		cos_ = math.cos(rotate);
		return [
			int(cos_*(pt[0]-centerPt[0]) - sin_*(pt[1]-centerPt[1]) + centerPt[0]),
			int(sin_*(pt[0]-centerPt[0]) + cos_*(pt[1]-centerPt[1]) + centerPt[1])
		];
	POWER = math.exp(8);
	def calcForce(self, pt, other, isSigmoid=False):
		deltaX = other[0]-pt[0];
		deltaY = other[1]-pt[1];
		distance = (deltaX**2+deltaY**2)+100;
		distanceSqrt = math.sqrt(distance);
		if isSigmoid:
			force = -1.0/(0.1+math.pow(Gravity.POWER,distanceSqrt-self.stoneDistance))
		else:
			force = 1.0/distanceSqrt;
		return (force * deltaX / distanceSqrt, force * deltaY / distanceSqrt)
	def updatePoints(self, pt, stones, others):
		fx = fy = 0.0;
		gx = gy = 0.0;
		for other in others:
			if other == pt:
				continue
			x, y = self.calcForce(pt, other, True);
			gx += x;
			gy += y;

		for stone in stones:
			x, y = self.calcForce(pt, stone, False);
			fx += x;
			fy += y;

		pt[0] += fx + gx;
		pt[1] += fy + gy;
		return fx ** 2 + fy ** 2;
	def gravityCycle(self, pts, stones):
		fsum = 0;
		for pt in pts:
			fsum += self.updatePoints(pt, stones, pts);
		return fsum / len(pts);
	def getStones(self, image):
		stones = [];
		w,h = image.size;
		for y in range(0, h):
			for x in range(0, w):
				r,g,b,_ = image.getpixel((x,y))
				weight = (255*3-(r+g+b)) / (3.0 * 255);
				if weight > 0.1:
					stones.append((x,y));
		return stones;
	def calcLine(self):
		stones = self.getStones(self.image);
		min_ = (self.width**2+self.height**2) / (10.0**5);
		pts = [
				[0, self.height/2],
				[self.width, self.height/2],
		];
		lastForce = 0.0;
		for i in xrange(0, 100):
			force = self.gravityCycle(pts, stones);
			delta = abs(force-lastForce);
			lastForce = force;
			if delta < min_ and i > 30:
				break;
		return pts;
	def getSupportLine(self):
		return self.supportLine;
	def getImage(self):
		return self.image;
	def getDebugImage(self):
		return self.debugImage;