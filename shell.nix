with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "trezor-firmware-dev";
  buildInputs = [
    SDL2
    SDL2_image
    autoflake
    check
    clang-tools
    gcc
    git
    gnumake
    graphviz
    libffi
    libjpeg
    libressl
    libusb1
    pipenv
    pkgconfig
    protobuf3_6
    valgrind
    zlib
  ] ++ stdenv.lib.optionals (!stdenv.isDarwin) [
    gcc-arm-embedded
  ] ++ stdenv.lib.optionals (stdenv.isDarwin) [
    darwin.apple_sdk.frameworks.CoreAudio
    darwin.apple_sdk.frameworks.AudioToolbox
    darwin.apple_sdk.frameworks.ForceFeedback
    darwin.apple_sdk.frameworks.CoreVideo
    darwin.apple_sdk.frameworks.Cocoa
    darwin.apple_sdk.frameworks.Carbon
    darwin.apple_sdk.frameworks.IOKit
    darwin.apple_sdk.frameworks.QuartzCore
    darwin.apple_sdk.frameworks.Metal
    darwin.libobjc
    libiconv
  ];
  LD_LIBRARY_PATH = "${libffi}/lib:${libjpeg.out}/lib:${libusb1}/lib:${libressl.out}/lib";
  NIX_ENFORCE_PURITY = 0;
  shellHook = ''
    pipenv shell
    exit
  '';
}
