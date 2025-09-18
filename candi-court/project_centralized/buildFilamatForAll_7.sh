#!/bin/bash
matc=/Users/zhouxiangyong/Workspace/light3d/ZPlanFilament/cmake-build-debug/tools/matc/matc
head_filamat_dir=.

for file in ` find $head_filamat_dir -name "*.fshader" `; do  
    output1=${file%.fshader}"_mobile.filamat"
    echo "input $file output $output1"
    $matc --api opengl --api metal --platform mobile -o $output1 $file

    output2=${file%.fshader}"_desktop.filamat"
    echo "input $file output $output2"
    $matc --api all --platform desktop -o $output2 $file
done  

for file in ` find $head_filamat_dir -name "*.mat" `; do  
    output1=${file%.mat}"_mobile.filamat"
    echo "input $file output $output1"
    $matc --api opengl --api metal --platform mobile -o $output1 $file

    output2=${file%.mat}"_desktop.filamat"
    echo "input $file output $output2"
    $matc --api all --platform desktop -o $output2 $file
done  
