============================
Continuous testing of xsuite
============================

Since GitHub do not yet support GPU on their own Actions runners, we set up
our own self-hosted runner on OpenStack for this purpose. The configuration
of the test workflow can be found in `.github/test_gpu.yaml` of the xsuite
repository. However, the test machine needs to first be prepared. As we use
Docker to run the tests in an isolated and controlled environment, some
dependencies need to be installed. These are Docker and Nvidia drivers and
Container Toolkit (assuming the test machine uses an Nvidia GPU). The steps
to accomplish this are listed below.

Setup of the test runner machine
================================

An OpenStack GPU-capable machine
--------------------------------

We use Ubuntu, because Nvidia does not provide drivers for CS8.
This can be set up largely following the guide
`here <https://abpcomputing.web.cern.ch/guides/openstackUbuntu/>`_.

.. code-block:: bash

    # Find the image uuid you want
    openstack image list --community | grep -i ubuntu
    # Commands to be passed during the setup of our machine
    cat > ubuntu-bootcmd.txt <<- EOF
    #cloud-config
    bootcmd:
    - printf "[Resolve]\nDNS=137.138.16.5 137.138.17.5\n" > /etc/systemd/resolved.conf
    - [systemctl, restart, systemd-resolved]
    EOF
    # Create the VM
    openstack server create \
      --image <IMAGE_UUID> \
      --user-data ubuntu-bootcmd.txt \
      --flavor g2.5xlarge \
      --key-name lxplus xsuite-ubuntu-tests

Configure the test machine
--------------------------

Once we ssh to the machine (as user `ubuntu`) we need to install
Docker and suitable Nvidia drivers. We can use the convenience script
provided by the Docker people, as described
`here <https://docs.docker.com/engine/install/ubuntu>`_.

.. code-block:: bash

    # Install docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    # Set up rootless for good practice
    dockerd-rootless-setuptool.sh install

To be able to run containers with GPU support we need the Nvidia
container toolkit. A prerequisite for that are the Nvidia drivers.
The up-to-date install instructions for the toolking can be found
`here <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>`_.
There is also a useful page available on the topic on the
`CERN OpenStack guide <https://clouddocs.web.cern.ch/gpu/index.html>`_.

.. code-block:: bash

    # Install cuda drivers
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
    sudo dpkg -i cuda-keyring_1.0-1_all.deb
    sudo apt-get update
    sudo apt-get -y install cuda

    # Install the container toolkit
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list


After restarting the Docker daemon with `sudo systemctl restart docker`, we can check
that everything works by running a sample image from Nvidia:

.. code-block::

    docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi

Install the GitHub Actions runner
---------------------------------

We can follow the steps listed under *xsuite/xsuite > Settings >
Actions > Runners > New self-hosted runner*.

This involves downloading and configuring the runner with the
repository.

Afterwards, we install and run the runner as a service with user `ubuntu`:

.. code-block::

    ./svc.sh install ubuntu
    ./svc.sh start
