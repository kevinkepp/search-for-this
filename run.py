import random

from lat.DeepQAgent import DeepQAgent
from lat.Evaluator import Evaluator
from lat.QAgent import QAgent
from lat.RandomAgent import RandomAgent
from lat.OldSimulator import Simulator, Actions
from lat.KerasMlpModel import KerasMlpModel


EPOCHS = 3000
GRID_SIZE = 5
MAX_STEPS = pow(GRID_SIZE, 1.7)

ACTIONS = Actions.all()
agent = RandomAgent(ACTIONS)
env_rand = Simulator(agent, MAX_STEPS, GRID_SIZE)

ALPHA = 1  # optimal for deterministic env
GAMMA = 0.975  #
Q_INIT = lambda state, action: random.random()
agent_q = QAgent(ACTIONS, ALPHA, GAMMA, Q_INIT)
env_q = Simulator(agent_q, MAX_STEPS, GRID_SIZE)

MODEL_IN_LAYER_SIZE = GRID_SIZE * GRID_SIZE
MODEL_HID_LAYER_SIZES = []
MODEL_OUT_LAYER_SIZE = len(ACTIONS)
model = KerasMlpModel(MODEL_IN_LAYER_SIZE, MODEL_HID_LAYER_SIZES, MODEL_OUT_LAYER_SIZE)
EPSILON = 1
EPSILON_UPDATE = lambda e: e - 1 / EPOCHS if e > 0.1 else e
agent_deep_q = DeepQAgent(ACTIONS, GAMMA, EPSILON, EPSILON_UPDATE, model)
env_deep_q1 = Simulator(agent_deep_q, MAX_STEPS, GRID_SIZE)

MODEL_HID_LAYER_SIZES = []
model = KerasMlpModel(MODEL_IN_LAYER_SIZE, MODEL_HID_LAYER_SIZES, MODEL_OUT_LAYER_SIZE)
agent_deep_q = DeepQAgent(ACTIONS, GAMMA, EPSILON, EPSILON_UPDATE, model)
env_deep_q2 = Simulator(agent_deep_q, MAX_STEPS, GRID_SIZE)

MODEL_HID_LAYER_SIZES = [50]
model = KerasMlpModel(MODEL_IN_LAYER_SIZE, MODEL_HID_LAYER_SIZES, MODEL_OUT_LAYER_SIZE)
agent_deep_q = DeepQAgent(ACTIONS, GAMMA, EPSILON, EPSILON_UPDATE, model)
env_deep_q2 = Simulator(agent_deep_q, MAX_STEPS, GRID_SIZE)

MODEL_HID_LAYER_SIZES = [150, 75]
model = KerasMlpModel(MODEL_IN_LAYER_SIZE, MODEL_HID_LAYER_SIZES, MODEL_OUT_LAYER_SIZE)
agent_deep_q = DeepQAgent(ACTIONS, GAMMA, EPSILON, EPSILON_UPDATE, model)
env_deep_q3 = Simulator(agent_deep_q, MAX_STEPS, GRID_SIZE)

envs = [env_rand, env_q, env_deep_q1, env_deep_q2, env_deep_q3]
names = ["RandomAgent", "QAgent", "DeepQAgent[]", "DeepQAgent[50]", "DeepQAgent[150,100]"]
Evaluator(envs, names, EPOCHS, grid="{0}x{1}".format(GRID_SIZE, GRID_SIZE), gamma=GAMMA).run()