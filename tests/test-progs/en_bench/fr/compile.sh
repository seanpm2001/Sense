export LIBRARY_PATH=/home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/fr/openssl-1.0.0
export LD_LIBRARY_PATH=/home/fan/en-gem5-fs/en-gem5/tests/test-progs/en_bench/fr/openssl-1.0.0

g++ -std=gnu++11 fr.cpp -o fr -I./openssl-1.0.0 -L./openssl-1.0.0 -lcrypto
g++ -std=gnu++11 pp.cpp -o pp -I./openssl-1.0.0 -L./openssl-1.0.0 -lcrypto
g++ -static -std=gnu++11 fr_static.cpp -o fr_static -I./openssl-1.0.0 -L./openssl-1.0.0 -lcrypto
g++ -static -std=gnu++11 pp_static.cpp -o pp_static -I./openssl-1.0.0 -L./openssl-1.0.0 -lcrypto
# g++ -std=gnu++11 fr_static.cpp ./openssl-1.0.0/libcrypto.a -o fr_static -I./openssl-1.0.0
# g++ -std=gnu++11 aes_no_hw.cpp ./openssl-1.0.0/libcrypto.a -o aes_no_hw -I./openssl-1.0.0
# g++ -std=gnu++11 aes_no_hw.cpp -o aes_no_hw -I./openssl-1.0.0 -L./openssl-1.0.0 -lcrypto
clang -static -mllvm -align-all-functions=8 -mno-red-zone -fomit-frame-pointer -mrtm aes_no_hw.cpp -o aes_no_hw -I./openssl-1.0.0 -L./openssl-1.0.0 -lcrypto
# g++ -std=gnu++11 switch_func.cpp ./openssl-1.0.0/libcrypto.a -o switch_func -I./openssl-1.0.0

# sudo mount -o loop,offset=1048576  ~/en-gem5-fs/disk-image/boot-exit-image/boot-exit /mnt/iso
# # mkdir /mnt/iso/root/fr_en
# sudo cp -r ./ /mnt/iso/root/fr_en
# sudo umount /mnt/iso