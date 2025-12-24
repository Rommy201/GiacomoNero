# 🎰 Giacomo Nero - App Android per Contare le Carte a Blackjack

App mobile per Android che aiuta a contare le carte al Blackjack usando la strategia Hi-Lo.

## 📱 Scarica l'APK

Vai su **Actions** → Clicca sull'ultima build → Scarica l'artifact **giacomo-nero-apk**

## 🚀 Come Compilare Automaticamente

1. Fai push dei file su GitHub
2. GitHub Actions compila automaticamente l'APK
3. Scarica l'APK dalla sezione Actions

## 📦 File del Progetto

- `main_kivy.py` - App principale per Android
- `card_counter.py` - Logica conteggio carte
- `strategy.py` - Strategia di gioco
- `buildozer.spec` - Configurazione build Android

## ⚙️ Compilazione Manuale (Opzionale)

Se vuoi compilare localmente su Linux:

```bash
sudo apt-get install -y openjdk-17-jdk build-essential
pip install buildozer
buildozer -v android debug
```

L'APK sarà in `bin/`

## 📄 Licenza

Progetto personale per uso educativo.
