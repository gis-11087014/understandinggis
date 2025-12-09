#a class is th code that defines a particular object, fudamental toobject oriented programming.
#class is how we deifne an object

#AMB is angent based modelling - computer simulation to replicate life 
#an AMB is made up of a class for the model and a class for the agents

#always an extra agrument in a class def called self that is passed first 

from random import shuffle
from matplotlib.pyplot import subplots, savefig, subplots_adjust
from copy import deepcopy
from random import choice

#this creates a class
class Schelling:
    
    """
    Constructor for Schelling Class.
    Stores the Parameter. 
    
    * This function is called a constructor. It is called automatically 
    * when an instance of the class is created, and is used to handle 
    * the setup of an instance of this class (i.e. 'construct' it)
    """
    
    # class variable containing list of neighbours
    neighbours = [ (i, j) for i in range(-1, 2) for j in range(-1, 2) if (i, j) != (0, 0) ]

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
        
    def is_unsatisfied(self, agent):
        
        #set these as 0 to keep track of how many neighbours are in the same and different groups
        count_similar = 0
        count_different = 0
        
        for n in self.neighbours: 
            try:
                #log whether the group of the neighbour matches the agent
                if self.agents[(agent[0]+n[0], agent[1]+n[1])] == self.agents[agent]:
                    count_similar += 1
                else:
                    count_different += 1

            # if we go off the edge of the map or house is empty, there is nothing to do
            except KeyError:
                continue
        try:
            # return whether or not the proportion of similar neighbours meets the threshold
            return count_similar / (count_similar + count_different) < self.similarity_threshold

        # catch the situation when there are only empty neighbours
        except ZeroDivisionError:
  
            # if this is the case they will be satisfied
            return False
    
    #print (all_houses)
    #print (self.empty_houses)
    #print (len(self.remaining_houses))
    #print (red_group)
    #print (blue_group)
    #print (self.agents)
    #print(neighbours)
    
    def run(self):
        
        #loop through itertaions of model 
        for i in range(1, self.n_iterations+1):
            
            #couns agents from 0
            n_changes = 0
            
            # create a new copy of the agents
            self.old_agents = deepcopy(self.agents)
            
            for agent in (self.old_agents):
                
                #is the person isnt satisifed then they need a new one from empty houses list
                if self.is_unsatisfied(agent):
                    
                    # randomly choose an empty house for them to move to
                    empty_house = choice(self.empty_houses)
                    
                    # add the new / remove the old location of the agent's house
                    self.agents[empty_house] = self.agents[agent]
                    del self.agents[agent]
                    
                    # add the new / remove the old house from the list of empty houses
                    self.empty_houses.append(agent)
                    self.empty_houses.remove(empty_house)
                    
                    #adding 1 to n_changes 
                    n_changes += 1
                    
            # update the user
            print(f"Iteration: {i+1}, Number of changes: {n_changes}")

            # stop iterating if no changes happened
            if n_changes == 0:
                print(f"\nFound optimal solution at {i+1} iterations\n")
                break
        
        return i
                    
    
#an instance of Schelling
schelling = Schelling(25, 25, 0.25, 0.6, 500, ({}))

#print(schelling.is_unsatisfied(list(schelling.agents.keys())[0]))

# initialise plot with two subplots (1 row, 2 columns)
fig, my_axs = subplots(1, 2, figsize=(14, 6))

# reduce the gap between the subplots
subplots_adjust(wspace=0.1)

# plot the initial state of the model into the first axis
schelling.plot(my_axs[0], 'Initial State')

#call stored in variable interaitons 
iterations = schelling.run()

# add the overall title into the model
fig.suptitle(f"Schelling Model of Segregation ({schelling.similarity_threshold * 100:.2f}% Satisfaction after {iterations} iterations)")

# plot the result into the second axis
schelling.plot(my_axs[1], "Final State")

# output image
savefig(f"./out/10.png", bbox_inches='tight')
print("done")









    