import pandas as pd

from .country import Country

# TODO Sebastian: at the end of the file, there is a dictionary that should be
# filled with country-sqrt_area pairs

def get_WTO_countries(year):
    """
    construct a list of countries from the WTO data for a particular year
    
    parameters:
        - year: int
    
    side effects:
        - gets data from csv-files, `captial_dict` and `area_dict`
    
    returns:
        - list of countries
        
    """
    print('WARNING: the areas of countries are not yet set. All countries are now set with (sqrt) area 1. Do do something about this, the sqrt_area_dict in city_coordinates.py should be filled')
    
    df_e = pd.read_csv('country_data_e.csv', sep=';', na_values=[""])
    df_i = pd.read_csv('country_data_i.csv', sep=';', na_values=[""])
    df_m = pd.read_csv('country_data_m.csv', sep=';', na_values=[""])
    
    series_m = clean_and_get_year(df_m, year).rename('M')
    series_i = clean_and_get_year(df_i, year).rename('i')
    series_e = clean_and_get_year(df_e, year).rename('e')
    df = pd.concat([series_m, series_i, series_e], axis=1, sort=True)
    
    incomplete_data_df = df[pd.isnull(df).any(axis=1)]
    if len(incomplete_data_df) > 0:
        print('WARNING: for the following countries, the data was incomplete:')
        print(incomplete_data_df)
        
    df = df.dropna()
    
    countries = []
    for name in df.index:
        country = Country(
            name, 
            df['M'].at[name], 
            capital_dict[name], 
            df['e'].at[name], 
            df['i'].at[name], 
            1 # TODO: replace this with the square root of the area of the country
        )
        countries.append(country)
        
    return countries

def clean_and_get_year(df,year):
    clean_df = df.rename(columns={'Unnamed: 0': 'Coutnry'}).set_index('Coutnry')
    year = str(year)
    return clean_df[year].dropna()

