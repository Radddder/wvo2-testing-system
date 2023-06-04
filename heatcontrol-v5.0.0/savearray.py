# Import the io module
import io

# Define an array of values
my_array = [
    [1, 2, 3], # First row of the array
    [4, 5, 6], # Second row of the array
    [7, 8, 9] # Third row of the array
]

# Create a string buffer object
buffer = io.StringIO()

# Write each row of the array to the buffer using a custom format
for row in my_array:
    # Join the values in the row with commas and add a newline at the end
    line = ','.join(str(value) for value in row) + '\n'
    # Write the line to the buffer
    buffer.write(line)

# Get the content of the buffer as a string
content = buffer.getvalue()

# Close the buffer
buffer.close()

# Open a text file for writing
with open('my_array.txt', 'w') as f:
    # Write the content to the file
    f.write(content)
