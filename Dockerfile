# This is a test runner Dockerfile. Specific branches used to
# build our image can be specified using the --build-arg's below.
FROM cern/alma8-base:latest
LABEL author="Szymon Lopaciuk <szymon@lopaciuk.eu>"
ENV PIP_ROOT_USER_ACTION=ignore
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

ARG xobjects_branch=xsuite:main
ARG xdeps_branch=xsuite:main
ARG xpart_branch=xsuite:main
ARG xtrack_branch=xsuite:main
ARG xfields_branch=xsuite:main
ARG xmask_branch=xsuite:main
ARG xcoll_branch=xsuite:main
ARG with_gpu

# Use bash as the default shell
SHELL ["/usr/bin/bash", "-c"]

# Set up the OpenCL profile
RUN if [[ "$with_gpu" == true ]]; then \
        mkdir -p /etc/OpenCL/vendors \
        && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd; \
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
        && dnf clean all \
        && rm -rf /var/cache/yum \
        && git clone --depth 1 https://github.com/geggo/gpyfft.git \
        && pip install ./gpyfft; \
    fi

# Install all the Xsuite packages in the required versions
WORKDIR /opt/xsuite
RUN for project in xobjects xdeps xpart xtrack xfields xmask xcoll; do \
        branch_varname="${project}_branch" \
        && project_branch=${!branch_varname} \
        && IFS=':' read -r -a parts <<< $project_branch \
        && user="${parts[0]}" \
        && branch="${parts[1]}" \
        && git clone \
        --recursive \
        --depth 1 \
        --single-branch -b "$branch" \
        "https://github.com/${user}/${project}.git" \
        && pip install -e ${project}[tests] \
        || break ; \
    done; \
    pip cache purge

# Copy the test runner script into the image
WORKDIR /opt
COPY run_tests.sh /opt/
RUN chmod +x run_tests.sh

CMD python /opt/xsuite/xtrack/examples/print_package_paths.py
