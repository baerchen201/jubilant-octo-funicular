<html>
  <head>
    <title>PHP Input</title>
  </head>
  <body>
    <form action="#" method="POST">
      <input type="text" name="text" placeholder="Text input" />
<button>Submit</button>
    </form>
    <span style="color: #f00">
<?php echo $_POST["text"]; ?>
</span>
  </body>
</html>
