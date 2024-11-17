document.addEventListener("DOMContentLoaded", function (event) {
  function OTPInput() {
    const inputs = document.querySelectorAll("#otp > *[id]");

    for (let i = 0; i < inputs.length; i++) {
      inputs[i].addEventListener("keydown", function (event) {
        if (
          (event.ctrlKey || event.metaKey) &&
          (event.key === "v" || event.key === "V")
        ) {
          return true;
        }

        if (event.keyCode == 37) {
          if (i !== 0) inputs[i - 1].focus();
          event.preventDefault();
        } else if (event.keyCode == 39) {
          if (i !== inputs.length - 1) inputs[i + 1].focus();
          event.preventDefault();
        } else if (event.key === "Backspace") {
          event.preventDefault();
          inputs[i].value = "";
          if (i !== 0) inputs[i - 1].focus();
        } else {
          if (event.keyCode > 47 && event.keyCode < 58) {
            inputs[i].value = event.key;
            if (i !== inputs.length - 1) inputs[i + 1].focus();
            event.preventDefault();
          } else if (event.keyCode > 64 && event.keyCode < 91) {
            inputs[i].value = String.fromCharCode(event.keyCode);
            if (i !== inputs.length - 1) inputs[i + 1].focus();
            event.preventDefault();
          }
        }
      });
      inputs[i].addEventListener("paste", (event) => {
        inputs[i].value = "";
        data = event.clipboardData.getData("text/plain");
        let text_len = data.length < inputs.length - i ? data.length : inputs.length - i;

        for (let j = 0; j < text_len; j++) {
          inputs[i + j].value = data[j].toUpperCase();
          if (i + j !== inputs.length) inputs[i + j].focus();
        }

        console.log(data, text_len);
        event.preventDefault();
      });
    }
  }
  OTPInput();
});
