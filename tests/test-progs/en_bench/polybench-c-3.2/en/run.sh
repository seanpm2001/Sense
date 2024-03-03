echo =================== base ===================

for file in base/*; do
    echo -n "$(basename $file)    "
    # ./time_benchmark.sh $file
    $file
    # echo
done

# echo
# echo ==================== en ====================

# for file in en/*; do
#     echo -n "$(basename $file)    "
#     # ./time_benchmark.sh $file
#     $file
#     # echo
# done