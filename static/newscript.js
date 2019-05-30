function myFunction() {
  var txt;
  var title = prompt("Please enter question title:");
  var message = prompt("Please enter your question:");
  if (title == null || title == "" && message == null || message == "") {
    txt = "User cancelled the prompt.";
  } else {
    txt = "Hello " + title + message + "! How are you today?";
  }
  document.getElementById("demo").innerHTML = txt;
}