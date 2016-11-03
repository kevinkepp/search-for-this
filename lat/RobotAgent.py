from abc import ABCMeta, abstractmethod
from enum import Enum


class Actions(Enum):
	up = 0
	down = 1
	left = 2
	right = 3


# abstract class for robot agent
class RobotAgent(metaclass=ABCMeta):

	# default the agent starts in trainingmode
	self.trainingmode = True

	# choose action based on current state
	@abstractmethod
	def choose_action(self, curr_state):
		pass

	# receive reward for a action that moved agent from old to new state
	# new_state is None if terminated
	@abstractmethod
	def incorporate_reward(self, old_state, action, new_state, value):
		pass

	# return if the agent currently is in training mode or not
	def is_in_training_mode(self):
		return self.training_mode