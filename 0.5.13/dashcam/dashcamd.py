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
import zmq
import selfdrive.messaging as messaging
from selfdrive.services import service_list

dashcam_videos = '/sdcard/dashcam/'
duration = 60 # max is 180
bit_rates = 2560000 # max is 4000000
max_size_per_file = bit_rates/8*duration # 2.56Mbps / 8 * 60 = 12.3MB per 60 seconds
max_storage = max_size_per_file/duration*1024*1024*60*60*6 # 6 hours worth of footage (around 6.5gb)
freespace_limit = 0.15 # we start cleaning up footage when freespace is below 10%

def dashcamd_thread():
  if not os.path.exists(dashcam_videos):
    os.makedirs(dashcam_videos)

  context = zmq.Context()
  thermal_sock = messaging.sub_sock(context, service_list['thermal'].port)

  while 1:
    # get health of board, log this in "thermal"
    msg = messaging.recv_sock(thermal_sock, wait=True)

    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    os.system("screenrecord --bit-rate %s --time-limit %s %s%s.mp4 &" % (bit_rates, duration, dashcam_videos, file_name))

    used_spaces = get_used_spaces()
    last_used_spaces = used_spaces

    # we should clean up files here if use too much spaces
    # when used spaces greater than max available storage
    # or when free space is less than 10%
    if used_spaces >= max_storage or msg.thermal.freeSpace < freespace_limit:
      # get all the files in the dashcam_videos path
      files = [f for f in sorted(os.listdir(dashcam_videos)) if os.path.isfile(dashcam_videos + f)]
      for file in files:
        msg = messaging.recv_sock(thermal_sock, wait=True)
        # delete file one by one and once it has enough space for 1 video, we stop deleting
        if used_spaces - last_used_spaces < max_size_per_file or msg.thermal.freeSpace < freespace_limit:
          os.system("rm -fr %s" % (dashcam_videos + file))
          last_used_spaces = get_used_spaces()
        else:
          break
    # we start the process 1 second before screenrecord ended
    # to make sure there are no missing footage
    time.sleep(duration-1)

def get_used_spaces():
  return sum(os.path.getsize(dashcam_videos + f) for f in os.listdir(dashcam_videos) if os.path.isfile(dashcam_videos + f))


def main(gctx=None):
  dashcamd_thread()

if __name__ == "__main__":
  main()
