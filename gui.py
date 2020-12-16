import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter import PhotoImage
from PIL import ImageTk,Image
from skewT_plotter import *
from matplotlib import pyplot as plt

window = tk.Tk()
window.title("Skew-T log-P Plotter")


#Header = tkFont.Font(family="Helvetica",size="40",weight="bold")
#Directions = tkFont.Font(slant="italic")
Title = tk.Label(text="Skew-T log-P Plotter", width=30,height=2)
Title.config(font=("Courier",40))
Title.pack()

##dulles button clicked
def run_IAD_data():
    plot_object = plot_handler()
    dulles_button.pack_forget()
    sounding_button.pack_forget()

    plot_object.plot_sounding('sounding most recent')

    plot_dict = plot_object.get_plot_dict()
    plot = metpy_plot_lines(plot_dict)
    plot_num = 1
    plt.savefig('skewt_plots_{}.png'.format(str(plot_num)))
    image = Image.open("skewt_plots_1.png")
    zoom = .75
    pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
    img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
    img_label = tk.Label(window, image=img)
    img_label.image = img
    img_label.pack()

#if they clicked sounding
#stimage = tk.PhotoImage(file="skewt_plots_1.png")
#Plot_label = tk.Label(window,image=stimage)

def Plot_skewT():

    entry.pack_forget()
    enter_P.pack_forget()
    P_box.pack_forget()
    enter_T.pack_forget()
    T_box.pack_forget()
    enter_Tb.pack_forget()
    Tb_box.pack_forget()
    enter_w.pack_forget()
    w_box.pack_forget()
    enter_ws.pack_forget()
    ws_box.pack_forget()
    enter_RH.pack_forget()
    RH_box.pack_forget()
    enter_LCL.pack_forget()
    LCL_box.pack_forget()
    enter_WB.pack_forget()
    WB_box.pack_forget()
    enter_WBP.pack_forget()
    WBP_box.pack_forget()
    enter_PT.pack_forget()
    PT_box.pack_forget()
    enter_EPT.pack_forget()
    EPT_box.pack_forget()
    go_button.pack_forget()

    plot_object = plot_handler()

    #If they checked Sounding
    if var1.get()==1:
        P = P_box.get()
        T = T_box.get()
        Tb = Tb_box.get()

        plot_object.add_temperatures(T)
        plot_object.add_pressures(P)
        plot_object.add_dew_points(Tb)
        plot_object.plot_sounding('sounding')

    #If they checked mixing ratio
    if var2.get()==1:
        w = w_box.get() #w is variable name for mixing ratio input values
        plot_object.plot_mixing_ratio(w)
    #If they checked saturation mixing ratio
    if var3.get()==1:
        ws = ws_box.get() #ws is variable name for saturated mixing ratio input values
        plot_object.plot_saturation_mixing_ratio(ws)
    #If they checked relative humidity
    if var4.get()==1:
        RH = RH_box.get() #RH is variable name for relative humidity input values
        # didnt do this one :(
        print("SORRY NOT IMPLEMENTED! :(")
    #If they checked LCL
    if var5.get()==1:
        LCL = LCL_box.get() #LCL is variable name for LCL input values
        plot_object.plot_lcl(LCL)
    #If they checked wet bulb temp
    if var6.get()==1:
        WB = WB_box.get() #WB is variable name for wet bulb temp input values
        plot_object.plot_wetbulb_temp(WB)
    #If they checked wet-bulb potential temp
    if var7.get()==1:
        WBP = WBP_box.get() #WBP is variable name for wet bulb potential temp input values
        plot_object.plot_potential_wetbulb_temp(WBP)
    #If they checked potential temp
    if var8.get()==1:
        PT = PT_box.get() #PT is variable name for potential temp input values
        plot_object.plot_potential_temp(PT)
    #If they checked equivalent potential temp
    if var9.get()==1:
        EPT = EPT_box.get() #EPT is variable name for equivalent potential temp input values
        plot_object.plot_equ_pot_temp(EPT)
    plot_dict = plot_object.get_plot_dict()
    plot = metpy_plot_lines(plot_dict)
    plot_num = 1
    plt.savefig('skewt_plots_{}.png'.format(str(plot_num)))
    image = Image.open("skewt_plots_1.png")
    zoom = .75
    pixels_x, pixels_y = tuple([int(zoom * x)  for x in image.size])
    img = ImageTk.PhotoImage(image.resize((pixels_x, pixels_y)))
    img_label = tk.Label(window, image=img)
    img_label.image = img
    img_label.pack()


entry = tk.Label(text="Enter sounding values below separated by spaces:")
enter_P = tk.Label(text="\nPressures (hPa):")
P_box = tk.Entry()
enter_T = tk.Label(text="\nTemperatures (\N{DEGREE SIGN}C):")
T_box = tk.Entry()
enter_Tb = tk.Label(text="\nDew point temperatures (\N{DEGREE SIGN}C):")
Tb_box = tk.Entry()

