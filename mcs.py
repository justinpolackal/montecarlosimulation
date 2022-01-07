import numpy as np
from numpy.random import default_rng
import matplotlib.pyplot as plt


class MonteCarloSimulator(object):
    def __init__(self, transfer_equation, bag_of_variables, variable_pdfs, num_iterations=1000):
        self.transfer_equation = transfer_equation
        self.bov = bag_of_variables
        self.variable_pdfs = variable_pdfs
        self.num_iterations = num_iterations

        self.rng = default_rng()
        self.samplers = {
                "normal": self.random_sampler_normal,
                "poisson": self.random_sampler_poisson,
                "binomial": self.random_sampler_binomial,
                "lognormal": self.random_sampler_lognormal,
                "pareto": self.random_sampler_pareto,
                "exponential": self.random_sampler_exponential,
                "gamma": self.random_sampler_gamma,
                "weibull": self.random_sampler_weibull,
                "chisquare": self.random_sampler_chisquare,
                "uniform": self.random_sampler_uniform,
                "wald": self.random_sampler_wald
            }

    def random_sampler_normal(self, pdf, size=None):
        """
        Return a random sample from a given normal distribution
        :param pdf: Dictionary of parameters that defines a normal distribution - mean and standard deviation are mandatory keys in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.normal(loc=pdf.get("mean"), scale=pdf.get("sd"), size=size)

    def random_sampler_wald(self, pdf, size=None):
        """
        Return a random sample from a given wald distribution
        :param pdf: Dictionary of parameters that defines a wald distribution - mean and scale are mandatory keys in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.wald(loc=pdf.get("mean"), scale=pdf.get("scale"), size=size)

    def random_sampler_poisson(self, pdf, size=None):
        """
        Return a random sample from a given poisson distribution
        :param pdf: Dictionary of parameters that defines a poisson distribution - lambda is a mandatory key in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.poisson(loc=pdf.get("lambda"), size=size)

    def random_sampler_binomial(self, pdf, size=None):
        """
        Return a random sample from a given binomial distribution
        :param pdf: Dictionary of parameters that defines a binomial distribution - numtrials and probsuccess are mandatory keys in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.binomial(pdf.get("numtrials"), pdf.get("probsuccess"), size=size)

    def random_sampler_uniform(self, pdf, size=None):
        """
        Return a random sample from a given uniform distribution
        :param pdf: Dictionary of parameters that defines a uniform distribution - low and high are mandatory keys in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.uniform(pdf.get("low"), pdf.get("high"), size=size)

    def random_sampler_chisquare(self, pdf, size=None):
        """
        Return a random sample from a given chisquare distribution
        :param pdf: Dictionary of parameters that defines a chisquare distribution - degfreedom is a mandatory key in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.chisquare(pdf.get("degfreedom"), size=size)

    def random_sampler_weibull(self, pdf, size=None):
        """
        Return a random sample from a given weibull distribution
        :param pdf: Dictionary of parameters that defines a weibull distribution - shape is a mandatory key in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.weibull(pdf.get("shape"), size=size)

    def random_sampler_gamma(self, pdf, size=None):
        """
        Return a random sample from a given gamma distribution
        :param pdf: Dictionary of parameters that defines a gamma distribution - shape and scale are mandatory keys in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.gamma(pdf.get("shape"), pdf.get("scale"), size=size)

    def random_sampler_lognormal(self, pdf, size=None):
        """
        Return a random sample from a given lognormal distribution
        :param pdf: Dictionary of parameters that defines a lognormal distribution - mean and sigma are mandatory keys in the dictionary.
                    Note: mean and sigma are not the values for the distribution itself, but of the underlying normal distribution it is derived from.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.lognormal(pdf.get("mean"), pdf.get("sigma"), size=size)

    def random_sampler_exponential(self, pdf, size=None):
        """
        Return a random sample from a given exponential distribution
        :param pdf: Dictionary of parameters that defines a exponential distribution - scale is a mandatory key in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.exponential(pdf.get("scale"), size=size)

    def random_sampler_pareto(self, pdf, size=None):
        """
        Return a random sample from a given pareto distribution
        :param pdf: Dictionary of parameters that defines a pareto distribution - shape is a mandatory key in the dictionary.
        :param size: Number / Shape of the returned result set. By Default set to None - which means the result is a single value
        :return: random sample
        """
        return self.rng.pareto(pdf.get("shape"), size=size)

    def get_random_sample(self, pdf):
        """
        Return a random sample using the distribution function for the given variable
        :param pdf: Dictionary containing attributes of the variable's distribution function.
                    For E.g: If the variable follows normal distribution, the dictionary will look like {"mean": <value>, "sd": <value>}
        :return: random sample for the given variable
        """
        rand_sample = 0
        try:
            distribution = pdf.get("name")
            if distribution is None or self.samplers.get(distribution) is None:
                raise Exception(f"Sampler for {distribution} not implemented")

            rand_sample = self.samplers[distribution](pdf, size=None)

        except Exception as e:
            print(f"get_random_sample: {e}")
        return rand_sample

    def refresh_bov(self):
        """
        Refresh bov with new set of random samples for each variable in the transfer equation.
        """
        try:
            for key in self.bov.keys():
                pdf = self.variable_pdfs.get(key)
                if pdf is None:
                    continue

                rand_sample = self.get_random_sample(pdf)
                self.bov[key] = rand_sample

        except Exception as e:
            print(f"refresh_bov: {e}")
            return False
        return True


    def simulate(self):
        """
        Perform simulation.
        :return:
        """
        values = []
        for i in range(self.num_iterations):
            self.refresh_bov()
            te_result = eval(self.transfer_equation, self.bov)
            values.append(te_result)

        values_np = np.array(values)
        calc_mean = values_np.mean()
        calc_sd = values_np.std()

        return {"mean": calc_mean, "sd": calc_sd}

"""
Example: calculates total road cost from unit cost per km and total road length
"""
transfer_equation = "unit_cost_km * total_road_length"

bov = {
    "unit_cost_km": 0.0,
    "total_road_length": 0.0
}

pdfs = {
    "unit_cost_km": {"name": "normal", "mean": 1000.0, "sd": 150.0},    #unit cost follows normal distribution
    "total_road_length": {"name": "uniform", "low": 45.0, "high": 55.0}  # total road length follows uniform distribution
}

mcs = MonteCarloSimulator(transfer_equation, bov, pdfs, num_iterations=10000)
res = mcs.simulate()
print(res)


# Now plot the histogram of all the values generated
#num_bins = 100
#n, bins, patches = plt.hist(values, num_bins, facecolor='blue', alpha=0.5)
#plt.show()


