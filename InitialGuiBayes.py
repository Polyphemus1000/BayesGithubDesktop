import customtkinter
import tkinterDnD
import tkinter

#from Calculation_Numeric import Calculation_Numeric
#from SliderGui import SliderGui
from Bayes import Bayes


'''
This is the main program it sets up the initial Gui where the user is asked to input via drop-downs, the SOL Mid-point 
density and the heat flux in W/m^3
When the button 'Calculate values is clicked, the SliderGui program is insubstatiated and from this the plots are produced.

'''

class InitialGui(customtkinter.CTk):
    
    def button_callback(self):
        PriorDistribution =self.radio_var.get()
        LikelihoodDistribution = self.radio_var1.get()
        print(PriorDistribution)
        print(LikelihoodDistribution)
        # insubstatiate the Slider Gui class as the S object
        B= Bayes()
        B.InitialValues(20,100, 40,200, PriorDistribution, LikelihoodDistribution)
      
        
    
    def __init__(self):
        #customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
        
        #customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
        #customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
        
        # set up the GUI
        
        super().__init__()
        self.geometry("1000x480")
        self.title("Bayes Analysis for different distributions")
        
       # print(type(app), isinstance(app, tkinterDnD.Tk))
       
       # Set up the way to get the information back from the GUI
        
       
        
        
        self.radio_var = tkinter.IntVar(value=0)
        self.radio_var1 = tkinter.IntVar(value=0)
        print(self.radio_var)
        
        # set up the overall shape
        
        frame_1 = customtkinter.CTkFrame(master=self)
        frame_1.pack(pady=20, padx=60, fill="both", expand=True)
        
        # set up the labels
        
        label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text = "Whiich distribution should be used for the Prior")
        label_1.grid(row=1, column=0, padx=20, pady=20)
        
        self.radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, text="Cauchy",
                                             variable= self.radio_var, value = 1)
        self.radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, text="Guassian",
                                             variable= self.radio_var, value = 2)
        self.radiobutton_3 = customtkinter.CTkRadioButton(master=frame_1, text="Flat",
                                              variable= self.radio_var, value = 3)
        self.radiobutton_1.grid(row=1, column=1, padx=20, pady=20)
        self.radiobutton_2.grid(row=1, column=2, padx=20, pady=20)
        self.radiobutton_3.grid(row=1, column=3, padx=20, pady=20)
        
        label_2 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text = "Whiich distribution should be used for the Likelihood")
        label_2.grid(row=2, column=0, padx=20, pady=20)
        
        self.radiobutton_4 = customtkinter.CTkRadioButton(master=frame_1, text="Binomial",
                                              variable= self.radio_var1, value = 4)
        self.radiobutton_5 = customtkinter.CTkRadioButton(master=frame_1, text="Guassian",
                                              variable= self.radio_var1, value = 5)
        self.radiobutton_4.grid(row=2, column=1, padx=20, pady=20)
        self.radiobutton_5.grid(row=2, column=2, padx=20, pady=20)
        
        button_1 = customtkinter.CTkButton(master=frame_1, command=self.button_callback, text = 'Show Distributions')
        button_1.grid(row=6, column=1, padx=20, pady=20)
     
        
  
        
#insubstatiate      
app = InitialGui() 

# Keep it on the screen      
app.mainloop()