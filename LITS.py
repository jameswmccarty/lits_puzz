"""
https://www.puzzle-lits.com

LITS is a logic puzzle with simple rules and challenging solutions.

The rules of LITS are simple:
You have to place one tetromino* in each region in such a way that:
- 2 tetrominoes of matching types cannot touch each other horizontally or vertically. Rotations and reflections count as matching.
- The shaded cells should form a single connected area.
- 2x2 shaded areas are not allowed.

* Tetromino is a shape made of 4 connected cells. There are 5 types of tetrominoes, which are usually named L, I, T, S and O, based on their shape. The O tetromino is not used in this puzzle because it is a 2x2 shape, which is not allowed.

"""

from collections import deque
import math

def normalize(points):
	dx = min( p[0] for p in points )
	dy = min( p[1] for p in points )
	points = { (x-dx,y-dy) for x,y in points }
	if (0,0) in points:
		return points
	if (1,0) in points:
		return { (x-1,y) for x,y in points }
	return { (x,y-1) for x,y in points }

def vis(shape):
	x_coords = [ p[0] for p in shape ]
	y_coords = [ p[1] for p in shape ]
	for y in range( min(y_coords), max(y_coords)+1 ):
		for x in range( min(x_coords), max(x_coords)+1 ):
			if (x,y) in shape:
				print('X',end='')
			else:
				print(' ',end='')
		print()
	print()

def print_solution(shape):
	vis(shape)
	print()

def no2x2(shape):
	for x,y in shape:
		if all( (x+dx,y+dy) in shape for dx,dy in ((0,1),(1,0),(1,1)) ):
			return False
	return True

def piece_fits(tetromino,region):
	fits = set()
	for pt in region:
		if all((pt[0]+dx,pt[1]+dy) in region for dx,dy in tetromino):
			fits.add(frozenset((pt[0]+dx,pt[1]+dy) for dx,dy in tetromino))
	return fits

# is shape 'a' adjacent to shape 'b'?
def contacts(a,b):
	for pt in a:
		if any( (pt[0]+dx,pt[1]+dy) in b for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)) ):
			return True
	return False

def fully_connected(set_of_points):
	walk_start = list(set_of_points)[0]
	rebuild = set()
	q = deque()
	q.append(walk_start)
	while q:
		x,y = q.popleft()
		rebuild.add((x,y))
		for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
			if (x+dx,y+dy) in set_of_points and (x+dx,y+dy) not in rebuild:
				q.append((x+dx,y+dy))
	if rebuild == set_of_points:
		return True
	return False

def puzz_to_puzzareas(puzz):
	dim = int(math.sqrt(len(puzz)))
	areas = []
	for i in range(1,max(puzz)+1):
		area = []
		for x in range(dim):
			for y in range(dim):
				if puzz[y*dim+x] == i:
					area.append((x,y))
		areas.append(area)
	return areas

def tetro_type(shape):
	x_coords = [ p[0] for p in shape ]
	y_coords = [ p[1] for p in shape ]
	side_counts = [ y_coords.count(max(y_coords)),
					y_coords.count(min(y_coords)),
					x_coords.count(max(x_coords)),
					x_coords.count(min(x_coords)) ]
	if max(side_counts) == 4:
		return "I"
	if max(side_counts) == 2:
		return "S"
	if 2 not in side_counts:
		return "T"
	return "L"

def gen_all_tetrominos():
	q = deque()
	pos = { (0,0) }
	q.append( pos )
	tetrominos = set()
	while q:
		shape = q.popleft()
		if len(shape) == 4 and no2x2(shape):
			tetrominos.add(frozenset(normalize(shape)))
		elif len(shape) < 4:
			for pt in shape:
				x,y = pt
				for dx,dy in ((0,1),(1,0),(-1,0),(0,-1)):
					if (x+dx,y+dy) not in shape:
						q.append( {*shape,(x+dx,y+dy)} )
	return tetrominos

def search(region_options,pieces_selected=[],joined_set=set()):
	if len(region_options) == 0:
		if no2x2(joined_set) and fully_connected(joined_set):
			print_solution(joined_set)
	elif len(region_options) > 0:
		for fitting_piece in region_options[0]:
			# no two tiles of the same shape touching
			if not any(contacts(fitting_piece,x) and tetro_type(x)==tetro_type(fitting_piece) for x in pieces_selected):
				next_joined_set = joined_set.copy()
				next_joined_set.update( x for x in fitting_piece )
				if no2x2(next_joined_set):
					search(region_options[1:],pieces_selected+[fitting_piece],next_joined_set)

def solve(a_puzzle):
	possibilities = []
	tetrominos = gen_all_tetrominos()
	for region in puzz_to_puzzareas(a_puzzle):
		fittings = []
		for tetromino in tetrominos:
			for e in piece_fits(tetromino,region):
				fittings.append(e)
		possibilities.append(fittings)
	search(possibilities) 

if __name__ == "__main__":

	#6x6 Normal LITS Puzzle ID: 11,990,516

	puzz = [1,1,1,2,3,3,
			4,1,1,2,2,3,
			4,4,4,4,2,3,
			4,4,4,5,5,3,
			6,6,5,5,5,3,
			6,6,6,6,3,3]

	solve(puzz)

	# 10x10 Hard LITS Puzzle ID: 19,192,092
	puzz = [ 1, 2, 2, 3, 3, 3, 4, 4, 4, 5,
			 1, 2, 2, 3, 3, 4, 4, 6, 4, 5,
			 1, 2, 2, 7, 7, 4, 6, 6, 4, 5,
			 1, 8, 7, 7, 9, 9, 6, 6, 5, 5,
			 1, 8, 7, 7,10, 9, 9, 6, 6,10,
			 8, 8, 7, 7,10,10, 9,10,10,10,
			11, 7, 7,12,10,10,10,10,10,10,
			11,11, 7,12,12,10,10,13,13,10,
			11, 7, 7,12,12,14,10,10,13,13,
			 7, 7, 7,14,14,14,10,10,10,10]
	
	solve(puzz)

