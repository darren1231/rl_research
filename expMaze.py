"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018, University of Alberta.
  Implementation of the interaction between the Gambler's problem environment
  and the Monte Carlo agent using RLGlue.
"""
from cProfile import label
from rl_glue import RLGlue
from envMaze import Environment
from agentMaze import Q_learning_agent
import pygame
import numpy as np
import sys
import matplotlib.pyplot as plt
from param import Param
import random 

def run(n,maze_h,maze_w,if_c):

    width=50
    surface=create_window(maze_w,maze_h,width)
    maxEpisodes=100
    environment=Environment(maze_w,maze_h)
    agent=Q_learning_agent(n,environment)
    
    
    rlglue=RLGlue(environment,agent,surface,width,time_sleep=0)
    rlglue.rl_init()
    # np.random.seed(0)

    reward_list =[]
    for i in range(maxEpisodes):
        rlglue.rl_episode()
        print("{}".format(i)+"Steps took in this episode was %d" %(rlglue.num_ep_steps()))
        reward_list.append(rlglue.num_ep_steps())

    map_dict = {True:"use combine q",False:"normal q"}
    plt.plot(reward_list,label="{}".format(map_dict[if_c]))
    plt.legend()

    plt.savefig('afterdebug_20220125_{}X{}.png'.format(maze_h,maze_w))
    # plt.show()

def create_window(maze_w,maze_h,width):

    title = "Dyna Maze"
    size = (maze_w*width,maze_h*width)
    pygame.init()
    surface = pygame.display.set_mode(size,0,0)
    # surface = pygame.display.set_mode((20,20),0,0)
    pygame.display.set_caption(title)

    return surface




for i in range(3,6):
    random.seed(i)
    Param.COMBINE_Q=True
    run(0,i,i,True)

    random.seed(i+1)
    Param.COMBINE_Q=False
    run(0,i,i,False)
    plt.clf()

# random.seed(3)
# print (random.random())
# Param.COMBINE_Q=True
# run(0,5,5,False)
# run(int(sys.argv[1]))


