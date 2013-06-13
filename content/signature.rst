Linux kernel releases PGP signatures
====================================

:date: 2013-01-01
:slug: signature
:category: Signatures

All kernel releases are cryptographically signed using OpenPGP-compliant
signatures. Everyone is strongly encouraged to verify the integrity of
downloaded kernel releases by verifying the corresponding signatures.

**Linux kernel releases and all other files distributed via kernel.org
mirrors are no longer signed by one centrally issued key. You will need
to rely on the PGP Web of Trust in order to verify the authenticity of
downloaded archives.**

Basic concepts
--------------
Every kernel release comes with a cryptographic signature from the
person making the release. This cryptographic signature allows anyone to
verify whether the files have been modified or otherwise tampered with
since the developer created and signed them. The signing and
verification process uses public-key cryptography and it is next to
impossible to forge a PGP signature without first gaining access to the
developer's private key. If this does happen, the developers will revoke
the compromised key and will re-sign all their previously signed
releases with the new key.

To learn more about the way PGP works, please consult Wikipedia_.

.. _Wikipedia: https://en.wikipedia.org/wiki/Pretty_Good_Privacy#How_PGP_encryption_works

Kernel.org web of trust
-----------------------
In order for this section to make sense, you should first familiarize
yourself with the way PGP Web of Trust works. You can start by reading
the `Wikipedia article`_ on the subject.

In a few words, **PGP keys used by members of kernel.org are
cross-signed by other members of kernel.org** (and, frequently, by many
other people). If you wanted to verify the validity of any key
belonging to a member of kernel.org, you could review the list of
signatures on their public key and then make a decision whether you trust
that key or not. This article from the GnuPG manual is a good first step
towards understanding how you can use PGP trust relationships to
validate keys: `Using trust to validate keys`_.

In order to become part of the kernel.org web of trust, you should
locate kernel.org members in your geographical area, then verify and
sign their keys. To locate members of kernel.org in your area, you can
either use the `Google Map`_ created for this purpose, or send an email
to the users@kernel.org mailing list, requesting key signing.

Once you have verified and signed a few keys, you can use the trust
relationship established in the process to verify other keys used in the
kernel.org web of trust.

.. _`Wikipedia article`: https://en.wikipedia.org/wiki/Web_of_trust
.. _`Using trust to validate keys`: http://www.gnupg.org/gph/en/manual.html#AEN385
.. _`Google Map`: https://j.mp/kgpgmap

Using GnuPG to verify kernel signatures
---------------------------------------
All software released via kernel.org has corresponding PGP signatures.
It should not be possible to upload any files to the kernel.org mirrors
without providing a trusted PGP signature to go along with them.

To better illustrate the verification process, let's use Linux 3.1.5
release as a walk-through example. First, use "``wget``" or "``curl
-O``" to download the release and the corresponding signature::

    $ wget https://www.kernel.org/pub/linux/kernel/v3.0/linux-3.1.5.tar.xz
    $ wget https://www.kernel.org/pub/linux/kernel/v3.0/linux-3.1.5.tar.sign

You will notice that the signature is made against the uncompressed
version of the archive. This is done so there is only one signature
required for .gz, .bz2 and .xz compressed versions of the release. Start
by uncompressing the archive, using ``unxz`` in our case::

    $ unxz linux-3.1.5.tar.xz
    
Now verify the .tar archive against the signature::

    $ gpg --verify linux-3.1.5.tar.sign

You can combine these steps into a one-liner::

    $ xz -cd linux-3.1.5.tar.xz | gpg --verify linux-3.1.5.tar.sign -

The likely output will be::

    gpg: Signature made Fri 09 Dec 2011 12:16:46 PM EST using RSA key ID 6092693E
    gpg: Can't check signature: public key not found
    
You will need to first download the public key from the PGP keyserver in
order to verify the signature. Look at the first line of the output and
note the "key ID" listed, which in our example is ``6092693E``. Now
download this key from the key servers::

    $ gpg --recv-keys 6092693E
    gpg: requesting key 6092693E from hkp server subkeys.pgp.net
    gpg: key 6092693E: public key "Greg Kroah-Hartman 
         (Linux kernel stable release signing key) <greg@kroah.com>" imported
    gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
    gpg: depth: 0  valid:   3  signed:   1  trust: 0-, 0q, 0n, 0m, 0f, 3u
    gpg: depth: 1  valid:   1  signed:   0  trust: 0-, 0q, 0n, 0m, 1f, 0u
    gpg: Total number processed: 1
    gpg:               imported: 1  (RSA: 1)

