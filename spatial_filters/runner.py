from filters import *  # Importing all functions from spatial_filters module
import sys
import os

def main(argv):
    # Applies the specified filter to the input image and saves the output image
    apply_filter(argv[1], f"./input/{argv[2]}", f"./output/{argv[2]}", *argv[3:])
    
if __name__ == "__main__":
    # Ensure correct usage with at least two arguments: filter name and image file name
    if len(sys.argv) < 3:
        print(f"Usage: {os.path.relpath(__file__)} [Filter Name] [Image File Name] [Filter Arguments]")
        print()
        print_available_filters()
        sys.exit()
    
    # Check if the specified filter exists
    if sys.argv[1] not in filter_names:
        print("Filter doesn't exist")
        sys.exit()
    
    main(sys.argv)  # Execute the main function