#!/usr/bin/env sh

set -eu

image="flow-test-ping-contract:local"
container="flow-test-ping-contract-$$"

cleanup() {
  docker rm --force "$container" >/dev/null 2>&1 || true
}

trap cleanup EXIT INT TERM

docker build --tag "$image" .
docker run --detach --name "$container" --publish 127.0.0.1::80 "$image" >/dev/null

port="$(docker port "$container" 80/tcp | sed -n '1s/.*://p')"
test -n "$port"
endpoint="http://127.0.0.1:$port"

# Wait on an always-healthy endpoint instead of sleeping for server startup.
curl --fail --silent --show-error --retry 30 --retry-connrefused --retry-max-time 30 \
  --output /dev/null "$endpoint/"

# Exercise the known intermittent failure window without an arbitrary delay.
while [ "$(( $(date +%s) % 3 ))" -ne 0 ]; do
  :
done

for request in $(seq 1 10); do
  if ! status="$(curl --silent --show-error --output /dev/null --write-out '%{http_code}' "$endpoint/ping")"; then
    echo "request $request to /ping could not be completed" >&2
    exit 1
  fi

  case "$status" in
    2??) ;;
    *)
      echo "request $request to /ping returned HTTP $status (expected 2xx)" >&2
      exit 1
      ;;
  esac
done
