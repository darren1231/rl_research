import csv
from param import Param
import numpy as np
import shutil

def search_total_steps(filename):
    
    step_sum = 0
    with open(filename,newline="") as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            # print (int(row[0]))
            step_sum+=int(row[0])
    return step_sum
        
try:
    step_sum = search_total_steps("test1.csv")
    print (step_sum)
except FileNotFoundError:
    print ("file not found")

loop_range = np.arange(0.1,1,0.1)
ex_list = loop_range.tolist()

num_better = 0
for alpha_p in ex_list:
    for gamma_p in ex_list:
        for alpha in ex_list:
            for gamma in ex_list:
                Param.ALPHA_P=alpha_p
                Param.GAMMA_P= gamma_p
                Param.ALPHA= alpha
                Param.GAMMA= gamma

                map_dict = {True:"use combine q",False:"normal q"}

                if_c = True
                experiment_name = "fivetimesfive/ex2_{}_{}_{}_{}_{}".format(map_dict[if_c],\
                    str(Param.ALPHA_P),str(Param.GAMMA_P),\
                    str(Param.ALPHA),str(Param.GAMMA))
                
                if_find_combineq_file = True
                try:
                    combineq_step_sum = search_total_steps("{}.csv".format(experiment_name))
                except FileNotFoundError:
                    if_find_combineq_file = False

                if_c = False
                experiment_name = "fivetimesfive/ex2_{}_{}_{}_{}_{}".format(map_dict[if_c],\
                    str(Param.ALPHA_P),str(Param.GAMMA_P),\
                    str(Param.ALPHA),str(Param.GAMMA))

                if_find_normal_file = True
                try:
                    normal_step_sum = search_total_steps("{}.csv".format(experiment_name))
                except FileNotFoundError:
                    if_find_normal_file = False

                
                if (if_find_combineq_file and if_find_normal_file):
                    if combineq_step_sum+500<normal_step_sum:
                        print(experiment_name)
                        num_better+=1

                        src = "{}.png".format(experiment_name)
                        dst = "fivetimesfive/better/"
                        shutil.copy(src, dst)


print(num_better)