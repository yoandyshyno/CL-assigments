#!/usr/bin/python

# Yoandy Sanchez 09, 2012
# Mprimes problem

import sys, re

def parse(f):
	"""
	This function aims to extract variables and storage them in list data structures.
	by parsing the input file using simple regular expressions.
	The function returns a list of objects locations,vehicles,cargoes,goals in this order.
	"""
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

def distance(n, l1, l2):
	"""
	Assuming that in the problem the locations are linked circularly, we can calculate distance.
	There's always a way to reach one location from other, so we always take the shortest.
	"""
	d = abs(l1 - l2)
	if d > (n / 2):
		d = n - d
	return d

def dist(n, orig, med, dest):
	"""
	Just a helper function to calculate distance with an intermediary location.
	"""
	return distance(n, orig, med) + distance(n, med, dest)

class mprime(object):
	"""
	The object mprime represent the problem. Here we deal with the variable and
	operations defined in the domain.
	"""
	def __init__(self, arg):
		super(mprime, self).__init__()
		(self.loc, self.veh, self.car, self.g) = arg
		self._in = []
		self.plan = []
		self.n = len(self.loc)
		self.optimize()

	def optimize(self):
		"""
		This method remove every meaningless goal, that is if the cargo is already
		in the location described by its corresponding goal.
		"""
		lg = []
		for g in self.g:
			if self.car[g[0]] != g[1]:
				lg.append(g)
		self.g = lg

	def move(self,_veh, lfrom, lto):
		"""
		In this method we take into account the preconditions, if a matter of fuel, we put
		a donation step before go on with the move.
		If the destination is more than 1 step from the origen, then intermediaries move plans
		are added.
		"""
		if lfrom == lto:
			return True
		n = self.n
		s = (lfrom - lto) / abs(lfrom - lto)
		if abs(lfrom-lto) > n / 2:
			route = map(lambda x: x % n, xrange(lfrom + s * (-1) * n,lto + s,s))
		else:	
			route = xrange(lfrom,lto + s * (-1),-1 * s)
		for i in xrange(len(route)-1):
			(a,b) = (route[i],route[i+1])
			if self.loc[a] < 1:
				self.donate(a)
			fp = self.loc[a]
			if fp > 0:
				self.loc[a] -= 1
				self.veh[_veh][0] = b 
				self.plan.append("(move v%d l%d l%d f%d f%d)" % (_veh,a,b,fp,fp-1))
				#return True
			else:
				print "Fail move"
				return False
		return True

	def load(self,_car, _veh, _loc):
		sp = self.veh[_veh][1]
		if self.car[_car] == _loc and self.veh[_veh][0] == _loc and sp:
			self.car[_car] = -1
			self._in.append([_car,_veh])
			self.veh[_veh][1] -= 1
			self.plan.append("(load c%d v%d l%d s%d s%d)" % (_car,_veh,_loc,sp,sp-1))
			return True
		else:
			print "Fail load"
			return False

	def unload(self,_car, _veh, _loc):
		sp = self.veh[_veh][1]
		if self.car[_car] == -1 and self.veh[_veh][0] == _loc:
			self.car[_car] = _loc
			self._in.remove([_car,_veh])
			self.veh[_veh][1] += 1
			self.plan.append("(unload c%d v%d l%d s%d s%d)" % (_car,_veh,_loc,sp,sp+1))
			return True
		else:
			return False

	def donate(self, lto):
		"""
		When the donate method is called we perform a search of a location which contains
		enough fuel, then we force a donation to the target location.
		"""
		for i in xrange(len(self.loc)):
			if self.loc[i] > 1:
				fo = self.loc[i]
				fd = self.loc[lto]
				self.loc[i] -= 1
				self.loc[lto] += 1
				self.plan.append("(donate l%d l%d f%d f%d f%d f%d f%d)" % (i,lto,fo,fo-1,fo-2,fd,fd+1))
				return True
		#print "Fail donation"
		return False

	def makeplan(self, comb):
		"""
		We make the plan according to a strategy.
		"""
		[v, c, d] = comb
		med = self.car[c]
		r = self.move(v, self.veh[v][0], med) and self.load(c, v, self.car[c]) and \
		self.move(v, med, d) and self.unload(c, v, d)
		for i in range(len(self.g)):
			if self.g[i][0] == c:
				self.g.pop(i)
				break
		return r

if __name__ == '__main__':
	vrs = parse(sys.argv[1])
	mp = mprime(vrs)
	comb = []
	for i in range(len(mp.g)):
		maxd = 1000000000
		for g in mp.g:
			for k in range(len(mp.veh)):
				dd = dist(mp.n, mp.veh[k][0], mp.car[g[0]], g[1])
				if dd < maxd:
					comb = [k, g[0], g[1]]
					maxd = dd
					
		if not mp.makeplan(comb):
			print "FAIL"
			exit()
	for p in mp.plan:
		print p
