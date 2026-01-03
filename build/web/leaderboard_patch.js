// Leaderboard patch for prebuilt web (build/web)
(function(){
  const LB_KEY = 'space_shooter_lb';
  function lbLoad(){ try { return JSON.parse(localStorage.getItem(LB_KEY) || '[]'); } catch(e){ return []; } }
  function lbSave(list){ try { localStorage.setItem(LB_KEY, JSON.stringify(list)); } catch(e){} }
  function renderLB(){
    const lb = lbLoad();
    let html = '<div id="lb_patch" style="position:fixed;top:60px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,.8);padding:12px 16px;border-radius:6px;border:1px solid #fff;color:#ddd;font-family:monospace;z-index:9999;min-width:260px;text-align:left;">';
    html += '<div style="font-weight:700;text-align:center;margin-bottom:6px">LEADERBOARD</div>';
    if (lb.length){ lb.slice(0,10).forEach((s,i)=>{ html += '<div>' + (i+1) + '. ' + s + '</div>'; }); } else { html += '<div style="text-align:center">No scores yet!</div>'; }
    html += '</div>';
    var el = document.getElementById('lb_patch');
    if(!el){ el = document.createElement('div'); el.id = 'lb_patch'; document.body.appendChild(el); }
    el.innerHTML = html;
  }
  window.lbAddScore = function(score){
    if(typeof score !== 'number') return;
    var lb = lbLoad();
    lb.push(score);
    lb.sort(function(a,b){ return b-a; });
    lb = lb.slice(0,10);
    lbSave(lb);
    renderLB();
  };
  document.addEventListener('keydown', function(e){ if((e.key||'').toLowerCase()==='l'){ const el=document.getElementById('lb_patch'); if(el){ el.style.display = 'block'; renderLB(); } }});
  document.addEventListener('click', function(ev){ const t = ev.target; if(t && t.textContent && /QUIT/i.test(t.textContent)){ try { window.close(); } catch(err){ window.location.assign('about:blank'); } } }, true);
  if(!localStorage.getItem(LB_KEY)) lbSave([]);
  renderLB();
})();