AbuDhabi = (24, 53.64)
Abuja = (9.4, 7.29)
Accra = (5.56,-0.21)
Amman = (31.95,35.92)
Amsterdam = (52.37, 4.89)
Ankara = (39.92,32.85)
Antananarivo = (-18.91, 47.53)
Apia = (-13.83, -171.77)
Astana = (51.15, 71.44)
Asuncion = (-25.30, -57.63)
Athens = (37.28, 23.43)
Bamako = (12.61, -7.99)
BandarSeriBegawan = (4.89, 114.94)
Bangkok = (13.75, 100.82)
Bangui = (4.39, 18.55)
Banjul = (13.45, -16.58)
Basseterre = (17.30, -62.72)
Beijing = (39.91, 116.40)
Belmopan = (17.25, -88.77)
Berlin = (52.52, 13.41)
Bern = (46.5, 7.45)
Bishkek = (42.88, 74.59)
Bissau = (11.86, -15.58)
Bogota = (4.60, -74.08)
Brasilia = (-15.46, -47.55)
Bratislava = (48.14, 17.16)
Brazzaville = (-4.27, 15.27)
Bridgetown = (13.10, -59.62)
Brussels = (50.85, 4.35)
Bucharest = (44.44, 26.10)
Budapest = (47.50, 19.04)
BuenosAires = (-34.36, -58.22)
Bujumbura = (-3.36, 29.37)
Cairo = (30.01, 31.49)
Canberra = (-35.17, 149.07)
CapeTown = (-33.93, 18.42)
Caracas = (10.51, -66.91)
Castries = (14, -60.99)
Chaguanas = (10.51, -61.41)
Chisinau = (47.01, 28.86)
Conakry = (9.52, -13.70)
Copenhagen = (55.68, 12.57)
Dakar = (14.69, -17.45)
DaresSalaam = (-6.81, 39.28)
Dhaka = (23.76, 90.38)
Djibouti = (11.86, 42.76)
Doha = (25.30, 51.50)
Dublin = (53.21, -6.16)
Dushanbe = (38.54, 68.82)
Freetown = (8.48, -13.27)
Gaborone = (-24.66, 25.91)
Georgetown = (6.80, -58.16)
GuatemalaCity = (14.64, -90.51)
Hanoi = (21.03, 105.85)
Harare = (-17.83, 31.05)
Havana = (23.14, -82.37)
Helsinki = (60.17, 24.94)
HongKong = (22.29, 114.16)
Honiara = (-9.43, 159.96)
Islamabad = (33.43, 73.04)
Jakarta = (-6.12, 106.50)
Kabul = (34.53, 69.18)
Kampala = (0.318, 32.58)
Kathmandu = (27.71, 85.32)
Kiev = (50.45, 30.52)
Kigali = (-1.86, 30.13)
Kingston = (17.97, -76.79)
Kingstown = (13.16, -61.23)
Kinshasa = (-4.32, 15.31)
KualaLumpur = (3.15, 101.71)
KuwaitCity = (29.38, 47.97)
LaPaz = (-16.50, -68.13)
Libreville = (0.39, 9.45)
Lilongwe = (-13.97, 33.79)
Lima = (-12.06, -77.04)
Lisbon = (38.42, -9.70)
Ljubljana = (46.05, 14.51)
Lome = (6.13, 1.22)
London = (51.51, -0.13)
Luanda = (-8.83, 13.24)
Lusaka = (-15.42, 28.28)
Luxembourg = (49.37, 6.07)
Macau = (22.19, 113.54)
Madrid = (40.42, -3.70)
Male = (4.18, 73.51)
Managua = (12.15, -86.273717)
Manama = (26.22, 50.58)
Manila = (14.59, 120.98)
Maputo = (-26.05, 32.79)
Maseru = (-29.31, 27.48)
Mbabane = (-26.33, 31.14)
MexicoCity = (19.25, -99.07)
Monrovia = (6.33, -10.80)
Montevideo = (-34.91, -56.19)
Moscow = (55.45, 37.36)
Muscat = (23.51, 58.55)
Nairobi = (-1.28, 36.82)
Naypyidaw = (19.75, 96.13)
NDjamena = (12.12, 15.05)
NewDelhi = (28.61, 77.02)
Niamey = (13.50, 2.11)
Nicosia = (35.18, 33.37)
Nouakchott = (18.08, -15.98)
Nukualofa = (-21.13, -175.20)
Oslo = (59.91, 10.74)
Ottawa = (45.42, -75.69)
Ouagadougou = (12.37, -1.53)
PanamaCity = (8.97, -79.53)
Paramaribo = (5.82, -55.18)
Paris = (48.86, 2.35)
PhnomPenh = (11.57, 104.92)
Podgorica = (42.44, 19.26)
PortLouis = (-20.16, 57.5)
PortMoresby = (-9.47, 147.16)
PortVila = (-17.74, 168.32)
PortauPrince = (18.55, -72.34)
PortoNovo = (6.5, 2.63)
Prague = (50.09, 14.42)
Praia = (14.92, -23.51)
Quito = (-0.21, -78.5)
Rabat = (33.97, -6.84)
Reykjavik = (64.15, -21.94)
Riga = (56.94, 24.11)
Riyadh = (15.58, 32.57)
Rome = (41.89,12.48)
Roseau = (15.30, -61.39)
SanJose = (9.93, -84.08)
SanSalvador = (13.7, -89.19)
Sanaa = (15.42, 44.19)
Santiago = (-33.44, -70.65)
SantoDomingo = (18.48, -69.94)
Seoul = (37.57, 126.98)
Singapore = (1.29, 103.85)
Skopje = (42, 21.43)
Sofia = (42.70, 23.32)
SriJayawardenepuraKotte = (6.89, 79.92)
StGeorges = (12.05, -61.75)
StJohns = (17.12, -61.84)
Stockholm = (59.33,18.07)
Suva = (-18.14, 178.44)
Taipei = (25.04, 121.56)
Tallinn = (59.44, 24.75)
Tbilisi = (41.69, 44.80)
Tegucigalpa = (14.09, -87.20)
TelAviv = (32.08, 34.78)
Tirana = (41.33, 19.82)
Tokio = (34.70, 139.40)
Tunis = (33.84, 9.4)
Ulaanbaatar = (47.95, 106.97)
Vaduz = (47.14, 9.52)
Valletta = (35.9, 14.51)
Victoria = (-4.6232085, 55.452359)
Vienna = (48.21, 16.37)
Vientiane = (17.96, 102.61)
Vilnius = (54.69, 25.28)
Warsaw = (52.23, 21.01)
Washington = (38.52, -77.02)
Wellington = (-41.29, 174.78)
Windhoek = (-22.55, 17.05)
Yamoussoukro = (6.87, -5.28)
Yaounde = (3.87, 11.52)
Yerevan = (40.18, 44.51)
Zagreb = (45.81, 15.98)


