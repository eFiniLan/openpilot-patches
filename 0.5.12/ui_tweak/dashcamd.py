#!/usr/bin/env python2.7
#
# courtesy of pjlao307 (https://github.com/pjlao307/)
# this is just his original implementation but
# in openpilot service form so it's always on
#
# with the highest bit rates, the video is approx. 0.5MB per second
# the default value is set to 2.56Mbps = 0.32MB per second
#
import os
import time
import datetime

dashcam_videos = '/sdcard/dashcam/'
duration = 180 # max is 180
bit_rates = 2560000 # max is 4000000
max_size_per_file = bit_rates/8*duration # 2.56Mbps / 8 * 180 = 57.6MB per 180 seconds
max_storage = max_size_per_file/duration*1024*1024*60*60*6 # 6 hours worth of footage (around 6.5gb)

def dashcamd_thread():
  if not os.path.exists(dashcam_videos):
    os.makedirs(dashcam_videos)

  while 1:
    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    os.system("screenrecord --bit-rate %s --time-limit %s %s%s.mp4 &" % (bit_rates, duration, dashcam_videos, file_name))

    # we should clean up files here if use too much spaces
    used_spaces = get_used_spaces()
    #print("used spaces: %s" % used_spaces)
    last_used_spaces = used_spaces

    # when used spaces greater than max available storage
    if used_spaces >= max_storage:
      # get all the files in the dashcam_videos path
      files = [f for f in sorted(os.listdir(dashcam_videos)) if os.path.isfile(dashcam_videos + f)]
      for file in files:
        # delete file one by one and once it has enough space for 1 video, we skip deleting
        if used_spaces - last_used_spaces < max_size_per_file:
          os.system("rm -fr %s" % (dashcam_videos + file))
          #print("Cleaning")
          last_used_spaces = get_used_spaces()
          #print("last used spaces: %s" % last_used_spaces)
        else:
          break
    # we start the process 1 second before screenrecord ended
    # so we can make sure there are no missing footage
    time.sleep(duration-1)

def get_used_spaces():
  return sum(os.path.getsize(dashcam_videos + f) for f in os.listdir(dashcam_videos) if os.path.isfile(dashcam_videos + f))


def main(gctx=None):
  dashcamd_thread()

if __name__ == "__main__":
  main()
