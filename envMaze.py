"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018,
  University of Alberta.
  Gambler's problem environment using RLGlue.
"""
from rl_glue import BaseEnvironment
import numpy as np


class Environment(BaseEnvironment):

    def __init__(self,maze_w,maze_h):
        """Declare environment variables."""
        self._maze_h = maze_h
        self._maze_w = maze_w
        self.goal = (self._maze_w-1,self._maze_h-1)

    def env_init(self,maze):
        """
        Arguments: Nothing
        Returns: Nothing
        Hint: Initialize environment variables necessary for run.
        """
        self.state=None
        self.terminal=None
        self.update_wall(maze)

    def env_start(self,maze,start,goal):
        """
        Arguments: Nothing
        Returns: state - numpy array
        Hint: Sample the starting state necessary for exploring starts and return.
        """

        self.state=start
        self.terminal=goal
        return self.state

    def env_step(self, action):
        """
        Arguments: action - integer
        Returns: reward - float, state - numpy array - terminal - boolean
        Hint: Take a step in the environment based on dynamics; also checking for action validity in
        state may help handle any rogue agents.
        """
        #calculate next state based on the action taken
        # origin_x,origin_y = self.state
        testState=tuple(map(sum,zip(self.state,action)))
        x,y=testState
        

        #hit wall
        if x<0 or x>=self._maze_w or y<0 or y>=self._maze_h:
            return -10,self.state,False 
        
        #hit goal
        elif testState==self.goal:
            return 1,self.state,True
        
        #normal
        else:
            self.state =testState
            return 0,self.state,False

        

        

    def env_message(self, in_message):
        """
        Arguments: in_message - string
        Returns: response based on in_message
        This function is complete. You do not need to add code here.
        """
        if in_message == "return":
            return self.state

    def update_wall(self,maze):
        self.wall=set([])
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 1:
                    self.wall.add((row,col))

    def update_start_gola(self,start,goal):
        self.state=start
        self.terminal=goal
