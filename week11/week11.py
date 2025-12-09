#a class is th code that defines a particular object, fudamental toobject oriented programming.
#class is how we deifne an object

#AMB is angent based modelling - computer simulation to replicate life 

#always an extra agrument in a class def called self that is passed first 

from random import shuffle
from matplotlib.pyplot import subplots, savefig, subplots_adjust

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
        
        # get the agents for each group using list slicing and comprehension
        red_group = [[coords, 'red'] for coords in self.remaining_houses[0::2]]    # every other cell from 0 to the end
        
        # get the agents for each group using list slicing and comprehension
        blue_group = [[coords, 'blue'] for coords in self.remaining_houses[1::2]]    # every other cell from 1 to the end
        
        # add both sets of agents to the instance variable
        self.agents.update(dict(red_group + blue_group))
        
    def plot(self, my_ax, title):
        """
       Plot the current state of the model
       """
        my_ax.set_title(title, fontsize=10, fontweight='bold')
        my_ax.set_xlim([0, self.width])
        my_ax.set_ylim([0, self.height])
        my_ax.set_xticks([])
        my_ax.set_yticks([])

        # plot agents one by one
        for agent in self.agents:

            # we can use the agent's group name as the colour directly!
            my_ax.scatter(agent[0]+0.5, agent[1]+0.5, color=self.agents[agent])
        
        #print (all_houses)
        #print (self.empty_houses)
        #print (len(self.remaining_houses))
        #print (red_group)
        #print (blue_group)
        #print (self.agents)
    
#an instance of Schelling
schelling = Schelling(25, 25, 0.25, 0.6, 500, ({}))

# initialise plot with two subplots (1 row, 2 columns)
fig, my_axs = subplots(1, 2, figsize=(14, 6))

# reduce the gap between the subplots
subplots_adjust(wspace=0.1)

# plot the initial state of the model into the first axis
schelling.plot(my_axs[0], 'Initial State')

# output image
savefig(f"./out/10.png", bbox_inches='tight')
print("done")




#PART 2

#an AMB is made up of a class for the model and a class for the agents 

#building up our class...




    