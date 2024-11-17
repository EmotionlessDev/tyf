let timerOn = true;
function timer(remaining) {
  document.getElementById("countdown").innerHTML = ``;

  var m = Math.floor(remaining / 60);
  var s = remaining % 60;
  m = m < 10 ? "0" + m : m;
  s = s < 10 ? "0" + s : s;
  document.getElementById("countdown").innerHTML = `Resend code in ${m}:${s}`;
  remaining -= 1;
  if (remaining >= 0 && timerOn) {
    setTimeout(function () {
      timer(remaining);
    }, 1000);
    document.getElementById("resend").innerHTML = ``;
    return;
  }
  if (!timerOn) {
    return;
  }

  document.getElementById("countdown").innerHTML = ``;
  document.getElementById(
    "resend"
  ).innerHTML = `Don't receive the code? <a class="text-color" id="send-otp" onclick="timer(60);" style="cursor: pointer !important;">Resend</a>`;
}
timer(60);
