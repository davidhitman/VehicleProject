class stationStatus:
    def __init__(self,station_id,num_bikes_available,num_docks_available,is_installed,is_renting,is_returning):
        self.station_id = station_id
        self.num_bikes_available = num_bikes_available
        self.num_docks_available = num_docks_available
        self.is_installed = is_installed
        self.is_renting = is_renting
        self.is_returning = is_returning
        # self.last_reported = last_reported


