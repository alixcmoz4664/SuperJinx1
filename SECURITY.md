# Security

- The first login is `admin / admin`. Change it right away with the OWNER KEY printed in the Railway logs (Settings > Change password, or: API Keys > owner key, then login page > "Forgot password?"). After that the password is never reset automatically.
- The panel, the Xray core and all internal ports (8000, 10001-10005, 62050) listen on `127.0.0.1` only. The only public entry is nginx on port 8080 behind Railway's TLS.
- Every install generates its own random config paths on first boot (stored on the volume), so forks never share paths.
- The demo reseller `reseller / reseller` is created once. Change its password or delete it; it is never re-created. Set `DEMO_RESELLER=off` to skip it.
- The "Admins" menu is visible to the owner only.
- Settings > Change password needs the current username and password, is checked by the panel itself, verified after saving, and locked for 10 minutes after 5 wrong tries.
- Groups, hosts, cores, nodes and admin roles are read-only from outside (nginx blocks every change), so nobody can delete them from the dashboard or the API.
- The owner key is made by Super JinX itself: one use, 5 minutes, kept only in memory, 5 wrong tries lock it for 10 minutes. It works even with simple passwords (PasarGuard's own owner form rejects them).
- The internal node API key and TLS certificate are generated on first boot and stored on the volume.

Found a problem? Report it in the [Super JinX channel](https://t.me/+WvKFv0lU_i5lNGE0).
