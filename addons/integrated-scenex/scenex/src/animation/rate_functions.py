# """
# Animation rate functions for SceneX.
# Controls timing and easing of animations.
# """

# import math
# from typing import Callable
# from ..core.config import RateFuncType

# class RateFunc:
#     """Collection of animation rate functions"""
    
#     @staticmethod
#     def linear(t: float) -> float:
#         return t
    
#     @staticmethod
#     def smooth(t: float) -> float:
#         return t * t * (3 - 2 * t)
    
#     @staticmethod
#     def rush_into(t: float) -> float:
#         return 2 * t * t
    
#     @staticmethod
#     def rush_from(t: float) -> float:
#         return t * (2 - t)
    
#     @staticmethod
#     def ease_in(t: float) -> float:
#         return t * t * t
    
#     @staticmethod
#     def ease_out(t: float) -> float:
#         return (t - 1) * (t - 1) * (t - 1) + 1
    
#     @staticmethod
#     def get_function(rate_type: RateFuncType) -> Callable[[float], float]:
#         return {
#             RateFuncType.LINEAR: RateFunc.linear,
#             RateFuncType.SMOOTH: RateFunc.smooth,
#             RateFuncType.RUSH_INTO: RateFunc.rush_into,
#             RateFuncType.RUSH_FROM: RateFunc.rush_from,
#             RateFuncType.EASE_IN: RateFunc.ease_in,
#             RateFuncType.EASE_OUT: RateFunc.ease_out,
#         }[rate_type]


# SceneX/src/animation/rate_functions.py

import math
from enum import Enum, auto
from typing import Callable

class RateFuncType(Enum):
    LINEAR = auto()
    SMOOTH = auto()
    RUSH_INTO = auto()
    RUSH_FROM = auto()
    EASE_IN = auto()
    EASE_OUT = auto()
    EASE_IN_OUT = auto()
    EXPONENTIAL = auto()
    ELASTIC = auto()
    BOUNCE = auto()
    BACK = auto()

class RateFunc:
    @staticmethod
    def linear(t: float) -> float:
        return t
    
    @staticmethod
    def smooth(t: float) -> float:
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def rush_into(t: float) -> float:
        return 2 * t * t
    
    @staticmethod
    def rush_from(t: float) -> float:
        return t * (2 - t)
    
    @staticmethod
    def ease_in(t: float) -> float:
        return t * t * t
    
    @staticmethod
    def ease_out(t: float) -> float:
        return 1 - (1 - t) * (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out(t: float) -> float:
        t *= 2
        if t < 1:
            return 0.5 * t * t * t
        t -= 2
        return 0.5 * (t * t * t + 2)

    @staticmethod
    def exponential(t: float) -> float:
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))
    
    @staticmethod
    def elastic(t: float) -> float:
        if t == 0 or t == 1:
            return t
        p = 0.3
        s = p / 4
        return -math.pow(2, 10 * (t - 1)) * math.sin((t - s) * (2 * math.pi) / p)
    
    @staticmethod
    def bounce(t: float) -> float:
        if t < (1/2.75):
            return 7.5625 * t * t
        elif t < (2/2.75):
            t -= (1.5/2.75)
            return 7.5625 * t * t + 0.75
        elif t < (2.5/2.75):
            t -= (2.25/2.75)
            return 7.5625 * t * t + 0.9375
        else:
            t -= (2.625/2.75)
            return 7.5625 * t * t + 0.984375
    
    @staticmethod
    def back(t: float) -> float:
        s = 1.70158
        return t * t * ((s + 1) * t - s)

    @classmethod
    def get_function(cls, rate_type: RateFuncType) -> Callable[[float], float]:
        return {
            RateFuncType.LINEAR: cls.linear,
            RateFuncType.SMOOTH: cls.smooth,
            RateFuncType.RUSH_INTO: cls.rush_into,
            RateFuncType.RUSH_FROM: cls.rush_from,
            RateFuncType.EASE_IN: cls.ease_in,
            RateFuncType.EASE_OUT: cls.ease_out,
            RateFuncType.EASE_IN_OUT: cls.ease_in_out,
            RateFuncType.EXPONENTIAL: cls.exponential,
            RateFuncType.ELASTIC: cls.elastic,
            RateFuncType.BOUNCE: cls.bounce,
            RateFuncType.BACK: cls.back
        }[rate_type]