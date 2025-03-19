// ==UserScript==
// @name         Green Roblox Play Button
// @namespace    https://baerchen201.github.io/
// @version      2025-03-19
// @description  Brings back the old green play button on roblox
// @author       baer1
// @match        https://*.roblox.com/games/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=roblox.com
// @grant        none
// ==/UserScript==

(function () {
  "use strict";

  let style = new CSSStyleSheet();
  style.insertRule(
    `.btn-common-play-game-lg {background-color: #00b06f !important;}`,
  );
  document.adoptedStyleSheets.push(style);

  console.log("Play button greenified", style);
})();