Top = tk.Label(text="In box(es) below enter pressure (hPa), temperature (\N{DEGREE SIGN}C), and dew point (\N{DEGREE SIGN}C) separated by spaces")

enter_w = tk.Label(text="Mixing ratio:")
w_box = tk.Entry()

enter_ws = tk.Label(text="Saturation mixing ratio:")
ws_box = tk.Entry()

enter_RH = tk.Label(text="RH:")
RH_box = tk.Entry()

enter_LCL = tk.Label(text="LCL:")
LCL_box = tk.Entry()

enter_WB = tk.Label(text="Wet-bulb temperature:")
WB_box = tk.Entry()

enter_WBP = tk.Label(text="Wet-bulb potential temperature:")
WBP_box = tk.Entry()

enter_PT = tk.Label(text="Potential temperature:")
PT_box = tk.Entry()

enter_EPT = tk.Label(text="Equivalent potential temperature:")
EPT_box = tk.Entry()

##input data button clicked

go_button = tk.Button(text="Go",bg="LightGreen",command=Plot_skewT)

def enter_sdata():
#clearing checklist, label and button
  c1.pack_forget()
  c2.pack_forget()
  c3.pack_forget()
  c4.pack_forget()
  c5.pack_forget()
  c6.pack_forget()
  c7.pack_forget()
  c8.pack_forget()
  c9.pack_forget()
  Label.pack_forget()
  options_button.pack_forget()

 #If they checked Sounding
  if var1.get()==1:
    entry.pack()
    enter_P.pack()
    P_box.pack()
    enter_T.pack()
    T_box.pack()
    enter_Tb.pack()
    Tb_box.pack()
  if var2.get()==1 or var3.get()==1 or var4.get()==1 or var5.get()==1 or var6.get()==1 or var7.get()==1 or var8.get()==1 or var9.get()==1:
    Top.pack()
    #If they checked mixing ratio
  if var2.get()==1:
    enter_w.pack()
    w_box.pack()
#If they checked saturation mixing ratio
  if var3.get()==1:
    enter_ws.pack()
    ws_box.pack()

#If they checked relative humidity
  if var4.get()==1:
    enter_RH.pack()
    RH_box.pack()

#If they checked LCL
  if var5.get()==1:
    enter_LCL.pack()
    LCL_box.pack()

#If they checked wet bulb temp
  if var6.get()==1:
    enter_WB.pack()
    WB_box.pack()

#If they checked wet-bulb potential temp
  if var7.get()==1:
    enter_WBP.pack()
    WBP_box.pack()

#If they checked potential temp
  if var8.get()==1:
    enter_PT.pack()
    PT_box.pack()

#If they checked equivalent potential temp
  if var9.get()==1:
    enter_EPT.pack()
    EPT_box.pack()

  #Go button
  go_button.pack(padx=5,pady=5)

Label=tk.Label(text="Choose output options:")
var1=tk.IntVar()
var2=tk.IntVar()
var3=tk.IntVar()
var4=tk.IntVar()
var5=tk.IntVar()
var6=tk.IntVar()
var7=tk.IntVar()
var8=tk.IntVar()
var9=tk.IntVar()
c1 = tk.Checkbutton(master=window, text="Plot sounding", variable=var1,onvalue=1,offvalue=0)
c2 = tk.Checkbutton(master=window, text="Mixing raio", variable=var2,onvalue=1,offvalue=0)
c3 = tk.Checkbutton(master=window, text="Saturation mixing ratio", variable=var3,onvalue=1,offvalue=0)
c4 = tk.Checkbutton(master=window, text="Relative humidity (RH)", variable=var4,onvalue=1,offvalue=0)
c5 = tk.Checkbutton(master=window, text="Lifting condensation level (LCL)", variable=var5,onvalue=1,offvalue=0)
c6 = tk.Checkbutton(master=window, text="Wet-bulb temperature", variable=var6,onvalue=1,offvalue=0)
c7 = tk.Checkbutton(master=window, text="Wet-bulb potential temperature", variable=var7,onvalue=1,offvalue=0)
c8 = tk.Checkbutton(master=window, text="Potential temperature", variable=var8,onvalue=1,offvalue=0)
c9 = tk.Checkbutton(master=window, text="Equivalent potential temperature", variable=var9,onvalue=1,offvalue=0)
options_button = tk.Button(master=window, text='Go',bg="LightGreen", command=enter_sdata)

def choose_options():
  Label.pack()
  c1.pack()
  c2.pack()
  c3.pack()
  c4.pack()
  c5.pack()
  c6.pack()
  c7.pack()
  c8.pack()
  c9.pack()
  options_button.pack(pady=4)
  dulles_button.pack_forget()
  sounding_button.pack_forget()

dulles_button = tk.Button(master=window,text="Use most recent\nsounding data from\nDulles International Airport",bg="SkyBlue", command = run_IAD_data)
dulles_button.pack(padx=10,pady=3)

sounding_button = tk.Button(master=window,text="Enter your own data",bg="SkyBlue",command=choose_options)
sounding_button.pack(padx=10,pady=10)

window.mainloop()
