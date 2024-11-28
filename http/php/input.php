<html>
  <head>
    <title>PHP Input</title>
  </head>
  <body>
    <form action="#" method="POST">
      <input type="text" name="text" placeholder="Text input" />
      <button>Submit to server</button>
      <button type="button" onclick="document.querySelector('span').innerText=document.querySelector('input').value" >Process locally</button>
    </form>
    <span style="color: #f00"><?php echo $_POST["text"]; ?> </span>
  </body>
</html>
