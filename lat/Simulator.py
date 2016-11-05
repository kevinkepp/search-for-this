from random import random
import numpy as np
from scipy.ndimage.interpolation import shift
from lat import RobotAgent
from lat.Environment import Environment
from enum import Enum


class Actions(Enum):
	up = 0
	down = 1
	left = 2
	right = 3

	@staticmethod
	def all():
		return [a for a in Actions]


class Simulator(Environment):
	NO_TARGET = 0
	TARGET = 1

	# agent is RobotAgent
	def __init__(self, agent, max_steps, grid_size):
		self._agent = agent
		self._max_steps = max_steps
		self._grid_size = grid_size
		self._state = None

	def _rnd_pos(self):
		x = int(random() * self._grid_size)
		y = int(random() * self._grid_size)
		return x, y

	def rnd_pos_except_center(self):
		pos = self._rnd_pos()
		mid = np.floor(self._grid_size / 2)
		if pos == (mid, mid):
			return self.rnd_pos_except_center()
		else:
			return pos

	def get_init_state(self, target_pos):
		x, y = target_pos
		mat = np.full((self._grid_size, self._grid_size), self.NO_TARGET, np.int)
		mat[x, y] = self.TARGET
		return mat

	# is out of bounds
	def _is_oob(self):
		return np.sum(self._state) == 0

	def get_middle(self):
		mid = int(np.floor(self._grid_size / 2))
		return mid, mid

	def _is_success(self):
		x, y = self.get_middle()
		return self._state is not None and self._state[x, y] == self.TARGET

	def run_epoch(self):
		target_pos = self.rnd_pos_except_center()
		self._state = self.get_init_state(target_pos)
		steps = 0
		while steps < self._max_steps:
			action = self._agent.choose_action(self._state)
			if action is None:
				return False
			# update state
			old_state = self._state
			self.execute_action(action)
			# check if success or out of bounds (failure)
			success = self._is_success()
			oob = self._is_oob()
			# reward success, failure and neutral state
			reward = 10 if success else -1 if not oob else -10
			self._agent.incorporate_reward(old_state, action, self._state, reward)
			if success:
				return True
			if oob:
				return False
		return False

	def run(self, epochs=1):
		res = []
		for i in range(epochs):
			print("Epoch " + str(i))
			r = self.run_epoch()
			res.append(r)
			self._agent.new_epoch()
		return res

	def get_current_state(self):
		return self._state

	def shift_state(self, action):
		if action == Actions.up:
			return shift(self._state, [-1, 0], cval=0)
		elif action == Actions.down:
			return shift(self._state, [1, 0], cval=0)
		elif action == Actions.left:
			return shift(self._state, [0, -1], cval=0)
		else:
			return shift(self._state, [0, 1], cval=0)

	def execute_action(self, action):
		self._state = np.rint(self.shift_state(action)).astype(int)
