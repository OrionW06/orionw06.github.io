// JavaScript Document
// Initialize EmailJS with your user ID
emailjs.init("U9zI1ePXYxKZGoWhc");

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
