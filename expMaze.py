"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018, University of Alberta.
  Implementation of the interaction between the Gambler's problem environment
  and the Monte Carlo agent using RLGlue.
"""
from rl_glue import RLGlue
from envMaze import Environment
from agentMaze import MazeAgent,Q_learning_agent
import pygame
import numpy as np
import sys

def run(n):

    surface=create_window()
    maxEpisodes=200
    environment=Environment(6,6)
    agent=Q_learning_agent(n,environment)
    
    rlglue=RLGlue(environment,agent,surface)
    rlglue.rl_init()
    np.random.seed(0)

    for i in range(maxEpisodes):
        rlglue.rl_episode()
        print("Steps took in this episode was %d" %(rlglue.num_ep_steps()))

def create_window():

    title = "Dyna Maze"
    size = (550,370)
    pygame.init()
    surface = pygame.display.set_mode(size,0,0)
    pygame.display.set_caption(title)

    return surface

run(10)
# run(int(sys.argv[1]))


