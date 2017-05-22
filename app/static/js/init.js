(function($){
  $(function(){

    $('.button-collapse').sideNav('show');
    $('.parallax').parallax();
    $('.datepicker').pickadate({
        onSet: function (val) {
            if (val && val.highlight) {
                return;
            }
            $('.picker__close').click();
        },
        closeOnSelect: true,
        format: "yyyy-mm-dd",
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 50 // Creates a dropdown of 15 years to control year
    });
  }); // end of document ready
})(jQuery); // end of jQuery name space