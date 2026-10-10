# برومت: صف الأوراق المقوّس

انسخ هذا النص وحطه في Claude Code داخل Visual Studio Code، وخل مجلد `cards/` (صور الأوراق) في نفس المشروع.

## المطلوب
ابي الأوراق اللي في يد اللاعب تطلع على شكل مروحة مقوّسة:
1. الأوراق متراكبة من اليسار لليمين، وكل ورقة فوق اللي على يسارها، والورقة اللي على اليمين فوق الكل.
2. كل ورقة مايلة شوي: الأوراق اللي على اليسار مايلة لليسار واللي على اليمين لليمين، والنص مستقيم.
3. قوس خفيف: الأوراق اللي في النص أعلى من اللي على الأطراف.
4. التراكب يتعدل تلقائياً حسب عرض الشاشة وعدد الأوراق (من ٥ لين ١٣ ورقة) بحيث ما تطلع ولا ورقة برا الشاشة على الجوال.
5. الورقة المختارة ترتفع ٢٦ بكسل ويصير حولها توهج ذهبي، والأوراق اللي ما تنلعب الحين تكون باهتة.
6. شريط الرسائل والأزرار فوق الأوراق دايماً (z-index أعلى) عشان ما تغطيه الأوراق المرتفعة.
7. صور الأوراق من مجلد `cards/`: الاسم = الرقم + النوع، مثل `KS.webp` و`10D.webp` و`AH.webp` (S سبيت، H حاس، D ديمن، C كلفس). الجوكر: `joker-color.png` (الجيكر) و`joker-bw.png` (الميكر). نسبة الورقة ١٠٠ عرض × ١٤٥ طول.

استخدم هذا الكود كما هو، واربطه مع منطق اللعبة الموجود عندي (وش الأوراق اللي في اليد، والمختارة، واللي تنلعب):

```
<!-- HTML: put this where the player's hand goes -->
<div id="bar"></div>   <!-- hints / buttons: always above the cards -->
<div id="hand"></div>

/* CSS */
:root { --cw: clamp(64px, 22vw, 118px); }          /* card width; height = width x 1.45 */
.me   { min-width: 0; }                            /* the hand's parent must not grow wider than the screen */
#bar  { position: relative; z-index: 5; padding-bottom: 22px; }
#hand { height: calc(var(--cw) * 1.45 + 26px); display: flex; justify-content: center;
        align-items: flex-end; direction: ltr; padding-bottom: 4px; }
.card { width: var(--cw); aspect-ratio: 100 / 145; padding: 0; border: 0; background: none;
        cursor: pointer; position: relative; transform-origin: 50% 100%;
        transition: transform .18s, filter .18s; filter: drop-shadow(0 4px 6px rgba(0,0,0,.45)); }
.card + .card { margin-left: calc(var(--cw) * var(--ov, -0.5)); }  /* each card overlaps the one on its left */
.card.sel { filter: drop-shadow(0 0 8px #e9bd62) drop-shadow(0 6px 8px rgba(0,0,0,.5)); }
.card.dim .pc { filter: brightness(.6) saturate(.6); }               /* cards that cannot be played now */
.pc { display: block; width: 100%; height: 100%; background: #fff; border: 1px solid #cfc8b6;
      border-radius: 8% / 5.5%; padding: 3.2% 3.6%; overflow: hidden; }
.pc img { width: 100%; height: 100%; display: block; object-fit: contain; pointer-events: none; }
.pc.jk { padding: 0; }  .pc.jk img { object-fit: cover; }

// JS
const RN = {1:'A', 11:'J', 12:'Q', 13:'K', 14:'A'};
const cardSrc = c => c.s === 'X' ? (c.r === 15 ? 'cards/joker-color.png' : 'cards/joker-bw.png')
                                 : `cards/${RN[c.r] || c.r}${c.s}.webp`;     // e.g. cards/KS.webp, cards/10D.webp
const cardHTML = c => `<span class="pc${c.s === 'X' ? ' jk' : ''}"><img src="${cardSrc(c)}" alt=""></span>`;

// hand = array of {s:'S'|'H'|'D'|'C'|'X', r:2..14 (15 = colour joker, 16 = black-and-white joker)}
// selected(c) / playable(c) come from your game
function drawHand(hand, selected = () => false, playable = () => true) {
  const n = hand.length, el = document.getElementById('hand');
  el.innerHTML = hand.map((c, k) => {
    const off  = k - (n - 1) / 2;                                    // position from the centre
    const ang  = off * (n > 9 ? 2.4 : n > 6 ? 3.4 : 4.5);            // small tilt per card
    const sel  = selected(c);
    const lift = (off * off - ((n - 1) / 2) ** 2) * (n > 9 ? .7 : 2.4) + (sel ? -26 : 0); // arc: middle up, edges down
    return `<button class="card${sel ? ' sel' : ''}${playable(c) ? '' : ' dim'}" data-k="${k}"
              style="transform:translateY(${lift}px) rotate(${ang}deg)">${cardHTML(c)}</button>`;
  }).join('');
  fitHand();
}
// overlap just enough that every card fits the screen, leaving room for the tilted outer cards
function fitHand() {
  const el = document.getElementById('hand'), first = el.querySelector('.card'), n = el.children.length;
  if (!first || n < 2) return;
  const cw = first.offsetWidth, room = el.clientWidth - cw * .5;
  const step = Math.min(cw * .5, (room - cw) / (n - 1));
  el.style.setProperty('--ov', (step / cw - 1).toFixed(3));
}
addEventListener('resize', fitHand);
```

## بعد ما تخلص تأكد من
- على شاشة عرضها ٣٩٠ بكسل، ١٣ ورقة كلها تبان داخل الشاشة بدون سكرول جانبي.
- الضغط على الجزء الظاهر من أي ورقة يختار هذي الورقة نفسها.
- زر «مرّر» أو أي زر في الشريط ينضغط حتى لو فيه أوراق مرفوعة.
