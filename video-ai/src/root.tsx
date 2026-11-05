import React from 'react';
import {Audio, Img, staticFile, Composition, AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';

type Cue = {start: number; end: number; text: string};
type Props = {headline: string; detail: string; cta: string; logo?: string; audio?: string; captions?: Cue[]};

// Only local, authorized assets from public/: no remote fetches or API credentials.
const asset = (name: string) => {
  if (!/^[a-zA-Z0-9_./-]+$/.test(name) || name.startsWith('/') || name.split('/').includes('..')) {
    throw new Error('Media must be a relative path inside video-ai/public');
  }
  return staticFile(name);
};
const Promo: React.FC<Props> = ({headline, detail, cta, logo, audio, captions = []}) => {
  const frame = useCurrentFrame();
  let previousEnd = 0;
  for (const cue of captions) {
    if (!Number.isFinite(cue.start) || !Number.isFinite(cue.end) || cue.start < previousEnd ||
        cue.end <= cue.start || Math.round(cue.end * 30) <= Math.round(cue.start * 30) || cue.end > 15 || !cue.text.trim()) {
      throw new Error('Captions must be ordered, nonoverlapping and inside the 15-second timeline');
    }
    previousEnd = cue.end;
  }
  const cue = captions.find(c => frame >= Math.round(c.start * 30) && frame < Math.round(c.end * 30));
  const opacity = interpolate(frame, [0, 18], [0, 1], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{backgroundColor: '#10263d', color: '#ffffff', fontFamily: 'Arial, sans-serif', padding: 90, justifyContent: 'center', gap: 55}}>
    {audio ? <Audio src={asset(audio)}/> : null}
    {logo ? <Img src={asset(logo)} style={{width: 360, height: 150, objectFit: 'contain', objectPosition: 'left center'}}/> :
      <div style={{fontSize: 44, color: '#8dd5ed', fontWeight: 700}}>ARQUINDEX</div>}
    <div style={{fontSize: 90, fontWeight: 800, lineHeight: 1.08, opacity}}>{headline}</div>
    <div style={{fontSize: 48, lineHeight: 1.3}}>{detail}</div>
    <div style={{fontSize: 48, backgroundColor: '#ffffff', color: '#10263d', padding: 32, borderRadius: 20, fontWeight: 700}}>{cta}</div>
    <div style={{fontSize: 29}}>arquindex.com.br</div>
    {cue ? <div style={{position: 'absolute', left: 90, right: 90, bottom: 260, padding: 20, borderRadius: 12,
      backgroundColor: 'rgba(0,0,0,0.85)', color: 'white', fontSize: 42, lineHeight: 1.25, textAlign: 'center'}}>{cue.text}</div> : null}
  </AbsoluteFill>;
};
export const Root: React.FC = () => <Composition id="ArquindexPromo" component={Promo} durationInFrames={450} fps={30} width={1080} height={1920}
  defaultProps={{headline: 'Digitalização de documentos', detail: 'Organização, segurança e acesso à informação.', cta: 'Solicite um orçamento'}}/>;
