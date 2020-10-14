from cv2 import cvtColor, COLOR_BGR2GRAY, resize, INTER_AREA
import numpy as np
import gym



def atari_enduro_processor(raw_frame):
    # convert input frame to gray scale
    gray_frame = cvtColor(raw_frame, COLOR_BGR2GRAY)
    # resize frame
    resized_frame = resize(gray_frame, (84, 105), interpolation=INTER_AREA)
    # return cropped frame
    return(resized_frame[0:84])

def atari_montezuma_processor(raw_frame):
    # convert input frame to gray scale
    gray_frame = cvtColor(raw_frame, COLOR_BGR2GRAY)
    # resize frame
    resized_frame = resize(gray_frame, (84, 105), interpolation=INTER_AREA)
    # return cropped frame
    return(resized_frame[15:99])

def atari_pong_processor(raw_frame):
    # convert input frame to gray scale
    gray_frame = cvtColor(raw_frame, COLOR_BGR2GRAY)
    # resize frame
    resized_frame = resize(gray_frame, (84, 111), interpolation=INTER_AREA)
    # return cropped frame
    return(resized_frame[18:102])

def atari_spaceinvaders_processor(raw_frame):
    # convert input frame to gray scale
    gray_frame = cvtColor(raw_frame, COLOR_BGR2GRAY)
    # resize frame
    resized_frame = resize(gray_frame, (84, 97), interpolation=INTER_AREA)
    # return cropped frame
    return(resized_frame[6:90])

def atari_breakout_processor(raw_frame):
    # convert input frame to gray scale
    gray_frame = cvtColor(raw_frame, COLOR_BGR2GRAY)
    # resize frame
    resized_frame = resize(gray_frame, (84, 105), interpolation=INTER_AREA)
    # return cropped frame
    return(resized_frame[15:99])

def atari_mspacman_processor(raw_frame):
    # convert input frame to gray scale
    gray_frame = cvtColor(raw_frame, COLOR_BGR2GRAY)
    # resize frame
    resized_frame = resize(gray_frame, (84, 102), interpolation=INTER_AREA)
    # return cropped frame
    return(resized_frame[0:84])




class ProcessedAtariEnv(gym.Wrapper):
    """
    ***********************
    ** ProcessedAtariEnv **
    ***********************
        Class for handling some preprocessing techniques 
        (such as processing frames, actions or rewards) 
        for the openai gym environment wrappers

        -----------
        Parameters:
        -----------
            env:                 object;
                                 the basic (possibly already wrapped) OpenAI gym environment
            
            frame_processor:     callable;
                                 function for processing (eg. grayscale conversion, resizing, cropping) the raw frames

            action_processor:    callable;
                                 function for processing the raw actions

            reward_processor:    callable;
                                 function for processing the raw rewards

            neg_reward_terminal: bool;
                                 variable indicating that a negative reward is considered as the end of an episode
    """
    
    def __init__(self, 
                 env = gym.make('PongDeterministic-v4'), 
                 frame_processor = atari_pong_processor,
                 action_processor = lambda x: x, 
                 reward_processor = lambda x: x,
                 neg_reward_terminal = False):
        gym.Wrapper.__init__(self, env)
        self.frame_processor = frame_processor
        self.action_processor = action_processor
        self.reward_processor = reward_processor
        self._unprocessed_reward = 0.
        self._unprocessed_frame = self.env.reset()
        self.neg_reward_terminal = neg_reward_terminal
    
  
    def true_reset(self):
        """Perform a true reset on OpenAI's EpisodicLifeEnv"""
        return(self.unwrapped.reset())
    
    def reset(self):
        """Reset the environment and return the processed frame"""
        return(self.frame_processor(self.env.reset()))
    
    def step(self, action):
        """Perform one step in the processed environment"""
        action = self.action_processor(action)
        frame, reward, done, info = self.env.step(action)
        self._unprocessed_reward = reward
        self._unprocessed_frame = frame
        if self.neg_reward_terminal:
            done = done or reward < 0
        return(self.frame_processor(frame), self.reward_processor(reward), done, info)


        
