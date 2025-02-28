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

## Job Management
Cancel a Job:
```bash
scancel job_id
```

Get cluster information
```bash
sinfo -o "%n %e %m %a %C"
```

## Job efficiency
```bash
seff <jobID>
```
