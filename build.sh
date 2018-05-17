# Run by travis
MUNKI_DIR=/usr/local/munki
mkdir -p {ROOT/usr/local/munki/,build}
cp middleware_s3.py ROOT/${MUNKI_DIR}/

VERSION=1.2
  echo "building package $VERSION"
  pkgbuild --root ROOT --identifier com.github.s3-auth \
  --version $VERSION build/com.github.s3-auth.pkg
