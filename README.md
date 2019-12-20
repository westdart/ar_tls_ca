# ar_tls_ca

Setup a basic CA and sign certificates
The 'main.yml' set of tasks sets up a CA using openssl.
The 'sign.yml' separates out the signing of certificates, enabling it to be included
separately when required.
Optionally a git repo can be specified, where the state of the CA will 
be held, keys are wrapped in a vault file

# Requirements

- openssl

## Role Variables

| Variable                  | Description                 | Default    |
| --------                  | -----------                 | -------    |
| ar_tls_ca_path            | Path to hold all CA files   | None       |
| ar_tls_ca_name            | Name for the CA             | None       |
| ar_tls_ca_certlist        | List of CSRs to sign        | [] (empty) |
| ar_tls_ca_revocation_list | List of CRT names to revoke | [] (empty) |


## Dependencies

None

## Example Playbook

    - hosts: servers
      tasks:
        - name: "Setup CA"
          include_role:
            name: ar_tls_ca
          vars:
            ar_tls_ca_path: "/tmp/ca"
            ar_tls_ca_name: "test-ca"
            ar_tls_ca_certlist: [
              {"certfile": "my-cert-1.crt", "csrfile": "my-cert-1.csr", "altnames": ["my-cert-1.domain"], "ipaddrs": ["1.2.3.4"]},
              {"certfile": "my-cert-2.crt", "csrfile": "my-cert-2.csr", "altnames": ["my-cert-2.domain"], "ipaddrs": ["1.2.3.4"]}
            ]


## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a
website (HTML is not allowed).


# Notes leading to creation of this role
## Create the CA:
```
mkdir ca
mkdir ca/newcerts
touch ca/index.txt
echo '01' > ca/serial

openssl genrsa -out ca/dev.my-company.ca.key 2048
openssl req -new -x509 -key ca/dev.my-company.ca.key -out ca/dev.my-company.ca.crt -subj "/CN=dev.my-company.ca"
```

## Create the server key and CSR:
```
openssl req -nodes -batch -out tls-csr.pem -newkey rsa:2048 -days 365 -keyout tls-key.pem \
  -subj "/C=UK/ST=Buckinghamshire/L=Milton Keynes/O=Boeing/OU=MJDI Dev/CN=amq-interconnect.amqtest1.svc"

-passout pass:password 
```

## Sign the CSR:
```
openssl ca -bath -config ca/ca.cfg -out tls-crt.pem -extfile san.cfg -infiles tls-csr.pem
```

## Check the CRT has the alternate names (DNS)
```
openssl x509 -in tls-crt.pem -text | grep amq-interconnect-tls-amqtest1.a1.training.local
```

## Create java truststore from CA key
```
keytool -import -keystore truststore.ks -alias caroot -file ca/dev.my-company.ca.crt -storepass password \
  -trustcacerts -no-prompt
```

## Clear the CA state:
```
rm -f ca/index.txt* ca/serial* ca/newcerts/* 
touch ca/index.txt
echo '01' > ca/serial
```

## Comparing the moduli:
Cert Modulus:
```
openssl x509 -noout -text -in generated/DEV/certs/MESH.crt | grep -A18 'Modulus:' | tr -d ' '
```

CSR Modulus:
```
openssl req -in generated/DEV/certs/MESH.csr -noout -pubkey | openssl pkey -pubin -inform PEM -text -noout | tr -d ' '
```

Private key Modulus:
```
cat  private.key | openssl pkey -pubout -text | grep -A18 'modulus:' | tr -d ' '
```
or with key base64 encoded in ansible vault:
```
ansible-vault view vault | grep key | awk -F "'" '{print $2}' | base64 -d | openssl pkey -pubout -text | grep -A18 'modulus:' | tr -d ' '
```
