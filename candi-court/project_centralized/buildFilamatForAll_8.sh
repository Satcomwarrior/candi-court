#!/bin/bash
matc=/Users/zhouxiangyong/Workspace/light3d/ZPlanFilament/cmake-build-debug/tools/matc/matc
head_filamat_dir=.

for file in ` find $head_filamat_dir -name "*.mat" `; do  
    output2=${file%.mat}".filamat"
    echo "input $file output $output2"
    $matc --api all --platform all -o $output2 $file
done  
