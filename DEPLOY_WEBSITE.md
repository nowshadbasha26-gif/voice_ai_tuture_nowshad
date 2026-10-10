# Publish SpeakWise as an Android-accessible website (Render + GitHub)

This is a private-code-protected website starter. **It is not yet hosted:** your Render account supplies the actual `https://...onrender.com` link once deployed. You do not need Termux on your phone.

## 1. Set up GitHub
1. On your computer, unzip this project. Open the `SpeakWise_Android` folder (the one containing `server.py` and `render.yaml`).
2. Create a new **private** repository at https://github.com/new (example: `speakwise-private`).
3. In the repository, choose **uploading an existing file**. Upload the contents of `SpeakWise_Android` (not the ZIP itself), including the `static/` folder. Commit.
4. **Never upload your OpenAI API key or `.api_key` file.**

## 2. Deploy to Render
1. Go to https://dashboard.render.com/ and create/sign into a Render account.
2. Choose **New > Blueprint**, connect your GitHub account and choose your SpeakWise repository. Render reads `render.yaml`.
3. Set the two environment variables when asked:
   - `OPENAI_API_KEY`: your secret OpenAI API key from https://platform.openai.com/api-keys (requires API billing/credits).
   - `SPEAKWISE_ACCESS_CODE`: choose a strong, *different* private password (e.g. 20+ random characters). Do not post it publicly or put it in code.
4. Deploy and wait for the status to become Live. The dashboard shows the `https://speakwise-....onrender.com` address. Copy the **actual** URL from your dashboard (do not guess it).
5. Open that HTTPS address in **Chrome on Android**, enter your private access code when prompted, and allow microphone access.
6. In Chrome's three-dot menu use **Add to Home screen** / **Install app** if available.

## Notes
- Render free instances can go idle, and startup can take a while. Free plan availability and limits may change: confirm during signup.
- The browser speech recognition feature depends on Chrome/Android support for the chosen Telugu, Hindi, Urdu or English language. Microphone input is not guaranteed on all phones; typing works.
- Spoken replies use your phone's speech synthesizer/installed voice, not real-time streaming AI voice. It is turn-based, not continuous hands-free conversation.
- The app's daily counters are stored in that browser only. Your conversation text is transmitted to OpenAI for processing.
- Anyone who obtains your access code can make billable API requests. Use a strong code, keep it private and monitor API usage/budgets.
- This is suitable for a private pilot, not a production multi-user app. For public use add sign-in, per-user accounts, proper quotas, and server-side rate limiting with shared storage.
- Do not use the old Termux `start_android.sh` for the hosted version. Render starts `python server.py` automatically.
