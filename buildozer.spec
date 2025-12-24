[app]

# Nome dell'app
title = Giacomo Nero

# Nome del package (formato: com.dominio.nomeapp)
package.name = giacomonero

# Dominio del package
package.domain = com.blackjack

# Directory sorgente
source.dir = .

# Main file (IMPORTANTE: usa main_kivy.py per Android!)
source.main = main_kivy.py

# Estensioni da includere
source.include_exts = py,png,jpg,kv,atlas

# Versione
version = 1.0

# Requisiti Python (versioni automatiche per massima compatibilità)
requirements = python3,kivy

# Orientamento (portrait = verticale, landscape = orizzontale)
orientation = portrait

# Permessi (non necessari per questa app, ma utili)
# android.permissions = 

# Servizi
# android.permissions = INTERNET

# Icona (opzionale, puoi aggiungere un'icona)
# icon.filename = %(source.dir)s/icon.png

# Splash screen (opzionale)
# presplash.filename = %(source.dir)s/presplash.png

# Android API (versioni più stabili e compatibili)
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Colore del tema
android.presplash_color = #0f1419

# Abilita fullscreen
fullscreen = 0

[buildozer]

# Log level
log_level = 2

# Disabilita ccache (causa problemi con NDK r25b su WSL)
no_byte_compile_python = False

# Usa versione specifica di python-for-android che funziona
p4a.branch = master
p4a.source_dir = /tmp/python-for-android

# Pulisci prima di compilare
# warn_on_root = 1
