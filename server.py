"""SpeakWise Gemini web server. Standard library only."""
import json, os, urllib.request, urllib.error, mimetypes, secrets, time, threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY_FILE = ROOT / '.api_key'
MODEL = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash-lite')
ACCESS_CODE = os.environ.get('SPEAKWISE_ACCESS_CODE', '').strip()
MAX_ACTIVE = threading.BoundedSemaphore(3)
LAST_REQUEST = {}
LOCK = threading.Lock()
SYSTEM = '''You are SpeakWise, a wise, emotionally intelligent, engaging English communication tutor, not a human. Users may speak Telugu, Hindi, Urdu, English, or mix them. Preserve meaning faithfully. Be a supportive and tactful mentor with situational humor only when useful. Return a JSON object with these exact string fields: understood, natural, better, why, social_tip, reply, practice. natural is grammatically fluent English, better is diplomatically and socially smarter, why explains one language improvement, social_tip gives a practical people-skills insight, reply is a brief friendly humanlike conversational continuation (without claiming to be human), practice is one short phrase for repetition. Do not fabricate facts, ridicule, or flatter excessively. Respect the user's communication situation and level.'''

def key():
    if os.environ.get('GEMINI_API_KEY'): return os.environ['GEMINI_API_KEY'].strip()
    return KEY_FILE.read_text(encoding='utf-8').strip() if KEY_FILE.exists() else ''

class Handler(BaseHTTPRequestHandler):
    def send(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store')
        self.end_headers();self.wfile.write(data)
    def authorized(self):
        # Only a private access code permits paid AI calls on a public server.
        return bool(ACCESS_CODE) and secrets.compare_digest(self.headers.get('X-SpeakWise-Code',''), ACCESS_CODE)
    def do_GET(self):
        route=self.path.split('?')[0]
        if route=='/api/health':return self.send(200, {'ready':bool(key()) and bool(ACCESS_CODE),'model':MODEL,'protected':True})
        if route=='/': route='/static/index.html'
        allowed={'/static/index.html','/static/manifest.webmanifest','/static/icon.svg','/static/sw.js'}
        if route not in allowed:return self.send(404,{'error':'Not found'})
        file=ROOT/route.lstrip('/')
        if not file.exists():return self.send(404,{'error':'Not found'})
        data=file.read_bytes(); mime=mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
        if route.endswith('.webmanifest'):mime='application/manifest+json'
        self.send_response(200);self.send_header('Content-Type',mime+'; charset=utf-8');self.send_header('Content-Length',str(len(data)))
        self.send_header('Cache-Control','no-store' if route.endswith('index.html') else 'public, max-age=86400');self.end_headers();self.wfile.write(data)
    def do_POST(self):
        if self.path!='/api/tutor':return self.send(404,{'error':'Not found'})
        if not self.authorized(): return self.send(401, {'detail':'Incorrect access code. Use the private code you configured on Render.'})
        api_key=key()
        if not api_key:return self.send(503,{'detail':'Gemini API key missing on the server.'})
        identity = self.headers.get('X-SpeakWise-Code','')
        with LOCK:
            current=time.monotonic()
            if current-LAST_REQUEST.get(identity,0)<2:
                return self.send(429,{'detail':'Please wait a couple of seconds before trying again.'})
            LAST_REQUEST[identity]=current
        if not MAX_ACTIVE.acquire(blocking=False): return self.send(429,{'detail':'Tutor is busy. Try again shortly.'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length<1 or length>40000:return self.send(413,{'detail':'Message too large'})
            body=json.loads(self.rfile.read(length));msg=body.get('message','')
            if not isinstance(msg,str) or not 0<len(msg)<=4000:return self.send(400,{'detail':'Enter a message (up to 4000 characters).'})
            options={k:str(body.get(k,''))[:60] for k in ('language','situation','tone','level')}
            history=body.get('history',[])
            if not isinstance(history,list):history=[]
            # Gemini expects user/model turns, followed by the latest user input.
            contents=[]
            for t in history[-8:]:
                if isinstance(t,dict) and t.get('role') in ('user','assistant') and isinstance(t.get('content'),str):
                    contents.append({'role':'user' if t['role']=='user' else 'model','parts':[{'text':t['content'][:4000]}]})
            contents.append({'role':'user','parts':[{'text':msg}]})
            instruction=SYSTEM+' Learner settings: '+json.dumps(options)
            payload=json.dumps({
                'systemInstruction':{'parts':[{'text':instruction}]},
                'contents':contents,
                'generationConfig':{'temperature':0.65,'responseMimeType':'application/json'}
            }).encode('utf-8')
            from urllib.parse import quote
            model=quote(MODEL,safe='-._')
            req=urllib.request.Request(
                'https://generativelanguage.googleapis.com/v1beta/models/'+model+':generateContent',
                data=payload,
                headers={'x-goog-api-key':api_key,'Content-Type':'application/json'},method='POST')
            with urllib.request.urlopen(req,timeout=80) as response: result=json.load(response)
            chunks=result.get('candidates',[{}])[0].get('content',{}).get('parts',[])
            raw=''.join(str(x.get('text','')) for x in chunks)
            if not raw:raise ValueError('No text response returned from Gemini')
            obj=json.loads(raw); fields=['understood','natural','better','why','social_tip','reply','practice']
            return self.send(200,{k:str(obj.get(k,'')) for k in fields})
        except urllib.error.HTTPError as e:
            return self.send(502,{'detail':f'Gemini API error ({e.code}). Check that your Gemini API key and free-tier model are available. If 429, wait for quota reset.'})
        except Exception as e:
            print('Request error:',type(e).__name__,str(e)[:250]);return self.send(502,{'detail':'Unable to get a reply. Check internet connection and try again.'})
        finally:
            MAX_ACTIVE.release()
    def log_message(self, fmt, *args):
        if self.path.startswith('/api/tutor'):print('Tutor request completed')
        else:super().log_message(fmt,*args)

if __name__=='__main__':
    port=int(os.environ.get('PORT','8765'))
    print(f'SpeakWise server listening on port {port}')
    ThreadingHTTPServer(('0.0.0.0',port),Handler).serve_forever()
