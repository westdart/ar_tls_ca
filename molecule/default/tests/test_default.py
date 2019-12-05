import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

CERTS = ['my-cert-1', 'my-cert-2']
CERT_OPTS = "no_subject,no_header,no_version,no_serial,no_signame,no_validity,no_issuer,no_pubkey,no_sigdump,no_aux"


@pytest.mark.parametrize('cert', CERTS)
def test_alternate_names(host, cert):
    cmd = host.run("openssl x509 -in /tmp/ca/out/%s.crt -noout -text "
                   "-certopt %s | grep 'DNS:%s.domain, IP Address:1.2.3.4'", cert, CERT_OPTS, cert)
    assert cmd.rc == 0
