

import pandas as pd
import time
import requests
from datetime import datetime
import pytz
import pickle
import json
patch = pd.read_csv("patch_1_streets.csv")

set_of_streets = set()
list_of_streets_points = []


def speedAndDelay(lat, long, zoom, api_key):
    list_of_data_traffic = []
    Dict_speed = {}
    host_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/" + str(zoom) + "/json"
    request_data = requests.get(host_url, params={"key": api_key, "point": str(lat) + "," + str(long)})
    # print(request_data.url)
    traffic_data = request_data.json()
    current_speed = traffic_data["flowSegmentData"]["currentSpeed"]
    free_speed = traffic_data["flowSegmentData"]["freeFlowSpeed"]
    current_travel_time = traffic_data["flowSegmentData"]["currentTravelTime"]
    free_travel_time = traffic_data["flowSegmentData"]["freeFlowTravelTime"]
    confidence_level = traffic_data["flowSegmentData"]["confidence"]
    is_close = traffic_data["flowSegmentData"]["roadClosure"]
    segment_distance = free_travel_time * free_speed * (1000 / 3600)
    list_of_data_traffic.append(current_speed)
    list_of_data_traffic.append(free_speed)
    list_of_data_traffic.append(current_travel_time)
    list_of_data_traffic.append(free_travel_time)
    list_of_data_traffic.append(segment_distance)
    list_of_data_traffic.append(confidence_level)
    list_of_data_traffic.append(is_close)

    Dict_speed["current speed"] = current_speed
    Dict_speed["free speed"] = free_speed
    Dict_speed["current travel time"] = current_travel_time
    Dict_speed["free travel time"] = free_travel_time
    Dict_speed["segment distance"] = segment_distance
    Dict_speed["confidece"] = confidence_level
    Dict_speed["road closure"] = str(is_close)

    """if street_id not in set_of_streets:
        set_of_streets.add(street_id)
        list_of_streets_points.append({street_id:traffic_data["flowSegmentData"]["coordinates"]["coordinate"]})"""

    return Dict_speed


