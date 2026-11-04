# Generates compositions/suche.html for the new Teil-1 ending (deterministic pile offsets).
import sys

out = sys.argv[1]
offs = [(-14, -7), (18, 5), (-6, -3), (22, 8), (-20, -6), (8, 4), (-12, -9), (16, 6), (-4, -2), (10, 3)]
doc_icon = '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" /><path d="M14 2v4a2 2 0 0 0 2 2h4" /><path d="M10 9H8" /><path d="M16 13H8" /><path d="M16 17H8" />'
sheets = "\n".join(
    f'''    <div id="sh{k}" class="sheet" style="left: {960 - 200 + dx}px; top: {640 - 143 - 14 * (k + 1)}px; z-index: {10 + k}">
      <div class="sheet-icon"><svg width="30" height="30" viewBox="0 0 24 24">{doc_icon}</svg></div>
      <div class="sheet-line" style="top: 112px; width: {220 + (k * 37) % 80}px"></div>
      <div class="sheet-line" style="top: 144px; width: {150 + (k * 53) % 90}px"></div>
      <div class="sheet-line" style="top: 176px; width: {180 + (k * 29) % 70}px"></div>
      <div class="sheet-x"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M18 6 6 18" /><path d="m6 6 12 12" /></svg></div>
    </div>'''
    for k, (dx, _) in enumerate(offs)
)
rots = [r for _, r in offs]
years = "".join(f"<span>{y}</span>" for y in range(2019, 2027))

