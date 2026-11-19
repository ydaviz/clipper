# Clipper – Einrichtung (ca. 10 Minuten, kostenlos)

1. Auf GitHub ein **öffentliches** Repository anlegen, z. B. `clipper`.
2. Den Inhalt dieses Ordners hochladen (inkl. des versteckten Ordners `.github`). Der Standard-Branch muss `main` heißen.
3. Repository → **Settings → Pages**: Source „Deploy from a branch", Branch `main`, Ordner `/ (root)`. Danach ist die Seite unter `https://DEINNAME.github.io/clipper/` erreichbar.
4. Repository → **Settings → Actions → General → Workflow permissions**: „Read and write permissions" aktivieren.
5. GitHub → Settings → Developer settings → **Fine-grained personal access tokens**: Token nur für dieses Repository, Berechtigung **Actions: Read and write**.
6. Seite öffnen, unter „Verbindung zu GitHub" Repository (`DEINNAME/clipper`) und Token eintragen, Stream-Link einfügen, „Clips erstellen".

Hinweise
- Funktioniert mit Videos von bereits beendeten Streams (Twitch-VODs, YouTube).
- Auswahl der Momente: Lautstärke-Spitzen im Vergleich zur normalen Stimmung des Streams.
- „Auf X teilen" öffnet den Beitrags-Editor mit Link. Das Video selbst lädst du herunter und hängst es in X an.
