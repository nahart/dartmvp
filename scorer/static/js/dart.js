$(document).ready(function() {
    var throwFocus = 1;
    var $throwFocus = $("#throw1");

    console.log("hello");
//    $("#throw1").val('0');
//    $("#throw2").val('0');
//    $("#throw3").val('0');

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
        $throwFocus =  $("#throw2");
      } else if (throwFocus === 2) {
        throwFocus = 3;
        $throwFocus =  $("#throw3");
      } else {
        throwFocus = 1;
        $throwFocus =  $("#throw1");
      }
    }

    function foo() {
        console.log('foo');
    }

    $("#next-throw").on('click', update_throw_state);
    $("#next-throw").on('click', function(){console.log('NEXT');});


});