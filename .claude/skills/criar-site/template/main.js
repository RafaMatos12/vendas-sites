// Interações e efeitos dos sites. Sem dependências.
// Intensidade: <body data-efeitos="sutil|medio|marcante">. prefers-reduced-motion desliga o movimento.
(() => {
  const doc = document.documentElement;
  doc.classList.add("js");
  const body = document.body;
  const nivel = body.dataset.efeitos || "medio";
  const calmo = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const toque = matchMedia("(hover: none)").matches;

  document.querySelectorAll("[data-ano]").forEach((el) => (el.textContent = new Date().getFullYear()));

  // ---- Menu mobile ----
  const botaoMenu = document.querySelector(".menu-botao");
  const menu = document.getElementById("menu");
  const fecharMenu = () => { menu.classList.remove("aberto"); botaoMenu.setAttribute("aria-expanded", "false"); body.style.overflow = ""; };
  botaoMenu?.addEventListener("click", () => {
    const abrir = !menu.classList.contains("aberto");
    menu.classList.toggle("aberto", abrir);
    botaoMenu.setAttribute("aria-expanded", String(abrir));
    body.style.overflow = abrir ? "hidden" : "";
  });
  menu?.querySelectorAll("a").forEach((a) => a.addEventListener("click", fecharMenu));

  // ---- Revelar ao rolar, em cascata dentro de cada grade ----
  document.querySelectorAll(".grade-cards, .grade-depoimentos, .grade-galeria").forEach((grade) => {
    [...grade.children].forEach((filho, i) => filho.style.setProperty("--atraso", `${Math.min(i, 8) * 0.09}s`));
  });
  const revelar = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("visivel"); revelar.unobserve(e.target); } });
  }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
  document.querySelectorAll(".revelar").forEach((el) => revelar.observe(el));

  // ---- Contadores (nota e nº de avaliações) ----
  const contar = (el) => {
    const alvo = parseFloat(el.dataset.contar);
    const casas = parseInt(el.dataset.casas || "0", 10);
    if (isNaN(alvo) || calmo) return;
    const inicio = performance.now(), dur = 1400;
    const passo = (t) => {
      const p = Math.min((t - inicio) / dur, 1);
      const v = alvo * (1 - Math.pow(1 - p, 3));
      el.textContent = v.toLocaleString("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });
      if (p < 1) requestAnimationFrame(passo);
    };
    requestAnimationFrame(passo);
  };
  const obsContador = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => { if (e.isIntersecting) { contar(e.target); obsContador.unobserve(e.target); } });
  }, { threshold: 0.6 });
  document.querySelectorAll("[data-contar]").forEach((el) => obsContador.observe(el));

  // ---- Rolagem: barra de progresso, topo que encolhe/esconde, parallax, botão do WhatsApp ----
  const topo = document.getElementById("topo");
  const progresso = document.querySelector(".progresso");
  const whats = document.querySelector(".whats-flutuante");
  const heroImg = document.querySelector(".hero-midia img");
  const hero = document.querySelector(".hero");
  let ultimoY = 0, agendado = false;
  const aoRolar = () => {
    agendado = false;
    const y = scrollY;
    const max = doc.scrollHeight - innerHeight;
    if (progresso) progresso.style.transform = `scaleX(${max > 0 ? y / max : 0})`;
    topo.classList.toggle("rolou", y > 30);
    if (!menu.classList.contains("aberto")) topo.classList.toggle("escondido", y > 400 && y > ultimoY);
    whats?.classList.toggle("visivel", y > (hero ? hero.offsetHeight * 0.5 : 300));
    if (heroImg && !calmo && nivel !== "sutil" && y < innerHeight * 1.2) {
      heroImg.style.transform = `translateY(${y * (nivel === "marcante" ? -0.12 : -0.07)}px)`;
    }
    ultimoY = y;
  };
  addEventListener("scroll", () => { if (!agendado) { agendado = true; requestAnimationFrame(aoRolar); } }, { passive: true });
  aoRolar();

  // Balão "Fale com a gente" aparece uma vez, alguns segundos após o botão surgir.
  if (whats) setTimeout(() => {
    whats.classList.add("balao");
    setTimeout(() => whats.classList.remove("balao"), 6000);
  }, 7000);

  // ---- Link ativo no menu conforme a seção na tela ----
  const links = new Map([...document.querySelectorAll('.menu a[href^="#"]')].map((a) => [a.getAttribute("href").slice(1), a]));
  const obsSecao = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (e.isIntersecting) { links.forEach((a) => a.classList.remove("ativo")); links.get(e.target.id)?.classList.add("ativo"); }
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  document.querySelectorAll("section[id]").forEach((s) => obsSecao.observe(s));

  // ---- Inclinação 3D leve nos cards (só com mouse) ----
  if (!calmo && !toque && nivel !== "sutil") {
    const forca = nivel === "marcante" ? 8 : 4;
    document.querySelectorAll(".card").forEach((card) => {
      card.addEventListener("mousemove", (ev) => {
        const r = card.getBoundingClientRect();
        const x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(800px) rotateY(${x * forca}deg) rotateX(${-y * forca}deg) translateY(-6px)`;
      });
      card.addEventListener("mouseleave", () => (card.style.transform = ""));
    });
  }

  // ---- Lightbox da galeria ----
  const caixa = document.querySelector(".lightbox");
  if (caixa) {
    const img = caixa.querySelector("img");
    const fechar = () => { caixa.hidden = true; body.style.overflow = ""; };
    document.querySelectorAll(".grade-galeria img").forEach((f) => f.addEventListener("click", () => {
      img.src = f.currentSrc || f.src; img.alt = f.alt; caixa.hidden = false; body.style.overflow = "hidden";
    }));
    caixa.addEventListener("click", (ev) => { if (ev.target !== img) fechar(); });
    addEventListener("keydown", (ev) => { if (ev.key === "Escape" && !caixa.hidden) fechar(); });
  }
})();
