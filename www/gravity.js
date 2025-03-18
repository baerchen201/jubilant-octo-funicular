// All underlying scripts extracted from https://mrdoob.com/projects/chromeexperiments/google-gravity/

window.addEventListener("load", async () => {
  console.info("gravity.js loading...");
  let _load = new Date();

  await new Promise((resolve, reject) => {
    let e = document.createElement("link");
    e.rel = "stylesheet";
    console.log((e.href = "gravity.css"), "=>", e);
    e.addEventListener("load", () => resolve());
    document.body.appendChild(e);
  });

  for (let src of ["gravity_1.js", "gravity_physics.js", "gravity_apply.js"])
    await new Promise((resolve, reject) => {
      let e = document.createElement("script");
      console.log((e.src = src), "=>", e);
      e.addEventListener("load", () => resolve());
      document.body.appendChild(e);
    });

  let _loaded = new Date();
  console.info(
    "gravity.js loaded",
    `in ${_loaded - _load >= 1000 ? `${Math.floor((_loaded - _load) / 1000)}s ` : ""}${(_loaded - _load) % 1000 > 0 ? `${(_loaded - _load) % 1000}ms` : ""}`,
  );
});
