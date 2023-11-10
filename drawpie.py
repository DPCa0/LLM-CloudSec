import matplotlib.pyplot as plt

# Data to plot
labels = 'Correct Predictions', 'Incorrect Predictions'
sizes = [414, 21]  # The number of correct and incorrect predictions respectively
colors = ['lightgrey', 'darkgrey']  # Using grayscale for academic style
explode = (0.1, 0)  # Slightly explode the first slice for emphasis

# Plot
plt.figure(figsize=(8, 8))  # Increase the figure size if needed
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Save the figure
plt.savefig('relative_prediction_accuracy_pie_chart.png', format='png', dpi=300)

# Display the pie chart
plt.show()
