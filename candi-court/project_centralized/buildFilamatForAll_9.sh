#!/bin/bash
matc=/Users/zhouxiangyong/Workspace/light3d/ZPlanFilament/cmake-build-debug/tools/matc/matc
head_filamat_dir=.

for file in ` find $head_filamat_dir -name "*.fshader" `; do  
    output2=${file%.fshader}"_mobile.filamat"
    echo "input $file output $output2"
    $matc --api opengl --platform mobile -o $output2 $file
done  
