import sys 
from calculations import *
from plotting import *
from matplotlib import pyplot as plt
import metpy.calc as mpcalc
from metpy.plots import SkewT
from metpy.units import units
from bs4 import BeautifulSoup
import requests
import numpy as np

'''
requests the url of noaa soundings page
makes the data readable and extracts all the hyperlinks
all sounding hyperlinks have OBS so find first one, which will
be the most recent sounding and save the date
'''
def get_most_recent_sounding():
    first_page = requests.get("https://www.spc.noaa.gov/exper/soundings/")
    assert first_page.ok, 'Something went wrong in requests'
    soup = BeautifulSoup(first_page.content, 'html.parser')
    for i in soup.find_all('a'):
        if i.get('href').endswith('12_OBS/') or i.get('href').endswith('00_OBS/'):
            return i.get('href').split('/')[3].split('_')[0]

'''
parses the most recent sounding
'''
def parse_most_recent_sounding():
    most_recent = get_most_recent_sounding()
    url = "https://www.spc.noaa.gov/exper/soundings/" + str(most_recent) + "_OBS/IAD.txt"
    page = requests.get(url)
    assert page.ok, 'Something went wrong in requests plotting'
    soup = BeautifulSoup(page.content, 'html.parser')
    pressures = []
    height = []
    temp = []
    dew_point = []
    wind_dir = []
    wind_speed = []
    # loops through text line by line
    for line in page.text.split("%RAW%")[1].split("%END%")[0].split("\n"):
        # removes whitespace and splits the text on commas
        data = line.replace(" ", "").split(",")
        # for valid lines
        if len(data) == 6: 
            # save sounding data to list
            pressures.append(float(data[0]))
            height.append(float(data[1]))
            temp.append(float(data[2]))
            dew_point.append(float(data[3]))
            wind_dir.append(float(data[4]))
            wind_speed.append(float(data[5]))
    return pressures, temp, dew_point


