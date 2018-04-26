from .country import *
from .city_coordinates import *
from .strategies import *
from .match import *
from .tournament import *

netherlands =  Country("Netherlands", 17, Amsterdam, 0.1, 0.1, collaborate)
germany = Country("Germany", 80, Berlin, 0.1, 0.1, collaborate)
uk = Country("United Kingdom", 60, London, 0.1, 0.1, defect)
france = Country("France", 70, Paris, 0.1, 0.1, tit_for_tat)
italy = Country("Italy", 60, Rome, 0.1, 0.1, random_move)
sweden = Country("Sweden", 12, Stockholm, 0.1,0.1, random_move)
denmark = Country("Denmark", 7, Copenhagen, 0.1,0.1, tit_for_tat)
belgium = Country("Belgium", 10, Brussels, 0.1,0.1, random_move)
china = Country("China", 800, Beijing, 0.1,0.1, grudge)
india = Country("India", 600, NewDelhi, 0.1,0.1, alternate)
us = Country("United States", 300, WashingtonDC, 0.1,0.1, defect)
canada = Country("Canada", 20, Ottawa, 0.1,0.1, collaborate)
japan = Country("Japan", 100, Tokyo, 0.1, 0.1, collaborate)
russia = Country("Russia", 200, Moscow, 0.1, 0.1, random_move)
southAfrica = Country("South Africa", 50, Johannesburg, 0.1,0.1, tit_for_tat)
northKorea = Country("North Korea", 30, Pyongyang, 0.1,0.1, defect)
southKorea = Country("South Korea", 50, Seoul, 0.1,0.1, tit_for_tat)
australia = Country("Australia", 25, Sydney, 0.1,0.1, collaborate)
newZealand = Country("New Zealand", 5, Auckland, 0.1,0.1, collaborate)
spain = Country("Spain", 50, Madrid, 0.1,0.1, random_move)
israel = Country("Israel", 12, TelAviv, 0.1,0.1, defect)
ireland = Country("Ireland", 5, Dublin, 0.1,0.1, tit_for_tat)
finland = Country("Finland", 9, Helsinki, 0.1,0.1, random_move)
portugal = Country("Portugal", 7, Lisbon, 0.1,0.1, random_move)
brazil = Country("Brazil", 208, Brasilia, 0.1,0.1, tit_for_tat)
argentina = Country("Argentina", 40, BuanosAires, 0.1,0.1, grudge)
indonesia = Country("Indonesia", 260, Jakarta, 0.1,0.1, random_move)
pakistan = Country("Pakistan", 190, Islamabad, 0.1,0.1, collaborate)
nigeria = Country("Nigeria", 180, Abuja, 0.1,0.1, collaborate)
egypt = Country("Egypt", 96, Cairo, 0.1,0.1, random_move)
mexico = Country("Mexico", 127, MexicoCity, 0.1, 0.1, alternate)
ethiopia = Country("Ethiopia", 100, AddisAbaba, 0.1,0.1, alternate)




tour = Tournament(netherlands, germany, uk, france, italy, sweden, denmark, belgium, china, \
    india, us, canada, japan, russia, southAfrica, northKorea, southKorea, australia, newZealand, spain, \
    israel, ireland, finland, portugal, brazil, argentina, indonesia, pakistan, nigeria,\
    egypt, mexico, ethiopia)

tourtje = TournamentRound(netherlands, southKorea, finland, newZealand)
