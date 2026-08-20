#!/usr/bin/env python3
"""
Description: Graph GPU logging outputs from GPU-Z
Usage:
"""
import pandas as pandas
import matplotlib.pyplot as pyplot

def trim_to_bench_start(data, idle):
    start = data[' GPU Clock [MHz] '] > idle
    return data.loc[start.idxmax():].reset_index(drop=True)

if __name__ == "__main__":
    data1 = pandas.read_csv('GPU-Z Sensor Log_bm1.txt', encoding="iso-8859-1")
    data2 = pandas.read_csv('GPU-Z Sensor Log_bm4.txt', encoding="iso-8859-1")

    idle = 150.0

    data1 = trim_to_bench_start(data1, idle)
    data2 = trim_to_bench_start(data2, idle)

    tograph = [
        ' GPU Clock [MHz] ',
        ' Board Power Draw [W] ',
        ' Power Consumption (%) [% TDP] ',
        ' GPU Temperature [°C] ',
        ' Hot Spot [°C] ',
        ]

    for i in tograph:
        data1[i] = pandas.to_numeric(data1[i], errors='coerce')
        data2[i] = pandas.to_numeric(data2[i], errors='coerce')
        pyplot.plot(data1[i])
        pyplot.plot(data2[i])
        pyplot.savefig(f"{i}.png")
        pyplot.clf()
