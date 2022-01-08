# Monte Carlo Simulation in Python
Python implementation of Monte Carlo Simulation.

**Reference**: **[Minitab blog](https://blog.minitab.com/en/the-4-simple-steps-for-creating-a-monte-carlo-simulation-with-engage-or-workspace)**

## Usage
### Creating the simulator object

**MonteCarloSimulator** class accepts four parameters:
- transfer_equation: The expression that needs to be simulated with random values.
E.g: "unit_cost_km * total_road_length"
- bag_of_variables: A python dictionary having all variables used in the transfer equation. Variables must be keys and values can be 0
E.g:
```json
bag_of_variables = {
    "unit_cost_km": 0.0,
    "total_road_length": 0.0
}
```
- variable_pdfs: A python dictionary that defines the probability distribution of all variables used in the transfer equation. variable name must be the key and the value must be a dictionary having all parameters that define the distribution. 
E.g: A normal distribution can be defined as 
```json
variable_pdfs = {
    "unit_cost_km": {"name": "normal", "mean": 1000.0, "sd": 150.0},    
    "total_road_length": {"name": "uniform", "low": 45.0, "high": 55.0}  
}
```
- num_iterations: Number of times the simulation has to be run

Example: 
```python
mcs = MonteCarloSimulator(transfer_equation, bag_of_variables, variable_pdfs, num_iterations=10000)
```

### Setting up variable_pdfs input
Parameters for each distribution will be different. These parameters are used to generate randome samples for the respective variable.

Following distributions are supported currently. The example below shows mandatory keys to be present in the dictionary, for a given distribution:

*normal:* 
```
"<variable>": {"name": "normal", "mean": 1000.0, "sd": 15.0}
```
*poisson: *
```
"<variable>": {"name": "poisson", "mean": 1000.0, "scale": 5.0}
```
*binomial:*
```
"<variable>": {"name": "uniform", "low": 950.0, "high": 1050.0}
```
*lognormal:*
```
"<variable>": {"name": "lognormal", "mean": 950.0, "sigma": 50.0}
```
*pareto:*
```
"<variable>": {"name": "pareto", "mean": 950.0, "sigma": 50.0}
```
*exponential:*
```
"<variable>": {"name": "exponential", "scale": 950.0}
```
*gamma:*
```
"<variable>": {"name": "gamma", "shape": 1000.0, "scale": 950.0}
```
*weibull:*
```
"<variable>": {"name": "weibull", "shape": 1000.0}
```
*chisquare:*
```
"<variable>": {"name": "chisquare", "degfreedom": 1000.0}
```
*uniform:*
```
"<variable>": {"name": "uniform", "high": 1050.0, "low": 950.0}
```
*wald:*
```
"<variable>": {"name": "wald", "mean": 1050.0, "scale": 10.0}
```

### Running the simulation
To run the simulation,
```python
result = mcs.simulate()
```

### Result
The result of the simulation will be a dictionary containing the mean and standard deviation of the result set. 

Example:
```json
{'mean': 50047.51633784391, 'sd': 8073.175921116423}
```

## Implementation Details
Uses numpy library to generate random samples for a given variable using the supplied probability distribution

1. In each iteration, one random sample for each variable in the transfer equation is generated.

2. Transfer equation is evaluated with the generated random values, and the result is added into a list.
    - Evaluation of an expression is handled using python eval() function. The bag of variables dictionary is used to supply all constituent variables and their values (random values generated)
3. Steps 1 and 2 are repeated *num_iterations* times
4. Values obtained from each iteration are accumulated, and its *mean* and *standard deviation* are calculated

## Customize and Enhance - TODO Items
- Wrap python eval function and secure its usage. THis can be done by creating a module for performing evaluation and to supply all necessary python functions that may come up in transfer equations
- Avoid having to supply *bag_of_variables* as an input. *variable_pdfs* can be re-purposed 
- Explore the possibility of multi-processing for the simulation execution, inorder to speed things up
- simulate() method to return the list of generated result values, along with mean and standard deviation, so that the consuming code can use that data - for example plotting a histogram.

