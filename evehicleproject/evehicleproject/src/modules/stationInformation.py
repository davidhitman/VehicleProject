class stationInforamtion:
    def __init__(self,station_id,name,short_name,lat,lon,region_id,is_virtual_station,capacity):
        self.station_id= station_id
        self.name = name
        self.short_name = short_name
        self.lat = lat
        self.lon = lon
        self.region_id = region_id
        self.is_virtual_station = is_virtual_station
        if capacity == 'NaN':
            self.capacity = 0
        else:
            self.capacity = capacity
