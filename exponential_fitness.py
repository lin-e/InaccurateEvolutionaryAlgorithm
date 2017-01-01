from turtle import *
from math import *
from random import *

# display config
WIDTH = 1280 # size of 'canvas'
HEIGHT = 720 # ''
MARGIN = 25 # margin on 'canvas'
SCALE = 100 # scale (just leave it)
UPDATES_PER_SECOND = 20 # the higher this number, the smoother the line, but the slower it runs

# simulation config
GRAVITY = 9.81 # using earth's gravity
VARIATION = 0.01 # percentage of which a value can mutate by
MUTATION = 0.005 # percentage of mutation
TARGET_WIDTH = 0.2 # width of the target zone (in metres, technically)
POPULATION = 16 # the size of the population per generation
GENERATIONS = 1000 # the number of generations to simulate
HIT_BOOST = 0.0 # the amount the fitness is boosted by when it hits the target zone
fitness_EXPONENT = 2 # the higher this value, the more drastic the change in fitness from the previous fitness; such that evolution occurs faster
SPEED_RANGE = (5, 15) # random range for initial population
ANGLE_RANGE = (0, 90) # ''
RANDOM = True
OPT_SPEED = randint(7, 11) if RANDOM else 10 # apparently the average speed of a thrown basketball? 
OPT_ANGLE = randint(25, 65) if RANDOM else 45 # optimal value for distance

print("Target made with a speed of ", OPT_SPEED, "m/s and an angle of", OPT_ANGLE, "degrees.")

# var init
horizontal_bounds = (MARGIN - (WIDTH / 2), (WIDTH / 2) - MARGIN) # creates boundaries
vertical_bounds = (MARGIN - (HEIGHT / 2), (HEIGHT / 2) - MARGIN) # ''
screen = Screen() # init screen
screen.colormode(255) # ''
screen.setup(width=WIDTH, height=HEIGHT) # ''
speed(0) # ''
delay(0) # ''
target_x = (cos(radians(OPT_ANGLE)) * OPT_SPEED) * ((2 * (sin(radians(OPT_ANGLE)) * OPT_SPEED)) / GRAVITY) # calculated target

# functions
def draw_line(x1, y1, x2, y2, settings=[1, 1, 0, 0]):
    max_height = vertical_bounds[1] # sets max height
    if (y1 * settings[1]) + settings[3] > max_height: # prevents it from drawing outside the bounds
        return # ''
    if (y2 * settings[1]) + settings[3] > max_height: # ''
        return # ''
    penup() # takes the pen off canvas
    goto((x1 * settings[0]) + settings[2], (y1 * settings[1]) + settings[3]) # go to remapped x1
    pendown() # starts drawing
    goto((x2 * settings[0]) + settings[2], (y2 * settings[1]) + settings[3]) # go to remapped x2
    penup() # takes the pen off canvas
def fade(c1, c2, amount):
    cr = list() # consider each colour as a 3d matrix
    for i in range(0, 3): # does this 3 times
        cr.append(round(c1[i] + (amount * (c2[i] - c1[i])))) # c1 + (i)delta(c)
    return (cr[0], cr[1], cr[2]) # returns as array

# classes
class path:
    def __init__(self, initial_speed, initial_direction):
        self.angle = initial_direction # sets values
        self.speed = initial_speed # ''
        # the trigonometric functions arent perfect, but its close enough for a 2d model
        self.initial_x = cos(radians(self.angle)) * self.speed # resolves from a speed to vector
        self.initial_y = sin(radians(self.angle)) * self.speed # ''
        self.fitness = 0 # initial fitness of 0
    def position(self, time):
        global GRAVITY # uses gravity from config
        return (self.initial_x * time, time * (self.initial_y - ((GRAVITY * time) / 2))) # trust me, this equation works
    def distance(self):
        global GRAVITY # uses gravity from config
        return self.initial_x * ((2 * self.initial_y) / GRAVITY) # this also works
