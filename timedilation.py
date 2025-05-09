from math import radians, sin, cos, sqrt, atan2
import time
import location

stop_program = False
speed_of_light = 3e8

"""function to grab current location data"""
def get_location():
   location.start_updates()
   loc = location.get_location()
   location.stop_updates()
   if loc:
       return loc['latitude'], loc['longitude']
   else:
       return None, None
       

"""function to calculate time dilation"""
def time_equation(change_in_time, velocity):

   speed_of_light_sqrd = speed_of_light * speed_of_light

   velocity_sqrd = velocity * velocity

   divided = 1 - (velocity_sqrd / speed_of_light_sqrd)

   sqroot = sqrt(divided)

   ans = change_in_time / sqroot

   return ans
   
   
   
def haversine(lat1, lon1, lat2, lon2):
   """Calculate the great-circle distance between two points on Earth."""
   R = 6371.0  # Radius of Earth in kilometers
   lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
   dlat = lat2 - lat1
   dlon = lon2 - lon1
   a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
   c = 2 * atan2(sqrt(a), sqrt(1 - a))
   return R * c
   
   
   
def main():
   global stop_program
   print("Starting location tracker...")

   total_distance = 0.0
   prev_lat, prev_lon = None, None
   start_time = time.time()

   while not stop_program:
       current_lat, current_lon = get_location()
      
       if current_lat is None or current_lon is None:
           print("Unable to fetch location. Retrying...")
           time.sleep(5)
           continue

       print(f"Current Location: Latitude {current_lat}, Longitude {current_lon}")
      
       if prev_lat is not None and prev_lon is not None:
           distance = haversine(prev_lat, prev_lon, current_lat, current_lon)
           total_distance += distance
           print(f"Distance since last check: {distance:.4f} km")
           print(f"Total Distance Traveled: {total_distance:.4f} km")
       else:
           print("This is the starting point.")

       elapsed_time = time.time() - start_time
       elapsed_minutes, elapsed_seconds = divmod(elapsed_time, 60)
       print(f"Program has been running for {int(elapsed_minutes)} minutes and {int(elapsed_seconds)} seconds.")

       prev_lat, prev_lon = current_lat, current_lon
       time.sleep(5)
       
       if elapsed_time > 30:
       	stop_program = True

   print("Tracking stopped by user.")
   if total_distance > 0:
       velocity = elapsed_time / total_distance

       change = time_equation(elapsed_time, velocity)

       print(change)
       true_change = change - elapsed_time
       print(f"YOU ARE {true_change} seconds YOUNGER!")

if __name__ == "__main__":
   main()
