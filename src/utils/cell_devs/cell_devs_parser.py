import numpy as np
import re


class cell_devs_parser:

    def __init__(self, filename, N, M):
        self.filename = filename
        self.M = M
        self.N = N

    def str2time(self, s):
        ls = list(map(lambda x : float(x), s.split(':'))) # hh : mm : ss : ms : ???

        return round(ls[0] * 3600 + ls[1] * 60 + ls[2] + ls[3] / 1000., 2) 

    def get_evolution_from_log(self, nombre_modelo):
        evolution = [[ [] for j in range(self.M) ] for i in range(0, self.N)]
        max_time = 0
        max_val = 0
        for ln in open(self.filename,"r").readlines():
            if ln.startswith("0 / L / Y /"):
                time = re.compile(r"\d+:\d+:\d+:\d+:\d+[\.\d+]*").search(ln.split('/')[3]).group(0)
                cell = re.compile(nombre_modelo + "\(\d+,\d+,0\)\(\d*\) / out /[ ]*-*\d+[\.\d+]*").findall(ln)
                if len(cell) == 0:
                    continue
                else:
                    cell = cell[0]
                    coord = re.search(re.compile(r"\(.*,.*,0\)"), cell).group(0)[1:-1].split(',')
                    i, j = int(coord[0]), int(coord[1])
                    val  = float(re.compile(r"-*\d+[\.\d+]*").search(cell.split('/')[2]).group(0))
                    evolution[i][j].append({
                        "time" : time,
                        "time_converted" : self.str2time(time),
                        "val" : float(val)
                    })
                    max_time = max(max_time, self.str2time(time))
                    max_val = max(max_val, val)
        return evolution, max_time

    def get_cut_values(self, ev, pts):
        res = []
        i, j = 0, 0
        while i < len(ev)-1:
            if (ev[i]['time_converted'] <= pts[j] and ev[i+1]['time_converted'] > pts[j]) \
                or ev[i]['time_converted'] > pts[j]:
                res.append({
                    'time' : pts[j], 
                    'interval' : (ev[i]['time_converted'], ev[i+1]['time_converted']),
                    'value' : ev[i]['val']
                })
                j = j+1        
            else:
                i = i + 1
        while j < len(pts):
            res.append({
                'time' : pts[j],
                'interval' : (ev[i-1]['time_converted'], ev[i]['time_converted']),
                'value' : ev[i]['val']
            })
            j = j+1  
        return res