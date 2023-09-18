#!/usr/bin/env bash
set -eu

TGARGET="tmp"
OUTPUT="out"
BASEURL="weblog"

###########
# init
###########
echo "install weblog"
pip install .

echo "mkdir ${TGARGET}, ${OUTPUT} "
if [[ -d "${TGARGET}" ]]; then
    echo "remove ${TGARGET}"
    rm -rf ${TGARGET}
fi
if [[ -d "${OUTPUT}" ]]; then
    echo "remove ${OUTPUT}"
    rm -rf ${OUTPUT}
fi
mkdir -p ${TGARGET}
mkdir -p ${OUTPUT}
cd $TGARGET

###########
# build
###########
examples=("site" "blog" "notes")

for sitename in ${examples[@]}; do
    datapath="../examples/${sitename}/"
    echo "init ${sitename}"
    if [[ ${sitename} == "site" ]]; then
        echo "set url ${BASEURL}"
        python -m weblog init --path ${sitename} --url ${BASEURL}
    else
        python -m weblog init --path ${sitename}
    fi
    if [[ -d "${datapath}" ]]; then
        cp -rp ${datapath}/* ${sitename}/
    fi
    cd ${sitename}/
    python -m weblog build
    cd ..
done

###########
# output
###########
cd ..
cp -rp ${TGARGET}/{site,blog,notes}/deploy/${BASEURL}/* ${OUTPUT}/

echo "ok"
