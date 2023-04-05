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

country_codes = ["PAK", "GBR", "CHN", "NAC", "IND"]  # country codes
wb.series.info('EN.ATM.GHGT.KT.CE')  # getting info from world bank api
indicator_id = {"EN.ATM.GHGT.KT.CE", "EN.ATM.CO2E.KT",
                "AG.LND.ARBL.ZS", "AG.LND.AGRI.ZS"}  # indicators to access data

#creating dictionary to access indicators.
AG = {"AG.LND.AGRI.ZS": "AGRICULTURAL LAND(%)"}
AGL = {"AG.LND.ARBL.ZS": "ARABLE LAND (%)"}
CO2 = {"EN.ATM.CO2E.KT": "CO2 EMISSIONS(KT)"}
GHG = {"EN.ATM.GHGT.KT.CE": "TOTAL GREENHOUSE GAS EMISSIONS(KT)"}

wb.series.info(indicator_id)

#accessing data by calling "world" function
AG_T, AG_world = world(AG.keys(), country_codes, 30)

#accessing data by calling "world" function
CO2_T, CO2_world = world(CO2.keys(), country_codes, 30)

#accessing data by calling "world" function
AGL_T, AGL_world = world(AGL.keys(), country_codes, 30)

#accessing data by calling "world" function
GHG_T, GHG_world = world(GHG.keys(), country_codes, 30)

#performing few operations like mean and renaming index to compare with world data
C = CO2_world.mean()
C1 = pd.DataFrame(C)
C1.reset_index(level=0, inplace=True)
CO2W = C1.rename(columns={"index": "year", 0: "mean"})

G = GHG_world.mean()
G1 = pd.DataFrame(G)
G1.reset_index(level=0, inplace=True)
GHGW = G1.rename(columns={"index": "year", 0: "mean"})

A = AG_world.mean()
A1 = pd.DataFrame(A)
A1.reset_index(level=0, inplace=True)
AGW = A1.rename(columns={"index": "year", 0: "mean"})

AL = AGL_world.mean()
AL1 = pd.DataFrame(AL)
AL1.reset_index(level=0, inplace=True)
AGLW = AL1.rename(columns={"index": "year", 0: "mean"})

c = CO2_T.rename(columns={"index": "year", 0: "mean"})
co2_t = c.rename_axis("year")

a = AG_T.rename(columns={"index": "year", 0: "mean"})
ag_t = a.rename_axis("year")

ag = AGL_T.rename(columns={"index": "year", 0: "mean"})
agl_t = ag.rename_axis("year")

g = GHG_T.rename(columns={"index": "year", 0: "mean"})
ghg_t = g.rename_axis("year")

# Making plot between foreast cover and arable land for whole world
fig, ax = plt.subplots(figsize=[7, 3])
color1 = "BLACK"
color2 = "RED"
color3 = "BLUE"

ax.plot(AGLW["year"], AGLW["mean"], marker="*", color=color1)
ax.set_ylabel("Arable land (% of land area)", color=color1, fontsize=7)
ax.set_xlabel("Year", color=color1, fontsize=16)
plt.xticks(rotation=90)

ax1 = ax.twinx()
ax1.plot(AGW["year"], AGW["mean"], color=color2, marker="o")
ax1.set_ylabel("Agricultural land (% of land area)",
               color=color2,
               fontsize=7)

plt.margins(x=0)
plt.title("Time series plot of ARABLE LAND and AGRICULTURAL LAND (% of total land)")

#boxplot
dd = [CO2_T["IND"], CO2_T["NAC"], CO2_T["CHN"], CO2W["mean"]]
ff = ["INDIA", "UNITED KINGDOM", "CHINA", "world"]
box(dd, ff)

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

#Heat map of agricultural land
rs = np.random.RandomState(0)
FORW = pd.DataFrame(rs.rand(8, 8))
corr = AG_T.corr()
plt.figure(figsize=(6, 7))
sns.heatmap(corr, annot=True)
plt.show()
