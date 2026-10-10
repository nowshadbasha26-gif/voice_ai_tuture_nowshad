# SpeakWise Android — phone-only installation

This is an Android-friendly **web app / PWA**, not an APK. It runs locally on Android using **Termux** and opens in Chrome. A Windows computer, cloud hosting, and Python libraries are not required.

## Install (Android)

1. Install **Termux** from the official F-Droid repository or Termux GitHub releases. Do not use the outdated Google Play copy if it causes errors.
2. Download `SpeakWise_Android.zip` onto your phone and extract it into the Downloads folder so you have a folder named `SpeakWise_Android`.
3. Start Termux and grant it access to your Downloads folder:
   ```sh
   termux-setup-storage
   ```
   Tap **Allow** on the Android permission dialog.
4. In Termux run (one line at a time):
   ```sh
   pkg update -y
   pkg install -y python unzip
   cd ~
   cp /sdcard/Download/SpeakWise_Android.zip .
   unzip -o SpeakWise_Android.zip
   cd SpeakWise_Android
   bash start_android.sh
   ```
   If the zip is only available inside an extracted `SpeakWise_Android` folder, skip the copy and unzip steps and run `cp -r /sdcard/Download/SpeakWise_Android ~` before `cd`.
5. At the prompt paste your **OpenAI API key**. The key is hidden during entry and saved as a permission-restricted file in Termux. API usage is billed separately from ChatGPT subscriptions.
6. Open **Chrome on that phone** and visit **http://127.0.0.1:8765**. This local address is a secure-context exception for browser mic access (subject to Android Chrome support and permissions).
7. In Chrome, menu `⋮` > **Add to Home screen** > **Install app** or **Add** (exact label varies). Use the SpeakWise icon to open it.
8. Keep Termux running in the background while practising. For another day: in Termux run `cd ~/SpeakWise_Android && bash start_android.sh`. Android battery optimization may stop Termux in the background.

## How to talk to SpeakWise

- Select Telugu, Hindi, Urdu, or English as your **speech recognition language**.
- Tap **Speak**, grant microphone permission and talk. Mixed speech may be misrecognized; edit the transcription before sending, or use the keyboard mic (Gboard may work better for code switching).
- Turn on **Send automatically after speaking** for hands-friendlier turn-by-turn conversation; **Automatically speak tutor replies** plays each AI reply aloud through Android's text-to-speech engine.
- Tap **Give me today’s speaking exercise** for interactive daily coaching.
- Practice counts are stored in the browser locally. Clearing Chrome website data may erase counts.

## Troubleshooting

- Browser shows `ERR_CONNECTION_REFUSED`: go back to Termux; run the startup command, and leave Termux open.
- Microphone blocked: Chrome Settings > Site settings > Microphone; allow it. Recognition capability varies across languages and Android versions; try Gboard voice typing.
- Tutor reports API error: check internet, API credits/billing, and the key. To replace key in Termux: `cd ~/SpeakWise_Android && rm .api_key && bash start_android.sh`.
- Not accessible from a different device: deliberate security choice. Server binds to `127.0.0.1` only.
- You need an internet connection for OpenAI replies, and for browser speech recognition on many devices.
- This is **not** fully continuous simultaneous voice chat nor phoneme-level pronunciation scoring; it records one utterance, coaches you, and speaks back.
