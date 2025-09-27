import pandas as pd
import matplotlib.pyplot as plt


df_c02 = pd.read_csv("co2_emission.csv")                
df_le  = pd.read_csv("Life Expectancy Data.csv")        
df_wdi = pd.read_csv("f5a9ad86-f7cb-42ba-868e-b444c1d52fa4_Data.csv") 


countries = ["Argentina","Australia","Brazil","Canada","China","France","Germany","Italy",
             "India","Indonesia","Japan","Korea, Rep.","Mexico","Russia","Russian Federation",
             "Saudi Arabia","South Africa","United Kingdom","United States"]
years = list(range(2000, 2016))  


df_c02 = df_c02[["Entity", "Year", "Annual CO₂ emissions (tonnes )"]]
df_c02 = df_c02.rename(columns={"Entity": "Country",
                                "Annual CO₂ emissions (tonnes )": "CO2 Use"})
df_c02 = df_c02[df_c02["Country"].isin(countries) & df_c02["Year"].isin(years)]


df_le = df_le[["Country", "Year", "Life expectancy "]] 
df_le = df_le.rename(columns={"Life expectancy ": "Life Expectancy"})
df_le = df_le[df_le["Country"].isin(countries) & df_le["Year"].isin(years)]


df_wdi = df_wdi[["Country Name", "Time", "Value"]]
df_wdi = df_wdi.rename(columns={"Country Name": "Country",
                                "Time": "Year",
                                "Value": "GDP per capita USD"})
df_wdi = df_wdi[df_wdi["Country"].isin(countries) & df_wdi["Year"].isin(years)]

print("Years in Life Expectancy:", df_le["Year"].unique())
print("Years in CO2:", df_c02["Year"].unique())
print("Years in WDI:", df_wdi["Year"].unique())

#Life Expectancy dataset: descriptives + yearly mean plot
le_desc = df_le[["Life Expectancy"]].describe()
le_desc.to_csv("LE_descriptives.csv")

le_yearly = df_le.groupby("Year", as_index=False)["Life Expectancy"].mean()
chart = le_yearly.plot(x="Year", y="Life Expectancy", kind="line",
                    title="Life Expectancy — Mean Across Selected Countries")
chart.set_ylabel("Years")
chart.figure.tight_layout(); chart.figure.savefig("LE_yearly_mean.png"); chart.figure.clear()


# CO2 (total tonnes) — yearly mean (individual dataset)
co2_yearly_ind = df_c02.groupby("Year", as_index=False)["CO2 Use"].mean()
chart = co2_yearly_ind.plot(x="Year", y="CO2 Use", kind="line",
    title="Mean CO₂ (Total, Tonnes) — Individual Dataset")
chart.set_ylabel("Tonnes (mean across countries)")
chart.figure.tight_layout()
chart.figure.savefig("mean_CO2_over_time_individual.png")
chart.figure.clear()


# WDI (GDP per capita) dataset: descriptives 
gdp_yearly_ind = df_wdi.groupby("Year", as_index=False)["GDP per capita USD"].mean()

chart = gdp_yearly_ind.plot(x="Year", y="GDP per capita USD", kind="line",
    title="Mean GDP per capita — Individual Dataset")
chart.set_ylabel("USD")
chart.figure.tight_layout()
chart.figure.savefig("mean_GDPpc_over_time_individual.png")
chart.figure.clear()


#From here on charts are for the merged datasets
merged = df_le.merge(df_c02, on=["Country","Year"], how="inner") \
              .merge(df_wdi, on=["Country","Year"], how="inner")

merged = merged.dropna(subset=["Life Expectancy", "CO2 Use", "GDP per capita USD"])
merged.to_csv("merged_country_year.csv", index=False)
print("Merged rows:", len(merged))
print(merged.head())


yearly = merged.groupby("Year", as_index=False).agg({
    "Life Expectancy": "mean",
    "CO2 Use": "mean",
    "GDP per capita USD": "mean"
})

#All charts produced here are for merged datasets
"""
removed these as they provided charts for merged datasets which were already being covered by individual datasets

chart = yearly.plot(x="Year", y="Life Expectancy", kind="line",
                 title="Mean Life Expectancy (Selected Countries)")
chart.set_ylabel("Years"); chart.figure.tight_layout(); chart.figure.savefig("mean_LE_over_time.png"); chart.figure.clear()

chart = yearly.plot(x="Year", y="GDP per capita USD", kind="line",
                 title="Mean GDP per capita (Selected Countries)")
chart.set_ylabel("USD"); chart.figure.tight_layout(); chart.figure.savefig("mean_GDPpc_over_time.png"); chart.figure.clear()

chart = yearly.plot(x="Year", y="CO2 Use", kind="line",
                 title="Mean CO₂ (Total, Tonnes) — Selected Countries")
chart.set_ylabel("Tonnes (total)"); chart.figure.tight_layout(); chart.figure.savefig("mean_CO2_over_time.png"); chart.figure.clear()
"""

chart = merged.plot(kind="scatter", x="GDP per capita USD", y="Life Expectancy",
                 title="Life Expectancy vs GDP per capita")
chart.set_xlabel("GDP per capita (USD)"); chart.set_ylabel("Life Expectancy (years)")
chart.figure.tight_layout(); chart.figure.savefig("scatter_LE_vs_GDPpc.png"); chart.figure.clear()

chart = merged.plot(kind="scatter", x="CO2 Use", y="Life Expectancy",
                 title="Life Expectancy vs CO₂ (Total, Tonnes)")
chart.set_xlabel("CO₂ (total, tonnes)"); chart.set_ylabel("Life Expectancy (years)")
chart.figure.tight_layout(); chart.figure.savefig("scatter_LE_vs_CO2.png"); chart.figure.clear()

print("Saved per-dataset summaries and cross-dataset comparisons.")
