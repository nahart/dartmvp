$(document).ready(function() {
    console.log("hello");
    $("#throw1").val('0');
    $("#throw2").val('0');
    $("#throw3").val('0');
    var throw = 1;

    $(".num_input").on("click", function() {
        $throw1 = $(this);
        $throw1.value += $(this);
        $this.css("background-color", "blue");
        console.log("jjuy");
        console.log($this);
    });

    function next(){
    var throw = throw++;
    console.log(throw);
    )
});