Let's rerun "``gpg --verify``"::

    $ gpg --verify linux-3.1.5.tar.sign 
    gpg: Signature made Fri 09 Dec 2011 12:16:46 PM EST using RSA key ID 6092693E
    gpg: Good signature from "Greg Kroah-Hartman 
         (Linux kernel stable release signing key) <greg@kroah.com>"
    gpg: WARNING: This key is not certified with a trusted signature!
    gpg:          There is no indication that the signature belongs to the owner.
    Primary key fingerprint: 647F 2865 4894 E3BD 4571  99BE 38DB BDC8 6092 693E
    
Notice the **WARNING: This key is not certified with a trusted
signature!** You will now need to verify that the key used to sign the
archive really does belong to the owner (in our example, Greg
Kroah-Hartman). There are several ways you can do this:

1. Use the `Kernel.org web of trust`_. This will require that you first
   locate the members of kernel.org in your area and sign their keys.
   **Short of meeting the actual owner of the PGP key in real life, this
   is your best option to verify the validity of a PGP key signature.**
2. Review the list of signatures on the developer's key by using "``gpg
   --list-sigs``". Email as many people who have signed the key as
   possible, preferably at different organizations (or at least
   different domains). Ask them to confirm that they have signed the key
   in question. You should attach at best marginal trust to the
   responses you receive in this manner (if you receive any).

If at any time you see "BAD signature" output from "``gpg --verify``",
please first check the following first:

1. **Make sure that you are verifying the signature against the .tar
   version of the archive, not the compressed (.tar.xz) version.**
2. Make sure the the downloaded file is correct and not truncated or
   otherwise corrupted.

If you repeatedly get the same "BAD signature" output, email
ftpadmin@kernel.org immediately, so we can investigate the problem.

Kernel.org checksum autosigner and sha256sums.asc
-------------------------------------------------
We have a dedicated off-the-network system that connects directly to our
central attached storage and calculates checksums for all uploaded
software releases. The generated ``sha256sums.asc`` file is then signed
with a PGP key generated for this purpose and that doesn't exist outside
of that system.

These checksums are **NOT** intended to replace the web of trust. It is
merely a way for someone to quickly verify whether contents on one of
the many kernel.org mirrors match the contents on the master mirror.
While you may use them to quickly verify whether what you have
downloaded matches what we have on our central storage system, you
should still use the GPG web of trust to verify whether the release
tarball actually matches what the kernel developer published.

Kernel releases prior to September, 2011
----------------------------------------
Prior to September, 2011 all kernel releases were signed automatically by
the same PGP key::

    pub   1024D/517D0F0E 2000-10-10 [revoked: 2011-12-11]
          Key fingerprint = C75D C40A 11D7 AF88 9981  ED5B C86B A06A 517D 0F0E
    uid                  Linux Kernel Archives Verification Key <ftpadmin@kernel.org>

Due to the kernel.org systems compromise, this key has been retired and
revoked. **It will no longer be used to sign future releases and you
should NOT use this key to verify the integrity of any archives. It is
almost certain that this key has fallen into malicious hands.**

All kernel releases that were previously signed with this key are being
cross-checked and will be signed with another key, created specifically
for this purpose. Once the process is completed, the new key information
will be put on this page.

Revocation certificates
-----------------------
The following revocation certificates have been issued for keys used in
the past to sign kernel.org software releases:

Key ID 0x517D0F0E
~~~~~~~~~~~~~~~~~
Key fingerprint::

    pub   1024D/517D0F0E 2000-10-10 [revoked: 2011-12-11]
          Key fingerprint = C75D C40A 11D7 AF88 9981  ED5B C86B A06A 517D 0F0E
    uid                  Linux Kernel Archives Verification Key <ftpadmin@kernel.org>

Revocation certificate::

    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v1.4.11 (GNU/Linux)
    Comment: A revocation certificate should follow

    iIkEIBECAEkFAk7lL6xCHQJLZXkgd2FzIHVzZWQgdG8gYXV0b3NpZ25pbmc7IGF1
    dG9zaWduaW5nIHNlcnZlciB3YXMgY29tcHJvbWlzZWQuAAoJEMhroGpRfQ8OS7EA
    nikD5S7mmNM0QRX+H4BDxvdWzXWyAKCTuDGOdLoZs8gnl/G5UKVjX9mVkg==
    =eL49
    -----END PGP PUBLIC KEY BLOCK-----
    
Key ID 0x1E1A8782
~~~~~~~~~~~~~~~~~
Key fingerprint::

    pub   1024D/1E1A8782 1999-10-05 [revoked: 2000-10-10]
          Key fingerprint = 9DB4 C3A4 EF2A 3111 9072  82F3 F2A5 75DC 1E1A 8782
    uid                  Linux Kernel Archives Verification Key <ftpadmin@kernel.org>
    
