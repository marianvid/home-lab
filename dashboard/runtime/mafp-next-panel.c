#include <fcntl.h>
#include <fprint.h>
#include <glib.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NEXT_PANEL_TRIGGER "/run/aoostar-next-panel"
#define DETAILS_PANEL_TRIGGER "/run/aoostar-details-panel"
#define LONG_PRESS_MS 400

typedef struct {
    gint64 down_us;
    gboolean down;
    gboolean long_fired;
    guint long_press_source;
} TouchState;

static void create_trigger(const char *path) {
    int fd = open(path, O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (fd < 0) {
        g_warning("Could not create %s", path);
        return;
    }
    close(fd);
}

static gboolean fire_long_press(gpointer user_data) {
    TouchState *state = user_data;
    state->long_press_source = 0;

    if (!state->down || state->long_fired)
        return G_SOURCE_REMOVE;

    state->long_fired = TRUE;
    create_trigger(DETAILS_PANEL_TRIGGER);
    g_print("Gesture: hold (%d ms threshold reached)\n", LONG_PRESS_MS);
    fflush(stdout);
    return G_SOURCE_REMOVE;
}

static void on_finger_status(GObject *object, GParamSpec *spec,
                             gpointer user_data) {
    (void)spec;
    FpDevice *device = FP_DEVICE(object);
    TouchState *state = user_data;
    gboolean present =
        (fp_device_get_finger_status(device) & FP_FINGER_STATUS_PRESENT) != 0;

    if (present && !state->down) {
        state->down = TRUE;
        state->long_fired = FALSE;
        state->down_us = g_get_monotonic_time();
        state->long_press_source =
            g_timeout_add(LONG_PRESS_MS, fire_long_press, state);
        g_print("Contact: down\n");
        fflush(stdout);
        return;
    }

    if (!present && state->down) {
        gint64 duration_ms = (g_get_monotonic_time() - state->down_us) / 1000;
        if (state->long_press_source != 0) {
            g_source_remove(state->long_press_source);
            state->long_press_source = 0;
        }

        if (!state->long_fired) {
            create_trigger(NEXT_PANEL_TRIGGER);
            g_print("Gesture: click (%lld ms)\n", (long long)duration_ms);
        } else {
            g_print("Contact: up after hold (%lld ms), no click\n",
                    (long long)duration_ms);
        }
        fflush(stdout);
        state->down = FALSE;
    }
}

static void ignore_progress(FpDevice *device, gint completed_stages,
                            FpPrint *print, gpointer user_data, GError *error) {
    (void)device;
    (void)completed_stages;
    (void)print;
    (void)user_data;
    (void)error;
}

int main(void) {
    /* Driver-specific mode: report contact/release without biometric capture. */
    setenv("MAFP_TOUCH_MODE", "1", 1);

    g_autoptr(FpContext) context = fp_context_new();
    GPtrArray *devices = fp_context_get_devices(context);
    if (devices->len == 0) {
        g_printerr("No fingerprint reader detected\n");
        return EXIT_FAILURE;
    }

    FpDevice *device = g_ptr_array_index(devices, 0);
    g_autoptr(GError) error = NULL;
    g_autoptr(GCancellable) cancel = g_cancellable_new();
    g_autoptr(FpPrint) template = NULL;
    TouchState state = {0};

    if (!fp_device_open_sync(device, NULL, &error)) {
        g_printerr("Reader open failed: %s\n", error->message);
        return EXIT_FAILURE;
    }

    g_signal_connect(device, "notify::finger-status",
                     G_CALLBACK(on_finger_status), &state);
    template = fp_print_new(device);
    fp_print_set_finger(template, FP_FINGER_RIGHT_INDEX);

    g_print("Using %s (%s): permanent touch mode, click=next, "
            "hold=enter/back, threshold=%d ms\n",
            fp_device_get_name(device), fp_device_get_driver(device),
            LONG_PRESS_MS);
    fflush(stdout);

    g_autoptr(FpPrint) result = fp_device_enroll_sync(
        device, template, cancel, ignore_progress, NULL, &error);

    if (error)
        g_printerr("Gesture reader stopped: %s\n", error->message);
    return EXIT_FAILURE;
}
