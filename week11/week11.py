#a class is th code that defines a particular object, fudamental toobject oriented programming.
#class is how we deifne an object

#AMB is angent based modelling - computer simulation to replicate life 

#always an extra agrument in a class def called self that is passed first 

#this creates a class
class Schelling:
    
    def __init__(self, width, height, empty_ration, similarity_threshold, n_iterations): 
        self.width = width
        self.height = height
        self.empty_ration = empty_ration
        self.similarity_threshold = similarity_threshold
        self.n_iterations = n_iterations
        #storing each argument except self in instance variable with the same name
        
schelling = Schelling(25, 25, 0.25, 0.6, 500)
print (schelling.width)

    