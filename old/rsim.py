#!/usr/bin/env python

from random import random

class Spin (object):
	"""
	A single roulette spin
	"""

	roll = None
	dozen = None
	column = None

	def __init__ (self):

		self.spin = int(random()*10000) % 38

		if self.spin in [0, 37]:
			# zero, double-zero
			self.dozen = 0
		elif self.spin < 13:
			self.dozen = 1
		elif self.spin < 25:
			self.dozen = 2
		else:
			self.dozen = 3

		if self.spin in [0,37]:
			# 0, 00
			self.column = 0
		else:
			self.column = self.spin % 3
			if not self.column:
				# col 3 is when mod 3 == 0
				self.column = 3
	
	def __str__ (self):
		return("number: %d doz: %d col: %d" % (self.spin, self.dozen, self.column))


class Game (object):
	"""
	given a bankroll limit and bet progression,
	run a game to completion

	progression is an array of ordered bets to be placed upon repeated losses,
	resetting to the first element after a win is hit
	"""
	
	dbg = False			# debug output
	bankroll = 0
	max_bankroll = 0
	progression = None
	spins = None
	dozbet_hist = None
	colbet_hist = None

	def __init__ (self, bankroll, progression):
		self.bankroll = bankroll
		self.progression = progression
		self.spins = []
	
	def debug (self, msg):
		if self.dbg:
			print("%s" % msg)
		
	def run (self):
		dozbet = colbet = None	# when a bet is set, it's a tuple of (x, y) where x
								# is the dozen or column, and y is the bet amount

		dozidx = colidx = 0		# track where we are in the progression

		while True:
			# spin
			spin = Spin()
			self.spins += [spin]
			self.debug("bankroll: %d" % self.bankroll)
			self.debug("spin: %s" % spin)

			if self.bankroll > self.max_bankroll:
				self.max_bankroll = self.bankroll

			# evaluate bets
			if dozbet:
				if dozbet[0] == spin.dozen:
					# win
					dozidx = 0
					payout = dozbet[1] * 2
					self.bankroll += (payout + dozbet[1])
					self.debug("win on dozen, payout %d + %d" % (payout, dozbet[1]))
					dozbet = None
				else:
					# lose
					dozidx += 1
					self.debug("lose on dozen")

			if colbet:
				if colbet[0] == spin.column:
					# win
					colidx = 0
					payout = colbet[1] * 2
					self.bankroll += (payout + colbet[1])
					self.debug("win on column, payout %d + %d" % (payout, colbet[1]))
					colbet = None
				else:
					# lose
					colidx += 1
					self.debug("lose on column")

			# check game over conditions
			gameover = False
			if dozidx == len(progression):
				gameover = True
				self.debug("game over: dozen progression busted")
			if colidx == len(progression):
				gameover = True
				self.debug("game over: column progression busted")

			if gameover:
				self.debug("final bankroll: %d" % self.bankroll)
				self.debug("max   bankroll: %d" % self.max_bankroll)
				self.debug("total spins: %d" % len(self.spins))
				break

			# place next bets
			if dozbet:
				next_bet = progression[dozidx]
				if next_bet > self.bankroll:
					self.debug("game over: you broke, bitch! next dozen bet is %d" % next_bet)
					gameover = True
				else:
					dozbet = (dozbet[0], next_bet)
					self.bankroll -= next_bet
					self.debug("next dozen bet is %d" % next_bet)
			else:
				# see if we should place a new one
				lastdoz = [x.dozen for x in self.spins[-3:]]
				if len(self.spins) > 3:
					for i in [1, 2, 3]:
						if i in lastdoz:
							continue
						# new bet
						dozidx = 0
						dozbet = (i, progression[dozidx])
						self.bankroll -= progression[dozidx]
						self.debug("new dozens bet on dozen %d" % i)
						break

			if colbet:
				next_bet = progression[colidx]
				if next_bet > self.bankroll:
					self.debug("game over: you broke, bitch! next column bet is %d" % next_bet)
					gameover = True
				else:
					colbet = (colbet[0], next_bet)
					self.bankroll -= next_bet
					self.debug("next column bet is %d" % next_bet)
			else:
				# see if we should place a new one
				lastcol = [x.column for x in self.spins[-3:]]
				if len(self.spins) > 3:
					for i in [1, 2, 3]:
						if i in lastcol:
							continue
						# new bet
						colidx = 0
						colbet = (i, progression[colidx])
						self.bankroll -= progression[colidx]
						self.debug("new column bet on column %d" % i)
						break

			if gameover:
				self.debug("final bankroll: %d" % self.bankroll)
				self.debug("max   bankroll: %d" % self.max_bankroll)
				self.debug("total spins: %d" % len(self.spins))
				break


if __name__ == '__main__':
	# 10% return progression
	progressions = {
			'tenpct_return':		[5,5,10,15,25,35,55,90,140,220,350],
			'fivepct_return':		[5,5,10,15,20,30,50,75,115,175,270,415],
			'minpositive_return':	[5,5,10,15,20,30,45,70,105,155,235,350],
			'breakevens':			[5,5,5,10,15,20,30,45,70,105,155,235,350]
		}

	progression = progressions['breakevens']
#	progression = progressions['minpositive_return']

	Game.dbg = True
	g = Game(2500, progression)
	g.run()

