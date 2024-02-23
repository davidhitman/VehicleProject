class vehicle:
    def __init__(self,vehicle_type_id,vehicle_image,name,rider_capacity,propulsion_type,max_range_meters):
        self.vehicle_type_id = vehicle_type_id
        self.vehicle_image = vehicle_image
        self.name = name
        self.rider_capacity = rider_capacity
        self.propulsion_type = propulsion_type
        if max_range_meters == 'NaN':
            self.max_range_meters = 0
        else:
            self.max_range_meters = max_range_meters
        


