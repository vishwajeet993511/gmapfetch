
import googlemaps 
import pandas as pd
import numpy 
import time

def getgeocord(ipList):
    result = []
    for i in range(len(ipList)):
        result.append( gmaps.geocode(address='CA '+str(int(ipList[i]))) )
        if i%3==0:
            time.sleep(1)
        if i%100 == 0:
            time.sleep(600)
    return result
   
def getnearbyplaces(zipCord,place):
    result = []
    count = 0
    for i in range(len(zipCord)):
        temp = gmaps.places_nearby(location = zipCord[i]['Coordinates'],radius = 5000 , keyword = place)['results']      
        for j in range(len(temp)):
            name = temp[j]['name']
            loc = temp[j]['geometry']['location']
            area = zipCord[i]['Address'] 
            result.append({'Name':name,'Coordinates':loc,'Area':area,'Type':place})
        count += 1
        if count%20==0:
            time.sleep(120)
    return result

   
# reading in the excel file. Edit the path to the file
atmList = pd.ExcelFile('C:\\Users\\vishwajeet\\Desktop\\Work\\INTER HALL\\INTER HALL 2017\\List_ATM.xlsx') 
apList = atmList.parse(u'atm location all point')
mpList = atmList.parse(u'atm location moneypass')
coList = atmList.parse(u'atm_location_co_op')

#Pooling in all the result zip codes
zipList = [apList.result_zip_code, mpList.result_zip_code, coList.result_zip_code]
zipList=pd.concat(zipList) #single series obtained. Make it a set and 
                           #remove repeated entries. Then we remove na
zipList=list(set(zipList)) 
zipList=[value for value in zipList if not (numpy.isnan(value))]
zipList=[value for value in zipList if not int(value)/1000000 >0]
#Setting up the google API with my API key
gmaps = googlemaps.Client(key='put key here', 
        client_id = 'put client id here')

gmaps = googlemaps.Client(key='', 
        client_id = '')
 
 
#Obtaining the latitude and longitude coordinates of all zipcodes
zipList_a = getgeocord(zipList[800:900])
zipCord_temp= [ ]
for i in range(len(zipList)):
    x = zipList[i]
    address = str(x[0]['formatted_address'])
    coordinates = x[0]['geometry']['location']
    dict = {'Address' : address, 'Coordinates' : coordinates}
    zipCord_temp.append(dict)

zipCord=[[x['Address'],x['Coordinates']['lat'],x['Coordinates']['lng']] for x in zipCord]
for i in zipPlaces:
    if i not in zipPlaces_new:
        zipPlaces_new.append(i)
#looking for hotels, shopping malls, hospitals, colleges in all these zip codes

zipPlaces = []
places=['hotels','shopping malls','hospitals','colleges','metro stations']
zipPlaces_temp=[]
for place in places:
    zipPlaces_temp=zipPlaces_temp+getnearbyplaces(zipCord[150:200],place) 
    
for x in zipPlaces_temp:
    zipPlaces+=x