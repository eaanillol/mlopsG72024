#!bin/bash
PORT_MICROKS8="8089"
INPUT_PORT=""
echo "Please type a valid port for exposing the UI-dashboard [by default 8089]:"
read INPUT_PORT

INPUT_PORT=${INPUT_PORT:-${PORT_MICROKS8}}
echo "Value ${INPUT_PORT}"

if [ "$INPUT_PORT" = "$PORT_MICROKS8" ]]; then
   echo "We are going to use the default port ${PORT_MICROKS8}"
else
   PORT_MICROKS8=${INPUT_PORT}
fi

sudo microk8s kubectl port-forward -n kube-system service/kubernetes-dashboard ${PORT_MICROKS8}:443 --address 0.0.0.0

