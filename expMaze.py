"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018, University of Alberta.
  Implementation of the interaction between the Gambler's problem environment
  and the Monte Carlo agent using RLGlue.
"""
from rl_glue import RLGlue
from envMaze import Environment
from agentMaze import Q_learning_agent
import pygame
import numpy as np
import sys
import matplotlib.pyplot as plt

def run(n,maze_h,maze_w):

    width=100
    surface=create_window(maze_w,maze_h,width)
    maxEpisodes=100
    environment=Environment(maze_w,maze_h)
    agent=Q_learning_agent(n,environment)
    
    
    rlglue=RLGlue(environment,agent,surface,width)
    rlglue.rl_init()
    np.random.seed(0)

    reward_list =[]
    for i in range(maxEpisodes):
        rlglue.rl_episode()
        print("{}".format(i)+"Steps took in this episode was %d" %(rlglue.num_ep_steps()))
        reward_list.append(rlglue.num_ep_steps())

    plt.plot(reward_list)
    plt.savefig('n_{}_{}_{}.png'.format(n,maze_h,maze_w))
    # plt.show()

def create_window(maze_w,maze_h,width):

    title = "Dyna Maze"
    size = (maze_w*width,maze_h*width)
    pygame.init()
    surface = pygame.display.set_mode(size,0,0)
    # surface = pygame.display.set_mode((20,20),0,0)
    pygame.display.set_caption(title)

    return surface
# for i in [10,20]:
run(5,5,5)
# run(int(sys.argv[1]))


