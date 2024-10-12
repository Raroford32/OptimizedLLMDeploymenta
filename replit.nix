{pkgs}: {
  deps = [
    pkgs.zlib
    pkgs.pkg-config
    pkgs.grpc
    pkgs.c-ares
    pkgs.openssl
    pkgs.postgresql
  ];
}
