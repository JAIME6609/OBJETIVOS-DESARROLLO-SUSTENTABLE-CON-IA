# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 19:42:30 2024

@author: Jaime
"""

# Import PuLP library for linear optimization
import pulp as pl

# Create the optimization model (minimization)
model = pl.LpProblem("Water_Management", pl.LpMinimize)

# Definition of the variables: x[i,j] is the amount of water from source i used in sector j
# Sources: 1 - Potable water, 2 - Rainwater, 3 - Recycled water
# Sectors: 1 - Human consumption, 2 - Irrigation, 3 - Cleaning
x = pl.LpVariable.dicts("x", [(i, j) for i in range(1, 4) for j in range(1, 4)], lowBound=0, cat='Continuous')

# ---------------------------------------------------------------
# Constants and parameters from section "6. Description of model constants and instances"

# 1. Costs associated with water C_ij, CO_ij, CE_ij, CM_ij, CEN_ij
Cij = {1: 0.03, 2: 0.02, 3: 0.015}  # Cost per quantity of water consumed by sector
COij = {1: 0.03, 2: 0.02, 3: 0.01}  # Cost associated with use and treatment
CEij = {1: 0.01, 2: 0.008, 3: 0.005}  # Environmental cost
CMij = {1: 0.02, 2: 0.015, 3: 0.01}  # Maintenance cost
CENij = {1: 0.02, 2: 0.015, 3: 0.01}  # Energy cost

# 2. Water availability per source (A_i)
A = {1: 5000000,  # Potable water
     2: 5000000,  # Rainwater
     3: 5000000}  # Recycled water

# 3. Demand for each sector (D_j)
D = {1: 500000,  # Human consumption
     2: 500000,  # Irrigation
     3: 500000}  # Cleaning

# Treatment capacity (C_t)
Ct = 600000  # Liters

# Definición de los coeficientes Tij según la tabla
Tij = {
    (1, 1): 0.9,  # Agua potable - Residencial
    (1, 2): 0.85, # Agua potable - Industrial
    (1, 3): 0.8,  # Agua potable - Agrícola
    (2, 1): 0.7,  # Agua residual tratada - Residencial
    (2, 2): 0.65, # Agua residual tratada - Industrial
    (2, 3): 0.6,  # Agua residual tratada - Agrícola
    (3, 1): 0.5,  # Agua sin tratar - Residencial
    (3, 2): 0.45, # Agua sin tratar - Industrial
    (3, 3): 0.4   # Agua sin tratar - Agrícola
}

# 4. Definition of constants for water quality restriction
Qij = {
    (1, 1): 1.0,
    (1, 2): 1.2,
    (1, 3): 1.1,
    (2, 1): 0.8,
    (2, 2): 1.0,
    (2, 3): 1.3,
    (3, 1): 1.1,
    (3, 2): 0.9,
    (3, 3): 1.4
}

# Maximum allowable cost limit for water quality
Q_max = 100000  

# 5. Maximum budget (B)
B = 1000000  # Dollars

# 6. Environmental sustainability (Emax)
Eij = {
    (1,1): 1.0, (1,2): 1.2, (1,3): 0.8,
    (2,1): 0.2, (2,2): 0.3, (2,3): 0.2,
    (3,1): 0.5, (3,2): 0.4, (3,3): 0.3
}

Emax = 1195000  # Daily environmental impact limit in m³

# 7. Equity constraint in water distribution (Dj)
D = {1: 43600, 2: 305200, 3: 87200}  # Total demand by sector

# 8. Energy limit for treatment (ENlim)
ENlim = 200000  # kWh Límite máximo de energía permitida para eficiencia energética

# Definition of constants for energy efficiency constraint
ENij = {
    (1, 1): 0.3,
    (1, 2): 0.5,
    (1, 3): 0.4,
    (2, 1): 0.2,
    (2, 2): 0.6,
    (2, 3): 0.7,
    (3, 1): 0.4,
    (3, 2): 0.3,
    (3, 3): 0.5
}

# 9. Minimum proportion of recycled water usage (Rmin)
Rmin = 0.30  # 30% minimum recycled water

# 10. Infrastructure transport capacity (Cinfra)
# Condition 10: Infrastructure capacity
Tr = {
    (1,1): 1.0, (1,2): 1.1, (1,3): 1.0,
    (2,1): 1.3, (2,2): 1.3, (2,3): 1.2,
    (3,1): 1.5, (3,2): 1.4, (3,3): 1.3
}

Cinfra = 800000  # Transport infrastructure capacity

# 11. Groundwater extraction limit (Amax)
Pmax = 4000000  # Liters per year

# 12. Minimum proportion of rainwater usage (Lmin)
Lmin = 0.20  # Minimum proportion of rainwater usage

# 13. Maximum daily consumption per sector (Dijmax)
Dijmax = {1: 250000,  # Human sector
          2: 200000,  # Irrigation
          3: 50000}   # Cleaning

# 14. Definition of constant for restriction of use ratio in cleaning
Imax = 0.40  # Maximum proportion of water for cleaning activities

# 15. Definition of constant for aquifer protection restriction
Aij = {
    (1,1): 1.0, (1,2): 1.3, (1,3): 1.2,
    (2,1): 0.2, (2,2): 0.3, (2,3): 0.2,
    (3,1): 0.4, (3,2): 0.5, (3,3): 0.4
}

Amax = 2000000  # Maximum water extraction limit from aquifers (in cubic meters)

# 16. Minimum water quality index
Qij = {
    (1,1): 1.0, (1,2): 0.9, (1,3): 0.8,
    (2,1): 0.6, (2,2): 0.8, (2,3): 0.7,
    (3,1): 0.5, (3,2): 0.7, (3,3): 0.9
}

Qmin =0.80  # Quality index on a scale of 100

# 17. Maximum permitted storage (Smax)
Sij = {
    (1,1): 1.0, (1,2): 0.9, (1,3): 0.9,
    (2,1): 0.6, (2,2): 0.8, (2,3): 0.7,
    (3,1): 0.7, (3,2): 0.9, (3,3): 0.8
}

Smax = 60000   # Maximum storage capacity (m³/day)

# 18. Maximum water delivery time (Treq)
Treq = 100000  # Maximum allowable delivery time (hours)

tij = {
    (1,1): 2, (1,2): 3, (1,3): 2,
    (2,1): 4, (2,2): 5, (2,3): 4,
    (3,1): 5, (3,2): 6, (3,3): 5
}

# 19. Definition of constant for irrigation use proportion restriction
I_min = 0.25  # Minimum proportion of water for irrigation use

# 20. Definition of constant for drought resilience constraint
R_drought = 0.20  # Minimum proportion of total water to maintain in case of drought

# 21. Definition of constants for energy cost optimization constraint
E_cost_max = 90000  # Maximum daily energy cost (kWh)

C_Eij = {
    (1,1): 0.8, (1,2): 0.6, (1,3): 0.7,
    (2,1): 0.5, (2,2): 0.4, (2,3): 0.6,
    (3,1): 1.2, (3,2): 1.0, (3,3): 0.9
}

# 22. CO2 emissions constraint (CO2max)
CO2_max = 500000  # Maximum daily carbon emissions (kgCO₂)

C_CO2ij = {
    (1,1): 0.6, (1,2): 0.4, (1,3): 0.5,
    (2,1): 0.3, (2,2): 0.2, (2,3): 0.3,
    (3,1): 1.0, (3,2): 0.8, (3,3): 0.9
}

# 23. Maximum proportion of surface water in total use
S_max = 900000  # Maximum daily surface water storage (m³)

S_ij = {
    (1,1): 1.2, (1,2): 1.0, (1,3): 1.1,
    (2,1): 0.7, (2,2): 0.6, (2,3): 0.8,
    (3,1): 0.9, (3,2): 0.8, (3,3): 0.9
}

# 24. Maximum permitted limit of contamination in wastewater
W_max = 500  # Maximum allowable pollution load (mg/L COD)

W_ij = {
    (1,1): 10, (1,2): 30, (1,3): 50,
    (2,1): 20, (2,2): 40, (2,3): 60,
    (3,1): 200, (3,2): 350, (3,3): 500
}

# 25. Minimum proportion of water that must be reused
R_min = 0.30  # Minimum required proportion of reused water

R_ij = {
    (1,1): 0.05, (1,2): 0.15, (1,3): 0.25,
    (2,1): 0.10, (2,2): 0.35, (2,3): 0.40,
    (3,1): 0.50, (3,2): 0.60, (3,3): 0.80
}

# 26. Consumption limit allowed according to local regulations
L_norm = 10000

# 27. Water balance in the system
B_hidro=1

# 28. Proportion of equitable distribution in scarcity
D = {
    1: 4360,   # Human Consumption & Food
    2: 3052,  # Agriculture & Irrigation
    3: 8720    # Industry & Sanitation
}

# 29. Minimum strategic reserves
R_strategic = 100000 # liters

# 30. Leakage loss limit (Lmax)
L_max = 0.08  # Maximum leakage rate (8%)

# Define leakage coefficients per sector (L_ij) based on infrastructure conditions
L = {
    (1, 1): 0.05,  # Human Consumption & Health
    (1, 2): 0.07,  # Agriculture & Irrigation
    (1, 3): 0.06,  # Essential Industry
    (2, 1): 0.04,  
    (2, 2): 0.06,  
    (2, 3): 0.05,  
    (3, 1): 0.03,  
    (3, 2): 0.05,  
    (3, 3): 0.04   
}

# 31. Maximum limit for the use of grey water
G_max = 0.35  # Maximum proportion of total water supply from greywater (35%)

# Define greywater supply variables
greywater_sources = [3]  # Source 3 represents greywater

# 32. Per capita consumption limit
C_max = 3000  # Define maximum per capita water consumption (C_max) in m³/year

# Define population per sector (P_j)
P = {
    1: 131_000_000,  # Human Consumption (National Population Estimate)
    2: 25_000_000,   # Agriculture (Farmers and Agricultural Workers)
    3: 10_000_000    # Industry (Industrial and Manufacturing Workers)
}

# 33. Minimum proportion of water savings through technologies
T_min = 15000  # Minimum water savings required in m³/year

# Define efficiency coefficients for water-saving technologies per sector (T_save_ij)
T_save = {
    (1, 1): 0.12,  # Human Consumption & Health
    (1, 2): 0.15,  # Agriculture & Irrigation
    (1, 3): 0.10,  # Essential Industry
    (2, 1): 0.14,  
    (2, 2): 0.18,  
    (2, 3): 0.11,  
    (3, 1): 0.10,  
    (3, 2): 0.13,  
    (3, 3): 0.09   
}

# 34. Safe limit for the protection of aquatic ecosystems.
E_safe = 350000  # Safe extraction limit to avoid ecosystem degradation

# 35. Minimum proportion of continuous improvement in water management.
M_min = 50000  # Minimum efficiency improvement required in water management

# Define water management improvement factors per sector (M_ij)
M = {
    (1, 1): 1.2,  # Human Consumption & Health
    (1, 2): 1.5,  # Agriculture & Irrigation
    (1, 3): 1.1,  # Essential Industry
    (2, 1): 1.3,  
    (2, 2): 1.6,  
    (2, 3): 1.2,  
    (3, 1): 1.1,  
    (3, 2): 1.4,  
    (3, 3): 1.0   
}

# 36. Sediment control (SEDmax)
SED_max = 50  # Maximum sediment concentration in mg/L to protect infrastructure and water quality

# Define sedimentation coefficients per sector (SED_ij)
SED = {
    (1, 1): 35,  # Human Consumption & Health
    (1, 2): 40,  # Agriculture & Irrigation
    (1, 3): 30,  # Essential Industry
    (2, 1): 38,  
    (2, 2): 45,  
    (2, 3): 32,  
    (3, 1): 28,  
    (3, 2): 35,  
    (3, 3): 25   
}

# 37. Maximum stormwater management capacity
P_min = 100000  # Minimum required stormwater management capacity

# Define the set of stormwater sources (P)
stormwater_sources = [2]  # Source 2 represents rainwater/stormwater

# 38. Salinity limit to avoid salinization
SAL_max = 1.5  # Maximum allowed salinity concentration to prevent soil and water degradation

# Define salinity levels per sector (SAL_ij)
SAL = {
    (1, 1): 0.8,  # Human Consumption & Health
    (1, 2): 1.2,  # Agriculture & Irrigation
    (1, 3): 1.0,  # Essential Industry
    (2, 1): 0.9,  
    (2, 2): 1.3,  
    (2, 3): 1.1,  
    (3, 1): 0.7,  
    (3, 2): 1.0,  
    (3, 3): 0.9   
}

# 39. Maximum limit of nitrates allowed in water
NO3_max = 50  # Maximum allowed nitrate concentration to ensure water quality

# Define nitrate levels per sector (NO3_ij)
NO3 = {
    (1, 1): 30,  # Human Consumption & Health
    (1, 2): 45,  # Agriculture & Irrigation
    (1, 3): 40,  # Essential Industry
    (2, 1): 32,  
    (2, 2): 48,  
    (2, 3): 42,  
    (3, 1): 28,  
    (3, 2): 38,  
    (3, 3): 35   
}

# 40. Universal water access (Umin)
# Define the minimum required water supply for universal access (U_min) in hm³/year
U_min = {
    1: 50000,   # Human Consumption & Basic Needs
    2: 80000,   # Agriculture & Irrigation
    3: 60000    # Essential Industry & Public Services
}

# 41. Define the maximum water extraction allowed from natural sources (N_max) in hm³/year
N_max = {
    1: 120000,  # Human Consumption & Essential Needs
    2: 250000,  # Agriculture & Irrigation
    3: 180000   # Industry & Public Services
}

# Define natural source extraction levels per sector (N_ij)
N = {
    (1, 1): 90000,  # Human Consumption
    (1, 2): 200000,  # Agriculture
    (1, 3): 150000,  # Industry
    (2, 1): 100000,  
    (2, 2): 220000,  
    (2, 3): 160000,  
    (3, 1): 95000,  
    (3, 2): 210000,  
    (3, 3): 170000   
}

# 42: Wastewater treatment
# Define the minimum amount of wastewater treatment required (S_min) in hm³/year
S_min = {
    1: 60000,  # Domestic & Urban Treatment
    2: 150000,  # Agricultural Effluents
    3: 100000   # Industrial Wastewater
}

# Define wastewater treatment efficiency per sector (T_resid_ij)
T_resid = {
    (1, 1): 0.85,  # Domestic Treatment Efficiency
    (1, 2): 0.75,  # Agricultural Treatment Efficiency
    (1, 3): 0.80,  # Industrial Treatment Efficiency
    (2, 1): 0.88,
    (2, 2): 0.78,
    (2, 3): 0.82,
    (3, 1): 0.90,
    (3, 2): 0.80,
    (3, 3): 0.85
}

# 43: Compliance with international standards

# Define the international compliance limit (I_std) in hm³/year
I_std = {
    1: 100000,  # Drinking water quality compliance
    2: 250000,  # Industrial and agricultural discharge limits
    3: 180000   # Sustainable water extraction limits
}

# Define the compliance factors per sector (I_ij)
I = {
    (1, 1): 0.95,  # Compliance with drinking water quality
    (1, 2): 0.90,  # Compliance with wastewater discharge norms
    (1, 3): 0.92,  # Compliance with sustainable extraction
    (2, 1): 0.96,
    (2, 2): 0.88,
    (2, 3): 0.91,
    (3, 1): 0.97,
    (3, 2): 0.89,
    (3, 3): 0.93
}

# 44. Maximum allowed micropollutants in the supplied water
M_max = {
    1: 5.0,   # Human Consumption & Health (mg/L)
    2: 10.0,  # Agriculture & Irrigation (mg/L)
    3: 8.0    # Industrial Use (mg/L)
}

# Define micropollutant concentration per sector (M_ij) in mg/L
M = {
    (1, 1): 3.5,  # Human Consumption & Health
    (1, 2): 7.0,  # Agriculture & Irrigation
    (1, 3): 6.5,  # Industrial Use
    (2, 1): 4.0,  
    (2, 2): 8.5,  
    (2, 3): 7.0,  
    (3, 1): 3.8,  
    (3, 2): 9.0,  
    (3, 3): 7.5   
}

# 45. Efficient use of financial resources

# Define financial costs per sector (F_ij) in USD/year
F = {
    (1, 1): 150000,  # Drinking water for Human Consumption
    (1, 2): 250000,  # Drinking water for Agriculture
    (1, 3): 200000,  # Drinking water for Industry
    (2, 1): 100000,  # Rainwater for Human Consumption
    (2, 2): 180000,  # Rainwater for Agriculture
    (2, 3): 150000,  # Rainwater for Industry
    (3, 1): 80000,   # Recycled water for Human Consumption
    (3, 2): 120000,  # Recycled water for Agriculture
    (3, 3): 100000   # Recycled water for Industry
}

# Maximum allowed budget for water management (F_max) in USD/year
F_max = 1000000  

# 46. Prevention of infiltrations
INF = {
    (1,1): 0.05, (1,2): 0.08, (1,3): 0.06,
    (2,1): 0.07, (2,2): 0.09, (2,3): 0.05,
    (3,1): 0.04, (3,2): 0.06, (3,3): 0.03
}

INF_max = 0.15

# 47. pH Control
pH_Control = [[7.2, 7.5, 7.8],  # pH values for i=1, j=1 to 3
              [7.1, 7.3, 7.6],  # pH values for i=2, j=1 to 3
              [6.8, 7.0, 7.2]]  # pH values for i=3, j=1 to 3

pH_max = 8.5  # Maximum allowed pH value

# 48. Quality monitoring

# Define the minimum required quality monitoring (Q_mon_min)
Q_mon_min = 0.75  # Minimum monitoring required

# Define quality monitoring efficiency per sector (Q_mon_ij)
Q_mon = {
    (1,1): 18, (1,2): 20, (1,3): 22,
    (2,1): 16, (2,2): 19, (2,3): 21,
    (3,1): 17, (3,2): 20, (3,3): 23
}

# 49. Infrastructure maintenance
Minfij = [
    [50, 60, 55],
    [65, 70, 60],
    [55, 50, 45]
]

Minf_min = 200

# 50. Education and awareness
Emin = 20000

Eij = [
    [5000, 7000, 6500],  # Sector 1
    [6000, 7200, 6800],  # Sector 2
    [5500, 7100, 6700]   # Sector 3
]

# ---------------------------------------------------------------
# Objective function: Minimize the total cost of water supply
model += pl.lpSum([
    Cij[i] * x[i, j] + COij[i] * x[i, j] + CEij[i] * x[i, j] + CMij[i] * x[i, j] + CENij[i] * x[i, j]
    for i in range(1, 4) for j in range(1, 4)
]), "Total_Cost"

# ---------------------------------------------------------------
# Constraints:

# Condition 0: All consumption must be greater than or equal to zero (Non-negativity of variables (xij ≥ 0))
# (This is already included in the definition of the variable with lowBound=0)

# Condition 1: Water availability from each source (Ai)
for i in range(1, 4):
    model += pl.lpSum([x[i, j] for j in range(1, 4)]) <= A[i], f"Water_Availability_Source_{i}"

# Condition 2: Demand from each sector (Dj)
for j in range(1, 4):
    model += pl.lpSum([x[i, j] for i in range(1, 4)]) >= D[j], f"Sector_Demand_{j}"

# Condition 3: Treatment capacity (Ct)
model += pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= Ct, "Treatment_Capacity"

# Condition 5: Maximum allowed cost (B)
model += pl.lpSum([
    Cij[i] * x[i, j] + COij[i] * x[i, j] + CEij[i] * x[i, j] + CMij[i] * x[i, j] + CENij[i] * x[i, j]
    for i in range(1, 4) for j in range(1, 4)]) <= B, "Max_Budget"

# Condition 15: Protection of aquifers
model += pl.lpSum([x[i, j] * Aij[i, j] for i in range(1, 4) for j in range(1, 4)]) <= Amax, "Protection_Aquifers"

# Condition 10: Infrastructure capacity
model += pl.lpSum([x[i, j] * Tr[i, j] for i in range(1, 4) for j in range(1, 4)]) <= \
         Cinfra * pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]), "Infrastructure_Capacity"

# Condition 20: Resilience to droughts
model += pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]) >= R_drought, "Resilience_Droughts"

# Condition 29: Maintenance of strategic reserves
model += pl.lpSum([x[i, j] for i in range(1, 4)]) <= R_strategic, "Maintenance_Strategic_Reserves"

# Condition 26: Compliance with local regulations
for i in range(1, 4):
    for j in range(1, 4):
        model += x[i, j] <= L_norm, f"Compliance_Local_Regulations_{i}_{j}"

# Condition 27: Water balance in the system
model += pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]) >= B_hidro, "Water_Balance"

# Condition 28: Equitable distribution in times of scarcity
for j in range(1, 4):
    for k in range(1, 4):
        if j != k:  # Avoid self-comparison
            model += (pl.lpSum([x[i, j] for i in range(1, 4)]) / D[j]) >= \
                     (pl.lpSum([x[i, k] for i in range(1, 4)]) / D[k]), \
                     f"Equitable_Distribution_Scarcity_{j}_{k}"

# Condition 30: Minimizing losses due to leaks
model += (pl.lpSum([L[i, j] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= L_max * pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)])), "Minimize_Leak_Losses"

# Condition 34: Protection of aquatic ecosystems
model += pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= E_safe, "Aquatic_Ecosystem_Protection"

# Condition 6: Environmental sustainability (Emax)
model += pl.lpSum([CEij[i] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= Emax, "Environmental_Sustainability"

# Condition 7: Equity in distribution
model += pl.lpSum([x[i, 1] for i in range(1, 4)]) / D[1] == \
         pl.lpSum([x[i, 2] for i in range(1, 4)]) / D[2], "Equity_Distribution_Human_Irrigation"

model += pl.lpSum([x[i, 2] for i in range(1, 4)]) / D[2] == \
         pl.lpSum([x[i, 3] for i in range(1, 4)]) / D[3], "Equity_Distribution_Irrigation_Cleaning"

# Condition 8: Energy efficiency
model += pl.lpSum([ENij[(i, j)] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= ENlim, "Energy_Efficiency"

# Condition 9: Use of wastewater
model += pl.lpSum([x[3, j] for j in range(1, 4)]) >= Rmin * pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]), "Use_of_Wastewater"

# Condition 11: Limitation on the use of drinking water
model += pl.lpSum([x[1, j] for j in range(1, 4)]) <= Pmax, "Limit_Drinking_Water"

# Condition 12: Use of rainwater
model += pl.lpSum([x[2, j] for j in range(1, 4)]) >= Lmin * pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]), "Use_of_Rainwater"

# Condition 13: Maximum daily consumption by sector (Dijmax)
for j in range(1, 4):
    model += pl.lpSum([x[i, j] for i in range(1, 4)]) <= Dijmax[j], f"Max_Daily_Consumption_Sector_{j}"

# Condition 17: Storage capacity
model += pl.lpSum([x[i, j] * Sij[i, j] for i in range(1, 4) for j in range(1, 4)]) <= Smax, "Storage_Capacity"

# Condition 18: Delivery time
model += pl.lpSum([tij[i, j] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= Treq, "Delivery_Time_Limit"

# Condition 16: Maintaining water quality
model += pl.lpSum([Qij[i, j] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) >= \
         Qmin * pl.lpSum([x[i, j] for i in range(1, 4) for j in range(1, 4)]), "Maintaining_Water_Quality"

# Condition 4: Water quality cost
model += pl.lpSum([Qij[(i, j)] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= Q_max, "Water_Quality_Cost"

# Condition 21: Energy cost optimization
model += pl.lpSum([C_Eij[i, j] * x[i, j] for i in range(1, 4) for j in range(1, 4)]) <= E_cost_max, "Energy_Cost_Optimization"

# ---------------------------------------------------------------
# **Resolver el modelo**
status = model.solve()

# **Verificar el estado del modelo antes de acceder a la solución**
print("Status:", pl.LpStatus[model.status])

# **Si la solución es óptima, mostrar los resultados**
if pl.LpStatus[model.status] == "Optimal":
    # Imprimir los valores de las variables
    for v in model.variables():
        print(v.name, "=", v.varValue)

    # Mostrar el valor de la función objetivo
    print("Total Cost of Water Supply = ", pl.value(model.objective))
else:
    print("No se encontró una solución óptima.")