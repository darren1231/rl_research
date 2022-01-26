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
import csv

def run(n,maze_h,maze_w,Param):

    ############################
    map_dict = {True:"use combine q",False:"normal q"}
    if_c = Param.COMBINE_Q
    experiment_name = "ex2_{}_{}_{}_{}_{}".format(map_dict[if_c],\
        str(Param.ALPHA_P),str(Param.GAMMA_P),\
        str(Param.ALPHA),str(Param.GAMMA))
    ############################

    width=100
    surface=create_window(maze_w,maze_h,width)
    maxEpisodes=100
    environment=Environment(maze_w,maze_h)
    agent=Q_learning_agent(n,environment)
    
    
    rlglue=RLGlue(environment,agent,surface,width,time_sleep=0)
    rlglue.rl_init()
    # np.random.seed(0)
    

    reward_list =[]
    with open('{}.csv'.format(experiment_name), 'w', newline='') as csvfile:
    # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile,delimiter=' ')

        for i in range(maxEpisodes):
            rlglue.rl_episode()
            print("{}".format(i)+"Steps took in this episode was %d" %(rlglue.num_ep_steps()))
            
            steps= rlglue.num_ep_steps()
            reward_list.append(steps)

            writer.writerow([steps])

    
    plt.plot(reward_list,label="{}".format(map_dict[if_c]))
    plt.legend()

    plt.savefig('{}.png'.format(experiment_name))
    # plt.show()

def create_window(maze_w,maze_h,width):

    title = "Dyna Maze"
    size = (maze_w*width,maze_h*width)
    pygame.init()
    surface = pygame.display.set_mode(size,0,0)
    # surface = pygame.display.set_mode((20,20),0,0)
    pygame.display.set_caption(title)

    return surface

loop_range = np.arange(0.1,1,0.1)
ex_list = loop_range.tolist()

for alpha_p in ex_list:
    for gamma_p in ex_list:
        for alpha in ex_list:
            for gamma in ex_list:
                Param.ALPHA_P=alpha_p
                Param.GAMMA_P= gamma_p
                Param.ALPHA= alpha
                Param.GAMMA= gamma

                
                Param.COMBINE_Q=True
                run(0,5,5,Param)
                Param.COMBINE_Q=False
                run(0,5,5,Param)
                plt.clf()

# for i in [3,4]:
#     random.seed(i)
#     Param.COMBINE_Q=True
#     run(0,i,i,True)

#     random.seed(i+1)
#     Param.COMBINE_Q=False
#     run(0,i,i,False)
#     plt.clf()

# random.seed(3)
# print (random.random())
# Param.COMBINE_Q=True
# run(0,5,5,False)
# run(int(sys.argv[1]))


