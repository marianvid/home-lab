#include <errno.h>
#include <fcntl.h>
#include <linux/input.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define POWER_INPUT "/dev/input/by-path/platform-PNP0C0C:00-event"
#define SYSTEM_ACTIONS_TRIGGER "/run/aoostar-system-actions"

static int create_trigger(void) {
    int fd = open(SYSTEM_ACTIONS_TRIGGER, O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd < 0)
        return -1;
    return close(fd);
}

int main(void) {
    int fd = open(POWER_INPUT, O_RDONLY);
    if (fd < 0) {
        fprintf(stderr, "Cannot open %s: %s\n", POWER_INPUT, strerror(errno));
        return EXIT_FAILURE;
    }

    printf("Watching %s: short Power opens SYSTEM ACTIONS\n", POWER_INPUT);
    fflush(stdout);

    for (;;) {
        struct input_event event;
        ssize_t size = read(fd, &event, sizeof(event));
        if (size < 0 && errno == EINTR)
            continue;
        if (size != sizeof(event)) {
            fprintf(stderr, "Power input read failed: %s\n",
                    size < 0 ? strerror(errno) : "short read");
            close(fd);
            return EXIT_FAILURE;
        }

        if (event.type == EV_KEY && event.code == KEY_POWER && event.value == 1) {
            if (create_trigger() < 0) {
                fprintf(stderr, "Cannot create %s: %s\n",
                        SYSTEM_ACTIONS_TRIGGER, strerror(errno));
                continue;
            }
            printf("Power: SYSTEM ACTIONS requested\n");
            fflush(stdout);
        }
    }
}
