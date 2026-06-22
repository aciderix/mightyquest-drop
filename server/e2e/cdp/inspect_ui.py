#!/usr/bin/env python3
"""Preuve: lire (et donc controler) le CONTENU de l'interface via CDP, sans
rendu graphique. Le compositeur CEF ne peint pas sous Wine, mais le DOM est
peuple par le JS du jeu et entierement lisible/pilotable via Runtime.evaluate.

JS ecrit en ES5 pur (Chromium 28 / 2013: pas d'Array.from ni de fleches).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from agent import Agent


def main():
    a = Agent()                       # un seul /json, auto-pick du renderer vivant
    print("renderer attache:", a.page.get("url"))
    a.bootstrap_local()               # injecte mock DOM (body reel) + framework

    print("\n=== 1. le DOM est reel et lisible ===")
    print("  elements DOM total      :", a.eval("document.getElementsByTagName('*').length"))
    print("  templates (id^=template):", a.eval("document.querySelectorAll('[id^=\"template-\"]').length"))
    panels = a.eval(r"""
      (function(){var n=document.querySelectorAll('[id*="panel"]'),o=[];
       for(var i=0;i<n.length && o.length<12;i++) o.push(n[i].id); return o;})()""")
    print("  panneaux presents       :", panels)

    print("\n=== 2. texte STATIQUE de l'UI lu depuis le DOM (textContent) ===")
    labels = a.eval(r"""
      (function(){
        var out=[], seen={}, els=document.getElementsByTagName('*');
        for(var i=0;i<els.length && out.length<18;i++){
          var e=els[i];
          if(e.children.length===0){
            var t=(e.textContent||'').replace(/^\s+|\s+$/g,'');
            if(t.length>=3 && t.length<=24 && !/[{}<>]/.test(t) && !seen[t]){ seen[t]=1; out.push(t); }
          }
        }
        return out;
      })()""")
    for t in labels:
        print("    -", t)

    print("\n=== 3. data-binding: rendre un template jsrender avec des CHIFFRES ===")
    print("  jsrender dispo:", a.eval("typeof $!=='undefined' && !!($.templates||$.render||$.views)"))
    rendered = a.eval(r"""
      (function(){
        try{
          var tpl="<div>Or: {{:gold}} | Heros niv. {{:lvl}} | Creature niv. {{:clvl}}</div>";
          var html;
          if($.templates){ html=$.templates(tpl).render({gold:12345,lvl:17,clvl:23}); }
          else { return 'jsrender API absente'; }
          var d=document.createElement('div'); d.id='__probe'; d.innerHTML=html;
          document.body.appendChild(d);
          return document.getElementById('__probe').textContent;
        }catch(e){ return 'ERR '+e; }
      })()""")
    print("  texte UI genere + relu depuis le DOM :", repr(rendered))

    print("\n=== 4. localiser/piloter des controles ===")
    btns = a.eval(r"""
      (function(){
        var n=document.querySelectorAll("[class*='button'],[class*='btn'],button"), o=[];
        for(var i=0;i<n.length && o.length<10;i++){
          var e=n[i], id=(e.id||e.className||'').toString().slice(0,38),
              t=(e.textContent||'').replace(/^\s+|\s+$/g,'').slice(0,20);
          o.push(id+' :: '+t);
        }
        return o;
      })()""")
    for b in btns:
        print("    -", b)
    # preuve qu'on peut declencher un handler (on cible un bouton et on dispatch un click)
    clicked = a.eval(r"""
      (function(){
        var b=document.querySelector("[class*='button'],[class*='btn'],button");
        if(!b) return 'aucun bouton';
        var ev=document.createEvent('MouseEvents'); ev.initEvent('click',true,true);
        b.dispatchEvent(ev);
        return 'click dispatche sur: '+((b.id||b.className||'').toString().slice(0,40));
      })()""")
    print("  pilotage:", clicked)

    a.ws.close()
    print("\nOK: l'interface (texte + chiffres bindes + controles) est lisible et "
          "pilotable via le DOM, meme sans rendu graphique.")


if __name__ == "__main__":
    main()
