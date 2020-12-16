import metpy.calc as mpcalc
from metpy.units import units
import math

# This file is for calculations that we will be calling as we plot our sounding


'''
Calculates the wet bulb temperature using metpy calculations
https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.wet_bulb_temperature.html#wet-bulb-temperature

    Parameters
    ----------
    pressure_in: pressure in hPa
    temperature_in: temperature in C
    dew_point_in: dew point temperature in C
    Output
    ----------
    wet_bulb_temperature in C
'''
def get_wet_bulb_temperature(pressure_in, temperature_in, dew_point_in):
    wet_bulb_temp = mpcalc.wet_bulb_temperature(pressure_in,
                                                temperature_in, dew_point_in)
    return wet_bulb_temp


'''
Calculates the potential temperature using metpy calculations
https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.potential_temperature.html#metpy.calc.potential_temperature
    Parameters
    ----------
    pressure_in: pressure in hPa
    temperature_in: temperature in C
    Output
    ----------
    potential in C
'''
def get_potential_temperature(pressure_in, temperature_in):
    potential_temperature = mpcalc.potential_temperature(pressure_in,
                                                temperature_in)
    return potential_temperature


'''
Calculates the saturation equivalent potential temperature using metpy calculations
https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.saturation_equivalent_potential_temperature.html#metpy.calc.saturation_equivalent_potential_temperature    Parameters
    ----------
    pressure_in: pressure in hPa
    temperature_in: temperature in C
    Output
    ----------
    potential in C
'''
def get_sat_eq_potential_temperature(pressure_in, temperature_in):
    sat_eq_potential_temperature = mpcalc.saturation_equivalent_potential_temperature(pressure_in,
                                                temperature_in)
    return sat_eq_potential_temperature




'''
Calculates the equivalent potential temperature from metpy calculations
https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.equivalent_potential_temperature.html#metpy.calc.equivalent_potential_temperature

    Parameters
    ----------
    pressure_in: pressure in hPa
    temperature_in: temperature in C
    dew_point_in: dew point temperature in C
    Output
    ----------
    eq_potential_temperature in C
'''
def get_equivalent_potential_temperature(pressure_in, temperature_in, dew_point_in):
    eq_potential_temperature = mpcalc.equivalent_potential_temperature(pressure_in,
                                                temperature_in, dew_point_in)
    return eq_potential_temperature




'''
Calculates vapor pressure
https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf

    Parameters
    ----------
    dew_point_in: dew point temperature in C
    Output
    ----------
    vapor_pressure hPa
'''

def get_vapor_pressure(pressure_in, mixing_in):
#     vapor_pressure = 6.11*(10**((7.5 * dew_point_in)/(237.7 + dew_point_in)))
    vapor_pressure = mpcalc.vapor_pressure(pressure_in, mixing_in)
    return vapor_pressure 
    
    
'''
Calculates saturated vapor pressure
https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf

    Parameters
    ----------
    temperature_in: temperature in C
    Output
    ----------
    sat_vapor_pressure in hPa
'''

def get_saturated_vapor_pressure(temperature_in):
#     sat_vapor_pressure = 6.11*(10**((7.5 * temperature_in)/(237.7 + temperature_in)))
    sat_vapor_pressure = mpcalc.saturation_vapor_pressure(temperature_in)
    return sat_vapor_pressure



'''
Calculates relative humidity
https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf

    Parameters
    ----------
    temperature_in: temperature in C
    dew_point_in: dew point temperature in C
    Output
    ----------
    rel_humidity in hPa
'''
def get_relative_humidity(temperature_in, dew_point_in):
#     sat_vapor_pressure = get_saturated_vapor_pressure(temperature_in)
#     vapor_pressure = get_vapor_pressure(dew_point_in)
    
#     rel_humidity = (vapor_pressure / sat_vapor_pressure) * 100
    rel_humidity = mpcalc.relative_humidity_from_dewpoint(temperature_in, dew_point_in)
    return rel_humidity



'''
Calculates mixing ratio from temperature, pressure and dew point 

    Parameters
    ----------
    temperature_in: temperature in C
    dew_point_in: dew point temperature in C
    Output
    ----------
    mixing ratio
'''
def get_mixing_ratio(temperature_in, pressure_in, dew_point_in):
    rel_humidity = get_relative_humidity(temperature_in, dew_point_in)
    
    m_r = mpcalc.mixing_ratio_from_relative_humidity(rel_humidity, 
                                                  temperature_in, pressure_in)
    return m_r


'''
Calculates temperature from mixing ratio and pressure 

    Parameters
    ----------
    pressure_in: pressure in hPa
    mixing_ratio_in: mixing_ratio
    Output
    ----------
    temperature
'''
def get_temp_from_mixing_and_pressure(pressure_in, mixing_ratio_in):
    e_s = mpcalc.vapor_pressure(pressure_in, mixing_ratio_in).m
    temp = (237.3 * math.log10(e_s/6.11)) / (7.5 - math.log10(e_s/6.11))
    
    return temp * units.degC



'''
Calculates saturation mixing ratio from temperature, pressure 

    Parameters
    ----------
    temperature_in: temperature in C
    pressure_in: pressure in hPa
    Output
    ----------
    saturation mixing ratio
'''
def get_saturation_mixing_ratio(temperature_in, pressure_in):
    
    s_m_r = mpcalc.saturation_mixing_ratio(pressure_in, temperature_in) 
    return s_m_r



'''
Calculates Lifting Condensation level using metpy calculations
https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.lcl.html#metpy.calc.lcl

    Parameters
    ----------
    pressure_in: pressure in hPa
    temperature_in: temperature in C
    dew_point_in: dew point temperature in C
    Output
    ----------
    lcl_pressure: pressure of LCL
    lcl_temperature: temperature of LCL
'''
def get_LCL(pressure_in, temperature_in, dew_point_in):
    lcl_pressure, lcl_temperature = mpcalc.lcl(pressure_in, 
                                               temperature_in, dew_point_in)
    
    return lcl_pressure, lcl_temperature
    
# TODO: Do the same for the other values we would want
# LFC, potential temp, equivalent temperature, virtiual temp, etc. any other values we would want to know 



    