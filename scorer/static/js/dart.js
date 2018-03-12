$(document).ready(function() {
    var throwFocus = 1;
    var $throwFocus = $("#throw1");
    var playerScore = 301;

    console.log("hello");
//    $("#throw1").val('0');
//    $("#throw2").val('0');
//    $("#throw3").val('0');

    document.getElementById('score').innerHTML = playerScore;

// This waits fot a number to be clicked and adds it to the input
    $(".num_input").on("click", function() {
        var $this = $(this);
        console.log("$this:", $this[0]);
        console.log("$this.value:", $this[0].value);

        var numButtonClickedVal = $this[0].value;
        var currentVal = $throwFocus.val();
        var newVal = currentVal + numButtonClickedVal;
        $throwFocus.val(newVal);
//        $(this).css("background-color", "blue");
    });

    function update_throw_state() {
      console.log("next throw");
      if (throwFocus === 1) {
        throwFocus = 2;
        check_if_valid_score();
        $throwFocus =  $("#throw2");
      } else if (throwFocus === 2) {
        throwFocus = 3;
        check_if_valid_score();
        $throwFocus =  $("#throw3");
      } else {
        throwFocus = 1;
        check_if_valid_score();
        $throwFocus =  $("#throw1");
      }
    }

    function check_if_valid_score() {
      if ($throwFocus.val() <= 20) {
          console.log('valid');
      }
      else {
          console.log('invalid');
      }
    }

    $("#next-throw").on('click', update_throw_state);
    $("#next-throw").on('click', function(){console.log('NEXT');});

    check_if_valid_score();
    console.log($throwFocus.val())
});