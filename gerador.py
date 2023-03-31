import os
import random
import subprocess

num_films = [5, 10, 20, 30 , 50, 100, 200, 300, 500,1000]
num_categories = [1,2,3,4,6,8,10,20,50]

with open("inputs/sizes.txt", "w") as f:
    f.write("num_films: ")
    f.write(", ".join(str(n) for n in num_films))
    f.write("\n")
    f.write("num_categories: ")
    f.write(", ".join(str(m) for m in num_categories))
    f.write("\n")
cmd = "rm inputs/input_*.txt"
os.system(cmd)
for n in num_films:
    for m in num_categories:
        subprocess.run(['./gerador', str(n), str(m), f"inputs/input_{n}_{m}.txt"])

