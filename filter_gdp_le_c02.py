import pandas as pd
import matplotlib.pyplot as plt

df_c02 = pd.read_csv("co2_emission.csv")
df_le  = pd.read_csv("Life Expectancy Data.csv")
df_wdi = pd.read_csv("f5a9ad86-f7cb-42ba-868e-b444c1d52fa4_Data.csv")



countries = ["Argentina", "Australia","Brazil", "Canada", "China", "France",
              "Germany", "Italy", "India","Indonesia", "Japan", "Korea, Rep.",
              "Mexico","Russia","Russian Federation" "Saudi Arabia", "South Africa", "United Kingdom", 
              "United States"
            ]

years = list(range(2000, 2016))


df_c02 = df_c02[["Entity", "Year", "Annual CO₂ emissions (tonnes )"]]
df_c02 = df_c02.rename(columns={
    "Entity": "Country",
    "Annual CO₂ emissions (tonnes )": "CO2_use"
})
df_c02 = df_c02[df_c02["Country"].isin(countries) & df_c02["Year"].isin(years)]


df_le = df_le[["Country", "Year", "Life expectancy "]]  # trailing space matters
df_le = df_le.rename(columns={"Life expectancy ": "LifeExpectancy"})
df_le = df_le[df_le["Country"].isin(countries) & df_le["Year"].isin(years)]


df_wdi = df_wdi[["Country Name", "Time", "Value"]]
df_wdi = df_wdi.rename(columns={
    "Country Name": "Country",
    "Time": "Year",
    "Value": "GDP_per_capita_USD"
})
df_wdi = df_wdi[df_wdi["Country"].isin(countries) & df_wdi["Year"].isin(years)]


merged = df_le.merge(df_c02, on=["Country", "Year"], how="inner") \
              .merge(df_wdi, on=["Country", "Year"], how="inner")

merged = merged.dropna(subset=["LifeExpectancy", "CO2_use", "GDP_per_capita_USD"])
merged.to_csv("merged_country_year.csv", index=False)
print("Merged rows:", len(merged))
print(merged.head())

yearly = merged.groupby("Year", as_index=False).agg({
    "LifeExpectancy": "mean",
    "CO2_use": "mean",
    "GDP_per_capita_USD": "mean"
})

ax = yearly.plot(x="Year", y="LifeExpectancy", kind="line", title="Mean Life Expectancy (selected countries)")
ax.set_ylabel("Years"); ax.figure.tight_layout(); ax.figure.savefig("mean_LE_over_time.png"); ax.figure.clear()

ax = yearly.plot(x="Year", y="GDP_per_capita_USD", kind="line", title="Mean GDP per capita (selected countries)")
ax.set_ylabel("USD"); ax.figure.tight_layout(); ax.figure.savefig("mean_GDPpc_over_time.png"); ax.figure.clear()

ax = yearly.plot(x="Year", y="CO2_use", kind="line", title="Mean CO₂ (total, tonnes) — selected countries")
ax.set_ylabel("Tonnes (total)"); ax.figure.tight_layout(); ax.figure.savefig("mean_CO2_over_time.png"); ax.figure.clear()

ax = merged.plot(kind="scatter", x="GDP_per_capita_USD", y="LifeExpectancy",
                 title="Life Expectancy vs GDP per capita")
ax.set_xlabel("GDP per capita (USD)"); ax.set_ylabel("Life Expectancy (years)")
ax.figure.tight_layout(); ax.figure.savefig("scatter_LE_vs_GDPpc.png"); ax.figure.clear()

ax = merged.plot(kind="scatter", x="CO2_use", y="LifeExpectancy",
                 title="Life Expectancy vs CO₂ (total, tonnes)")
ax.set_xlabel("CO₂ (total, tonnes)"); ax.set_ylabel("Life Expectancy (years)")
ax.figure.tight_layout(); ax.figure.savefig("scatter_LE_vs_CO2.png"); ax.figure.clear()

print("Saved: merged_country_year.csv and 5 plot PNGs.")
