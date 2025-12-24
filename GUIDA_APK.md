# Guida per Creare l'APK Android di Giacomo Nero

## 1. Test su Desktop (già fatto ✓)

L'app Kivy funziona correttamente su Windows! Ora devi crearla per Android.

## 2. Requisiti per Creare l'APK

### Su Windows: Usa WSL (Windows Subsystem for Linux)

Buildozer funziona solo su Linux, quindi su Windows devi usare WSL:

#### Installa WSL
```powershell
wsl --install
```

Riavvia il PC e apri Ubuntu dal menu Start.

#### Dentro WSL/Ubuntu:
```bash
# Aggiorna sistema
sudo apt update
sudo apt upgrade -y

# Installa TUTTE le dipendenze necessarie (IMPORTANTE!)
sudo apt install -y python3-pip git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential ccache libltdl-dev python3-dev

# Installa Buildozer e Cython
pip3 install --user buildozer cython

# Aggiungi buildozer al PATH
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

## 3. Copia il Progetto in WSL

Da PowerShell (Windows):
```powershell
# Vai nella cartella del progetto
cd "C:\Users\loren\OneDrive\Desktop\Progetti\GiacomoNero"

# Copia tutto in WSL (nella home di Ubuntu)
wsl cp -r . ~/GiacomoNero/
```

### 3.1 Aggiornare File dopo Modifiche su Windows

#### Opzione A: Ricopiare tutto (più semplice)
```powershell
# Da PowerShell, nella cartella del progetto
cd "C:\Users\loren\OneDrive\Desktop\Progetti\GiacomoNero"
wsl rm -rf ~/GiacomoNero
wsl cp -r . ~/GiacomoNero/
```

#### Opzione B: Copiare solo i file modificati (più veloce)
```powershell
# Copia solo file specifici
wsl cp main_kivy.py ~/GiacomoNero/
wsl cp strategy.py ~/GiacomoNero/
wsl cp buildozer.spec ~/GiacomoNero/
```

#### Opzione C: Lavorare direttamente sui file WSL da Windows (consigliato!)
In Esplora Risorse, vai a:
```
\\wsl$\Ubuntu\home\<tuo-username>\GiacomoNero
```
Puoi modificare i file direttamente lì con VS Code o qualsiasi editor! Le modifiche saranno immediatamente visibili in WSL.

Oppure apri la cartella in VS Code:
```powershell
# Apri la cartella WSL direttamente in VS Code
wsl code ~/GiacomoNero
```

## 4. Compila l'APK

Dentro WSL/Ubuntu:
```bash
# Vai nella cartella
cd ~/GiacomoNero

# Prima compilazione (scarica SDK Android, ci vogliono ~30-60 minuti)
buildozer -v android debug

# Se tutto va bene, l'APK sarà in:
# ~/GiacomoNero/bin/giacomonero-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

## 5. Trasferisci l'APK sul Telefono

### Opzione A: Da WSL a Windows
```bash
# Copia l'APK in una cartella Windows accessibile
cp bin/*.apk /mnt/c/Users/loren/Desktop/
```

Poi trascina l'APK sul telefono via USB o inviatelo via email/WhatsApp.

### Opzione B: USB Debug (più tecnico)
```bash
# Abilita "Opzioni Sviluppatore" sul telefono Android
# Abilita "Debug USB"
# Collega il telefono al PC

# Installa direttamente
buildozer android deploy run
```

## 6. Installa sul Telefono

1. Copia l'APK sul telefono
2. Apri il file APK
3. Android chiederà di permettere "installazione da fonti sconosciute"
4. Permetti e installa
5. L'app "Giacomo Nero" apparirà nel drawer delle app!

## 7. Per Pubblicare sul Play Store

### Crea un APK "Release" (firmato)

```bash
# Genera una chiave per firmare l'app
keytool -genkey -v -keystore my-release-key.keystore -alias giacomonero -keyalg RSA -keysize 2048 -validity 10000

# Compila APK release
buildozer android release

# Firma l'APK
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/giacomonero-1.0-arm64-v8a_armeabi-v7a-release-unsigned.apk giacomonero

# Allinea l'APK
zipalign -v 4 bin/giacomonero-1.0-arm64-v8a_armeabi-v7a-release-unsigned.apk GiacomoNero.apk
```

### Carica sul Play Console

1. Vai su [Google Play Console](https://play.google.com/console)
2. Crea un account sviluppatore (€25 una tantum)
3. Crea una nuova app
4. Carica l'APK firmato
5. Compila le informazioni richieste (descrizione, screenshot, icona)
6. Invia per revisione

## 8. Note Importanti

### Icona dell'App
Crea un'icona 512x512 px e salvala come `icon.png` nella cartella del progetto, poi ricompila.

### Screenshot per Play Store
Avrai bisogno di:
- 2-8 screenshot del telefono
- 1 icona hi-res 512x512 px
- 1 banner (opzionale)

### Privacy Policy
Il Play Store richiede una privacy policy. Puoi crearla gratis su siti come app-privacy-policy-generator.com

## Troubleshooting

### Errore "buildozer command not found"
```bash
# Aggiungi buildozer al PATH
export PATH=$PATH:~/.local/bin
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc

# Oppure usa:
python3 -m buildozer -v android debug
```

### Errore "Command failed" con python-for-android
Questo errore è spesso causato da requirements incompatibili. Se vedi un errore con `kivymd`:
1. Apri `buildozer.spec`
2. Cambia `requirements = python3,kivy,kivymd` in `requirements = python3,kivy`
3. Pulisci e ricompila:
```bash
buildozer android clean
buildozer -v android debug
```

### Errore "C compiler cannot create executables"
Mancano i tool di compilazione. In WSL esegui:
```bash
sudo apt install -y build-essential ccache libltdl-dev python3-dev libffi-dev libssl-dev
cd ~/GiacomoNero
buildozer android clean
rm -rf .buildozer
buildozer -v android debug
```

### Errore "SDK not found"
Buildozer scarica automaticamente l'SDK Android alla prima compilazione. Sii paziente!

### Errore "NDK not found"
```bash
buildozer android clean
buildozer -v android debug
```

### L'app crasha sul telefono
Guarda i log:
```bash
buildozer android logcat
```

## Alternative più Semplici (se Buildozer è troppo complesso)

### Google Colab (online, gratis)
Puoi usare Google Colab per compilare l'APK senza installare nulla:

1. Vai su [colab.research.google.com](https://colab.research.google.com)
2. Crea un nuovo notebook
3. Esegui:

```python
!pip install buildozer cython
!apt-get install -y openjdk-17-jdk

# Carica i file del progetto
from google.colab import files
uploaded = files.upload()  # Carica main_kivy.py, card_counter.py, strategy.py, buildozer.spec

# Compila
!buildozer -v android debug

# Scarica l'APK
from google.colab import files
files.download('bin/giacomonero-1.0-arm64-v8a_armeabi-v7a-debug.apk')
```

Questo è più semplice se WSL ti sembra complicato!
