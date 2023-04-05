import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import wbgapi as wb
import seaborn as sns


def world(x, y, z):
    '''
    the function transposes the data and returns the original and transposed data

    Parameters
    ----------
    x : the index key of the data
    y : the country code
    z : the data count

    Returns
    -------
    data_t : transposed data
    worlddata : the complete world data

    '''
    data = wb.data.DataFrame(x, y, mrv=z)
    data_t = data.T
    worlddata = wb.data.DataFrame(x, mrv=z)
    return data_t, worlddata


def box(x, y):
    '''
    generate box plot comparing the countries- INDIA, UNITED KINGDOM, CHINA with world

    Parameters
    ----------
    x : x-axis data
    y : y-axis data

    Returns
    -------
    None.

    '''
    fig = plt.figure(figsize=(4, 3))
    ax = fig.add_axes([0, 0, 1, 1])
    cc = ax.boxplot(x)
    ax.set_xlabel("countries")
    ax.set_ylabel("CO2 EMISIONS(% change)")
    ax.set_title("CO2 EMMISIONS COMPARISIONS")
    ax.set_xticks([1, 2, 3, 4])
    ax.set_xticklabels(y)
    plt.show()
    return
