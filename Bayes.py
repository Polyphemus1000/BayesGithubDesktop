from numpy import linspace, pi, arange, min, max, inf, sqrt, exp, ones
from scipy.integrate import simpson
from scipy.special import beta
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider # We will be working with sliders

class Bayes():
    
    def __init__(self):
        
        n = 200
        k = 40
        precision = 1024
        k2 = k/2
        n2= n/2 
        
        '''
        We set up the axis and figure for the whole class as essentially the function of this class is to plot
        '''
        self.prob_axis = linspace(0., 1.0, num = precision) # Set up the x axis 0 to 1 with 1024 separations 
        self.figure, self.axis = plt.subplots(nrows=4, ncols=1) # create the figure and the 3 grids
        self.figure.subplots_adjust(hspace=1.2) # This is to create space between the 3 grids/axes
        self.figure.subplots_adjust(bottom=0.25)# This is where we create the space for the sliders at the bottom
    
    
    def InitialValues(self, k2,n2, k,n, PriorSelection, LikelihoodSelection):
        x0=0.5 # not sure why we have to put this here and not in the init function
       
        # get the values from the InitialGui Radio buttons and then set the distribution function
        if PriorSelection ==1:
            prior = self.cauchy(self.prob_axis, x0, gamma=0.02)
            prior2 = self.cauchy(self.prob_axis, x0, gamma=0.1)
        elif PriorSelection == 2:
            prior = self.guassian(self.prob_axis, u=x0, sigma=0.02)
            prior2 =self.guassian(self.prob_axis, u=x0, sigma=0.1)
        elif PriorSelection == 3:
            prior = self.uniform(self.prob_axis)
            prior2 = self.uniform(self.prob_axis)
            
        if LikelihoodSelection ==4:
            likelihood = self.binomial(k, n, p=self.prob_axis)
            likelihood_normal = self.beta_coinflip(self.prob_axis, k2, n2)
        elif LikelihoodSelection ==5:
            likelihood = self.guassian(self.prob_axis, u=0.2, sigma=0.02)
            likelihood_normal = self.guassian(self.prob_axis, u=0.2, sigma=0.02)
        # Do Bayes analysis
        joint = prior * likelihood
        joint_varied = prior2 * likelihood
        
        # Get the amount of stuff in the posterior so we can normalise it
        
        evidence = simpson(joint, x=self.prob_axis)
        evidence2 = simpson(joint_varied, x=self.prob_axis)
        
        # normalise the posterior
        
        posterior = joint / evidence
        posterior2 = joint_varied/evidence2
          
        
        
        # Create the intial plots
        
        self.setThetaPlot(self.prob_axis, prior, prior2)
        self.setLikelihoodPlot(self.prob_axis, likelihood_normal,n,k)
        self.setPosteriorPlot(self.prob_axis, posterior, posterior2)
        self.setPosteriorNotNormalisedPlot(self.prob_axis, joint, joint_varied)
        
        
        
        
    
    
        # set up the slider parameters
        
        
        
        left = 0.25
        bottom = 0.15
        
        width = 0.65
        height = 0.03
        
       
        
        axTheta = self.figure.add_axes([left, bottom,width, height]) # This is where we set the axes up relative to the other axes
        Theta = Slider(ax = axTheta,label= 'Theta', valmin= 0.0, valmax = 1.0, valinit =x0, valstep=0.1)
        
        axLikelihood = self.figure.add_axes([left, 0.1, width, height])
        Likelihood = Slider( ax=axLikelihood, label='Likelihood', valmin= 0.0, valmax = 1.0, valinit =k2/100, valstep=0.1 )
        
        # This function is within the InitialValues function. It is called when the either of the the two sliders are moved
        
        def update(val):
        # This is the function that updates the graphs based on where the sliders are
        # Get the values from the slider
            f = Theta.val
            h = Likelihood.val
            x0 = f # The new x) is where the top slider is 
            if PriorSelection ==1:
                NewPrior = self.cauchy(self.prob_axis, x0, 0.02)
                NewPrior2 = self.cauchy(self.prob_axis, x0, 0.1)
            elif PriorSelection == 2:
                NewPrior = self.guassian(self.prob_axis, x0, sigma=0.02)
                NewPrior2 =self.guassian(self.prob_axis, x0, sigma=0.1)
            elif PriorSelection == 3:
                 NewPrior = self.uniform(self.prob_axis)
                 NewPrior2= self.uniform(self.prob_axis)  
            self.axis[0].cla() # clear the whole of the 0 axis
            self.setThetaPlot(self.prob_axis, NewPrior, NewPrior2) #plot again
            knew = h * 100 # get the number of new successes from the slider
            print(knew)
            print(n2)
            if LikelihoodSelection ==4:
                NewLikelihood = self.binomial(knew, n2, p=self.prob_axis)
                NewLikelihood_normal =  self.beta_coinflip(self.prob_axis, knew, n2)
            elif LikelihoodSelection ==5:
                NewLikelihood = self.guassian(self.prob_axis, h, sigma=0.02)
                NewLikelihood_normal = self.guassian(self.prob_axis, h, sigma=0.02)
            self.axis[1].cla()
            self. setLikelihoodPlot(self.prob_axis, NewLikelihood_normal,n2,knew)
            NewJoint = NewPrior * NewLikelihood
            NewJoint2 = NewPrior2 * NewLikelihood
        
            NewEvidence = simpson(NewJoint, x=self.prob_axis)
            NewEvidence2 = simpson(NewJoint2, x=self.prob_axis)
        
            NewPosterior = NewJoint / NewEvidence
            NewPosterior1 = NewJoint2/NewEvidence2
            self.axis[2].cla()
            self.axis[3].cla()
            self.setPosteriorNotNormalisedPlot(self.prob_axis, NewJoint, NewJoint2)
            self.setPosteriorPlot(self.prob_axis, NewPosterior, NewPosterior1)
              
        Theta.on_changed(update) # update the above when we move the theta slider
        Likelihood.on_changed(update) #update the above when we move the Likelihood slider
        
        
        plt.show() # show what we have done
        
    '''
    These functions are all called from within the InitialValues function
    
    '''   
    
    def beta_coinflip(self, p, k, n):    
        return p**k * (1 - p)**(n - k) / beta(k + 1, n - k + 1)
    
    def binomial(self, k, n, p):    
        return p**k * (1 - p)**(n - k)
      # Run the plot function within the S object to produce the plots using the values obtained from the entrybox and the option menus
       # S.runplot(p,g, h, i)
       
    def cauchy(self,p, x0, gamma):    
        z = (p - x0) / gamma    
        return 1 / ((1 + z**2) * (gamma * pi))
    
    def guassian(self,p, u, sigma):
        r =1/(sqrt(2 * pi * sigma**2))
        s = (p- u)**2/(2 * sigma **2)*-1
        return r * exp(s)
    
    def uniform (self,p):
        b=1;
        a=0
        print(len(p))
        return(ones(len(p))*1/(b-a))
    
    def setThetaPlot(self,prob_axisvalues, priorvalues1, priorvalues2):
        self.axis[0].plot(prob_axisvalues, priorvalues1,  color = 'red', label = 'High belief in prediction')
        self.axis[0].fill_between(prob_axisvalues, priorvalues1 ,0, color='red', alpha= 0.1)
        self.axis[0].plot(prob_axisvalues, priorvalues2,  color = 'blue', label = 'Low belief in prediction')
        self.axis[0].fill_between(prob_axisvalues, priorvalues2 ,0, color='blue', alpha= 0.1)
        self.axis[0].set_xticks(arange(min(prob_axisvalues), max(prob_axisvalues)+0.1, 0.05))
        
        #self.axis[0].set_yticks((0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0))
        #self.axis[0].set_ylim(0,1)
        self.axis[0].grid()
        self.axis[0].set_xlabel('$\\theta$, [Number  of  heads per flip of coin]')
        self.axis[0].set_ylabel('Prob. Density,  P($\\theta$)')
        likelihood = self.guassian(self.prob_axis, u=0.2, sigma=0.02)
        self.axis[0].legend(loc = 1)
        self.axis[0].set_title('Probability Distribution Function (Prior)  of P($\\theta$)')
        
    def setLikelihoodPlot(self,prob_axisvalues, normalisedDistribution, n,k):
        self.axis[1].plot(prob_axisvalues, normalisedDistribution,  color = 'blue', label = 'Likelihood of $\\theta$ with ' + str(n) + ' flips '+ str(k) + ' heads')
        self.axis[1].fill_between(prob_axisvalues, normalisedDistribution ,0, color='blue', alpha= 0.1)
        self.axis[1].set_xticks(arange(min(prob_axisvalues), max(prob_axisvalues)+0.1, 0.05))
        self.axis[1].legend(loc = 1)
        self.axis[1].grid()
        self.axis[1].set_xlabel('$\\theta$, [Number  of  heads per flip of coin]')
        self.axis[1].set_ylabel('Prob. Density, P(D| $\\theta$)')
        self.axis[1].set_title('Probability Distribution Function (Likelihood [normalised]) of  P (D | ($\\theta$)')
        
    def setPosteriorPlot(self,prob_axisvalues, posterior1values, posterior2values):
        PosteriorPlot = self.axis[2].plot(prob_axisvalues, posterior1values,  color = 'maroon', label = ' Probability Distribution Function of P ( $\\theta$ | D) with  high initial belief')
        self.axis[2].plot(prob_axisvalues, posterior2values,  color = 'green', label = 'Probability Distribution Function of P ( $\\theta$ | D) with  low initial belief')
        self.axis[2].fill_between(prob_axisvalues, posterior1values ,0, color='maroon', alpha= 0.1)
        self.axis[2].fill_between(prob_axisvalues, posterior2values ,0, color='green', alpha= 0.1)
        self.axis[2].set_xticks(arange(min(prob_axisvalues), max(prob_axisvalues)+0.1, 0.05))
        self.axis[2].set_xlabel('$\\theta$, [Number  of  heads per flip of coin]')
        self.axis[2].set_ylabel('Prob. Density, P($\\theta$ |D ) ')
        self.axis[2].legend(loc = 1)
        xmin, xmax, ymin, ymax = plt.axis()
        self.axis[2].grid()
        self.axis[2].set_title(' Probability Distribution Function (Posterior) of P ( $\\theta$ | D)')
        
    def setPosteriorNotNormalisedPlot(self,prob_axisvalues, Joint1values, Joint2values):
        PosteriorPlot = self.axis[3].plot(prob_axisvalues, Joint1values,  color = 'blue', label = ' Probability Distribution Function of P ( $\\theta$ | D) with  high initial belief')
        self.axis[3].plot(prob_axisvalues, Joint2values,  color = 'orange', label = 'Probability Distribution Function of P ( $\\theta$ | D) with  low initial belief')
        self.axis[3].fill_between(prob_axisvalues, Joint1values ,0, color='blue', alpha= 0.1)
        self.axis[3].fill_between(prob_axisvalues, Joint2values ,0, color='orange', alpha= 0.1)
        self.axis[3].set_xticks(arange(min(prob_axisvalues), max(prob_axisvalues)+0.1, 0.05))
        self.axis[3].set_xlabel('$\\theta$, [Number  of  heads per flip of coin]')
        self.axis[3].set_ylabel('P($\\theta$ |D ) Not Normalised')
        self.axis[3].legend(loc = 1)
        xmin, xmax, ymin, ymax = plt.axis()
        self.axis[3].grid()
        self.axis[3].set_title(' Probability Distribution Function (Posterior) of P ( $\\theta$ | D) Not Normalised')
    
    
    
    
   

