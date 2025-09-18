#!/bin/bash
matc=/Users/zhouxiangyong/Workspace/light3d/ZPlanFilament/cmake-build-debug/tools/matc/matc
head_filamat_dir=.

for file in ` find $head_filamat_dir -name "*.mat" `; do  
    output1=${file%.mat}".filamat"
    echo "input $file output $output1"
    $matc --api opengl --platform mobile -o $output1 $file
done  