capital_dict = {
    "Afghanistan": Kabul,
    "Albania": Tirana,
    "Angola": Luanda,
    "Antigua and Barbuda": StJohns,
    "Argentina": BuenosAires,
    "Armenia": Yerevan,
    "Australia": Canberra,
    "Bahrain": Manama,
    "Bangladesh": Dhaka,
    "Barbados": Bridgetown,
    "Belize": Belmopan,
    "Benin": PortoNovo,
    "Bolivia": LaPaz,
    "Botswana": Gaborone,
    "Brazil": Brasilia,
    "Brunei Darussalam": BandarSeriBegawan,
    "Bulgaria":Sofia,
    "Burkina Faso": Ouagadougou,
    "Burundi": Bujumbura,
    "Cambodia": PhnomPenh,
    "Cameroon": Yaounde,
    "Canada": Ottawa,
    "Cape Verde": Praia,
    "Central African Republic": Bangui,
    "Chad": NDjamena,
    "Chile": Santiago,
    "China": Beijing,
    "Colombia": Bogota,
    "Congo": Brazzaville,
    "Costa Rica": SanJose,
    "Croatia": Zagreb,
    "Cuba": Havana,
    "Cyprus": Nicosia,
    "Czechia": Prague,
    "Djibouti": Djibouti,
    "Dominica": Roseau,
    "Dominican Republic": SantoDomingo,
    "DR Congo": Kinshasa,
    "Ecuador": Quito,
    "Egypt": Cairo,
    "El Salvador": SanSalvador,
    "Estonia": Tallinn,
    "Eswatini": Mbabane,
    "EU15":Brussels,
    "EU25":Brussels,
    "EU27":Brussels,
    "EU28":Brussels,
    "Gabon":Libreville,
    "Gambia":Banjul,
    "Georgia":Tbilisi,
    "Ghana":Accra,
    "Grenada":StGeorges,
    "Guatemala":GuatemalaCity,
    "Guinea-Bissau":Bissau,
    "Guinea": Conakry,
    "Guyana":Georgetown,
    "Haiti":PortauPrince,
    "Honduras":Tegucigalpa,
    "Hungary":Budapest,
    "Iceland":Reykjavik,
    "India":NewDelhi,
    "Indonesia":Jakarta,
    "Israel":TelAviv,
    "Cote d Ivoire":Yamoussoukro,
    "Jamaica":Kingston,
    "Japan":Tokio,
    "Jordan":Amman,
    "Kazakhstan":Astana,
    "Kenya":Nairobi,
    "Korea":Seoul,
    "Kuwait":KuwaitCity,
    "Kyrgyzstan":Bishkek,
    "Laos":Vientiane,
    "Latvia":Riga,
    "Lesotho":Maseru,
    "Liberia":Monrovia,
    "Lithuania":Vilnius,
    "North Macedonia":Skopje,
    "Madagascar":Antananarivo,
    "Malawi":Lilongwe,
    "Malaysia":KualaLumpur,
    "Maldives":Male,
    "Mali":Bamako,
    "Malta":Valletta,
    "Mauritania":Nouakchott,
    "Mauritius":PortLouis,
    "Mexico":MexicoCity,
    "Moldova":Chisinau,
    "Mongolia":Ulaanbaatar,
    "Montenegro":Podgorica,
    "Morocco":Rabat,
    "Mozambique":Maputo,
    "Myanmar":Naypyidaw,
    "Namibia":Windhoek,
    "Nepal":Kathmandu,
    "New Zealand":Wellington,
    "Nicaragua":Managua,
    "Niger":Niamey,
    "Nigeria":Abuja,
    "Norway":Oslo,
    "Oman":Muscat,
    "Pakistan":Islamabad,
    "Panama":PanamaCity,
    "Papua New Guinea":PortMoresby, 
    "Paraguay":Asuncion,
    "Peru":Lima,
    "Philippines":Manila,
    "Poland":Warsaw,
    "Qatar":Doha,
    "Romania":Bucharest,
    "Russia":Moscow,
    "Rwanda":Kigali,
    "Samoa":Apia,
    "Saudi Arabia":Riyadh,
    "Senegal":Dakar,
    "Seychelles":Victoria,
    "Sierra Leone":Freetown,
    "Singapore":Singapore,
    "Slovakia":Bratislava,
    "Slovenia":Ljubljana,
    "Solomon Islands":Honiara,
    "South Africa":CapeTown,
    "Sri Lanka":SriJayawardenepuraKotte,
    "St Kitts and Nevis":Basseterre,
    "St Lucia":Castries,
    "St Vincent and the Grenadines":Kingstown,
    "Suriname": Paramaribo,
    "Switzerland":Bern,
    "Taiwan":Taipei,
    "Tajikistan":Dushanbe,
    "Tanzania":DaresSalaam,
    "Thailand":Bangkok,
    "Togo":Lome,
    "Tonga":Nukualofa,
    "Tunisia":Tunis,    
    "Turkey":Ankara,
    "Uganda":Kampala,
    "Ukraine":Kiev,
    "United Arab Emirates":AbuDhabi,
    "United States":Washington,
    "Uruguay":Montevideo,
    "Vanuatu":PortVila,
    "Venezuela":Caracas,
    "Vietnam":Hanoi,
    "Zambia":Lusaka,
    "Zimbabwe":Harare,
}

sqrt_area_dict = {}
