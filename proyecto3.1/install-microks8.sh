#!bin/bash

echo "Installing microks8 with snap..."
sudo snap install microk8s --classic
echo "Installation finished!"
sleep 1
echo "Configuring service and dashboard"
sudo microk8s status --wait-ready
microk8s kubectl get all --all-namespaces
sudo microk8s enable dashboard


sleep 1
echo "Getting token for access:"
sudo microk8s kubectl describe secret -n kube-system microk8s-dashboard-token

sudo microk8s enable dashboard
sudo microk8s enable dns
sudo microk8s enable storage

sleep 1
echo "Installation and configuration finished!"
