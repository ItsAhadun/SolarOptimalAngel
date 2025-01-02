import matplotlib.pyplot as plt
import math

# Constants and location parameters
latitude = 31.4605  # Latitude for Faisalabad, Pakistan
days_per_year = 365
hours_per_day = 24

# Function to calculate the solar declination angle
def solar_declination(day_of_year):
    return 23.45 * math.sin(math.radians((360 / 365) * (day_of_year - 10)))

# Function to calculate the hour angle
def hour_angle(hour):
    return 15 * (hour - 12)

# Function to calculate solar elevation angle
def solar_elevation_angle(declination, latitude, hour_angle):
    declination_rad = math.radians(declination)
    latitude_rad = math.radians(latitude)
    hour_angle_rad = math.radians(hour_angle)
    return math.degrees(math.asin(math.sin(declination_rad) * math.sin(latitude_rad) + 
                                  math.cos(declination_rad) * math.cos(latitude_rad) * math.cos(hour_angle_rad)))

# Function to calculate zenith angle
def zenith_angle(solar_elevation):
    return 90 - solar_elevation

# Function to calculate azimuth angle
def azimuth_angle(declination, latitude, solar_elevation, hour_angle):
    declination_rad = math.radians(declination)
    latitude_rad = math.radians(latitude)
    solar_elevation_rad = math.radians(solar_elevation)
    hour_angle_rad = math.radians(hour_angle)

    cos_value = (math.sin(declination_rad) * math.cos(latitude_rad) - 
                 math.cos(declination_rad) * math.sin(latitude_rad) * math.cos(hour_angle_rad)) / math.cos(solar_elevation_rad)

    # Ensure the value is within the valid range for acos
    cos_value = min(1, max(-1, cos_value))

    az_angle = math.degrees(math.acos(cos_value))
    if math.sin(hour_angle_rad) > 0:
        az_angle = 360 - az_angle

    return az_angle

# Calculate angles for each hour of each day of the year
data = []
for day in range(1, days_per_year + 1):
    declination = solar_declination(day)
    for hour in range(hours_per_day):
        h_angle = hour_angle(hour)
        solar_elev = solar_elevation_angle(declination, latitude, h_angle)
        zen_angle = zenith_angle(solar_elev)
        azim_angle = azimuth_angle(declination, latitude, solar_elev, h_angle)
        data.append((day, hour, declination, solar_elev, zen_angle, azim_angle))

# Extracting the angles from the data
declinations = [d[2] for d in data]
solar_elevations = [se[3] for se in data]
zenith_angles = [za[4] for za in data]
azimuth_angles = [aa[5] for aa in data]

# Plotting each angle in separate graphs
plt.figure(figsize=(15, 20))

# Solar Declination Angle
plt.subplot(4, 1, 1)
plt.plot(declinations, color='orange')
plt.title('Solar Declination Angle over the Year')
plt.xlabel('Hour of the Year')
plt.ylabel('Declination Angle (degrees)')

# Solar Elevation Angle
plt.subplot(4, 1, 2)
plt.plot(solar_elevations, color='blue')
plt.title('Solar Elevation Angle over the Year')
plt.xlabel('Hour of the Year')
plt.ylabel('Elevation Angle (degrees)')

# Zenith Angle
plt.subplot(4, 1, 3)
plt.plot(zenith_angles, color='green')
plt.title('Zenith Angle over the Year')
plt.xlabel('Hour of the Year')
plt.ylabel('Zenith Angle (degrees)')

# Azimuth Angle
plt.subplot(4, 1, 4)
plt.plot(azimuth_angles, color='red')
plt.title('Azimuth Angle over the Year')
plt.xlabel('Hour of the Year')
plt.ylabel('Azimuth Angle (degrees)')

plt.tight_layout()
plt.show()