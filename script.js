function toggleStart() {
  var x = document.getElementById("window");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}



// Initialize EmailJS with your user ID
emailjs.init("U9zI1ePXYxKZGoWhc");

// sends me an email when someone submits me a 3D print for them. The idea is that I review the print (to make sure it's not copywrited, protected from commerical use via creative commons, or is literally just a gun)
// Once I review it, then I can slice it up and then get an invoice for how much it should cost. I'm accepting irl orders only, with cash to match since I can't ship anything, nor do I have a paypal (or cashapp, venmo, etc)
function sendEmail() {
  var modelLinkInput = document.getElementById("modelLink");
  var modelLink = modelLinkInput.value;

  var senderEmailInput = document.getElementById("senderEmail");
  var senderEmail = senderEmailInput.value;

  var emailParams = {
    to_email: "brandonwandrie@gmail.com",
    from_email: senderEmail,
    subject: "3D Model Request",
    message:
      "Please 3D print the model at the following link: " +
      modelLink +
      "\n\nSender's Email: " +
      senderEmail,
  };

  emailjs.send("service_yimantq", "template_3iuwiyq", emailParams).then(
    function (response) {
      console.log("Email sent successfully", response);
    },
    function (error) {
      console.error("Error sending email", error);
    }
  );
}