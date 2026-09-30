// Include the full architecture when printing, then restore the reader's view.
let printDisclosureState;
window.addEventListener("beforeprint", () => {
  if (printDisclosureState) return;
  printDisclosureState = [...document.querySelectorAll("details")]
    .map(detail => ({ detail, open: detail.open }));
  printDisclosureState.forEach(({ detail }) => { detail.open = true; });
});
window.addEventListener("afterprint", () => {
  printDisclosureState?.forEach(({ detail, open }) => { detail.open = open; });
  printDisclosureState = undefined;
});
