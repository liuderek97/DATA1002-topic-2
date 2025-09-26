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
                                "Annual CO₂ emissions (tonnes )": "CO2_use"})
df_c02 = df_c02[df_c02["Country"].isin(countries) & df_c02["Year"].isin(years)]


df_le = df_le[["Country", "Year", "Life expectancy "]] 
df_le = df_le.rename(columns={"Life expectancy ": "LifeExpectancy"})
df_le = df_le[df_le["Country"].isin(countries) & df_le["Year"].isin(years)]

# WDI GDP per capita (already long)
df_wdi = df_wdi[["Country Name", "Time", "Value"]]
df_wdi = df_wdi.rename(columns={"Country Name": "Country",
                                "Time": "Year",
                                "Value": "GDP_per_capita_USD"})
df_wdi = df_wdi[df_wdi["Country"].isin(countries) & df_wdi["Year"].isin(years)]



#Life Expectancy: descriptives + yearly mean plot
le_desc = df_le[["LifeExpectancy"]].describe()
le_desc.to_csv("LE_descriptives.csv")

le_yearly = df_le.groupby("Year", as_index=False)["LifeExpectancy"].mean()
chart = le_yearly.plot(x="Year", y="LifeExpectancy", kind="line",
                    title="Life Expectancy — Mean Across Selected Countries")
chart.set_ylabel("Years")
chart.figure.tight_layout(); chart.figure.savefig("LE_yearly_mean.png"); chart.figure.clear()

# CO2 (total tonnes) top 10 carbon emitters 
co2_desc = df_c02[["CO2_use"]].describe()
co2_desc.to_csv("CO2_descriptives.csv")

latest_year = int(df_c02["Year"].max())
co2_top = (df_c02[df_c02["Year"] == latest_year]
           .sort_values("CO2_use", ascending=False)
           .head(10)[["Country","CO2_use"]]
           .sort_values("CO2_use"))
chart= co2_top.set_index("Country")["CO2_use"].plot(kind="barh",
        title=f"Top 10 CO₂ Emitters (Total Tonnes) — {latest_year}")
chart.set_xlabel("Total CO₂ (tonnes)")
chart.figure.tight_layout(); chart.figure.savefig(f"CO2_top10_{latest_year}.png"); chart.figure.clear()

# WDI (GDP per capita): descriptives + histogram
gdp_desc = df_wdi[["GDP_per_capita_USD"]].describe()
gdp_desc.to_csv("GDPpc_descriptives.csv")

chart= df_wdi["GDP_per_capita_USD"].plot(kind="hist", bins=20,
        title="Distribution of GDP per capita (Selected Countries & Years)")
chart.set_xlabel("GDP per capita (USD)")
chart.figure.tight_layout(); chart.figure.savefig("GDPpc_hist.png"); chart.figure.clear()


merged = df_le.merge(df_c02, on=["Country","Year"], how="inner") \
              .merge(df_wdi, on=["Country","Year"], how="inner")

merged = merged.dropna(subset=["LifeExpectancy", "CO2_use", "GDP_per_capita_USD"])
merged.to_csv("merged_country_year.csv", index=False)
print("Merged rows:", len(merged))
print(merged.head())


yearly = merged.groupby("Year", as_index=False).agg({
    "LifeExpectancy": "mean",
    "CO2_use": "mean",
    "GDP_per_capita_USD": "mean"
})

chart = yearly.plot(x="Year", y="LifeExpectancy", kind="line",
                 title="Mean Life Expectancy (Selected Countries)")
chart.set_ylabel("Years"); chart.figure.tight_layout(); chart.figure.savefig("mean_LE_over_time.png"); chart.figure.clear()

chart = yearly.plot(x="Year", y="GDP_per_capita_USD", kind="line",
                 title="Mean GDP per capita (Selected Countries)")
chart.set_ylabel("USD"); chart.figure.tight_layout(); chart.figure.savefig("mean_GDPpc_over_time.png"); chart.figure.clear()

chart = yearly.plot(x="Year", y="CO2_use", kind="line",
                 title="Mean CO₂ (Total, Tonnes) — Selected Countries")
chart.set_ylabel("Tonnes (total)"); chart.figure.tight_layout(); chart.figure.savefig("mean_CO2_over_time.png"); chart.figure.clear()


chart = merged.plot(kind="scatter", x="GDP_per_capita_USD", y="LifeExpectancy",
                 title="Life Expectancy vs GDP per capita")
chart.set_xlabel("GDP per capita (USD)"); chart.set_ylabel("Life Expectancy (years)")
chart.figure.tight_layout(); chart.figure.savefig("scatter_LE_vs_GDPpc.png"); chart.figure.clear()

chart = merged.plot(kind="scatter", x="CO2_use", y="LifeExpectancy",
                 title="Life Expectancy vs CO₂ (Total, Tonnes)")
chart.set_xlabel("CO₂ (total, tonnes)"); chart.set_ylabel("Life Expectancy (years)")
chart.figure.tight_layout(); chart.figure.savefig("scatter_LE_vs_CO2.png"); chart.figure.clear()

print("Saved per-dataset summaries and cross-dataset comparisons.")
