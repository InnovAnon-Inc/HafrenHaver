from __future__ import division

"""
def pitches (freqs, base):
	return [base * freq for freq in freqs]
"""
"""
def harmonics (n):
	return [1 / (harmonic + 1) for harmonic in xrange (n)]
def harmonics2 (n):
	return set (harmonics20 (n) + harmonics21 (n))
def harmonics2all (n):
	return set (harmonics20 (n) + harmonics21 (n) + harmonics22 (n))
def harmonics20 (n):
	return [(harmonic + 1) / (harmonic + 2) for harmonic in xrange (n)]
def harmonics21 (n):
	return [(harmonic + 2) / (harmonic + 1) for harmonic in xrange (n)]
def harmonics22 (n):
	return [(n - harmonic) / (harmonic + 2) for harmonic in xrange (n)]
def harmonics3 (n):
	return [harmonic + 1 for harmonic in xrange (n)]
def scale4 (ns):
	return set(
		[n / n + m for n in ns for m in ns] +
		[m / n + m for n in ns for m in ns])
def harmonics4inv (n):
	return [(k + 1) * (1 / n) for k in xrange (n)]
def harmonics4inv2 (n):
	return [n / (1 + k) for k in xrange (n)]
def harmonics4 (n):
	return [k + 1 for k in xrange (n)]
def scale1 (n, m):
	return set ([(num + 1) / (den + 1) for num in xrange (n) for den in xrange (m)])
def scale2 (ns):
	#ns = {}
	#ns[2] = 20
	#ns[3] = 10
	#ns[5] =  5
	
	# every combination of every prime factor
	# by the same
	
	combos = []
	for key, value in ns:
		combos.extend ([key] * value)
	#print combos
	perms = []
	for i in xrange (len (combos)):
		perms.extend ([
			reduce (mul, p) for p in permutations (combos, i + 1)])
	perms = set (perms)
	#print perms
	return set ([p1 / p2 for p1 in perms for p2 in perms])
def scale3 (ns, E):
	perms = []
	for n in ns:
		perms.extend ([pow (n, e + 1) for e in xrange (E)])
	return set (perms)

indian_scale1 = [
	1/1, 9/8, 5/4, 4/3,
	3/2, 5/3, 15/8, 2/1]
just_scale = [
	1/1, 9/8, 5/4,
	3/2, 7/4, 2/1]
indian_scale2 = [
	1/1, 256/243, 16/15, 10/9,
	9/8, 32/27, 6/5, 5/4, 81/64, 4/3, 27/20]
"""
class Harmonic:
	scale_types = [None] * 13
	scale_types[12] = ["chromatic"]
	scale_types[8] = ["jazz", "modern classical"]
	scale_types[7] = ["modern western"]
	scale_types[6] = ["western folk"]
	scale_types[5] = ["oriental folk"]
	scale_types[4] = ["prehistoric"]
	scale_types[3] = ["prehistoric"]
	scale_types[2] = ["prehistoric"]
	scale_types[1] = ["liturgy", "modern art"]
	scale_types[0] = None

	scale_modes = [None] * 7
	scale_modes[0] = "Ionian"
	scale_modes[1] = "Dorian"
	scale_modes[2] = "Phrygian"
	scale_modes[3] = "Lydian"
	scale_modes[4] = "Mixolydian"
	scale_modes[5] = "Aeolian"
	scale_modes[6] = "Locrian"

	pythagorean_scale = [
		1/1, 256/243, 9/8, 32/27,
		81/64, 4/3, 729/512, 3/2,
		128/81, 27/16, 16/9, 243/128, 2/1]
	@staticmethod
	def harmonics5 (n):
		for h in xrange (n):
			yield (h + 2) / (h + 1)
	@staticmethod
	def harmonics5base (n):
		return [1] + sorted (harmonics5 (n))
	@staticmethod
	def equal_temperament_scale (n):
		return [2 ** h for h in equal_spacing (n)]
		#for h in xrange (n):
		#	yield 2 ** ((h + 1) / n)
	@staticmethod
	def harmonics6 (n):
		for i in xrange (1, n + 1):
			for j in xrange (1, i):
				yield (i + j) / i
	@staticmethod
	def harmonics7 (n):
		for h in set (harmonics6 (n)):
			hh = 1
			while hh * h < 2:
				hh *= h
				yield hh