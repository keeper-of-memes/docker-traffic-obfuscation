#!/bin/bash

CONTAINER_NAME="obfuscation-service-1"
DOCKER_BIN="/usr/local/bin/docker"  # Adjust this path if needed, run `which docker` 

random_between() {
  echo $(( RANDOM % ($2 - $1 + 1) + $1 ))
}

start_container() {
  $DOCKER_BIN start "$CONTAINER_NAME"
  echo "$(date): Started container"
}

stop_container() {
  $DOCKER_BIN stop "$CONTAINER_NAME"
  echo "$(date): Stopped container"
}

# Sleep random seconds between 0 and 5 hours (0 to 18000 seconds)
sleep_seconds=$(random_between 0 18000)
echo "$(date): Sleeping $sleep_seconds seconds before starting container"
sleep $sleep_seconds

start_container

# Randomly during the day (06:00 to 23:00) stop/start container a few times
cycles=$(random_between 3 6)
for i in $(seq 1 $cycles); do
  uptime=$(random_between 900 3600)    # 15-60 mins uptime
  echo "$(date): Container running for $(( uptime / 60 )) minutes"
  sleep $uptime

  stop_container

  downtime=$(random_between 300 900)   # 5-15 mins downtime
  echo "$(date): Container stopped for $(( downtime / 60 )) minutes"
  sleep $downtime

  start_container
done

# Schedule container stop at random time between 23:00 and 03:00
now_epoch=$(date +%s)

# Calculate next 23:00 timestamp
next_23=$(date -d "23:00 today" +%s)
if (( now_epoch > next_23 )); then
  next_23=$(date -d "23:00 tomorrow" +%s)
fi

# Random stop time between 23:00 and 03:00 next day (14400 seconds = 4 hours)
stop_time=$(( random_between next_23 next_23+14400 ))

sleep_seconds=$(( stop_time - now_epoch ))
if (( sleep_seconds > 0 )); then
  echo "$(date): Sleeping $(( sleep_seconds / 60 )) minutes before stopping container for the night"
  sleep $sleep_seconds
fi

stop_container

echo "$(date): Script finished for today."

