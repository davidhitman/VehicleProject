class freeBike:
    def __init__(self,bike_id,is_reserved,is_disabled,lat,lon,vehicle_type_id,station_id,pricing_plan_id):
        self.bike_id = bike_id
        self.is_reserved = is_reserved
        self.is_disabled = is_disabled
        self.lat = lat
        self.lon = lon
        self.vehicle_type_id = vehicle_type_id
        if station_id != 'NaN':
            self.station_id = station_id
        else:
            self.station_id = None
        self.pricing_plan_id = pricing_plan_id
