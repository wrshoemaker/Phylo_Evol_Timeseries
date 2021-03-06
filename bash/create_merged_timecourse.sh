#!/bin/bash
#PBS -k o
#PBS -l nodes=1:ppn=8,vmem=50gb,walltime=20:00:00
#PBS -M wrshoema@iu.edu
#PBS -m abe
#PBS -m n
#PBS -j oe

module unload python
module load python/2.7.16

declare -a strains=("F")
declare -a treats=("0")
declare -a reps=("3")

declare -a pops=()

for treat in "${treats[@]}"
do
  for strain in "${strains[@]}"
  do
    for rep in "${reps[@]}"
    do
      pops+=("${treat}${strain}${rep}")
    done
  done
done

create_breseq_timecourse=/N/dc2/projects/muri2/Task2/Phylo_Evol_Timeseries/bash/create_breseq_timecourse.py

for pop in "${pops[@]}"
do
  gd_files="/N/dc2/projects/muri2/Task2/Phylo_Evol_Timeseries/data/rebreseq/${pop}_"*"/output/evidence/evidence.gd"
  #ref="/N/dc2/projects/muri2/Task2/Phylo_Evol_Timeseries/data/rebreseq/${pop}_100/data/reference.fasta"
  merged_timecourse="/N/dc2/projects/muri2/Task2/Phylo_Evol_Timeseries/data/timecourse_merged/${pop}_merged_timecourse.bz"
  if [ -f $merged_timecourse ]; then
    rm $merged_timecourse
  fi
  cat "/N/dc2/projects/muri2/Task2/Phylo_Evol_Timeseries/data/timecourse_merged/${pop}_timecourse.txt" | python $create_breseq_timecourse $pop $gd_files | bzip2 -c > $merged_timecourse
done
