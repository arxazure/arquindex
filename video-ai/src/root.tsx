import React from 'react';
import {Composition, AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';

type Props = {headline:string; detail:string; cta:string};
const Promo: React.FC<Props> = ({headline,detail,cta}) => {
  const frame=useCurrentFrame();
  const opacity=interpolate(frame,[0,18],[0,1],{extrapolateRight:'clamp'});
  return <AbsoluteFill style={{backgroundColor:'#10263d',color:'#ffffff',fontFamily:'Arial, sans-serif',padding:90,justifyContent:'center',gap:55}}>
    <div style={{fontSize:44,color:'#8dd5ed',fontWeight:700}}>ARQUINDEX</div>
    <div style={{fontSize:90,fontWeight:800,lineHeight:1.08,opacity}}>{headline}</div>
    <div style={{fontSize:48,lineHeight:1.3}}>{detail}</div>
    <div style={{fontSize:48,backgroundColor:'#ffffff',color:'#10263d',padding:32,borderRadius:20,fontWeight:700}}>{cta}</div>
    <div style={{fontSize:29}}>arquindex.com.br</div>
  </AbsoluteFill>;
};
export const Root:React.FC=()=> <Composition id="ArquindexPromo" component={Promo} durationInFrames={450} fps={30} width={1080} height={1920} defaultProps={{headline:'Digitalização de documentos',detail:'Organização, segurança e acesso à informação.',cta:'Solicite um orçamento'}}/>;
