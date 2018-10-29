from slurmpy import Slurm

args={
    "time":"24:00:00",
    "ntasks":1,
    "cpus-per-task":4,
    "mem":"2G"   
}

commands=". activate seismology; python run.py {id1} {id2} > ./out/{id}.out"
name="fnet{id}"

for i in range(43):
    s = Slurm(name.format(id=i), args, bash_strict=False)

    id1=i*100
    id2=(i+1)*100
    job_id = s.run(commands.format(id=i,id1=id1,id2=id2), name_addition="", tries=1)
    print(i,job_id)

id1=4300
id2=4304
job_id = s.run(commands.format(id=43,id1=id1,id2=id2), name_addition="", tries=1)
print(43,job_id)