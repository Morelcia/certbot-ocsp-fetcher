#!/usr/bin/env bats

load _test_helper

@test "fetch OCSP response for a single valid certificate lineage" {
  fetch_sample_certs valid

  run "${BATS_TEST_DIRNAME}/../certbot-ocsp-fetcher.sh" \
    --no-reload-webserver \
    --certbot-dir "${CERTS_DIR}" \
    --output-dir "${OUTPUT_DIR}" \
    --cert-name valid

  [[ ${status} == 0 ]]
  [[ ${lines[1]} =~ ^valid[[:blank:]]+updated$ ]]
  [[ -f "${OUTPUT_DIR}/valid.der" ]]
}
