# This is a test runner Dockerfile. Specific branches used to
# build our image can be specified using the --build-arg's below.
FROM cupy/cupy:latest
ENV DEBIAN_FRONTEND=noninteractive
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

ARG xobjects_branch=xsuite:main
ARG xdeps_branch=xsuite:main
ARG xpart_branch=xsuite:main
ARG xtrack_branch=xsuite:main
ARG xfields_branch=xsuite:main

SHELL ["/usr/bin/bash", "-c"]

# Cupy is already provided, install all that is needed for OpenCL
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
      git clinfo python3.10-venv libclfft2 python3-gpyfft \
    && mkdir -p /etc/OpenCL/vendors \
    && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# We install the Python deps and projects in a venv, otherwise
# pip complains about installing as root
RUN python3 -m venv --system-site-packages /opt/xsuite
ENV PATH="/opt/xsuite/bin:$PATH"
WORKDIR /opt/xsuite
RUN pip install cython pytest pyopencl gitpython \
    && for project in xobjects xdeps xpart xtrack xfields; do \
      branch_varname="${project}_branch" \
      && project_branch=${!branch_varname} \
      && IFS=':' read -r -a parts <<< $project_branch \
      && user="${parts[0]}" \
      && branch="${parts[1]}" \
      && echo git clone -b "$branch" --single-branch "https://github.com/${user}/${project}.git" \
      && git clone -b "$branch" --single-branch "https://github.com/${user}/${project}.git" \
      && pip install -e ${project}[tests] \
      || break ; \
    done

# Don't run tests from /opt/venv not to confuse imports
WORKDIR /opt
CMD python3 /opt/xsuite/xtrack/examples/print_package_paths.py
