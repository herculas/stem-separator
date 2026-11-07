# PolyU remote execution policy

## SSH boundary

Use the existing VPS SSH configuration and trusted host keys. The VPS repo's
local Git config contains `stemseparator.sshHost` and `stemseparator.remoteRoot`.
Run this bounded connectivity check from the VPS checkout when needed.

```bash
polyu_host=$(git config --local --get stemseparator.sshHost) &&
ssh -T -F "$HOME/.ssh/config" -o BatchMode=yes -o StrictHostKeyChecking=yes \
  -o UpdateHostKeys=no -o ForwardAgent=no -- "$polyu_host" 'hostname; id -un'
```

Preserve the tunnel, SSH identity, host key records, authorized keys, account
permissions, system services, and local sandbox settings. Stop on a host key
failure and have the administrator verify it through a trusted channel. Keep
authentication material and sensitive environment data out of commands, logs,
and the repository. The remote account's permissions apply on PolyU. The VPS
workspace sandbox applies on the VPS.

## Authorization and preservation

1. Start with bounded read-only investigation. Check the host and account,
   actual checkout, mount, symlinks, pending Git state, and relevant capacity.
2. For writes, identify exact absolute paths, auxiliary writes, scope, and
   expected outcome. Work within explicit user authorization. Confirm scope
   changes separately. Directory placement and read access authorize no writes.
3. Inspect entry points, imports, subprocesses, loader behavior, caches,
   bytecode, temp files, and log redirects. Reject unexpected symlinks, same-name
   outputs, ambiguous ownership, and unexpected writes. Preserve partials and
   protect original audio, accepted runs, models, and archives.
4. Recursive deletion, bulk overwrite, forced resets, `git clean`, destructive
   `rsync`, database changes, `sudo`, permissions, and system or SSH changes
   require authorization for the specific operation.

## Execution and network acquisition

Use the absolute project interpreter and an approved run location. Record the
commands, inputs, code identity, outputs, and exit status. Before a long run,
identify the process, log location, progress check, and targeted stop method.
Use the [run closeout procedure](execution-and-storage-policy.md#run-and-archive)
to verify completion. Leave GPU thermal management to the driver and hardware.

Verify package or model sources, expected bytes and available space, and each
redirect destination before fetching. Restrict acquisitions to approved public
endpoints. The configured SSH endpoint is reserved for SSH control. Use a bounded
retry and storage budget, and a small approved pilot before any bulk transfer.
Check hashes against trusted records where available. Preserve partials and
failures until their disposition is authorized.
