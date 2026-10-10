# SpeakWise with Gemini free tier — Render deployment

This replaces OpenAI for text generation. The website address and interface remain the same.

1. Open https://aistudio.google.com/app/apikey and create a Gemini API key in a project eligible for the free tier. Never post the key publicly.
2. In your GitHub repository, upload/replace `server.py` and `render.yaml` from this ZIP **in the repository root** (not a nested folder). Keep the existing `static/` directory. Commit changes to your main branch.
3. In Render > speakwise-tutor > Environment, add `GEMINI_API_KEY` with your key. Keep `SPEAKWISE_ACCESS_CODE` as your private password. If you already deployed from an older Render Blueprint, check its Blueprint sync: the changed render.yaml may ask for GEMINI_API_KEY before redeployment.
4. Remove unused `OPENAI_API_KEY` after confirming you are on Gemini, and consider revoking the old OpenAI key if exposed.
5. In Render > Events/Deploys, wait for latest deploy to say Live. Open https://speakwise-tutor.onrender.com and test Improve my message.

Notes: Gemini free access depends on country, model availability, quota, and provider policies; not guaranteed. Client speech recognition and speech synthesis use supported browser features, not Gemini Live audio. AI text may be used by the provider to improve products on the free tier, so avoid private information. An HTTP 429 usually means free quota or rate limits.
