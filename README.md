## Automating Calulations and Plotting of Unreported Meterological Elements

### Install
Download the project as a zip file by clicking on the green button above. Make sure packages and python are installed. These can be installed using the pip command. The packages needed are (some of these come with standard python installation): 
1. matplotlib: https://pypi.org/project/matplotlib/
2. metpy: https://pypi.org/project/MetPy/
4. bs4: https://pypi.org/project/beautifulsoup4/
3. numpy: https://pypi.org/project/numpy/
4. requests: https://pypi.org/project/requests/
5. sys
6. math

### How to use skewT_plotter.py
First format your input .txt file as follows: 
For entering manual sounding data, type \*data\* followed by pressures, temperatures, and dewpoints like shown below. **All inputs must be in hectopascals or degree Celsius.** 
```
*data*
p = 1000 970 900 850 800 700 500
t = 30 25 18.5 16.5 20 11 -13
d = 21.5 21 18.5 16.5 5 -4 -20
```
If the most recent Dulles sounding is wanted instead, this step is not nessesary. 
For entering the calculations wanted, type \*plot\* followed by the code of the calculation and the pressure, temperature, and dew point seperated by spaces. The codes are shown below: 


1. **sounding** = Plot the sounding given by data above

2. **sounding most recent** = Plot the most recent sounding from Dulles

3. **lcl p t d** = Plot how to find lifting condensation level using p, t, d

4. **mixing ratio p t d** = Plot the mixing ratio at p, t, d

5. **saturation mixing ratio p t d** = Plot the saturation mixing ratio using p, t, d

6. **vapor pressure p t d** = Plot the vapor pressure using p,t,d 

7. **e_s p t d** = Plot the saturation vapor pressure using p, t, d

8. **pot p t** = Plot the potential temperature using p, t

9. **wetbulb p t d** = Plot the wetbulb using p, t, d

10. **pwetbulb p t d** = Plot the potential wetbulb temperature using p, t, d

11. **equivalent temp p t d** = Plot the equivalent temperature using p, t, d

12. **peq temp p t d** = Plot the potential equivalent temperature using p, t, d

### Example: 
```
*data*
p = 1000 970 900 850 800 700 500
t = 30 25 18.5 16.5 20 11 -13
d = 21.5 21 18.5 16.5 5 -4 -20

*plot*
sounding
equivalent temp 700 -5 -10
```
If the following text is saved as *example.txt*, run the program by using the command: 
```
python skewT_plotter.py example.txt 
```
It should run and the output should save to a file called *skewt_plot_1.png* and it should look like: 
![alt text](https://github.com/mangomadhava/automating_skewT/blob/main/skewt_plots_1.png)

Other examples are included in the directory. 

#### Explanation of files: 
1. **plotting.py**: This file handles all the plotting using metypy and matplotlib. Examples of how to plot directly are in the examples.ipynb notebook. 
2. **calculations.py**: This file handles the calculations needed for computing different values on the skewT graph. Most of the functions are calls to the metpy calculations libary. Examples using the calculation are also in the examples.ipynb notebook. 
3. **skewT_plotter.py**: This file handles the parsing of the input text and runs the program if not using the GUI. It reads through the intput text and calls the correct functions in plotting.py to display the correct lines needed for deriving a calculation using the skewT.


This project was done as a final project for AOSC 431. 
