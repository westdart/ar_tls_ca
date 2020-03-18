# ar_tls_ca

Setup a basic CA and sign certificates
The 'main.yml' set of tasks sets up a CA using openssl.
The 'sign.yml' separates out the signing of certificates, enabling it to be included
separately when required.
Optionally a git repo can be specified, where the state of the CA will 
be held, keys are wrapped in a vault file

# Requirements

- openssl
- git

## Role Variables
The following details:
- the parameters that should be passed to the role (aka vars)
- the defaults that are held
- the secrets that should generally be sourced from an ansible vault.

### Parameters:
| Variable                  | Description                                                                     | Default    |
| --------                  | -----------                                                                     | -------    |
| ar_tls_ca_name            | Name for the CA                                                                 | None       |
| ar_tls_ca_certlist        | List of CSRs to sign                                                            | [] (empty) |
| ar_tls_ca_revocation_list | List of CRT names to revoke                                                     | [] (empty) |
| ar_tls_ca_git_repo        | Git repository holding state                                                    | None       |
| ar_tls_ca_git_version     | The version of the repository to use (note should be updateable, i.e. a branch) | 'master'   |
| ar_tls_ca_git_comment     | Additional comment text to add to commits                                       | ''         |


### Defaults
| Variable                   | Description                                                              | Default           |
| --------                   | -----------                                                              | -------           |
| ar_tls_ca_ca_default_days  | Number of days that the CA certificate should be valid                   | 3650              |
| ar_tls_ca_default_days     | Number of days that the certificates being signed should be valid        | 365               |
| ar_tls_ca_lookahead_days   | Max number of days overlap with expiring certificates                    | 30                |
| ar_tls_ca_vault_file       | The vault file containing CA secrets                                     | '.vault'          |
| ar_tls_ca_git_ssh_key      | The key to use to access the git repository                              | Not Defined       |
| ar_tls_ca_basic_assertions | List of assertions made                                                  | See definitions   |
| ar_tls_ca_git_assertions   | List of assertions made                                                  | See definitions   |
| ar_tls_ca_git_dest_link    | Symbolic link to create to ensure paths in CA config files remain static | '/tmp/tls_ca_lnk' |
| ar_tls_ca_passphrases      | Dictionary of passphrases keyed on CA name                               | {} (empty)        |

### Secrets
The following variables should be provided through an encrypted source:
- ar_tls_ca_passphrases
- ar_tls_ca_git_ssh_key

## Dependencies

- ar_git_repo

## Example Playbook

    - hosts: servers
      tasks:
        - name: "Setup CA"
          include_role:
            name: ar_tls_ca
          vars:
            ar_tls_ca_name: "test-ca"
            ar_tls_ca_git_repo: "git@git-host:group/repo.git"
            ar_tls_ca_git_ssh_key: "my-key"
            ar_tls_ca_certlist: [
              {"certfile": "my-cert-1.crt", "csrfile": "my-cert-1.csr", "altnames": ["my-cert-1.domain"], "ipaddrs": ["1.2.3.4"]},
              {"certfile": "my-cert-2.crt", "csrfile": "my-cert-2.csr", "altnames": ["my-cert-2.domain"], "ipaddrs": ["1.2.3.4"]}
            ]


## License

MIT / BSD

## Author Information

This role was created in 2020 by David Stewart (dstewart@redhat.com)
