ARG VERSION=3.1.4
# FROM fluent/fluent-bit:${VERSION}
FROM fluent/fluent-bit:${VERSION}-debug AS builder
ARG VERSION

WORKDIR /build

# build on fluent-bit for supporting headers and libs
RUN git clone --depth 1 --branch v${VERSION} https://github.com/fluent/fluent-bit.git && \
    # rather dirty, will build in root dir rather than build dir so that built header files
    # will be available to the plugin on fluent-bit include paths
    cd fluent-bit && \
    cmake .

# build on fluent-bit-disk
RUN git clone --depth 1 https://github.com/nagi49000/fluent-bit-disk.git && \
    cd fluent-bit-disk && \
    mkdir -p build && \
    cd build && \
    cmake -DFLB_SOURCE=/build/fluent-bit/ -DPLUGIN_NAME=in_vdisk .. && \
    make && \
    find ./ -name *.so

FROM fluent/fluent-bit:${VERSION}-debug
RUN mkdir /fluent-bit/plugins && \
    echo "    Path /fluent-bit/plugins/flb-in_vdisk.so" >> /fluent-bit/etc/plugins.conf

COPY --from=builder /build/fluent-bit-disk/build/flb-in_vdisk.so /fluent-bit/plugins/flb-in_vdisk.so