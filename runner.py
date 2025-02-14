from spatial_filters import *
import sys
import os

def main(argv):
    apply_filter(argv[1], f"./input/{argv[2]}", f"./output/{argv[2]}", *argv[3:])
    
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {os.path.relpath(__file__)} [Filter Name] [Image File Name] [Optional Arguments]")
        sys.exit() 
    if sys.argv[1] not in filter_names:
        print("Filter doesn't exist")
        sys.exit()
    main(sys.argv)