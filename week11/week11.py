#a class is th code that defines a particular object, fudamental toobject oriented programming.
#class is how we deifne an object

#AMB is angent based modelling - computer simulation to replicate life 

#always an extra agrument in a class def called self that is passed first 

from random import shuffle


#this creates a class
class Schelling:
    
    """
    Constructor for Schelling Class.
    Stores the Parameter. 
    
    * This function is called a constructor. It is called automatically 
    * when an instance of the class is created, and is used to handle 
    * the setup of an instance of this class (i.e. 'construct' it)
    """
    
    def __init__(self, width, height, empty_ratio, similarity_threshold, n_iterations, agents): 
        #storing each argument except self in instance variable with the same name
        self.width = width
        self.height = height
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        self.agents = ({})
        
        # get all house addresses
        all_houses = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        # shuffle the order of the houses, randmoises it
        shuffle(all_houses)
        
        #calculating empty houses and storing as n_empty 
        #need self and len to make them multipliable numbers   
        n_empty = int(self.empty_ratio * len(all_houses))
        
        # identify the empty houses with list slicing
        self.empty_houses = all_houses[:n_empty]
        
        #identify the remaining houses w/ list slicing       
        self.remaining_houses = all_houses[n_empty:]
        
        #print (all_houses)
        #print (self.empty_houses)
        print(len(self.remaining_houses))
    
#an instance of Schelling
schelling = Schelling(25, 25, 0.25, 0.6, 500, ({}))




#PART 2

#an AMB is made up of a class for the model and a class for the agents 

#building up our class...




    