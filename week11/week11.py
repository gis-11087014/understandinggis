#a class is th code that defines a particular object, fudamental toobject oriented programming.
#class is how we deifne an object

#AMB is angent based modelling - computer simulation to replicate life 

#always an extra agrument in a class def called self that is passed first 

#this creates a class
class Schelling:
    
    """
    Constructor for Schelling Class.
    Stores the Parameter. 
    
    * This function is called a constructor. It is called automatically 
    * when an instance of the class is created, and is used to handle 
    * the setup of an instance of this class (i.e. 'construct' it)
    """
    
    def __init__(self, width, height, empty_ration, similarity_threshold, n_iterations, agents): 
        #storing each argument except self in instance variable with the same name
        self.width = width
        self.height = height
        self.empty_ration = empty_ration
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        self.agents = ({})

        # get all house addresses
        all_houses = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        print (all_houses)
    
#an instance of Schelling
schelling = Schelling(25, 25, 0.25, 0.6, 500, ({}))




#PART 2

#an AMB is made up of a class for the model and a class for the agents 

#building up our class...




    