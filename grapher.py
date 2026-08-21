#!/usr/bin/env python3
import pandas
import matplotlib.pyplot as pyplot
import argparse

def trim_to_bench_start(data, idle):
    start = data[' GPU Clock [MHz] '] > idle
    return data.loc[start.idxmax():].reset_index(drop=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="Filename(s) of GPU-Z log files")
    parser.add_argument("--idle-clock", type=float, default="0", help="Trim start of graph to first row with clock speed above this value [MHz]")
    parser.add_argument("--time", type=int, help="how many seconds of data to include in the graph")
    parser.add_argument("--output", "-o", type=str, default="output files prefix")
    args = parser.parse_args()

    prefix = f"{args.output}_" if args.output else ""

    data = []

    for filename in args.files:
        dataframe = pandas.read_csv(filename, encoding="iso-8859-1")
        dataframe = trim_to_bench_start(dataframe, args.idle_clock)
        data.append(dataframe)

    tograph = [
        ' GPU Clock [MHz] ',
        ' Board Power Draw [W] ',
        ' Power Consumption (%) [% TDP] ',
        ' GPU Temperature [°C] ',
        ' Hot Spot [°C] ',
        ]

    for i in tograph:
        for dataframe in data:
            dataframe[i] = pandas.to_numeric(dataframe[i], errors='coerce')
            pyplot.plot(dataframe[i].iloc[:args.time])
        filename = f"{prefix}{i.strip()}.png".replace(" ", "_")
        pyplot.savefig(filename)
        pyplot.clf()