Revocation certificate::

    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: GnuPG v1.0.0 (GNU/Linux)
    Comment: For info see http://www.gnupg.org
    Comment: A revocation certificate should follow

    iEYEIBECAAYFAjnisTIACgkQ8qV13B4ah4K3DgCfShKQe2kfz68OKu0WwEzgKkAE
    vIQAn3Y8CTCRZ9QEIwsIs93F501VUtPs
    =l5FV
    -----END PGP PUBLIC KEY BLOCK-----
    
Key ID 0x514C5279
~~~~~~~~~~~~~~~~~
Key fingerprint::

    pub   1024R/514C5279 1998-12-16 [revoked: 1999-10-05]
          Key fingerprint = 59 B1 5F 6F E3 13 4C 8B  33 E5 14 35 21 F1 D1 03
    uid                  Linux Kernel Archives <ftpadmin@kernel.org>

Revocation certificate::

    -----BEGIN PGP PUBLIC KEY BLOCK-----
    Version: 2.6.3a

    mQCNAzZ4N0EAAAEEAJpp8Hy0n2FBJqmrfX9dha1Ja/Uc7f63Afbv0SBTE4i+xeyg
    5O/4VWr11LlP1uAjM8Gvfw8neRMLhMUjvRaXPhRR9KoAaW84Bg0cBSyakY6j1JXz
    JcBVKGoGNgBo82cVM9bkE1/Qdy9v6pGDw3qhAqBNLDtYDUS8fgTPgU1RTFJ5AAUR
    iQCVAwUgN/p+yATPgU1RTFJ5AQGk3wP/YDsx7Wys/FSfBMpfQA+7IO5Ug2voBGDa
    hXHKIofT9H7/eYBr3Sctq+/eZAVwll1iS3dkzBIEuvbVlgVam/nvegfRrL2hKy7i
    ELespx5WEqfhnapawg/xpFRsPkYOq96IcoGSIQSwGCq4wqz/CwfG/tQx0eGP9k7j
    N176TIjYdzu0K0xpbnV4IEtlcm5lbCBBcmNoaXZlcyA8ZnRwYWRtaW5Aa2VybmVs
    Lm9yZz6JAJUDBRA2eFIpnE1kY6hrNcUBARi6BACbJhIzBynhTW75RUeOqGv097+c
    ybQZ5fysSf3zeAIxGSFlZcpruHpLylwRXumhiOjqWjKbEeN2r9MqcutIKUVt2lkP
    p2BsqKN7CzmSMWLO13DYr7cSufKqm6AOe0pTqJJKTI/yST7DpHkDsi+FYN7eZ79w
    xETITd0Z/7/dF1uwBIkAlQMFEDZ4S3QCetOcrPWlRQEBcwkEAJbhw4ggjcenRNNo
    357I8dzEHrIWIAhonjAnWddEwyGFUy1cmayNTO/PRXjubCEFuJttWZ50cKPpiwYr
    oxGOglUnX52aw7lZMIrQOTwe25VyrXIsSGDa3a+pyWHiWcRuAIAIP68rfFEYLhYf
    MMqBkh6f9QvipntvSYpuciS5xF9biQEVAwUQNnhHnTuFIe3ySu75AQH4NAf9GSYF
    T+rrPJhKHKnRT0qbnfwhgCGy6nQyjC1fEPLfnZnwoAvW1GO7JaXa516RbFkrrvHN
    vUeatXkRM3m94MSRdTfxabdgHlySbIkzGtCN0LaUI+it304UdheqP9cHbeQReMhf
    SmX0iEEbW+uUsfjv3+C2DiuHVb/xbql+Kacd+jf03OpRYRZg/lM7+WVJPhIg869Z
    WTeGc7THYVshQ8I/Ea9+O/PhqdZamHyG2bdpZVN24v6y/ULHrTTWZ4fUeybHNQzL
    bdJ2gpE58V+nbdcL7qkAU8fiHrTQwTWqp5tT1YBWUmFQKk/ETxQb1YEHnEIaPiKx
    p4FT/BTu0xj5D+72/4kAlQMFEDZ4N0EEz4FNUUxSeQEB6gQD/RqBgIU/BiVNUe/7
    iKOUxATGhetqm82FbOhSRuoeqZjL6NV+CfLzTzF17ngXPopQ4B7Nf0vKzEhkw6S4
    OqJ6PMOg/PG0dEbtTWFQL4BhUipkrCB+VfXnD8BbKz3cmUFgzTHdj/Rut3GTNjlL
    7gWZTFAiBtkNvSaeRl40S4+UG4ys
    =ejCq
    -----END PGP PUBLIC KEY BLOCK-----
    
