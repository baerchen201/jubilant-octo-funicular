import * as useragent from "useragent";
(document.querySelector("button") as HTMLButtonElement).addEventListener(
  "click",
  () => {
    let browser: useragent.Agent = useragent.parse(navigator.userAgent);
    window.alert(`Hello, ${browser.family} ${browser.major}.${browser.minor}!`);
  }
);
