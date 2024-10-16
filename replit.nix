{pkgs}: {
  deps = [
    pkgs.openssh
    pkgs.mpi
    pkgs.zlib
    pkgs.pkg-config
    pkgs.grpc
    pkgs.c-ares
    pkgs.openssl
    pkgs.postgresql
  ];
}
