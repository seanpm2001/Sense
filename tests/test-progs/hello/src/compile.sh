# g++ -fno-stack-protector -no-pie -falign-functions=128 hello.cpp -o hello

clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer hello.cpp -o hello
clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer hit_miss.cpp -o hit_miss
clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer hit_miss_en.cpp -o hit_miss_en
clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer flush_en.cpp -o flush_en
clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer on_demand_en.cpp -o on_demand_en
clang -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer safer_app_en.cpp -o safer_app_en
sudo mount -o loop,offset=1048576  ~/en-gem5-fs/disk-image/boot-exit-image/boot-exit /mnt/iso
sudo cp hello /mnt/iso/root/hello
sudo cp hit_miss /mnt/iso/root/hit_miss
sudo cp hit_miss_en /mnt/iso/root/hit_miss_en
sudo cp flush_en /mnt/iso/root/flush_en
sudo cp on_demand_en /mnt/iso/root/on_demand_en
sudo cp safer_app_en /mnt/iso/root/safer_app_en
sudo umount /mnt/iso