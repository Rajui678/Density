import pandas as pd
import numpy as np

# Create sample data
np.random.seed(42)
n_samples = 50

# Generate realistic density and temperature data
measured_density = np.random.uniform(0.8, 1.2, n_samples)
observed_temperature = np.random.uniform(15, 35, n_samples)

# Create corresponding density with some relationship to the inputs
corresponding_density = (
    0.9 * measured_density + 
    0.1 * (1 - (observed_temperature - 20) / 20) + 
    np.random.normal(0, 0.02, n_samples)
)

# Create DataFrame
data = pd.DataFrame({
    'Measured Density': measured_density,
    'Observed Temperature': observed_temperature,
    'Corresponding Density': corresponding_density
})

# Round to 4 decimal places
data = data.round(4)

# Save to Excel
data.to_excel('sample_data.xlsx', index=False)
print("Sample data created successfully!")
print(f"Created {len(data)} rows of sample data")
print("\nFirst 5 rows:")
print(data.head())
