from slurmpy import Slurm

args={
    "time":"24:00:00",
    "ntasks":1,
    "cpus-per-task":2,
    "mem":"2G"   
}

commands="sh download.sh {id} > ./out/{id}.out"
name="fdsn{id}"

for i in range(44):
    s = Slurm(name.format(id=i), args, bash_strict=False)
    job_id = s.run(commands.format(id=i), name_addition="", tries=1)
    print(i,job_id)