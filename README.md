# InaccurateEvolutionaryAlgorithm

This is probably horrible. Written to show a genetic algorithm for a computer science project - simulates the evolution of a species learning to throw a projectile onto a target.

This aims to find an optimal path, without using any actual maths (of course there is a lot of maths involved in the path calculation, but in real life, it's called gravity) in the numbers (maths involved is probability mapping).

We can work out the optimal speed, through the following;

- v = the new speed
- u = the old speed (given)
- b = the new angle (given)
- a = the old angle (given)

v = sqrt((sin(a)cos(a)u^2)/(sin(b)cos(b)))

# Credit
- [Daniel Shiffman] (http://natureofcode.com/) His tutorials introduced me to the basics of genetic algorithms.

# Versions
## main.py

First version made, uses linear fitness (I called it health for some reason).

## exponential_fitness.py

Uses exponential fitness, to allow for more differentiation between levels of fitness near the upper bound (1)

