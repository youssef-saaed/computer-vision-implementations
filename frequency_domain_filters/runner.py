from frequency_domain import *
import sys

usage = """Usage: python runner.py [input] [output] [type] [method] [distance 1] [distance 2 (optional)]
input -> name of the image in folder "input"
output -> saving name of the output image in folder "output"
type -> [low-pass, high-pass, band-pass, band-stop]
method -> [ideal, guassian, butterworth]
distance 1 -> threshold for low and high pass or band start for band pass and band stop
distance 2 -> band end for band pass and band stop"""

def main(args):
    if len(args) < 6 or (len(args) != 7 and args[3] in ["band-pass", "band-stop"]):
        print(usage)
        return -1
    image = read_image(f"input/{args[1]}")
    filtered_image = apply_filter(image, args[4], args[3], int(args[5]), int(args[6]) if len(args) > 6 else int(args[5]) + 1)
    save_image(filtered_image, f"output/{args[2]}")
    return 0

if __name__ == "__main__":
    args = sys.argv
    sys.exit(main(args))