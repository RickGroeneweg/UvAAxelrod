from .country import *
from geopy import distance


def reward(country, other, d):
    return (country.e -  country.i*other.e)*other.m / d

def temptation(country, other, d):
    return country.e*other.m / d

def sucker(country, other, d):
    return -country.i*other.e*other.m / d

def punishment(country, other, d):
    return 0
