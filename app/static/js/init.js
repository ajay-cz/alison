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
    $('select').material_select();
     $('input,checkbox,radio, select').off('input').on('input',function(e){
//        $('#loader').addClass('shown');
//        $('#loader').removeClass('hidden');
//        $('#filters').submit();
    });
    $('select').off('change').on('change',function(e){
//        $('#loader').addClass('shown');
//        $('#loader').removeClass('hidden');
//        $('#filters').submit();
    });
    $('input:checkbox, input:radio').off('change').on('change',function(e){
//        $('#loader').addClass('shown');
//        $('#loader').removeClass('hidden');
        if($(this).is(':checked')){
           $('#is_clip_a').val('on');
           $('#is_clip').val('on');
           $('#is_clip').prop('checked', true);
        } else {
            $('#is_clip_a').val('off');
            $('#is_clip').val('off');
            $('#is_clip').prop('checked', false);
        }
//        $('#filters').submit();
    });
    $('a').off('click').on('click', function(){
//         $('#loader').addClass('shown');
//         $('#loader').removeClass('hidden');
    });
  }); // end of document ready
})(jQuery); // end of jQuery name space