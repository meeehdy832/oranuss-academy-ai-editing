// Paste into the built-in browser's JavaScript tool while on https://www.pexels.com (any page).
// 1) Set the queries, 2) run, 3) a few seconds later read window.__res (it fills in the background,
//    so the 45 s tool limit is never hit). Returns landscape photo IDs and 1920×1080 HD clip URLs.
//    window.__Q = { photos: { name: "query", ... }, videos: { v_name: "query", ... } };
window.pxv = async (q, n = 3) => { const t = await (await fetch('/search/videos/' + encodeURIComponent(q) + '/?orientation=landscape')).text();
  const urls = [...new Set(t.match(/https:\/\/videos\.pexels\.com\/video-files\/\d+\/\d+-hd_1920_1080_\d+fps\.mp4/g) || [])]; const by = {};
  for (const u of urls) { const id = u.match(/files\/(\d+)\//)[1]; by[id] = by[id] || u; } return Object.values(by).slice(0, n); };
window.pxp = async (q, n = 3) => { const t = await (await fetch('/search/' + encodeURIComponent(q) + '/?orientation=landscape')).text();
  return [...new Set((t.match(/images\.pexels\.com\/photos\/(\d+)\//g) || []).map(x => x.match(/(\d+)/)[1]))].slice(0, n); };
window.__res = { photos: {}, videos: {}, done: false };
(async () => { const Q = window.__Q || { photos: {}, videos: {} }; await Promise.all([
  (async () => { for (const [k, q] of Object.entries(Q.photos || {})) { try { __res.photos[k] = await pxp(q); } catch (e) { __res.photos[k] = []; } } })(),
  (async () => { for (const [k, q] of Object.entries(Q.videos || {})) { try { __res.videos[k] = await pxv(q); } catch (e) { __res.videos[k] = []; } } })()]);
  __res.done = true; })();
'started';
// Then: for (let i=0;i<40&&!__res.done;i++) await new Promise(r=>setTimeout(r,1000)); JSON.stringify(__res)
// Save that JSON as WORKDIR/media_candidates.json; fetch_media.py takes the first candidate of each.
