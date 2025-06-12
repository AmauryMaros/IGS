# SLURM Commands

## Submit a Job
```bash
sbatch ./slurm.sh
```

## Multi-threaded job
```bash
sbatch -n 10 ./slurm.sh 10
```

## Job Details
```bash
squeue --me
```

```bash
scontrol show job <jobid>
```

## Job Management
Cancel a Job:
```bash
# all the job
scancel job_id

# those running on specific machine
squeue -w grid-2-1-2 -u <user-id> -h | awk '{print $1}' | xargs -r scancel
```

Get cluster information
```bash
sinfo -o "%n %e %m %a %C"
```

## Job efficiency
```bash
seff <jobID>
```
