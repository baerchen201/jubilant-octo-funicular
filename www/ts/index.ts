(
  (
    ((document as Document).querySelector as Function)(
      "button" as string
    ) as HTMLButtonElement
  ).addEventListener as Function
)(
  "click" as string,
  function func(event: MouseEvent): void | undefined | null {
    ((window as Window).alert as Function)(
      "Slightly over-typed TypeScript code" as string
    ) as void;
  } as Function
) as void;
