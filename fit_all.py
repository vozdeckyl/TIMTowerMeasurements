import argparse
import os

def load_info(file_path):
    measurement_info = {}
    with open(file_path) as f:
        for line in f:
            variable = line.strip().split(",")[0]
            value = ",".join(line.strip().split(",")[1:])

            measurement_info[variable] = value.strip()
    
    return measurement_info

def print_measurements(output_file, info_list):

    is_new = not os.path.isfile(output_file)
    
    with open(output_file,"a") as f:
        if is_new:
            f.write("{} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \n".
            format(
            "#",
            "K_z",
            "err",
            "Sample ID",
            "Measurement",
            "Name",
            "Date",
            "Time",
            "Density [g/cm^3]",
            "Lens",
            "Load Cell [mV]",
            "Humidity [%]",
            "Heater Current [A]",
            "Heater Voltage [V]",
            "Distance [m]",
            "Ambient temperature [C]",
            "Comments"
            ))
        for info in info_list:
            f.write("{} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \t {} \n".
            format(
            info["measurement"],
            info["conductivity"],
            info["error"],
            info["Sample ID"],
            info["Measurement"],
            info["Name"],
            info["Date"],
            info["Time"],
            info["Density [g/cm^3]"],
            info["Lens"],
            info["Load Cell [mV]"],
            info["Humidity [%]"],
            info["Heater Current [A]"],
            info["Heater Voltage [V]"],
            info["Distance [m]"],
            info["Ambient temperature [C]"],
            info["Comments"]
            ))


def main(args):
    print("Folder: " + args.input_folder)

    if not os.path.isdir(args.input_folder):
        print("Invalid input_folder is invalid. Exiting.")
        exit()

    if (not args.measurement) and (not args.interval):
        print ("No measurement chosen. Choose an interval or a specific measurement.")

    if args.output:
        output_path = args.output
    else:
        output_path = "out.csv"

    if args.measurement:
        print("Measurement: {}".format(args.measurement))

        info_file_path = "{}/A40M-{}_info.csv".format(args.input_folder, str(args.measurement).zfill(6))

        info = load_info(info_file_path)
        info["measurement"] = args.measurement

        ### CALL THE MEASUREMENT HERE

        info["conductivity"] = 1.0000
        info["error"] = 0.0001
        
        info_list = [info]

        print_measurements(output_path,info_list)

    if args.interval:
        print("Interval: from {} to {}".format(args.interval[0],args.interval[1]))

        if args.interval[0] >= args.interval[1]:
            print("Invalid interval. Exiting.")
            exit()

        info_list = []
        for n in range(args.interval[0],args.interval[1]+1):
            print(n)
            info_file_path = "{}/A40M-{}_info.csv".format(args.input_folder, str(n).zfill(6))
            info = load_info(info_file_path)
            info["measurement"] = n
            
            ## CALL THE MEASUREMENT HERE
            info["conductivity"] = 1.0000
            info["error"] = 0.0001
            
            info_list.append(info)
        
        print_measurements(output_path, info_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fit all the files")
    parser.add_argument("input_folder", type=str, help="Folder with all the _box.csv and _info.csv files.")
    parser.add_argument("-m", "--measurement", type=int, help="Choose a specific measurement.")
    parser.add_argument("-i", "--interval", type=int, nargs=2, metavar=("start", "stop") ,help="Choose an interval of measurement.")
    parser.add_argument("-o", "--output", type=int, help="Name of the output csv file (out.csv is the default).")

    args = parser.parse_args()
    
    main(args)