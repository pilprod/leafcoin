#!/usr/bin/env node
// Exercise browser preferences, explicit choices, country failures and routing.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const root=path.join(__dirname,'..');
const languageSource=fs.readFileSync(path.join(root,'language.js'),'utf8');
const regionSource=fs.readFileSync(path.join(root,'visitor-region.js'),'utf8');
const key='leafcoin.language.v1';
class Element {
  constructor(){this.events={};this.attributes={};this.children={};}
  addEventListener(event,callback){this.events[event]=callback;}
  setAttribute(key,value){this.attributes[key]=value;}
  querySelector(selector){return this.children[selector]??=new Element();}
  focus(){this.focused=true;}
  showModal(){this.open=true;}
  close(){this.open=false;}
  fire(event,value={}){this.events[event]?.({preventDefault(){},...value});}
}
function app(options={}) {
  const initial=new URL(options.url||'https://leafcoin.org/articles/what-is-aeroponics.html?utm_source=test#questions');
  const state={redirects:[],dialogs:[],lookups:0};
  const local=new Map(options.saved?[[key,options.saved]]:[]),session=new Map();
  const storage=(map,blocked=false)=>({getItem(k){if(blocked)throw Error('blocked');return map.get(k)||null;},setItem(k,v){if(blocked)throw Error('blocked');map.set(k,v);},removeItem(k){if(blocked)throw Error('blocked');map.delete(k);}});
  const link=new Element();link.href=new URL(options.target||'/es/articles/what-is-aeroponics.html',initial).href;
  const document={documentElement:{lang:options.current||'en'},querySelector:()=>link,createElement(tag){assert.equal(tag,'dialog');return new Element();},body:{appendChild(e){state.dialogs.push(e);}}};
  const location={href:initial.href,origin:initial.origin,search:initial.search,hash:initial.hash,replace(value){state.redirects.push(value);}};
  const window={localStorage:storage(local,options.blocked),sessionStorage:storage(session,options.sessionBlocked),leafcoinVisitorCountry:async()=>{state.lookups++;return options.country||null;}};
  const context=vm.createContext({window,document,location,localStorage:window.localStorage,sessionStorage:window.sessionStorage,navigator:{language:options.language||'en-US',languages:options.languages},URL});
  vm.runInContext(languageSource,context);
  return {state,local,session,window,link};
}
let passed=0;
async function test(name,fn){await fn();passed++;console.log('PASS:',name);}
const flush=async()=>{for(let i=0;i<8;i++)await Promise.resolve();};
(async()=>{
  await test('Spanish primary language redirects while preserving article, query and fragment',async()=>{
    for(const language of ['es','es-AR','es-ES','ES-mx']){
      const a=app({language,country:'US'});await flush();
      assert.equal(a.state.redirects[0],'https://leafcoin.org/es/articles/what-is-aeroponics.html?utm_source=test#questions');
      assert.equal(a.state.lookups,0);assert.equal(a.local.has(key),false);
    }
    const primary=app({language:'es',languages:['en-US','es']});await flush();assert.equal(primary.state.redirects.length,0);
  });
  await test('saved English overrides Spanish preferences and geographic suggestions',async()=>{
    const a=app({saved:'en',language:'es-AR',country:'AR'});await flush();assert.equal(a.state.redirects.length,0);assert.equal(a.state.dialogs.length,0);
  });
  await test('saved Spanish opens the corresponding page independently of country',async()=>{
    const a=app({saved:'es',country:'DE'});await flush();assert.equal(a.state.redirects.length,1);assert.equal(a.state.dialogs.length,0);
  });
  await test('a Spanish URL stays accessible with English preferences',async()=>{
    const a=app({current:'es',url:'https://leafcoin.org/es/',target:'/',saved:'en',country:'AR'});await flush();assert.equal(a.state.redirects.length,0);assert.equal(a.state.lookups,0);
  });
  await test('Spanish-speaking regions offer a choice and never redirect based on country',async()=>{
    for(const country of 'AR BO CL CO CR CU DO EC ES GQ GT HN MX NI PA PE PR PY SV UY VE'.split(' ')){
      const a=app({country});await flush();assert.equal(a.state.dialogs.length,1,country);assert.equal(a.state.redirects.length,0);assert.equal(a.local.has(key),false);
      assert.equal(a.state.dialogs[0].attributes['aria-labelledby'],'language-dialog-title');
    }
  });
  await test('acceptance persists Spanish; keep-English and Escape persist English',async()=>{
    const a=app({country:'AR'});await flush();a.state.dialogs[0].querySelector('[data-language-accept]').fire('click');assert.equal(a.local.get(key),'es');assert.equal(a.state.redirects.length,1);
    for(const event of ['click','cancel']){
      const b=app({country:'ES'});await flush();
      if(event==='click')b.state.dialogs[0].querySelector('[data-language-stay]').fire(event);else b.state.dialogs[0].fire(event);
      assert.equal(b.local.get(key),'en');assert.equal(b.state.redirects.length,0);assert.equal(b.state.dialogs[0].open,false);
    }
  });
  await test('unknown and other countries leave English in place without prompting',async()=>{
    for(const country of [null,'XX','US','BR','FR']){
      const a=app({country});await flush();assert.equal(a.state.dialogs.length,0);assert.equal(a.state.redirects.length,0);
    }
  });
  await test('manual language link saves the choice and retains the same page',async()=>{
    const a=app();await flush();a.link.fire('click');assert.equal(a.local.get(key),'es');assert.equal(a.state.redirects.length,1);
    const b=app({current:'es',target:'/articles/what-is-aeroponics.html'});b.link.fire('click');assert.equal(b.local.get(key),'en');assert.equal(b.state.redirects[0],'https://leafcoin.org/articles/what-is-aeroponics.html?utm_source=test#questions');
    const c=app();c.link.fire('click',{ctrlKey:true});assert.equal(c.local.get(key),'es');assert.equal(c.state.redirects.length,0);
  });
  await test('blocked storage falls back to the visit without breaking language navigation',async()=>{
    const a=app({blocked:true});a.link.fire('click');assert.equal(a.session.get(key),'es');assert.equal(a.state.redirects.length,1);
    const b=app({blocked:true,sessionBlocked:true});b.link.fire('click');assert.equal(b.state.redirects.length,1);
  });
  await test('the shared lookup fetches once and discards IP and malformed traces',async()=>{
    for(const [text,type,expected] of [['ip=192.0.2.1\nloc=AR\n','text/plain','AR'],['loc=AR\nloc=ES\n','text/plain',null],['loc=AR\n','text/html',null],['x'.repeat(4097),'text/plain',null],['loc=ARX\n','text/plain',null]]){
      let calls=0;const window={};const timers=new Map();let timer=0;
      const context=vm.createContext({window,location:{origin:'https://leafcoin.org'},AbortController,setTimeout(fn){timers.set(++timer,fn);return timer;},clearTimeout(id){timers.delete(id);},fetch:async(url,options)=>{calls++;assert.equal(url,'/cdn-cgi/trace');assert.equal(options.credentials,'omit');return {ok:true,headers:{get:()=>type},text:async()=>text};}});
      vm.runInContext(regionSource,context);
      assert.equal(await window.leafcoinVisitorCountry(),expected);assert.equal(await window.leafcoinVisitorCountry(),expected);assert.equal(calls,1);assert.equal(timers.size,0);
    }
  });
  await test('shared lookup stays unknown for network failures and local previews',async()=>{
    for(const origin of ['https://leafcoin.org','http://127.0.0.1:8768']){
      const window={};const context=vm.createContext({window,location:{origin},AbortController,setTimeout:()=>1,clearTimeout(){},fetch:async()=>{throw Error('network unavailable');}});
      vm.runInContext(regionSource,context);assert.equal(await window.leafcoinVisitorCountry(),null);
    }
  });
  console.log(`Passed ${passed} language and shared-region checks.`);
})().catch(error=>{console.error(error);process.exitCode=1;});
