# This is a test runner Dockerfile. The branches used to
# build our image can be specified using the --build-arg's below.
FROM cern/alma8-base:latest
LABEL author="Szymon Lopaciuk <szymon@lopaciuk.eu>"
ENV PIP_ROOT_USER_ACTION=ignore
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV PYOPENCL_COMPILER_OUTPUT=1

ARG xobjects_branch=xsuite:main
ARG xdeps_branch=xsuite:main
ARG xpart_branch=xsuite:main
ARG xtrack_branch=xsuite:main
ARG xfields_branch=xsuite:main
ARG xmask_branch=xsuite:main
ARG xcoll_branch=xsuite:main
ARG xsuite_branch=xsuite:main
ARG with_gpu

# Use bash as the default shell
SHELL ["/usr/bin/bash", "-c"]

# If an Nvidia GPU is available, nvidia-container-toolkit takes care of
# providing the right libraries and drivers to the container. There is no need
# to install drivers inside the container. Only the ICD file is needed.
RUN cat /sys/class/drm/card*/device/vendor | grep 0x10de; \
    if [[ "$with_gpu" == true && $? == 0 ]]; then \
        mkdir -p /etc/OpenCL/vendors \
        && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd; \
    fi

# If an AMD GPU is available, the driver and ROCm libraries need to be installed
# inside the container, including the right ICD profile. There is no counterpart
# to nvidia-container-toolkit for AMD GPUs.
RUN cat /sys/class/drm/card*/device/vendor | grep 0x1002; \
    if [[ "$with_gpu" == true && $? == 0 ]]; then \
        ROCM_VERSION=5.3 && AMDGPU_VERSION=5.3 \
        && dnf install -y 'dnf-command(config-manager)' \
        && dnf install -y epel-release \
        && echo -e "[ROCm]\nname=ROCm\nbaseurl=https://repo.radeon.com/rocm/yum/$ROCM_VERSION/main\nenabled=1\ngpgcheck=0" >> /etc/yum.repos.d/rocm.repo \
        && echo -e "[amdgpu]\nname=amdgpu\nbaseurl=https://repo.radeon.com/amdgpu/$AMDGPU_VERSION/rhel/8.7/main/x86_64\nenabled=1\ngpgcheck=0" >> /etc/yum.repos.d/amdgpu.repo \
        && dnf install -y rocm-dev && dnf clean all && rm -rf /var/cache/yum \
        && export PATH=/opt/rocm/hcc/bin:/opt/rocm/hip/bin:/opt/rocm/bin:${PATH:+:${PATH}} \
        && export LD_LIBRARY_PATH=/opt/rocm/lib:/usr/local/lib; \
    fi

WORKDIR /opt

# Install mamba and set up an environment
RUN curl -OL https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh
RUN bash Mambaforge-Linux-x86_64.sh -b -p /opt/mambaforge
RUN rm Mambaforge-Linux-x86_64.sh

ENV PATH /opt/mambaforge/bin:$PATH
RUN mamba init bash
RUN mamba create --name xsuite python=3.11
RUN echo "mamba activate xsuite" >> ~/.bashrc

# Install dependencies (compilers, OpenCL and CUDA packages, test requirements)
# - mako is an optional requirement of pyopencl that we need
# - gitpython is useful for print_package_paths.py
# - cython is needed for cffi
# - pytest-html for generating html reports
# - gpyfft is a clfft wrapper that can only be installed from source or .deb
RUN mamba install git pip compilers openmp && mamba clean -afy
RUN pip install --no-cache-dir cython gitpython pytest-html \
    && dnf clean all \
    && rm -rf /var/cache/yum

RUN if [[ "$with_gpu" == true ]]; then \
        mamba install cupy cudatoolkit ocl-icd-system clinfo clfft \
        && mamba clean -afy \
        && pip install --no-cache-dir pyopencl mako \
        && git clone --depth 1 https://github.com/geggo/gpyfft.git \
        && pip install ./gpyfft; \
    fi

# Install all the Xsuite packages in the required versions
WORKDIR /opt/xsuite
COPY ./ /opt/xsuite/xsuite/

RUN chmod +x /opt/xsuite/xsuite/.github/scripts/install_branches.sh && bash /opt/xsuite/xsuite/.github/scripts/install_branches.sh && pip cache purge

# Copy the test runner script into the image
WORKDIR /opt
RUN ln -s /opt/xsuite/xsuite/.github/scripts/run_tests.sh /opt/
RUN chmod +x run_tests.sh

CMD python /opt/xsuite/xtrack/examples/print_package_paths.py
