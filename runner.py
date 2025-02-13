from spatial_filters import *
import sys
import os

filter_names = {
    "negative": negative_filter
}

def main(argv):
    filter_names[argv[1]](f"./input/{argv[2]}", f"./output/{argv[2]}")
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {os.path.relpath(__file__)} [Filter Name] [Image File Name]")
        sys.exit() 
    if sys.argv[1] not in filter_names:
        print("Filter doesn't exist")
        sys.exit()
    main(sys.argv)