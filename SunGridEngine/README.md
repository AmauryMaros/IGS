# Grid Engine Commands

Make script executable
```bash
chmod +x sge.sh
```

## Submit a Job
Submit a job to the queue:
```bash
qsub ./sge.sh
```

## Monitor Resources on the Grid
Check the status of all jobs and resources:

```bash
qstat
```

Check the status of jobs for a specific user:

```bash
qstat -u 'username'
qstat -u '*'
```

## Get Project Existence for QLOGIN
List the available project configurations:
```bash
qconf -sprjl
```

## Job Management
Cancel a Job:
```bash
qdel job_id
```

## Job Details
Display detailed information about a specific job:
```bash
qstat -j job_id
```





