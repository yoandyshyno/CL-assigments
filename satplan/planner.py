#!/usr/bin/python
import sys
import re
import random as R

def parse(f):
	# (define (problem strips-mprime-l5-f60-s10-v3-c6)
	d = re.compile(r'\(problem strips-mprime-l(\d+)-f(\d+)-s(\d+)-v(\d+)-c(\d+)\)')
	#(has-fuel l0 f53)
	hf = re.compile(r'\(has-fuel l(\d+) f(\d+)\)')
	#(has-space  v0 s10)
	hs = re.compile(r'\(has-space  v(\d+) s(\d+)\)')
	#(at v0 l3)
	atv = re.compile(r'\(at v(\d+) l(\d+)\)')
	atc = re.compile(r'\(at c(\d+) l(\d+)\)')

	# Init
	t = open(f, "r").read()
	varis = d.findall(t)
	loc = [0 for x in range(int(varis[0][0]))]
	veh = [[0,0] for x in range(int(varis[0][3]))]
	car = [0 for x in range(int(varis[0][4]))]
	
	r = re.compile(r'\(:init(\s+)(.+)(\s+)\)(\s+)\(', re.DOTALL)
	init_p = r.findall(t)[0][1]
	for (l,f) in hf.findall(init_p):
		loc[int(l)] = int(f)
	
	for (v,s) in hs.findall(init_p):
		veh[int(v)][1] = int(s)
	
	for (v,l) in atv.findall(init_p):
		veh[int(v)][0] = int(l)

	for (c,l) in atc.findall(init_p):
		car[int(c)] = int(l)

	# Goal
	r = re.compile(r'\(:goal(\s+)\(and(\s+)(.+)\)(\s+)\)(\s+)\)', re.DOTALL)
	g = [map(int,x) for x in atc.findall(r.findall(t)[0][2])]
	return (loc,veh,car,g)

class mprime(object):
	"""docstring for mprime"""
	def __init__(self, arg):
		super(mprime, self).__init__()
		(self.loc, self.veh, self.car, self.g) = arg


	def move(self,_veh, lfrom, lto):
		if lfrom == lto:
			return True
		n = len(self.loc)
		s = (lfrom - lto) / abs(lfrom - lto)
		if abs(lfrom-lto) > n / 2:
			route = map(lambda x: x % n, range(lfrom + s * (-1) * n,lto + s,s))
		else:	
			route = range(lfrom,lto + s * (-1),-1 * s)
		for i in range(len(route)-1):
			(a,b) = (route[i],route[i+1])
			if self.loc[a] < 0:
				self.donate(a)
			fp = self.loc[a]
			if fp > 0:
				self.loc[a] -= 1
				self.veh[_veh][0] = b 
				print "(move v%d l%d l%d f%d f%d)" % (_veh,a,b,fp,fp-1)
				#return True
			else:
				print "Fail move"
				return False

	def load(self,_car, _veh, _loc):
		sp = self.veh[_veh][1]
		if self.car[_car] == _loc and self.veh[_veh][0] == _loc and sp > 0:
			self.car[_car] = -1
			self.veh[_veh][1] -= 1
			print "(load c%d v%d l%d s%d s%d)" % (_car,_veh,_loc,sp,sp-1)
			return True
		else:
			print "Fail load"
			return False

	def unload(self,_car, _veh, _loc):
		sp = self.veh[_veh][1]
		if self.car[_car] == -1 and self.veh[_veh][0] == _loc:
			self.car[_car] = _loc
			self.veh[_veh][1] += 1
			print "(unload c%d v%d l%d s%d s%d)" % (_car,_veh,_loc,sp,sp+1)
			return True
		else:
			return False

	def donate(self, lto):
		for i in range(len(self.loc)):
			if self.loc[i] > 1:
				fo = self.loc[i]
				fd = self.loc[lto]
				self.loc[i] -= 1
				self.loc[lto] += 1
				print "(donate l%d l%d f%d f%d f%d f%d f%d)" % (i,lto,fo,fo-1,fo-2,fd,fd+1)
				return True
		print "Fail donation"
		return False

	def planing(self):
		for goal in self.g:
			# Start task
			v = R.randint(0,len(self.veh)-1)
			mit = self.car[goal[0]]
			if mit != goal[1]:
				v1=self.move(v,self.veh[v][0], mit)
				v2=self.load(goal[0],v,mit)
				v3=self.move(v,mit,goal[1])
				v4=self.unload(goal[0],v,goal[1])
				if v1 and v2 and v3 and v4:
					print "pass"


if __name__ == '__main__':
	vrs = parse(sys.argv[1])
	mp = mprime(vrs)
	mp.planing()

	