def Weather(lat, long, api_key):
    Dict_weather = {}
    list_of_data_weather = []
    host_url = "https://api.openweathermap.org/data/2.5/weather"
    request_data = requests.get(host_url,
                                params={"lat": str(lat), "lon": str(long), "appid": api_key, "units": "metric"})
    # print(request_data.url)
    CONVERTED_weather = request_data.json()
    try:
        list_of_data_weather.append(CONVERTED_weather["weather"][0]["id"])  # one of many states
        Dict_weather["weather id"] = CONVERTED_weather["weather"][0]["id"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["weather id"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["weather"][0]["main"])
        Dict_weather["Weather Main"] = CONVERTED_weather["weather"][0]["main"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["Weather Main"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["weather"][0]["description"])
        Dict_weather["weather description"] = CONVERTED_weather["weather"][0]["description"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["weather description"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["main"]["temp"])  # in Kelvin
        Dict_weather["temprature"] = CONVERTED_weather["main"]["temp"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["temprature"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["main"]["feels_like"])
        Dict_weather["feels like"] = CONVERTED_weather["main"]["feels_like"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["feels like"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["main"]["pressure"])  # in hPa
        Dict_weather["pressure"] = CONVERTED_weather["main"]["pressure"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["pressure"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["main"]["humidity"])  # percantage
        Dict_weather["humidity"] = CONVERTED_weather["main"]["humidity"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["humidity"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["visibility"])  # how many METERS can be seen
        Dict_weather["visibility"] = CONVERTED_weather["visibility"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["visibility"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["wind"]["speed"])  # meter/sec
        Dict_weather["wind speed"] = CONVERTED_weather["wind"]["speed"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["wind speed"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["wind"]["degree"])  # degree of wind
        Dict_weather["wind degree"] = CONVERTED_weather["wind"]["degree"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["wind degree"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["clouds"]["all"])  # percentage of cloudness
        Dict_weather["cloud"] = CONVERTED_weather["clouds"]["all"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["cloud"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["rain"]["1h"])  # volume of rain in the last hour
        Dict_weather["rain 1h"] = CONVERTED_weather["rain"]["1h"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["rain 1h"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["rain"]["3h"])  # volume of rain in the last 3 hour
        Dict_weather["rain 3h"] = CONVERTED_weather["rain"]["3h"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["rain 3h"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["snow"]["1h"])  # volume of snow in the last hour
        Dict_weather["snow 1h"] = CONVERTED_weather["snow"]["1h"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["snow 1h"] = 0
    try:
        list_of_data_weather.append(CONVERTED_weather["snow"]["3h"])  # volume of snow in the last 3 hour
        Dict_weather["snow 3h"] = CONVERTED_weather["snow"]["3h"]
    except KeyError:
        list_of_data_weather.append(0)
        Dict_weather["snow 3h"] = 0

    """if street_id not in set_of_streets:
        set_of_streets.add(street_id)
        list_of_streets_points.append({street_id:traffic_data["flowSegmentData"]["coordinates"]["coordinate"]})"""

    return Dict_weather


def Incidents(lat, long):
    APIKey = "Gy8J7zAX7af7ALx6fkAby6rRxzsbxsjU"
    LocationKey = "127005"
    Host = "https://api.tomtom.com/traffic/services/4/incidentDetails/s3/"
    Dict_Incidents = {}
    coords = (lat, long)

    df = pd.DataFrame()
    df = patch.loc[patch["incidenst_cluster_latup"] > lat]
    # df = df.reset_index()
    df = df.loc[df["incidents_cluster_longup"] > long]
    # df = df.reset_index()
    df = df.loc[df["icndienst_cluster_latdown"] < lat]
    # df = df.reset_index()
    df = df.loc[df["incidnets_cluster_longdown"] < long]
    cluster_number = int(df["incidents_cluster_number"].unique()[0])
    CoordsUR = [df["incidenst_cluster_latup"].unique()[0], df["incidents_cluster_longup"].unique()[0]]
    CoordsBL = [df["icndienst_cluster_latdown"].unique()[0], df["incidnets_cluster_longdown"].unique()[0]]
    boundingBox = str(CoordsBL[0]) + "," + str(CoordsBL[1]) + "," + str(CoordsUR[0]) + "," + str(CoordsUR[1])
    #print(lat, long, boundingBox)

    zoom = "16"
    trafficModelID = "1335294634919"
    format = "json"
    details = "true"
    ##The non-required parameters
    language = "en"
    projection = "EPSG4326"
    geometries = "original"
    expandCluster = "true"
    originalPosition = "true"
    tz_cairo = pytz.timezone("Africa/Cairo")
    date_cairo = datetime.now(tz_cairo)
    dateandtime = date_cairo.strftime("%D")
    datandtime2 = date_cairo.strftime("%D %H %M %S")
    dateandtime = dateandtime.replace("/", "_")

    GET = boundingBox + "/" + zoom + "/" + trafficModelID + "/" + format + "?key=" + APIKey + "&language=" + language + "&projection=" + projection + "&geometries=" + geometries + "&expandCluster=" + expandCluster + "&originalPosition=" + originalPosition
    # print(Host+GET)
    index = 0
    AccCount = 0
    clustered = 0
    free = 0
    cpoiLen = 0
    HTTP = urlopen(Host + GET)
    CONVERTED = json.load(HTTP)
    for accident in CONVERTED["tm"]["poi"]:  # ["tm"]["poi"] contains either a one accident or a cluster of accidents
        key = "cpoi"
        if key in accident:  # checking if it"s one accident or a cluster of accidents, if more than one key = true
            for index in range(len(accident["cpoi"])):
                Accident = []  # Creating an empty list to prevent errors
                Accident.append(datandtime2)  # Appending Current time
                Accident.append(accident["cpoi"][index]["d"])  # Accident Cause
                Accident.append(accident["cpoi"][index]["f"])  # Accident StreetName
                Accident.append(accident["cpoi"][index]["ic"])  # Incident indication
                Accident.append(accident["cpoi"][index]["ty"])  # The magnitude of delay associated with an incident
                Accident.append(accident["cpoi"][index]["l"])

                Dict_Incidents["datandtime2"] = datandtime2
                Dict_Incidents["Accident Cause"] = accident["cpoi"][index]["d"]
                Dict_Incidents["Street Name"] = accident["cpoi"][index]["f"]
                Dict_Incidents["Incident indication"] = accident["cpoi"][index]["ic"]
                Dict_Incidents["magnitude of delay"] = accident["cpoi"][index]["ty"]
                Dict_Incidents["Incident Length"] = accident["cpoi"][index]["l"]

                if "dl" in accident["cpoi"][index]:
                    Accident.append(accident["cpoi"][index]["dl"])
                    Dict_Incidents["Delay"] = accident["cpoi"][index]["dl"]
                else:
                    Accident.append(0)
                    Dict_Incidents["Delay"] = 0
                if "r" in accident["cpoi"][index]:
                    Accident.append(accident["cpoi"][index]["r"])

                    Dict_Incidents["roads affected"] = accident["cpoi"][index]["r"]
                    Dict_Incidents["Incident lat"] = 0
                    Dict_Incidents["Incident long"] = 0
                else:
                    Accident.append(0)
                    Accident.append(accident["cpoi"][index]["p"]["x"])  # Incident Lat
                    Accident.append(accident["cpoi"][index]["p"]["y"])  # Incident Long

                    Dict_Incidents["Incident lat"] = accident["cpoi"][index]["p"]["x"]
                    Dict_Incidents["Incident long"] = accident["cpoi"][index]["p"]["y"]
                    Dict_Incidents["roads affected"] = 0

        else:
            Accident = []
            Accident.append(datandtime2)
            Accident.append(accident["d"])  # Accident Cause
            Accident.append(accident["f"])  # Accident StreetName
            Accident.append(accident["ic"])  # Incident indication
            Accident.append(accident["ty"])  # The magnitude of delay associated with an incident
            Accident.append(accident["l"])

            Dict_Incidents["datandtime2"] = datandtime2
            Dict_Incidents["Accident Cause"] = accident["d"]
            Dict_Incidents["Street Name"] = accident["f"]
            Dict_Incidents["Incident indication"] = accident["ic"]
            Dict_Incidents["magnitude of delay"] = accident["ty"]
            Dict_Incidents["Incident Length"] = accident["l"]

            if "dl" in accident:
                Accident.append(accident["dl"])
                Dict_Incidents["Delay"] = accident["dl"]
            else:
                Accident.append(0)
                Dict_Incidents["Delay"] = 0
            if "r" in accident:
                Accident.append(accident["r"])

                Dict_Incidents["roads affected"] = accident["r"]
                Dict_Incidents["Incident lat"] = 0
                Dict_Incidents["Incident long"] = 0
            else:
                Accident.append(0)
                Accident.append(accident["p"]["x"])  # Incident Lat
                Accident.append(accident["p"]["y"])  # Incident Long

                Dict_Incidents["Incident lat"] = accident["p"]["x"]
                Dict_Incidents["Incident long"] = accident["p"]["y"]
                Dict_Incidents["roads affected"] = 0
    Dict_Incidents["Incidnts cluster number"] = cluster_number
    return Dict_Incidents


def mariam():
    """columns=["time","street_id","placesClusterNumber","currentSpeed","freeFlowSpeed","currentTravelTime","freeFlowTravelTime","segment_distance","confidence","roadClosure"]
    df = pd.read_csv("/home/OmarEssam/GP/patch_1_streets.csv")
    speed_df=pd.DataFrame(columns=columns)
    tz_cairo = pytz.timezone("Africa/Cairo")
    date_cairo = datetime.now(tz_cairo)
    date_cairo = date_cairo.strftime("%D")
    date_str_unmodefied_before = str(date_cairo)
    date_str_modefied = date_str_unmodefied_before.replace("/","-")"""
    speedlist = []
    # unused key: "la0NleqNYLLNMSxMwEJjpKOCsshkguCW"
    apikeyslist = ["oq3Js4iKS4QwPHoWS7cCOz4xqOFZcAL7", "SjX0EqcFgmnzNxeiVnSkW3mn1EH5FL0B",
                   "kTfXRbxV8ghTuUzbbBZX0ciVkJC8uQgX", "fkP5aNuCzTSWjINTxjOabNbLWyNKlpDT",
                   "Sh6LerG3mKfg0zqY5V2lcnjauAsOW8ic", "bR87jCwlSeVS4QlUCFzAEMxpYG4hgs8h",
                   "R7JRfWWe9FerZI6AZoDbAr8lZ5yFfwqN", "4JSpYGJiN9TZt92oJnlDohwGHKRoFsNg",
                   "DQpgoJh6vlcMKGUgfmsduBlBX4LMmG1a", "ZWohVmhukAaYVdc60UyLv4Awc5MQ5B35",
                   "EXStsDAtaF7vpx3qF2KTXMOZrk8eGKXT", "4OR9VWld1XX6L42rLsSMH4InZKLQ0XqF",
                   "gd5TyQTwcUuQRNswAPA301wSTqWft0bj", "13XZONYoWirOz6GKLLNUNGwGtxif7qoI",
                   "oPp4tvZqwDA0ljNBGnKdlW93WvN36VpC"]
    restart = True
    num_of_days = 0
    end = False
    num_of_typings = 0
    x = 30.0620851 + 30.061657
    x = x / 2
    y = 31.1743601 + 31.1744185
    y = y / 2
    api_key = "fkP5aNuCzTSWjINTxjOabNbLWyNKlpDT"
    lat1 = x
    long1 = y
    zoom = 5
    speedlist = speedAndDelay(lat1, long1, zoom, api_key)
    print(speedlist)


#mariam()

import pandas as pd
from urllib.request import urlopen
import json
import time
from datetime import datetime
import pytz
import pickle

set_of_places = set()
list_of_places = []


def places(lat, long, apikey):
    list_of_facilities = ["restaurant", "shopping_mall", "cafe", "tourist_attraction", "local_government_office"]
    apiKey = apikey
    list_of_data_places = []
    Dict_places = {}

    for iterate in list_of_facilities:

        request_places = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(
            lat) + "," + str(long) + "&radius=1500&type=" + iterate + "&opennow&key=" + apiKey
        places_data = json.load(urlopen(request_places))
        # print(request_places)
        places_results = places_data["results"]
        if (places_data["status"] == "OK") or (places_data["status"] == "ZERO_RESULTS"):
            number_of_places = len(places_results)
            total_rate = 0
            total_number_of_raters = 0
            for place in places_results:
                place_name = place["name"]
                place_vicinity = place["vicinity"]
                try:
                    place_rating = place["rating"]
                    place_num_of_raters = place["user_ratings_total"]
                except KeyError:
                    place_rating = 0
                    place_num_of_raters = 0
                total_rate += place_rating
                total_number_of_raters += place_num_of_raters
                place_id = place["place_id"]
                place_lat = place["geometry"]["location"]["lat"]
                place_long = place["geometry"]["location"]["lng"]
                if place_id not in set_of_places:
                    set_of_places.add(place_id)
                    list_of_places.append({"name": place_name, "vicinity": place_vicinity, "rating": place_rating,
                                           "number_of_raters": place_num_of_raters,
                                           "ID": place_id, "lat": place_lat, "long": place_long, "type": iterate})
            list_of_data_places.append(number_of_places)
            list_of_data_places.append(total_rate)
            list_of_data_places.append(total_number_of_raters)

            Dict_places[str(iterate) + " number of places"] = number_of_places
            Dict_places[str(iterate) + " total rating"] = total_rate
            Dict_places[str(iterate) + " total number of raters"] = total_number_of_raters

            time.sleep(1)
        else:
            list_of_data_places.append(0)
            list_of_data_places.append(0)
            list_of_data_places.append(0)
            Dict_places[str(iterate) + " number of places"] = 0
            Dict_places[str(iterate) + " total rating"] = 0
            Dict_places[str(iterate) + " total number of raters"] = 0

    return Dict_places


def main(lat,long):
    num_of_requests = 0
    """places_cluster = pd.read_csv("/home/Rana/GP/places_clusters.csv")
    places_cluster_lat = places_cluster.lat.values.tolist()
    places_cluster_long = places_cluster.long.values.tolist()
    list_of_keys = ["AIzaSyDBHbqh9GfkMLGp5dE_kWHru-l5kPtxDm8","AIzaSyAdndRi5QgjrfMu3qMRI73t9WcuUoKaSPQ"]"""
    columns = ["time", "cluster_number", "restaurant", "total_resturant_rate", "total_resturants_number_or_raters",
               "shopping_mall", "total_shopping_mall_rate", "total_shopping_mall_number_of_raters", "cafe",
               "total_cafe_rate", "total_cafe_number_of_raters", "tourist_attraction", "total_tourist_attraction_rate",
               "total_tourist_attraction_number_of_raters", "local_government_office",
               "total_local_government_office_rate", "total_local_government_office_number_of_raters"]
    places_df = pd.DataFrame(columns=columns)
    tz_cairo = pytz.timezone("Africa/Cairo")
    date_cairo = datetime.now(tz_cairo)
    date_cairo = date_cairo.strftime("%D")
    date_str_unmodefied_before = str(date_cairo)
    date_str_modefied = date_str_unmodefied_before.replace("/", "-")
    restart = True
    num_of_days = 0
    num_of_typings = 0
    x = 30.0620851 + 30.061657
    x = x / 2
    y = 31.1743601 + 31.1744185
    y = y / 2

    lat1 = lat
    long1 = long
    # print(x,y)

    placeslist = places(lat1, long1, "AIzaSyDBHbqh9GfkMLGp5dE_kWHru-l5kPtxDm8")
    trafficlist = speedAndDelay(lat1, long1, 5, "oq3Js4iKS4QwPHoWS7cCOz4xqOFZcAL7")
    weather = Weather(lat1, long1, "3a348ba58dc00d518a294df0f275f5b1")
    Incident = Incidents(lat1, long1)
    output={}
    output['weather']= weather
    output['Speed & Distance']=trafficlist
    output['Places']=placeslist
    output['Incident']=Incident


    '''for key in placeslist:
        print(key,type(placeslist[key]))'''
    return output


x=main(30.0620851,31.1743601)
print(x)
