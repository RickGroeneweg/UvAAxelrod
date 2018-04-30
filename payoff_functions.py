from .country import *
from geopy import distance
from math import sqrt

def reward(country, other, d):
    '''calculates how much reward would change fitness'''
    return (country.e -  country.i*other.e)*other.m / d

def temptation(country, other, d):
    '''calculates how much temptation would change fitness'''
    return country.e*other.m / d

def sucker(country, other, d):
    '''calculates how much sucker would change fitness'''
    return -country.i*other.e*other.m / d

def punishment(country, other, d):
    '''calculates how much punishment would chage fitness'''
    return 0
