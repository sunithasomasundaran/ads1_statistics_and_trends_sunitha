import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import wbgapi as wb
import seaborn as sns


def world(ind, code, years):
    '''
    this function returns original data, transposed data and world data for above indicators

    Parameters
    ----------
    ind : index
    code : country code
    years : total number of years

    Returns
    -------
    data : original data
    data_t : transposed data
    worlddata : complete world data

    '''
    data = wb.data.DataFrame(ind, code, mrv=years)
    data_t = data.T
    worlddata = wb.data.DataFrame(ind, mrv=years)
    return data, data_t, worlddata


def modify(data):
    '''
    this method can be used to clean up and generate modified data

    Parameters
    ----------
    data : the data to be modified

    Returns
    -------
    data_mod1 : modified data with mean
    data_mod3 : modified data after indexing and renaming

    '''
    data_mod1 = data.mean()
    data_mod2 = pd.DataFrame(data_mod1)
    data_mod2.reset_index(level=0, inplace=True)
    data_mod3 = data_mod2.rename(columns={"index": "year", 0: "mean"})
    return data_mod1, data_mod3


def box(x, y):
    '''
    box plot comparing the countries- INDIA, UNITED KINGDOM, CHINA with world

    Parameters
    ----------
    x : data for x-axis
    y : Tdata for y-axis

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

country_codes = ["PAK", "GBR", "CHN", "NAC", "IND"]  # country codes
wb.series.info('EN.ATM.GHGT.KT.CE')  # getting info from world bank api
indicator_id = {"EN.ATM.GHGT.KT.CE", "EN.ATM.CO2E.KT",
                "AG.LND.ARBL.ZS", "AG.LND.AGRI.ZS"}  # indicators to access data

#creating dictionary to access indicators.
AG = {"AG.LND.AGRI.ZS": "AGRICULTURAL LAND(%)"}
ABL = {"AG.LND.ARBL.ZS": "ARABLE LAND (%)"}
CO2 = {"EN.ATM.CO2E.KT": "CO2 EMISSIONS(KT)"}
GHG = {"EN.ATM.GHGT.KT.CE": "TOTAL GREENHOUSE GAS EMISSIONS(KT)"}

wb.series.info(indicator_id)

#accessing data by calling "world" function
AG, AG_T, AG_world = world(AG.keys(), country_codes, 30)
AG_T.describe()

#accessing data by calling "world" function
Co2, CO2_T, CO2_world = world(CO2.keys(), country_codes, 30)
CO2_T.describe()


#accessing data by calling "world" function
ABL, ABL_T, ABL_world = world(ABL.keys(), country_codes, 30)
ABL_T.describe()

#accessing data by calling "world" function
GHG, GHG_T, GHG_world = world(GHG.keys(), country_codes, 30)
GHG_T.describe()

#modified data for Co2
co2_mod, co2_W_mod = modify(CO2_world)
Ghg_mod, Ghg_W_mod = modify(GHG_world)
ag_mod, ag_W_mod = modify(AG_world)
abl_mod, abl_W_mod = modify(ABL_world)
abl_W_mod.describe()
c = CO2_T.rename(columns={"index": "year", 0: "mean"})
co2_t = c.rename_axis("year")
a = AG_T.rename(columns={"index": "year", 0: "mean"})
ag_t = a.rename_axis("year")
ag = ABL_T.rename(columns={"index": "year", 0: "mean"})
agl_t = ag.rename_axis("year")
g = GHG_T.rename(columns={"index": "year", 0: "mean"})
ghg_t = g.rename_axis("year")

# generate line plot of foreast cover over arable land for whole world
fig, ax = plt.subplots(figsize=[7, 3])
ax.plot(abl_W_mod["year"], abl_W_mod["mean"], marker="*")
ax.set_ylabel("Arable land (% of land area)", fontsize=7)
ax.set_xlabel("Year", fontsize=16)
plt.xticks(rotation=90)
ax1 = ax.twinx()
ax1.plot(ag_W_mod["year"], ag_W_mod["mean"], color="RED", marker="o")
ax1.set_ylabel("Agricultural land (% of land area)",
               fontsize=7)
plt.title("Time series plot of ARABLE LAND and AGRICULTURAL LAND (% of total land)")
plt.show()

#geberate box plot
data = [CO2_T["IND"], CO2_T["NAC"], CO2_T["CHN"], co2_W_mod["mean"]]
coun = ["INDIA", "UNITED KINGDOM", "CHINA", "world"]
box(data, coun)

#violin plot for Green house gas emissian for countries, INDIA, UNITED KINGDOM, CHINA
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)
ax1.violinplot(GHG_T["IND"], showmedians=True, points=10)
ax1.set_xticks([1])
ax1.set_ylabel("GREEN HOUSE GAS EMISSION")
ax1.set_xticklabels(["INDIA"])
ax2.violinplot(GHG_T["GBR"], showmedians=True, points=100)
ax2.set_xticks([1])
ax2.set_xticklabels(["UK"])
ax3.violinplot(GHG_T["CHN"], showmedians=True, points=500)
ax3.set_xticks([1])
ax3.set_xticklabels(["CHINA"])
plt.show()

#Heat map of greenhouse gases
rs = np.random.RandomState(0)
FORW = pd.DataFrame(rs.rand(8, 8))
corr = GHG_T.corr()
plt.figure(figsize=(6, 7))
sns.heatmap(corr, annot=True)
plt.show()
