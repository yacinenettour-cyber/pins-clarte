import json,wave,difflib,re,sys,numpy as np, sherpa_onnx
from piper import PiperVoice, SynthesisConfig
D='asr/sherpa-onnx-whisper-small/'
rec=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=D+'small-encoder.int8.onnx',decoder=D+'small-decoder.int8.onnx',tokens=D+'small-tokens.txt',language='fr',task='transcribe',num_threads=4)
m='voix/vits-piper-fr_FR-siwis-medium/fr_FR-siwis-medium.onnx'
v=PiperVoice.load(m,config_path=m+'.json');cfg=SynthesisConfig(length_scale=1.32,noise_scale=0.55,noise_w_scale=0.7)
cues=[c['texte'] for c in json.load(open('timeline.json'))['cues'] if len(c['texte'])>12]
norm=lambda s:re.sub(r'[^a-zàâçéèêëîïôûùüœ ]','',s.lower().replace("’","'").replace("'"," ")).split()
tot=[]
for t in cues:
    with wave.open('_v.wav','wb') as w: v.synthesize_wav(t,w,syn_config=cfg)
    with wave.open('_v.wav') as w: sr=w.getframerate(); a=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    s=rec.create_stream(); s.accept_waveform(sr,a); rec.decode_stream(s); r=s.result.text.strip()
    q=difflib.SequenceMatcher(None,norm(t),norm(r)).ratio(); tot.append(q)
    if q<0.9: print(round(q,2),'|',t,'|',r)
print('moyenne',round(sum(tot)/len(tot),3),'sur',len(tot))
