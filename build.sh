# Run by travis
MUNKI_DIR=/usr/local/munki
mkdir -p {ROOT/usr/local/munki/,build}
cp middleware_s3.py ROOT/${MUNKI_DIR}/

if [ ! -z $TRAVIS_TAG ]; then
VERSION=$(echo $TRAVIS_TAG | cut -c2-)
  echo "building package $VERSION"
  pkgbuild --root ROOT --identifier com.github.s3-auth \
  --version $VERSION build/com.github.s3-auth.pkg
fi
