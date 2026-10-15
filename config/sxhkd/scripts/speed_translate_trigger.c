#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#define SOCK_PATH "/tmp/speed_translate.sock"

int main() {
    int s = socket(AF_UNIX, SOCK_DGRAM, 0);
    if (s < 0) return 1;

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, SOCK_PATH, sizeof(addr.sun_path) - 1);

    char buf[1] = {'1'};
    ssize_t res = sendto(s, buf, 1, 0, (struct sockaddr*)&addr, sizeof(addr));
    close(s);

    if (res < 0) {
        // Socket failed (daemon not active); spawn daemon and trigger after a brief moment
        char *home = getenv("HOME");
        if (home) {
            char cmd[512];
            snprintf(cmd, sizeof(cmd), "setsid python3 %s/.config/sxhkd/scripts/speed_translate.py daemon </dev/null >/dev/null 2>&1 &", home);
            int _ignored = system(cmd);
            (void)_ignored;
            usleep(150000);
            int s2 = socket(AF_UNIX, SOCK_DGRAM, 0);
            if (s2 >= 0) {
                sendto(s2, buf, 1, 0, (struct sockaddr*)&addr, sizeof(addr));
                close(s2);
            }
        }
    }
    return 0;
}