class plot_handler(): 
    def __init__(self):
        self.temperatures = None
        self.dew_points = None
        self.pressures = None
        self.plot_dict = {}
    
    def add_temperatures(self, line):
        nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
        self.temperatures = nums * units.degC
    
    def add_pressures(self, line):
        nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
        self.pressures = nums * units.hPa
        
    def add_dew_points(self, line):
        nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
        self.dew_points = nums * units.degC

    def plot_sounding(self, line):
        if line.strip() == 'sounding': 
            self.plot_dict['sounding'] = (self.pressures, 
                             self.temperatures, self.dew_points)
        else:
            p,t,d = parse_most_recent_sounding()
            self.pressures = p * units.hPa
            self.temperatures = t * units.degC
            self.dew_points = d * units.degC
            self.plot_dict['sounding'] = (self.pressures, 
                             self.temperatures, self.dew_points)
        self.add_plotting_data('point', [(self.pressures[0], self.dew_points[0], - 13)])
        self.add_plotting_data('point', [(self.pressures[0], self.temperatures[0])])
        
    def add_plotting_data(self, line_type, data):
        if line_type not in self.plot_dict.keys():
            self.plot_dict[line_type] = data 
        else: 
            self.plot_dict[line_type].extend(data)
    
    def get_plot_dict(self):
        return self.plot_dict
    
    def reset_plot_dict(self):
        self.plot_dict = {}
            
    def plot_lcl(self, line):
        if line.strip() == 'lcl': 
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        lcl_pressure, lcl_temperature = get_LCL(p, t0, d)
        mix_ratio = get_mixing_ratio(t0, p, d)
        self.add_plotting_data('dry_adiabats', [(t0, p, lcl_pressure)])
        self.add_plotting_data('mixing_ratio', [(mix_ratio, p, lcl_pressure)])
        self.add_plotting_data('point', [(lcl_pressure, lcl_temperature)])
    
    def plot_mixing_ratio(self, line): 
        if line.strip() == 'mixing ratio':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()] 
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        mixing_ratio = get_mixing_ratio(t0, p, d)
        self.add_plotting_data('mixing_ratio', [(mixing_ratio, p, p - 400 * units.hPa)])
        self.add_plotting_data('point', [(p, d)])

    def plot_saturation_mixing_ratio(self, line):
        if line.strip() == 'mixing ratio':
            t0 = self.temperatures[0]
            p = self.pressures[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()] 
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
        sat_mixing_ratio = get_saturation_mixing_ratio(t0, p)
        self.add_plotting_data('mixing_ratio', [(sat_mixing_ratio, p, p - 400 * units.hPa)])
        self.add_plotting_data('point', [(p, t0)])
    
    def plot_vapor_pressure(self, line):
        if line.strip() == 'mixing ratio':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()] 
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        mixing_ratio = get_saturation_mixing_ratio(d, 622 * units.hPa)
        vap_pressure = get_vapor_pressure(p, mixing_ratio)
        self.add_plotting_data('constant_temp', [(d, p, 622 * units.hPa)])
        self.add_plotting_data('mixing_ratio', [(mixing_ratio, p, 622 * units.hPa)])
        self.add_plotting_data('point', [(622 * units.hPa, d)])
        
    def plot_sat_vapor_pressure(self, line):
        if line.strip() == 'mixing ratio':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()] 
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        saturation_mixing_ratio = get_saturation_mixing_ratio(t0, 622 * units.hPa)
        vap_pressure = get_vapor_pressure(p, saturation_mixing_ratio)
        sat_vap_pressure = get_saturated_vapor_pressure(t0)
        self.add_plotting_data('constant_temp', [(t0, p, 622 * units.hPa)])
        self.add_plotting_data('mixing_ratio', [(saturation_mixing_ratio, p, 622 * units.hPa)])
        self.add_plotting_data('point', [(622 * units.hPa, t0)])
        
    def plot_potential_temp(self, line):
        if line.strip() == 'pot':
            t0 = self.temperatures[0]
            p = self.pressures[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
        
        potential_temp = get_potential_temperature(p, t0).to(units.degC)
        self.add_plotting_data('dry_adiabats', [(potential_temp, 1000 * units.hPa, p)])
        self.add_plotting_data('point', [(1000 * units.hPa, potential_temp)]) 
        
    def plot_wetbulb_temp(self, line):
        if line.strip() == 'wetbulb':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        wet_bulb_temp = get_wet_bulb_temperature(p, t0, d)
        lcl_pressure, lcl_temperature = get_LCL(p, t0, d)
        mix_ratio = get_mixing_ratio(t0, p, d)
        self.add_plotting_data('dry_adiabats', [(t0, p, lcl_pressure)])
        self.add_plotting_data('mixing_ratio', [(mix_ratio, p, lcl_pressure)])
        # moist lapse
        corrected = mpcalc.moist_lapse([p.m] * units.hPa, lcl_temperature, lcl_pressure)
        self.add_plotting_data('moist_adiabats', [(corrected, p, lcl_pressure)])
        self.add_plotting_data('point', [(p, corrected)]) 
        
    def plot_potential_wetbulb_temp(self, line):
        if line.strip() == 'wetbulb':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        wet_bulb_temp = get_wet_bulb_temperature(p, t0, d)
        lcl_pressure, lcl_temperature = get_LCL(p, t0, d)
        mix_ratio = get_mixing_ratio(t0, p, d)
        self.add_plotting_data('dry_adiabats', [(t0, p, lcl_pressure)])
        self.add_plotting_data('mixing_ratio', [(mix_ratio, p, lcl_pressure)])
        # moist lapse
        corrected = mpcalc.moist_lapse([1000] * units.hPa, lcl_temperature, lcl_pressure)
        self.add_plotting_data('moist_adiabats', [(corrected, 1000 * units.hPa, lcl_pressure)])  
        self.add_plotting_data('point', [(1000 * units.hPa, corrected)]) 


    def plot_equ_temp(self, line):
        if line.strip() == 'wetbulb':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        wet_bulb_temp = get_wet_bulb_temperature(p, t0, d)
        lcl_pressure, lcl_temperature = get_LCL(p, t0, d)
        mix_ratio = get_mixing_ratio(t0, p, d)
        eq_potential_temp = get_equivalent_potential_temperature(p, t0, d).to(units.degC)
        self.add_plotting_data('dry_adiabats', [(t0, p, lcl_pressure)])
        self.add_plotting_data('mixing_ratio', [(mix_ratio, p, lcl_pressure)])
        # assume moist and dry are parallel by 200 hpa
        self.add_plotting_data('moist_adiabats', [(lcl_temperature, lcl_pressure, 150 * units.hPa)])
        # corrections
        temp_at_original_pressure = mpcalc.dry_lapse(p, eq_potential_temp, 1000*units.hPa).to(units.degC)
        self.add_plotting_data('dry_adiabats', [(temp_at_original_pressure, p, 150 * units.hPa)])
        self.add_plotting_data('point', [(p, temp_at_original_pressure)])                                          

            
    def plot_equ_pot_temp(self, line):
        if line.strip() == 'wetbulb':
            t0 = self.temperatures[0]
            p = self.pressures[0]
            d = self.dew_points[0]
        else: 
            nums = [float(i) for i in line.split() if i.replace('.', '1').replace('-','1').isdigit()]
            p = nums[0] * units.hPa
            t0 = nums[1] * units.degC
            d = nums[2] * units.degC
        wet_bulb_temp = get_wet_bulb_temperature(p, t0, d)
        lcl_pressure, lcl_temperature = get_LCL(p, t0, d)
        mix_ratio = get_mixing_ratio(t0, p, d)
        eq_potential_temp = get_equivalent_potential_temperature(p, t0, d).to(units.degC)
        self.add_plotting_data('dry_adiabats', [(t0, p, lcl_pressure)])
        self.add_plotting_data('mixing_ratio', [(mix_ratio, p, lcl_pressure)])
        # assume moist and dry are parallel by 150 hpa
        self.add_plotting_data('moist_adiabats', [(lcl_temperature, lcl_pressure, 150 * units.hPa)])
        self.add_plotting_data('dry_adiabats', [(eq_potential_temp, 
                                                 1000 * units.hPa, 150 * units.hPa)])
        self.add_plotting_data('point', [(1000 * units.hPa, eq_potential_temp)]) 
# Too hard too little time :'(
#     def plot_relative_humidity(self, line):
#         if line.strip() == 'relative humidity':
#             t0 = self.temperatures[0]
#             d = self.dew_points[0]
#             p = self.pressures[0]            
#         else: 
#             nums = [float(i) for i in line.split() if i.replace('.', '', 1).isdigit() 
#              or i.replace('-', '', 1).isdigit()]
#             p = nums[0] * units.hPa
#             t0 = nums[1] * units.degC  
#             d = nums[2] * units.degC
#         rel_hum = get_relative_humidity(t0, d)
#         print(rel_hum)
#         mixing_ratio_start = get_mixing_ratio(t0, p, d)
#         sat_mixing_ratio = get_saturation_mixing_ratio(t0, p)
#         rh_pressure_height = rel_hum * 10
#         rh_pressure_height = rh_pressure_height * units.hPa
#         c_temp = get_temp_from_mixing_and_pressure(rh_pressure_height, sat_mixing_ratio)
#         print(c_temp)
#         self.add_plotting_data('mixing_ratio', [(mixing_ratio_start, 1000 * units.hPa, p)])
#         self.add_plotting_data('constant_temp', [(c_temp, 1000 * units.hPa, rh_pressure_height)])
#         self.add_plotting_data('mixing_ratio', [(sat_mixing_ratio, p, rh_pressure_height)])


def main():
    assert len(sys.argv) == 2, 'Must provide txt file'
    plot_object = plot_handler()
    with open(sys.argv[1], 'r') as problem_txt: 
        lines = problem_txt.readlines()
    for line_num in range(0,len(lines)):
        line = lines[line_num]
        if line.strip() == '*data*':
            for i in range(1,4):
                vals = lines[line_num + i]
                if vals[0] == 'p':
                    plot_object.add_pressures(vals)
                elif vals[0] == 't': 
                    plot_object.add_temperatures(vals)
                elif vals[0] == 'd': 
                    plot_object.add_dew_points(vals)
            line_num = line_num + 3
        
        plot_num = 0
        if line.strip() == '*plot*':
            line = ''
            while line != '*plot*' and line_num < len(lines):
                line = lines[line_num]
                if line[0:3] == 'sou':
                    plot_object.plot_sounding(line)
                if line[0:3] == 'lcl': 
                    plot_object.plot_lcl(line)
                if line[0:3] == 'mix': 
                    plot_object.plot_mixing_ratio(line)
                if line[0:3] == 'sat': 
                    plot_object.plot_saturation_mixing_ratio(line)
#                 if line[0:3] == 'rel': 
#                     plot_object.plot_relative_humidity(line)
                if line[0:3] == 'vap':
                    plot_object.plot_vapor_pressure(line)
                if line[0:3] == 'e_s': 
                    plot_object.plot_sat_vapor_pressure(line)
                if line[0:3] == 'pot': 
                    plot_object.plot_potential_temp(line)
                if line[0:3] == 'wet':
                    plot_object.plot_wetbulb_temp(line)
                if line[0:3] == 'pwe':
                    plot_object.plot_potential_wetbulb_temp(line)
                if line[0:3] == 'equ':
                    plot_object.plot_equ_temp(line)
                if line[0:3] == 'eqp':
                    plot_object.plot_equ_pot_temp(line)
    
                line_num = line_num + 1
            plot_num = plot_num + 1
            plot_dict = plot_object.get_plot_dict()
            plot = metpy_plot_lines(plot_dict)
            plt.savefig('skewt_plots_{}.png'.format(str(plot_num)))
            plot_object.reset_plot_dict()
                
        
            
            
    
    
    
    
    
    
    
    
    
if __name__ == "__main__":
    main()