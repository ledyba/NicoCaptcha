#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2011/12/11

@author: psi
'''

import glob;
import os;
import random;
from captcha import Captcha, Trainer;

def _main():
	try:
		print "start lerning..."
		files = glob.glob("../renamed/*.png");
		random.shuffle(files);
		trainer = Trainer();
		for _ in xrange(0, 10000):
			fname = random.choice(files)
			absoluteName = os.path.abspath(fname);
			ans = os.path.basename(absoluteName).split(".")[0].split("_")[0];
			cap = Captcha(trainer, absoluteName);
			print ans,"->","".join(cap.analyze(ans))
	except:
		raise
	finally:
		try:
			trainer.save();
		except:
			pass

if __name__ == '__main__':
	_main();