def remove_duplicates(input_file, output_file):
    # Set to store unique lines
    unique_lines = set()

    # Read input file and store unique lines
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            unique_lines.add(line.strip())

    # Write unique lines to output file
    with open(output_file, "w", encoding="utf-8") as f:
        for line in unique_lines:
            f.write(line + "\n")


# Example usage:
input_file = "input.txt"
output_file = "output.txt"
remove_duplicates(input_file, output_file)
