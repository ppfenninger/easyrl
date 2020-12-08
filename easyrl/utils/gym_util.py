from copy import deepcopy

import gym
import numpy as np
from gym.spaces import Box
from gym.spaces import Dict
from gym.spaces import Discrete
from gym.spaces import MultiBinary
from gym.spaces import MultiDiscrete
from gym.spaces import Tuple
from gym.wrappers.time_limit import TimeLimit

from easyrl.envs.dummy_vec_env import DummyVecEnv
from easyrl.envs.shmem_vec_env import ShmemVecEnv
from easyrl.envs.timeout import TimeOutEnv
from easyrl.utils.rl_logger import logger


def num_space_dim(space):
    if isinstance(space, Box):
        return int(np.prod(space.shape))
    elif isinstance(space, Discrete):
        return int(space.n)
    elif isinstance(space, Tuple):
        return int(sum([num_space_dim(s) for s in space.spaces]))
    elif isinstance(space, Dict):
        return int(sum([num_space_dim(s) for s in space.spaces.values()]))
    elif isinstance(space, MultiBinary):
        return int(space.n)
    elif isinstance(space, MultiDiscrete):
        return int(np.prod(space.shape))
    else:
        raise NotImplementedError


def make_vec_env(env_id, num_envs, seed=1, no_timeout=True, env_kwargs=None):
    logger.info(f'Creating {num_envs} environments.')
    if env_kwargs is None:
        env_kwargs = {}

    def make_env(env_id, rank, seed, no_timeout, env_kwargs):
        def _thunk():
            env = gym.make(env_id, **env_kwargs)
            if no_timeout:
                env = TimeOutEnv(env)
            env.seed(seed + rank)
            return env

        return _thunk

    envs = [make_env(env_id,
                     idx,
                     seed,
                     no_timeout,
                     env_kwargs) for idx in range(num_envs)]
    if num_envs > 1:
        envs = ShmemVecEnv(envs, context='spawn')
    else:
        envs = DummyVecEnv(envs)
    return envs


def get_render_images(env):
    try:
        img = env.get_images()
    except AttributeError:
        try:
            img = env.render('rgb_array')
        except AttributeError:
            raise AttributeError('Cannot get rendered images.')
    return deepcopy(img)


def is_time_limit_env(env):
    if not (isinstance(env, TimeLimit)):
        if not hasattr(env, 'env') or (hasattr(env, 'env') and not isinstance(env.env, TimeLimit)):
            return False
    return True
