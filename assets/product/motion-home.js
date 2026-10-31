// Lab homepage motion. si-motion.js is not loaded here. Never pre-hide via .shell[style].
gsap.registerPlugin(ScrollTrigger);
const q = new URLSearchParams(location.search);
const done = q.get("done") === "1";
const SCROLL = [
  ["#research", "#research h2, #research .research-lede", 0.1, 18],
  ["#research .research-story", "#research .research-story", 0.12, 20],
  ["#lab", "#lab .shell.intro", 0, 12],
  [".principles", ".principles h2", 0, 18],
  [".principles .principle-list", ".principles .principle", 0.14, 20],
  ["section.shell.cross", "section.shell.cross", 0, 0, 1],
  ["aside.nodi-cameo", "aside.nodi-cameo", 0, 8, 0.9],
];
gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
  if (done) return;
  document.documentElement.classList.add("js-motion");
  const ease = "power2.out";
  gsap.fromTo(".hero-copy > *, .hero .scroll-cue", { autoAlpha: 0, y: 16 }, { autoAlpha: 1, y: 0, duration: 0.7, stagger: 0.09, ease });
  SCROLL.forEach(([trigger, targets, stagger, y, alpha = 1]) =>
    gsap.fromTo(targets, { autoAlpha: 0, y }, { autoAlpha: alpha, y: 0, duration: 0.75, ease, stagger,
      immediateRender: false, scrollTrigger: { trigger, start: "top 88%", once: true } }));
  return () => { ScrollTrigger.getAll().forEach((t) => t.kill()); document.documentElement.classList.remove("js-motion"); };
});
