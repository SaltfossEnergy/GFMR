/*
docs/javascripts/figures.js — Accessible figure viewer for GFMR geometry.

Copyright 2026 Saltfoss Energy ApS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

/* Progressive enhancement: each figure link works without JavaScript as well. */
(() => {
  const links = document.querySelectorAll("a.zoomable");
  if (!links.length || typeof HTMLDialogElement === "undefined") return;

  const dialog = document.createElement("dialog");
  dialog.className = "figure-dialog";
  dialog.setAttribute("aria-label", "Enlarged reactor geometry");

  const toolbar = document.createElement("div");
  toolbar.className = "figure-dialog__toolbar";
  const title = document.createElement("span");
  title.textContent = "GFMR / MODEL GEOMETRY";
  const close = document.createElement("button");
  close.type = "button";
  close.className = "figure-dialog__close";
  close.textContent = "Close ×";
  close.setAttribute("aria-label", "Close enlarged figure");
  const image = document.createElement("img");
  toolbar.append(title, close);
  dialog.append(toolbar, image);
  document.body.append(dialog);

  let trigger;
  links.forEach((link) => {
    link.setAttribute("aria-haspopup", "dialog");
    link.title = "Enlarge figure";
    link.addEventListener("click", (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      trigger = link;
      image.src = link.href;
      image.alt = link.querySelector("img").alt;
      dialog.showModal();
      close.focus();
    });
  });

  close.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    const box = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
  });
  dialog.addEventListener("close", () => trigger?.focus());
})();
