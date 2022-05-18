# computes the RSSI1 sampling rate given BLF

def fs_hz_calc(lf_khz, s=8.):
    max_fs_hz = 12.e6
    fs_hz = next(12.e6/2.**n for n in range(1,6) if max_fs_hz/(lf_khz*1.e3)/2.**n < (2*s) \
    and max_fs_hz/(lf_khz*1.e3)/2.**n >= s)

    return fs_hz

#print(f'blf MHz: {fs_hz_calc(426, s=7)/1.e6:.4f}')

lf_khz = [640, 320, 250, 160, 426]

for this_lf in lf_khz:
        assert(fs_hz_calc(this_lf, s=7) == fs_hz_calc(this_lf, s=8))