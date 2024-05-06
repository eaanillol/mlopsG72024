#!bin/bash
echo "Removing microk8s and kubectl with snap..."
sudo snap remove microk8s kubectl
echo "Removing folders and bin file..."
rm -rf ~/.kube /usr/local/bin/kubectl
echo "Finished!"