class generation:
    def __init__(self):
        self.population = list() # list of the entire population
        self.fitness = dict() # stores population with fitness (this is very inefficient, but it was useful when testing)
        self.sorted_fitness = list() # sorts the population by fitness
        self.probability = dict() # remaps probability
        self.hits = 0 # the number of hits in this generation
        self.average = 0 # the average fitness
    def simulate(self, c=(0, 0, 0)):
        if c == (0, 0, 0): # if the colour is black
            clear() # clears the screen
        color("blue") # sets to blue
        width(5) # sets width
        draw_line(target_x - (TARGET_WIDTH / 2), 0, target_x + (TARGET_WIDTH / 2), 0, (SCALE, SCALE, horizontal_bounds[0], vertical_bounds[0])) # draws target zone
        width(1) # sets width
        color("black") # sets to black
        draw_line(horizontal_bounds[0], vertical_bounds[0], horizontal_bounds[1], vertical_bounds[0]) # draws margins
        draw_line(horizontal_bounds[0], vertical_bounds[1], horizontal_bounds[1], vertical_bounds[1]) # ''
        draw_line(horizontal_bounds[1], vertical_bounds[0], horizontal_bounds[1], vertical_bounds[1]) # ''
        draw_line(horizontal_bounds[0], vertical_bounds[0], horizontal_bounds[0], vertical_bounds[1]) # ''
        total_fitness = 0 # sets total fitness, used later
        color(c) # sets colour to the specified value
        for individual in self.population: # each item in population
            last_point = (0, 0) # starts at origin
            i = 0 # current time step
            while True: # iterates until exited
                new_point = individual.position(i / UPDATES_PER_SECOND) # finds the item at the specified time step
                draw_line(last_point[0], last_point[1], new_point[0], new_point[1], (SCALE, SCALE, horizontal_bounds[0], vertical_bounds[0])) # draws line between new and previous point, im pretty sure there's an arc function, but thats a lot of maths
                last_point = new_point # sets the old point to the new point
                i += 1 # increments time
                if new_point[1] < 0: # if it lands (hits the ground)
                    break # exit
                if new_point[0] > (WIDTH - (2 * MARGIN)) / SCALE: # of it exits the bounds
                    break # exit
            fitness = float("{0:.4f}".format((target_x - abs(individual.distance() - target_x)) / target_x)) # it's possible to have a negative fitness if the distance from the target is huge
            if fitness < 0: # if it is negative
                fitness = 0 # set to zero (see, using a negative probability seems slightly redundant, this therefore sets an lower bound on the fitness)
            fitness = float("{0:.4f}".format(fitness**fitness_EXPONENT)) # prevents linear growth
            if (individual.distance() > target_x - (TARGET_WIDTH / 2)) and (individual.distance() < target_x + (TARGET_WIDTH / 2)): # if it lands in the target
                self.hits += 1 # increments number of hits
                fitness += HIT_BOOST # if it hits the target, it is boosted by this amount in the probability weight
                self.average -= HIT_BOOST # removes from average, as the hit boost is only used for probability
            total_fitness += fitness # increment total fitness
            self.average += fitness # increment average
            self.fitness[fitness] = individual; # sets the dictionary
            individual.fitness = fitness # sets the fitness value
        last_probability = 0 # last probability; we use a cumulative system in order to set boundaries
        self.average /= len(self.population) # divides by the population length to get a meme
        for individual in sorted(self.fitness.keys(), reverse=True): # sorts with highest first
            self.sorted_fitness.append(self.fitness[individual]) # adds into list
            next_probability = last_probability + (individual / total_fitness) # maps it to get a total of 1
            self.probability[next_probability] = self.fitness[individual] # sets value
            last_probability = next_probability # resets previous probability
    def pick(self):
        upper_bounds = sorted(self.probability.keys(), reverse=True) # gets a list of upper bounds, highest first
        position = uniform(0, 1) # sets a position between 0, and 1
        selected = self.probability[upper_bounds[0]] # selects the first item
        for i in upper_bounds: # for each item in the upper bound list
            if position > i: # if its larger than the upper bound
                break # exit
            selected = self.probability[i] # sets the current item to the random position
        return selected # returns the randomly selected item
    def reproduce(self):
        new_generation = generation() # starts new generation
        for i in range(0, len(self.population)): # same population as current generation
            parent_a = self.pick() # picks an individual
            parent_b = self.pick() # ''
            while parent_a == parent_b: # we assume that algorithms arent asexual, in order to create more variation
                parent_b = self.pick() # picks another
            new_speed = parent_a.speed if randint(0, 1) == 0 else parent_b.speed # randomly picks whether to use parent a or parent b's gene
            if uniform(0, 1) < MUTATION: # if it mutates
                new_speed = uniform(SPEED_RANGE[0], SPEED_RANGE[1]) # generates a new speed
            new_angle = parent_a.angle if randint(0, 1) == 0 else parent_b.angle # randomly picks whether to use parent a or parent b's gene
            if uniform(0, 1) < MUTATION: # if it mutates
                new_angle = uniform(ANGLE_RANGE[0], ANGLE_RANGE[1]) # generates a new angle
            new_generation.population.append(path(new_speed * (1 + uniform(0 - VARIATION, VARIATION)), new_angle * (1 + uniform(0 - VARIATION, VARIATION)))) # adds to new population with mutations
        return new_generation # returns the new generation
    
for i in range(1, 90): # just a proof that there is an optimal solution, as long as the angle is not 0 or 90
    break # this just outputs loads of information, so we are exiting the loop
    optimal_speed = sqrt(((OPT_SPEED**2) * sin(radians(OPT_ANGLE)) * cos(radians(OPT_ANGLE))) / (sin(radians(i)) * cos(radians(i)))) # calculates the optimal speed
    print("Optimal Calculations:", "{0:.2f}".format(optimal_speed), "m/s at", str(i), "degrees.") # outputs calculations
last_generation = generation() # creates a generation
for i in range(0, POPULATION):  # creates n number of individuals
    last_generation.population.append(path(uniform(SPEED_RANGE[0], SPEED_RANGE[1]), uniform(ANGLE_RANGE[0], ANGLE_RANGE[1]))) # creates a random individual
for generation_number in range(0, GENERATIONS): # does this per generation
    #c = fade((255, 255, 255), (1, 1, 1), generation_number / (GENERATIONS - 1)) # colour fading to show evolution
    #last_generation.simulate(c) # draws with colour
    last_generation.simulate() # simulates without colour
    print("Average fitness of generation [", str(generation_number), "]:", "{0:.4f}".format(last_generation.average), "(", str(last_generation.hits), ("hits" if not last_generation.hits == 1 else "hit") , ")") # shows generation stats
    print("    Best: [",
          "Speed:", "{0:.4f}".format(last_generation.sorted_fitness[0].speed), ",",
          "Angle:", "{0:.4f}".format(last_generation.sorted_fitness[0].angle), ",",
          "fitness:", "{0:.4f}".format((last_generation.sorted_fitness[0].fitness) if (last_generation.sorted_fitness[0].fitness <= 1) else (last_generation.sorted_fitness[0].fitness - HIT_BOOST)),
          "]")
    last_generation = last_generation.reproduce() # reproduces
