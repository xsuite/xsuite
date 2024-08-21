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

Setup of the test runner machine (Ubuntu)
=========================================

An OpenStack GPU-capable machine
--------------------------------

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
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \         && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get install -y nvidia-container-toolkit


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


Setup of the test runner machine (Alma 8)
=========================================

Synopsis
--------

On the AlmaLinux 8 virtual machine (the “host”) will be running a GitHub
runner executing Xsuite tests in a containerised environment. In order
to support GPU execution contexts, Nvidia drivers and the Nvidia
Container Toolkit will need to be installed. At the time of writing this
guide, the Nvidia guide states that Docker is not supported under RHEL
8/CentOS 8 (and so effectively Alma 8 as well), and that is why we will
use Podman instead of Docker. Podman is a container environment similar
to Docker, however it does not require a separate daemon to run
containers, which makes it more lighweight.

Setup a user account
--------------------

We can set up an appropriate GPU-capable OpenStack VM in the same way as
in the previous section (Ubuntu), or simply by following the GUI wizard
on openstack.cern.ch.

On the fresh Alma VM we first set up a user account which we will use to
run our actions:

.. code:: bash

   adduser xsuite

We add the user to the sudoers file, by appending a line to
``/etc/sudoers``: ``echo 'xsuite  ALL=(ALL)   NOPASSWD:ALL' >> /etc/sudoers``.
If necessary, copy the authorised SSH key from the root account
to the new account:
``cp /root/.ssh/authorized_keys /home/xsuite/.ssh/``. Fix permissions
with ``sudo chown -R xsuite:xsuite .ssh`` and ``chmod -R +rw .ssh``.

From now on we reconnect with SSH using the ``xsuite`` account or
switch to it with ``su xsuite``.

Install a Container Engine
--------------------------

We will need a container engine to run the tests. In this case
we install Podman as it is more lightweight:

.. code:: bash

   sudo dnf install podman

Let's make a link called ``docker`` pointing to ``podman``, so
that the workflows (which presume Docker) work on the new machine:

.. code:: bash

   sudo ln -s /usr/bin/podman /usr/bin/docker

Installing Nvidia drivers (can be skipped for CPU-only VM)
----------------------------------------------------------

We will largely be following the official Nvidia guide [1]_, however
only as far as installing the drivers. CUDA is not necessary on the host
machine, only inside the containers.

First, some prerequisites are necessary. In this guide, we will be
installing the drivers using the “network RPM” method in Nvidia’s guide.
We will perform a DKMS installation, so that the drivers get recompiled
whenever there is a kernel update, so that it does not need to be done
manually. To this end, we need to install kernel headers:

.. code:: bash

   sudo dnf install kernel-devel-$(uname -r) kernel-headers-$(uname -r)

To satisfy other requirements of the Nvidia driver package, we enable
the third party repository EPEL:

.. code:: bash

   sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm

Then we can enable the network repo and install the drivers:

.. code:: bash

   sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo
   sudo dnf clean all
   sudo dnf -y module install nvidia-driver:latest-dkms
   sudo dnf clean expire-cache  # clean dnf cache afterwards

To check if everything works, we can ``sudo reboot``, then run the
following command, which, if all went well, should return a summary of
the available GPUs:

.. code:: bash

   nvidia-smi

.. note::

   **Troubleshooting Note:** If at this stage the driver is not working,
   it could be that it was not picked up by DKMS. We can verify this by
   running ``dkms status``: if there is no ``nvidia/...`` entry, or if
   to the right of it its status is not listed as ``installed``, we can
   run ``dkms autoinstall`` to attempt to recompile the drivers.

Installing the Nvidia Container Toolkit (can be skipped for a CPU-only VM)
--------------------------------------------------------------------------

We will follow the instruction of the official Nvidia guide [2]_, the
steps of which are summarised below.

A container environment is a prerequisite for installing the NCT: earlier
we have installed Podman.

Podman is compatible with the Container Device Interface specification,
which means that only the base components of the Nvidia Container
Toolkit are needed. We install the required package:

.. code:: bash

   sudo dnf clean expire-cache
   sudo dnf install -y nvidia-container-toolkit-base

Check that it works:

.. code:: bash

   nvidia-ctk --version

And generate the CDI specification with:

.. code:: bash

   sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml

To be able to run rootless containers with ``podman``, we change the
following configuration:

.. code:: bash

   sudo sed -i 's/^#no-cgroups = false/no-cgroups = true/;' /etc/nvidia-container-runtime/config.toml

When running rootless, we may also encounter permission issues with
SELinux. We need to add an appropriate label ``container_file_t`` to the
Nvidia device files:

.. code:: bash

   sudo semanage fcontext -a -t container_file_t '/dev/nvidia.*'
   restorecon -v /dev/*

Note that it may be necessary to relabel the device files with the ``restorecon`` 
command in the case of changes/updates to the hypervisor.

.. note::

    **Troubleshooting Note:** It may be necessary to run
    ``sudo dnf install policycoreutils-python-utils``
    for ``semanage`` to work, as after a certain update to
    Alma it stopped being provided by default.

Check that everything works with:

.. code:: bash

   podman run --rm --gpus all cupy/cupy:latest nvidia-smi

Setup the GitHub runner
-----------------------

Navigate to *Settings > Actions > Runners* on GitHub and follow the
instructions for creating the new runner. Once this is done, there are
three final steps that need to be done before we enable the runner
service.

Take care to replace ``{runner-name}`` in the subsequent commands
with the chosen name of your runner.

Set the right container format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since we are using a docker Dockerfile format, which is slightly
different to the OCI format, to which podman defaults, we need to change
the setting for podman to use the Docker format. To achieve this, we add
an environment variable to the runner service file:

.. code:: bash

   sudo ./svc.sh install xsuite && sudo ./svc.sh stop  # create but don't start the service
   sudo systemctl edit actions.runner.xsuite-xsuite.{runner-name}.service

In the opened editor (which may be empty), we paste the following:

.. code:: ini

   [Service]
   Environment="BUILDAH_FORMAT=docker"

Configure SELinux
~~~~~~~~~~~~~~~~~

We need to label the service script as an executable to SELinux,
otherwise it will prevent us from launching the service.

.. code:: bash

   sudo semanage fcontext -a -t bin_t '/home/xsuite/actions-runner/runsvc.sh'
   sudo semanage fcontext -a -t bin_t '/home/xsuite/actions-runner/bin(/.*)?'
   sudo restorecon -v -R /home/xsuite/actions-runner/

Enable account lingering
~~~~~~~~~~~~~~~~~~~~~~~~

In order for Podman to be able to function headless, we need to enable
account lingering, as otherwise, systemd will kill any user process when
there is no login session for the user.

.. code:: bash

   sudo loginctl enable-linger xsuite

Enable and start the service
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, we can start the runner service, which will immediately begin
listening for new jobs:

.. code:: bash

   sudo ./svc.sh start

.. note::

    **Troubleshooting Note**: The status of the runner service can
    be checked with ``sudo ./svc.sh status`` which is an alias to
    ``systemctl status actions.runner.xsuite-xsuite.{runner-name}``
    More logs for the service can be viewed with 
    ``sudo journalctl -x -u actions.runner.xsuite-xsuite.{runner-name}``.
    In case of errors it can be useful to also consult SELinux logs:
    ``sudo cat /var/log/audit/audit.log | grep 'denied'``.

.. [1]
   https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html

.. [2]
   https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
