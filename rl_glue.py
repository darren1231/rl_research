"""
  Purpose: For use in the Reinforcement Learning course, Fall 2018, University of Alberta.
  Glues together an experiment, agent, and environment.
"""
from abc import ABCMeta, abstractmethod
from tracemalloc import start
import pygame
import numpy as np
import time

class RLGlue:
    """
    Facilitates interaction between an agent and environment for
    reinforcement learning experiments.

    args:
        env_obj: an object that implements BaseEnvironment
        agent_obj: an object that implements BaseAgent
    """

    def __init__(self, env_obj, agent_obj,surface,width,time_sleep):
        self._environment = env_obj
        self._agent = agent_obj
        self.maze_h = self._environment._maze_h
        self.maze_w = self._environment._maze_w
        # useful statistics
        self._total_reward = None
        self._num_steps = None  # number of steps in entire experiment
        self._num_episodes = None  # number of episodes in entire experiment
        self._num_ep_steps = None  # number of steps in this episode

        # the most recent action taken by the agent
        self._last_action = None

        #################attributes of Game
        self.surface = surface
        self.bg_color = pygame.Color('black')
        self.pause_time = 0.04
        self.close_clicked = False
        self.continue_game = True
        self.normal_color=pygame.Color('white')
        self.wall_color=pygame.Color('gray')
        self.w=width
        self.margin=1
        self.maze=[[0]*(self.maze_h+1) for n in range(self.maze_w+1)]
        self.start = (0,0)
        self.goal = (self.maze_w-1,self.maze_h-1)
        # self.start=(np.random.randint(0,9),np.random.randint(0,6))
        # self.goal=(np.random.randint(0,9),np.random.randint(0,6))
        color_tags=[hex(0xffffff),hex(0xedffed),hex(0xdbffdb),hex(0xc9ffc9),hex(0xb7ffb7),hex(0xa5ffa5),hex(0x93ff93),hex(0x81ff81),hex(0x6fff6f),hex(0x5dff5d)]
        self.color=dict(zip(list(range(10)),color_tags))
        self.time_sleep = time_sleep

    def handle_event(self):
        event=pygame.event.poll()
        if event.type == pygame.QUIT:
            self.close_clicked=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            y=pos[0] // (self.w+self.margin)
            x=pos[1] // (self.w+self.margin)
            if self.maze[y][x] == 0:
                self.maze[y][x]=1
            elif self.maze[y][x] == 1:
                self.maze[y][x]=0
            self._environment.update_wall(self.maze)

    def drawGrid(self):

        self.surface.fill(self.bg_color)
        for row in range(self._environment._maze_w+1):
            for col in range(self._environment._maze_h+1):
                grid=[(self.margin+self.w)*row+self.margin,(self.margin+self.w)*col+self.margin,self.w,self.w]
                if self.maze[row][col] == 1:
                    pygame.draw.rect(self.surface,self.wall_color,grid)
                    
                else:
                    value=(self._agent.calValue((row,col))*100)//10

                    if value<0 or value>9: value=0#debug                    
                    pygame.draw.rect(self.surface,pygame.Color(self.color[value]),grid)
                 
    
    def drawActionValue(self):
        for row in range(self.maze_w+1):
            for col in range(self.maze_h+1):
                start_pos = [(self.margin+self.w)*row+self.margin,(self.margin+self.w)*col+self.margin]
                end_pos =  [(self.margin+self.w)*(row+1)+self.margin,(self.margin+self.w)*(col+1)+self.margin]
                pygame.draw.line(self.surface, pygame.Color('red'), start_pos, end_pos)

                start_pos = [(self.margin+self.w)*row+self.margin,(self.margin+self.w)*(col+1)+self.margin]
                end_pos =  [(self.margin+self.w)*(row+1)+self.margin,(self.margin+self.w)*col+self.margin]
                pygame.draw.line(self.surface, pygame.Color('blue'), start_pos, end_pos)

        
        pygame.font.init() # you have to call this at the start, if you want to use this module.
        myfont = pygame.font.SysFont('Comic Sans MS', 10)
        # text = str(round(self._agent.Q[0,0,"right"],2))
        # start = myfont.render(text, False, (0, 0, 0))
        # self.surface.blit(start,(0,0))

        for row in range(self.maze_w+1):
            for col in range(self.maze_h+1):
                x= self.w*row
                y = self.w*col


                coordinate_dict = {"up":[0.5,0.1],"down":[0.5,0.75],"left":[0.25,0.5],"right":[0.75,0.5]}
                for action in ["up","down","left","right"]:
                    text = str(round(self._agent.Q[row,col,action],2))
                    render = myfont.render(text, False, (0, 0, 0))
                    coordinate = x + coordinate_dict[action][0]*self.w, y+coordinate_dict[action][1]*self.w
                    self.surface.blit(render,coordinate)
                
                coordinate_dict = {"up":[0.5,0.2],"down":[0.5,0.85],"left":[0.25,0.6],"right":[0.75,0.6]}
                for action in ["up","down","left","right"]:
                    text = str(round(self._agent.Q_p[row,col,action],2))
                    render = myfont.render(text, False, (0, 0, 0))
                    coordinate = x + coordinate_dict[action][0]*self.w, y+coordinate_dict[action][1]*self.w
                    self.surface.blit(render,coordinate)

                # up_text = str(round(self._agent.Q[row,col,"up"],2))
                # down_text = str(round(self._agent.Q[row,col,"down"],2))
                # left_text = str(round(self._agent.Q[row,col,"left"],2))
                # right_text = str(round(self._agent.Q[row,col,"right"],2))

                # up_render = myfont.render(up_text, False, (0, 0, 0))
                # down_render = myfont.render(down_text, False, (0, 0, 0))
                # left_render = myfont.render(left_text, False, (0, 0, 0))
                # right_render = myfont.render(right_text, False, (0, 0, 0))

                # uptext_coordinate = x + 0.5*self.w, y+0.1*self.w
                # downtext_coordinate = x + 0.5*self.w, y+0.75*self.w
                # lefttext_coordinate = x + 0.25*self.w, y+0.5*self.w
                # righttext_coordinate = x + 0.75*self.w, y+0.5*self.w
                
                # self.surface.blit(up_render,uptext_coordinate)
                # self.surface.blit(down_render,downtext_coordinate)
                # self.surface.blit(left_render,lefttext_coordinate)
                # self.surface.blit(right_render,righttext_coordinate)

                

    def showChar(self):
        pygame.font.init()
        myfont=pygame.font.SysFont('Comic Sans MS', 45)
        start = myfont.render('S', False, (0, 0, 0))
        self.surface.blit(start,(self.start[0]*(self.w+self.margin)+20,self.start[1]*(self.w+self.margin)+20))

        goal = myfont.render('G', False, (0, 0, 0))
        self.surface.blit(goal,(self.goal[0]*(self.w+self.margin)+20,self.goal[1]*(self.w+self.margin)+20))

    def drawBlackBox(self,pos):
        x,y=pos
        grid=[(self.margin+self.w)*x+self.margin,(self.margin+self.w)*y+self.margin,self.w,self.w]
        pygame.draw.rect(self.surface,self.bg_color,grid)

    ###############
    def total_reward(self):
        return self._total_reward

    def num_steps(self):
        return self._num_steps

    def num_episodes(self):
        return self._num_episodes

    def num_ep_steps(self):
        return self._num_ep_steps

    def rl_init(self):
        # reset statistics
        self._total_reward = 0
        self._num_steps = 0
        self._num_episodes = 0
        self._num_ep_steps = 0

        # reset last action
        self._last_action = None

        # reset agent and environment
        self._agent.agent_init()
        self._environment.env_init(self.maze)

    def rl_start(self):
        """
        Starts RLGlue experiment.

        Returns:
            tuple: (state, action)
        """
        self._num_ep_steps = 1
        self._num_steps = max(self._num_steps, 1)

        state = self._environment.env_start(self.maze,self.start,self.goal)
        self._last_action = self._agent.agent_start(state)

        return state, self._last_action

    def rl_step(self):
        """Takes a step in the RLGlue experiment.

        Returns:
            (float, state, action, Boolean): reward, last state observation,
                last action, boolean indicating termination
        """
        reward, state, terminal = self._environment.env_step(self._last_action)

        self._total_reward += reward

        if terminal:
            self._num_episodes += 1
            self._agent.agent_end(reward)
            self._last_action = None
            self._agent.agent_step(reward, state)
        else:
            self._num_ep_steps += 1
            self._num_steps += 1
            self._last_action = self._agent.agent_step(reward, state)

        return reward, state, self._last_action, terminal

    ### CONVENIENCE FUNCTIONS BELOW ###
    def rl_env_start(self):
        """
        Useful when manually specifying agent actions (for debugging). Starts
        RL-Glue environment.

        Returns:
            state observation
        """
        self._num_ep_steps = 0

        return self._environment.env_start()

    def rl_env_step(self, action):
        """
        Useful when manually specifying agent actions (for debugging).Takes a
        step in the environment based on an action.

        Args:
            action: Action taken by agent.

        Returns:
            (float, state, Boolean): reward, state observation, boolean
                indicating termination.
        """
        reward, state, terminal = self._environment.env_step(action)

        self._total_reward += reward

        if terminal:
            self._num_episodes += 1
        else:
            self._num_ep_steps += 1
            self._num_steps += 1

        return reward, state, terminal

    def rl_episode(self, max_steps_this_episode=0):
        """
        Convenience function to run an episode.

        Args:
            max_steps_this_episode (Int): Max number of steps in this episode.
                A value of 0 will result in the episode running until
                completion.

        returns:
            Boolean: True if the episode terminated within
                max_steps_this_episode steps, else False
        """
        terminal = False
        self.rl_start()

        while not terminal and ((max_steps_this_episode <= 0) or
                                (self._num_ep_steps < max_steps_this_episode)) and not self.close_clicked:
            self.handle_event()
            self.drawGrid()
            self.drawActionValue()
            self.showChar()
            _, state, _, terminal = self.rl_step()
            self.drawBlackBox(state)

            time.sleep(self.time_sleep)
            pygame.display.update()

            

        return terminal

    def rl_agent_message(self, message):
        """
        pass a message to the agent

        Args:
            message (str): the message to pass

        returns:
            str: the agent's response
        """
        if message is None:
            message_to_send = ""
        else:
            message_to_send = message

        the_agent_response = self._agent.agent_message(message_to_send)
        if the_agent_response is None:
            the_agent_response = ""

        return the_agent_response

    def rl_env_message(self, message):
        """
        pass a message to the environment

        Args:
            message (str): the message to pass

        Returns:
            the_env_response (str) : the environment's response
        """
        if message is None:
            message_to_send = ""
        else:
            message_to_send = message

        the_env_response = self._environment.env_message(message_to_send)
        if the_env_response is None:
            return ""

        return the_env_response


