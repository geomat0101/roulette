#!/usr/bin/env python

# figure out largest contiguous section of wheel which can be
# covered with minimal exposure using splits and straight up bets

wheel = [0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 100, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2]

board = []
board.append([1,2,3])
board.append([4,5,6])
board.append([7,8,9])
board.append([10,11,12])
board.append([13,14,15])
board.append([16,17,18])
board.append([19,20,21])
board.append([22,23,24])
board.append([25,26,27])
board.append([28,29,30])
board.append([31,32,33])
board.append([34,35,36])

def find_on_board(num):
	"""
	returns row,col coords for location of a number on the board
	"""
	row = 0
	for r in board:
		col = 0
		for c in r:
			if c == num:
				return(row,col)
			col += 1
		row += 1

def get_contig(run):
	"""
	get full array from starting position based on run iteration
	"""
	contig = wheel[run:]
	contig += wheel[:run]
	return(contig)


top_score = 0
top_slice = []
top_covered = []
top_play = []
all_permutations = []

for run in range(0,38):
	curr_wheel = get_contig(run)
	for curr_run in range(1,39):
		slice = curr_wheel[0:curr_run]
		covered = []
		cost = 0
		play = []
		permutation = {}
		for num in slice:
			if num in covered:
				# already covering it, skip
				continue
			if num == 0:
				if 100 in slice:
					# split
					cost += 1
					covered += [0,100]
					play += [(0,100)]
				else:
					# straight up
					cost += 2
					covered += [0]
					play += [0]
			elif num == 100:
				if 0 in slice:
					# split
					cost += 1
					covered += [0,100]
					play += [(0,100)]
				else:
					# straight up
					cost += 2
					covered += [100]
					play += [100]
			else:
				# numbers other than 0 and 00
				(row,col) = find_on_board(num)
				if row == 0:
					# top row
					if col in [0,2]:
						# left or right col, both split to the middle
						target = board[row][1]
						if target in slice:
							# wanted
							if target not in covered:
								# split
								cost += 1
								covered += [num, target]
								play += [(num, target)]
								continue
					else:
						# middle col
						for target in [board[row][0], board[row][2]]:
							if target in slice:
								# wanted
								if target not in covered:
									# split
									cost += 1
									covered += [num, target]
									play += [(num, target)]
									break

						if num in covered:
							# matched in multi-target loop
							continue

					# no center split, check underneath
					target = board[1][col]
					if target in slice:
						# wanted
						if target not in covered:
							# split
							cost += 1
							covered += [num, target]
							play += [(num, target)]
							continue

					# no splits, go straight up
					cost += 2
					covered += [num]
					play += [num]

				elif row == 11:
					# bottom row
					if col in [0,2]:
						# left or right col, both split to the middle
						target = board[row][1]
						if target in slice:
							# wanted
							if target not in covered:
								# split
								cost += 1
								covered += [num, target]
								play += [(num, target)]
								continue
					else:
						# middle col
						for target in [board[row][0], board[row][2]]:
							if target in slice:
								# wanted
								if target not in covered:
									# split
									cost += 1
									covered += [num, target]
									play += [(num, target)]
									break

						if num in covered:
							# matched in multi-target loop
							continue

					# no center split, check above
					target = board[10][col]
					if target in slice:
						# wanted
						if target not in covered:
							# split
							cost += 1
							covered += [num, target]
							play += [(num, target)]
							continue

					# no splits, go straight up
					cost += 2
					covered += [num]
					play += [num]
				else:
					# middle row
					if col in [0,2]:
						# left or right col, both split to the middle
						target = board[row][1]
						if target in slice:
							# wanted
							if target not in covered:
								# split
								cost += 1
								covered += [num, target]
								play += [(num, target)]
								continue
					else:
						# middle col
						for target in [board[row][0], board[row][2]]:
							if target in slice:
								# wanted
								if target not in covered:
									# split
									cost += 1
									covered += [num, target]
									play += [(num, target)]
									break

						if num in covered:
							# matched in multi-target loop
							continue

					# no center split, check above and below
					for target in [board[row-1][col], board[row+1][col]]:
						if target in slice:
							# wanted
							if target not in covered:
								# split
								cost += 1
								covered += [num, target]
								play += [(num, target)]
								break

					if num in covered:
						# matched in multi-target loop
						continue

					# no splits, go straight up
					cost += 2
					covered += [num]
					play += [num]
	
		score = len(slice) / float(cost)
		permutation = {
				'score': score,
				'slice': slice,
				'covered': covered,
				'play': play
			}
		all_permutations += [permutation]
		if score > top_score:
			top_score = score
			top_slice = slice
			top_covered = covered
			top_play = play

#print(top_score)
#print(top_slice)
#print(top_covered)
#print(top_play)

for p in all_permutations:
#	if len(p['play']) <= 10:
	print("%s: (%d/%d) %s" % (p['score'], len(p['play']), len(p['covered']), p['play']))
