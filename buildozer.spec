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

# Pattern di inclusione specifici per assicurarsi che tutti i file Python siano inclusi
source.include_patterns = *.py,card_counter.py,strategy.py

# Versione
version = 1.0

# Requisiti Python (versioni automatiche per massima compatibilità)
requirements = python3,kivy==2.2.1

# Orientamento (portrait = verticale, landscape = orizzontale)
orientation = portrait

# Permessi Android (aggiungi WRITE_EXTERNAL_STORAGE per sicurezza)
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

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