class BaseAgent:
    """
    Defines the interface of an RLGlue Agent

    ie. These methods must be defined in your own Agent classes
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """Declare agent variables."""
        pass

    @abstractmethod
    def agent_init(self):
        """Initialize agent variables."""

    @abstractmethod
    def agent_start(self, state):
        """
        The first method called when the experiment starts, called after
        the environment starts.
        Args:
            state (state observation): The agent's current state

        Returns:
            The first action the agent takes.
        """

    @abstractmethod
    def agent_step(self, reward, state):
        """
        A step taken by the agent.
        Args:
            reward (float): the reward received for taking the last action taken
            state (state observation): The agent's current state
        Returns:
            The action the agent is taking.
        """

    @abstractmethod
    def agent_end(self, reward):
        """
        Run when the agent terminates.
        Args:
            reward (float): the reward the agent received for entering the
                terminal state.
        """

    @abstractmethod
    def agent_message(self, message):
        """
        receive a message from rlglue
        args:
            message (str): the message passed
        returns:
            str : the agent's response to the message (optional)
        """


class BaseEnvironment:
    """
    Defines the interface of an RLGlue environment

    ie. These methods must be defined in your own environment classes
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """Declare environment variables."""

    @abstractmethod
    def env_init(self):
        """
        Initialize environment variables.
        """

    @abstractmethod
    def env_start(self):
        """
        The first method called when the experiment starts, called before the
        agent starts.

        Returns:
            The first state observation from the environment.
        """

    @abstractmethod
    def env_step(self, action):
        """
        A step taken by the environment.

        Args:
            action: The action taken by the agent

        Returns:
            (float, state, Boolean): a tuple of the reward, state observation,
                and boolean indicating if it's terminal.
        """

    @abstractmethod
    def env_message(self, message):
        """
        receive a message from RLGlue
        Args:
           message (str): the message passed
        Returns:
           str: the environment's response to the message (optional)
        """
