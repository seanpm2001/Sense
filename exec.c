#include <unistd.h>
#include <stdio.h>

int main(void)
{
    char *argv[] = { "/bin/sh", "/home/fan/Flush-Reload/newspy", 0 };
    char *envp[] =
    {
        "PATH=/home/fan/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "LD_LIBRARY_PATH=/home/fan/openssl-1.1.0f",
        0
    };
    execve("/home/fan/Flush-Reload/newspy", 0, envp);
    fprintf(stderr, "Oops!\n");
    return -1;
}
