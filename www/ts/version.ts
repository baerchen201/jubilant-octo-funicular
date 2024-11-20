let date_element: HTMLDivElement = document.getElementById(
  "date"
) as HTMLDivElement;
if (date_element.innerHTML)
  date_element.innerHTML = new Date(date_element.innerHTML).toLocaleString();
