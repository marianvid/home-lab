#include <fprint.h>
#include <glib.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define CALIBRATION_SAMPLES 15

typedef struct {
    gint64 down_us;
    unsigned count;
    gboolean down;
} Calibration;

static void on_finger_status(GObject *object, GParamSpec *spec, gpointer user_data) {
    (void)spec;
    FpDevice *device = FP_DEVICE(object);
    Calibration *cal = user_data;
    FpFingerStatusFlags status = fp_device_get_finger_status(device);
    gboolean present = (status & FP_FINGER_STATUS_PRESENT) != 0;

    if (present && !cal->down) {
        cal->down = TRUE;
        cal->down_us = g_get_monotonic_time();
        printf("contact\n");
        fflush(stdout);
        return;
    }

    if (!present && cal->down) {
        gint64 duration_ms = (g_get_monotonic_time() - cal->down_us) / 1000;
        cal->down = FALSE;
        cal->count++;
        printf("sample %u/%u: %lld ms\n", cal->count, CALIBRATION_SAMPLES,
               (long long)duration_ms);
        fflush(stdout);

        if (cal->count >= CALIBRATION_SAMPLES)
            _exit(EXIT_SUCCESS);
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
    setenv("MAFP_ENROLL_SAMPLES", "30", 1);

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
    Calibration cal = {0};

    if (!fp_device_open_sync(device, NULL, &error)) {
        g_printerr("Reader open failed: %s\n", error->message);
        return EXIT_FAILURE;
    }

    g_signal_connect(device, "notify::finger-status",
                     G_CALLBACK(on_finger_status), &cal);
    template = fp_print_new(device);
    fp_print_set_finger(template, FP_FINGER_RIGHT_INDEX);

    printf("Calibration ready: perform %u natural short and long presses.\n",
           CALIBRATION_SAMPLES);
    fflush(stdout);

    g_autoptr(FpPrint) result = fp_device_enroll_sync(
        device, template, cancel, ignore_progress, NULL, &error);

    if (error)
        g_printerr("Calibration stopped: %s\n", error->message);
    return EXIT_FAILURE;
}
