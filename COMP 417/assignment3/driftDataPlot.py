import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Linear function
def linear(x, m, b):
    return m * x + b

# Load your data
# Adjust as needed for your file format and path
data = np.loadtxt('DriftData.csv', delimiter=',')
time = data[:, 0]  # Assuming the first column is timestamps
yaw = data[:, 1]   # Assuming the second column is yaw values

# Fit the linear model
popt, _ = curve_fit(linear, time, yaw)

# Extract the drift rate (slope)
drift_rate = popt[0]

# Print the drift rate
print(f"Approximate Constant Drift Rate: {drift_rate} per unit time")

# Plot the data and the linear fit
plt.scatter(time, yaw, label='Data')
plt.plot(time, linear(time, *popt), label='Linear Fit', color='red')
plt.xlabel('Time')
plt.ylabel('Yaw')
plt.title('Yaw Drift Over Time with Linear Approximation')
plt.legend()
plt.show()
