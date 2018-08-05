$(document).ready(function() {
    //Set global variables
    //Need to figure out how to set these variables as part of a StartGame method.
    var throwFocus = 1;
    var $throwFocus = $("#throw1");
    var playerScore = 301;
    var numPlayers = 2;
    var playerTurn = 1;
    var endWithDoubles = 'False'

    console.log("hello");
//    $("#throw1").val('0');
//    $("#throw2").val('0');
//    $("#throw3").val('0');

    //Show Player Score
/*    document.getElementById('score').innerHTML = playerScore;*/

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

    // Moves the focus of throw to next state & checks if valid
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

    $('#play-again').on('click', function() {
      var playAgainURL = $(this).attr('href');
      console.log($(this).attr('href'));
      location.href = playAgainURL;
    });

    function check_if_valid_score() {
      if ($throwFocus.val() <= 20) {
          console.log('valid');
      }
      else {
          console.log('invalid');
          $('.alert').show('fade')
      }
    }

    $('#addplayer').on('click', function(){
        console.log('add player');
        var numVisiblePlayers = $('.player:visible').length;
        console.log(numVisiblePlayers);

        if (numVisiblePlayers == 1){
            $('#player2').show();
            $('#player-2-first-name').prop('required', true);
            $('#player-2-last-name').prop('required', true);
        } else if (numVisiblePlayers == 2){
            $('#player3').show();
            $('#player-3-first-name').prop('required', true);
            $('#player-3-last-name').prop('required', true);
        } else if (numVisiblePlayers == 3){
            $('#player4').show();
            $('#player-4-first-name').prop('required', true);
            $('#player-4-last-name').prop('required', true);
        }
    });

    $('#removeplayer').on('click', function(){
        console.log('remove player');
        var numVisiblePlayers = $('.player:visible').length;
        console.log(numVisiblePlayers);

        if (numVisiblePlayers == 4){
            $('#player4').hide();
            $('#player-4-first-name').prop('required', false);
            $('#player-4-last-name').prop('required', false);
        } else if (numVisiblePlayers == 3){
            $('#player3').hide();
            $('#player-3-first-name').prop('required', false);
            $('#player-3-last-name').prop('required', false);
        } else if (numVisiblePlayers == 2){
            $('#player2').hide();
            $('#player-2-first-name').prop('required', false);
            $('#player-2-last-name').prop('required', false);
        }
    });

    $('.alert').alert()

    $('.close').click(function() {
        $('.alert').hide('fade');
        //reset value
        //$throwFocus.val(0);
    })

    $("#next-throw").on('click', update_throw_state);
    $("#next-throw").on('click', function(){console.log('NEXT');});

    check_if_valid_score();
    console.log($throwFocus.val())

    $('#myModal').on('shown.bs.modal', function () {
        $('#myInput').trigger('focus')
    })
});