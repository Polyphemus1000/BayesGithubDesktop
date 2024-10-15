import customtkinter
import tkinterDnD
import tkinter

#from Calculation_Numeric import Calculation_Numeric
#from SliderGui import SliderGui
from Bayes import Bayes


'''
This is the main program it sets up the initial Gui where the user is asked to input which distributions he/she is interested in.
When the button 'Show Distributions'  is clicked, the Bayes program is insubstatiated and from this the plots are produced.

'''

class InitialGui(customtkinter.CTk):
    
    def button_callback(self):
        PriorDistribution =self.radio_var.get() # get the values from the radio button
        LikelihoodDistribution = self.radio_var1.get() # get the values from the radio button
        # insubstatiate the Slider Gui class as the S object
        B= Bayes() # create the Bayes object B
        B.InitialValues(20,100, 40,200, PriorDistribution, LikelihoodDistribution) # run the funciton that runs everything else
        
        
      
        
    
    def __init__(self):
       
        
        # set up the InitialGui object without any functions apart from the one that is used for the reaction to the button being clicked
        
        super().__init__()
        self.geometry("1000x480")
        self.title("Bayes Analysis for different distributions")
        

        
       
        
        
        self.radio_var = tkinter.IntVar(value=0) # set up the variables that will be updated when we click the radio buttons
        self.radio_var1 = tkinter.IntVar(value=0)
        print(self.radio_var)
        
        # set up the overall shape
        
        frame_1 = customtkinter.CTkFrame(master=self)
        frame_1.pack(pady=20, padx=60, fill="both", expand=True)
        
        # set up the labels and the radio buttons and the final big button which will launch the Bayes class
        
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