html = f'''<template>
  <style>
    @font-face {{
      font-family: "Ubuntu";
      font-weight: 500;
      src: url("assets/fonts/ubuntu-500.woff2") format("woff2");
    }}
    #root {{
      position: absolute;
      inset: 0;
      --teal: #107e96;
      --ink: #1e3542;
      --red: #e1474c;
    }}
    .card {{
      position: absolute;
    }}
    .sheet {{
      position: absolute;
      width: 400px;
      height: 286px;
      border-radius: 16px;
      background: #fff;
      box-shadow:
        0 16px 30px -12px rgba(30, 53, 66, 0.22),
        0 2px 6px rgba(30, 53, 66, 0.06);
    }}
    .sheet-icon {{
      position: absolute;
      left: 26px;
      top: 26px;
      width: 62px;
      height: 62px;
      border-radius: 50%;
      background: #edf1f3;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sheet-icon path {{
      fill: none;
      stroke: #9fb0ba;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    .sheet-line {{
      position: absolute;
      left: 28px;
      height: 14px;
      border-radius: 7px;
      background: #e3e9ed;
    }}
    .sheet-x {{
      position: absolute;
      right: -18px;
      top: -18px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: var(--red);
      border: 4px solid #fff;
      box-shadow: 0 4px 10px rgba(30, 53, 66, 0.2);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .sheet-x path {{
      fill: none;
      stroke: #fff;
      stroke-width: 3;
      stroke-linecap: round;
    }}
    #year {{
      position: absolute;
      left: 452px;
      top: 596px;
      width: 272px;
      height: 88px;
      border-radius: 44px;
      background: #fff;
      box-shadow:
        0 16px 30px -12px rgba(30, 53, 66, 0.2),
        0 2px 6px rgba(30, 53, 66, 0.06);
      display: flex;
      align-items: center;
      gap: 16px;
      padding-left: 34px;
      z-index: 40;
    }}
    #year path,
    #year rect {{
      fill: none;
      stroke: var(--teal);
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    #year-window {{
      height: 52px;
      overflow: hidden;
    }}
    #year-roll {{
      display: flex;
      flex-direction: column;
      font-family: "Ubuntu", sans-serif;
      font-weight: 500;
      font-size: 44px;
      line-height: 52px;
      color: var(--ink);
    }}
    #lens {{
      position: absolute;
      left: 1250px;
      top: 470px;
      width: 124px;
      height: 124px;
      border-radius: 50%;
      background: #fff;
      box-shadow:
        0 20px 36px -12px rgba(30, 53, 66, 0.3),
        0 2px 8px rgba(30, 53, 66, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 50;
    }}
    #lens path,
    #lens circle {{
      fill: none;
      stroke: var(--teal);
      stroke-width: 2.2;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
  </style>

  <div id="root" data-composition-id="suche" data-width="1920" data-height="1080">
    <!-- The three cards, cut 1:1 from frame 17.18 s of the original so the splice is seamless. -->
    <img id="c1" class="card" src="assets/cards/card1.png" style="left: 40px; top: 300px; width: 620px; height: 500px; z-index: 3" alt="" />
    <img id="c2" class="card" src="assets/cards/card2.png" style="left: 660px; top: 300px; width: 600px; height: 500px; z-index: 5" alt="" />
    <img id="c3" class="card" src="assets/cards/card3.png" style="left: 1260px; top: 300px; width: 620px; height: 500px; z-index: 4" alt="" />

{sheets}

    <div id="year">
      <svg width="40" height="40" viewBox="0 0 24 24"><path d="M8 2v4" /><path d="M16 2v4" /><rect width="18" height="18" x="3" y="4" rx="2" /><path d="M3 10h18" /></svg>
      <div id="year-window" data-layout-allow-overflow><div id="year-roll">{years}</div></div>
    </div>

    <div id="lens"><svg width="58" height="58" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></svg></div>
  </div>

  <script>
    (function () {{
      // Local clock: 0 = 17.2 s of the film. Spoken: "müssen" 17.2 · "jahrelang" 17.52 · "aufbewahrt" 18.16 ·
      // "werden" 18.88 · "und griffbereit" 19.2 / 19.44 · "sein" 20.16.
      const tl = gsap.timeline({{ paused: true }});
      const ROT = {rots};
      gsap.set(".sheet", {{ y: -760, opacity: 0, rotation: (i) => ROT[i] }});
      gsap.set(".sheet-x", {{ opacity: 0 }});
      gsap.set("#year", {{ opacity: 0, x: -24 }});
      gsap.set("#lens", {{ opacity: 0, x: 220, scale: 0.8 }});

      // "müssen jahrelang": the three cards shrink into one heap.
      [["#c1", 600, 100, -5], ["#c2", 0, 92, 3], ["#c3", -600, 96, -2]].forEach(([c, x, y, r], i) =>
        tl.to(c, {{ x, y, rotation: r, scale: 0.72, duration: 0.6, ease: "power3.inOut" }}, 0.02 + i * 0.06),
      );

      // Years pass ...
      tl.to("#year", {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out" }}, 0.35);
      for (let i = 1; i < 8; i++) tl.to("#year-roll", {{ y: -52 * i, duration: 0.16, ease: "power2.out" }}, 0.45 + i * 0.19);

      // "aufbewahrt werden": more and more paper lands on top and buries them.
      gsap.utils.toArray(".sheet").forEach((s, i) => {{
        const at = 0.55 + i * 0.1;
        tl.to(s, {{ opacity: 1, duration: 0.01 }}, at);
        tl.to(s, {{ y: 6, duration: 0.3, ease: "power2.in" }}, at);
        tl.to(s, {{ y: 0, duration: 0.14, ease: "power2.out" }}, at + 0.3);
      }});

      // "und griffbereit sein": the search starts - and keeps pulling out the wrong sheet.
      tl.to("#lens", {{ opacity: 1, x: 0, scale: 1, duration: 0.4, ease: "expo.out" }}, 1.88);
      [[-90, 40], [-180, -30], [-60, 60], [-150, 10], [-40, -20]].forEach(([x, y], i) =>
        tl.to("#lens", {{ x, y, duration: 0.26, ease: "sine.inOut" }}, 2.28 + i * 0.2),
      );
      [9, 8, 7].forEach((k, i) => {{
        const at = 2.05 + i * 0.4;
        tl.to(`#sh${{k}}`, {{ x: 480, y: -40, rotation: 9, duration: 0.3, ease: "power3.out" }}, at);
        tl.fromTo(`#sh${{k}} .sheet-x`, {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "expo.out" }}, at + 0.18);
        if (i < 2) tl.to(`#sh${{k}}`, {{ y: 320, rotation: 20, opacity: 0, duration: 0.3, ease: "power2.in" }}, at + 0.42);
      }});

      window.__timelines["suche"] = tl;
    }})();
  </script>
</template>
'''
open(out, "w").write(html)
print("wrote", out)
