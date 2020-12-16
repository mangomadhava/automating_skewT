import matplotlib.pyplot as plt
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
from bs4 import BeautifulSoup
import requests
import numpy as np
from calculations import *


# This file will handle all the plotting functions 


def format_text(p,t):
    string = ''
    string += 'P = {} hPa\n'.format(round(p, 3))
    string += 'T = {} C\n'.format(round(float(t), 3))
    w_s = str(mpcalc.saturation_mixing_ratio(p * units.hPa, t * units.degC).m)
    string += 'W_s = {}\n'.format(w_s[0:5])
    return string


'''
returns a metpy plot using the specified lines
    Parameters
    ----------
    plot_dict: dictionary with format
        'dry_adiabats': [(temperature, start_pressure, end_pressure)]
        'moist_adiabats': [(temperature, start_pressure, end_pressure)]
        'mixing_ratio': [(mixing_ratio, start_pressure, end_pressure)]
        'constant_temp':[(temperature, start_pressure, end_pressure)]
        'constant_pressure':[(pressure, start_temperature, end_temperature)
        'point': [(pressure, temperature)]
        'sounding': either 'most_recent' or (pressures, temperatures, dew_points) all type list
        
        where start_pressure > end_pressure and start_temperature < end_temperature
    Output
    ----------
    metpy with specified lines
    (If multiple of the same type of line is specified, the min pressure and max pressure of 
     all the lines are used)
'''
def metpy_plot_lines(plot_dict):
    f = plt.figure(figsize = (10,10))
    plot = SkewT(f, rotation = 45)

    if 'dry_adiabats' in plot_dict.keys():
        all_t0 = []
        all_p = []
        for dry_adiabat in plot_dict['dry_adiabats']:
            temperature = dry_adiabat[0].m
            start_pressure = int(dry_adiabat[1].m)
            end_pressure = int(dry_adiabat[2].m)
            if start_pressure * units.hPa < 1000 * units.hPa: 
                # dry lapse temperature correction
                temperature = get_potential_temperature(start_pressure * units.hPa, 
                                                        temperature * units.degC)
                temperature = temperature.to(units.degC).m
            assert start_pressure > end_pressure,'Start pressure, arg 2, should be > end pressure, arg 3'
            
            t0 = [temperature] 
            p = [i for i in range(end_pressure, start_pressure, 1)]
            all_t0.append(t0)
            all_p.extend(np.array(p))
        best_p = [i for i in range(min(all_p), max(all_p), 1)] 
        plot.plot_dry_adiabats(np.stack(all_t0) * units.degC, best_p * units.hPa)
    
    if 'moist_adiabats' in plot_dict.keys():
        all_t0 = []
        all_p = []
        for moist_adiabat in plot_dict['moist_adiabats']:
            temperature = moist_adiabat[0].m
            start_pressure = int(moist_adiabat[1].m)
            end_pressure = int(moist_adiabat[2].m)
            if start_pressure * units.hPa < 1000 * units.hPa: 
                # moist lapse temperature correction
                temperature = mpcalc.moist_lapse([1000] * units.hPa, 
                                 temperature * units.degC, ref_pressure = start_pressure * units.hPa)
                temperature = float(temperature.to(units.degC).m)
            
            assert start_pressure > end_pressure,'Start pressure, arg 2, should be > end pressure, arg 3'
            t0 = [temperature] 
            p = [i for i in range(end_pressure, start_pressure, 1)] 
            all_t0.append(t0)
            # stupid whacko plot moist adiabat function is acting up so we do some bad coding
            all_t0.append(t0)
            all_p.extend(np.array(p))
        best_p = [i for i in range(min(all_p), max(all_p), 1)] 
        plot.plot_moist_adiabats(np.stack(all_t0) * units.degC, best_p * units.hPa)
            
    if 'mixing_ratio' in plot_dict.keys():
        all_w0 = []
        all_p = []
        for mixing_ratio in plot_dict['mixing_ratio']:
            w = mixing_ratio[0]
            start_pressure = int(mixing_ratio[1].m)
            end_pressure = int(mixing_ratio[2].m)
            assert start_pressure > end_pressure,'Start pressure, arg 2, should be > end pressure, arg 3'
            w0 = [w] 
            p = [i for i in range(end_pressure, start_pressure, 1)] 
            all_w0.append(w0)
            all_p.extend(np.array(p))
        best_p = [i for i in range(min(all_p), max(all_p), 1)]
        plot.plot_mixing_lines(np.stack(all_w0), best_p * units.hPa)
            
    if 'constant_temp' in plot_dict.keys():
        for temp in plot_dict['constant_temp']:
            temperature = int(temp[0].m)
            start_pressure = int(temp[1].m)
            end_pressure = int(temp[2].m)
            t0 = [temperature] 
            assert start_pressure > end_pressure,'Start pressure, arg 2, should be > end pressure, arg 3'
            p = [i for i in range(end_pressure, start_pressure, 1)]
            plot.plot(p, np.tile(t0, len(p)) * units.degC, 'r')
    
    if 'constant_pressure' in plot_dict.keys():
        for pressures in plot_dict['constant_pressure']:
            p = [int(pressures[0].m)]
            start_temp = int(pressures[1].m)
            end_temp = int(pressures[2].m)
            assert start_temp < end_temp, 'Start temperature, arg 2, should be < end temperature, arg 3'
            t0 = [i for i in range(start_temp, end_temp, 1)]
            plot.plot(np.tile(p, len(t0)) * units.hPa, t0 * units.degC, 'b')
    
    if 'point' in plot_dict.keys():
        for points in plot_dict['point']:
            p = points[0].m
            t = points[1].m
            if len(points) > 2:
                offset = points[2]
                plot.ax.text(t + offset , p + offset , format_text(p,t))
            else: 
                plot.ax.text(t + 1 , p + 1 , format_text(p,t))
            plot.plot([p, p], [t - .0001, t + .0001], 'k', marker='o')
            
            
    if 'sounding' in plot_dict.keys():
        pressures = plot_dict['sounding'][0]
        temp = plot_dict['sounding'][1]
        dew_point = plot_dict['sounding'][2]
        plot.plot(pressures, temp, 'r')
        plot.plot(pressures, dew_point, 'g')
    return plot

