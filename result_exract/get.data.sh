#!/bin/sh
for i in 2e2 5e3 1e4  2e4  4e4  6e4  8e4 1e5;do
   adsorption=`grep "cm^3 STP/g],       " ${i}/Output/System_0/output_*.data | tail -n2| head -n1 | cut -d ',' -f 1`
   echo $i ${adsorption}
done

