// Case-page motion for .ai (field notes index + detail, evidence intelligence, work with us).
// Homepage motion stays in motion-home.js. Progressive enhancement:
//  - .js-motion is added ONLY inside gsap.matchMedia("(prefers-reduced-motion: no-preference)")
//  - ?done=1 skips everything (no .js-motion, content fully visible)
//  - missing gsap/ScrollTrigger or empty selectors fail silently and leave content visible
(() => {
  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  if (new URLSearchParams(location.search).get("done") === "1") return;

  // [selector, stagger (s), y (px)] — headers animate as one group; list items animate as each enters view.
  const HEADS = [[".lede > *", 0.09, 16], [".article-head > *", 0.09, 16]];
  const LISTS = [[".note-card", 0.1, 18], [".evidence-row", 0.1, 18], [".door-link", 0.1, 14],
    [".source-list a", 0.06, 12], [".path article", 0.12, 18], [".samples .sample", 0.12, 18]];
  const ease = "power2.out";
  const base = (stagger, y) => ({ from: { autoAlpha: 0, y }, to: { autoAlpha: 1, y: 0, duration: 0.72, ease, stagger,
    immediateRender: false, clearProps: "transform,translate" } });

  gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
    const root = document.documentElement;
    const triggers = [], all = [];
    const list = (sel) => Array.from(document.querySelectorAll(sel));
    const heads = HEADS.map(([sel, stagger, y]) => [list(sel), stagger, y]).filter(([els]) => els.length);
    const lists = LISTS.map(([sel, stagger, y]) => [list(sel), stagger, y]).filter(([els]) => els.length);
    if (!heads.length && !lists.length) return;

    root.classList.add("js-motion");
    try {
      heads.forEach(([els, stagger, y]) => {
        const { from, to } = base(stagger, y);
        all.push(...els);
        const tween = gsap.fromTo(els, from, { ...to, scrollTrigger: { trigger: els[0].parentElement, start: "top 88%", once: true } });
        if (tween.scrollTrigger) triggers.push(tween.scrollTrigger);
      });
      lists.forEach(([els, stagger, y]) => {
        const { from, to } = base(stagger, y);
        all.push(...els);
        triggers.push(...ScrollTrigger.batch(els, { start: "top 88%", once: true,
          onEnter: (batch) => gsap.fromTo(batch, from, to) }));
      });
    } catch (error) {
      triggers.forEach((t) => t.kill());
      gsap.set(all, { clearProps: "opacity,visibility,transform,translate" });
      root.classList.remove("js-motion");
      return;
    }
    return () => {
      triggers.forEach((t) => t.kill());
      gsap.set(all, { clearProps: "opacity,visibility,transform,translate" });
      root.classList.remove("js-motion");
    };
  });
})();
