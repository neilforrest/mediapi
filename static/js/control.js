$(function() {
  $(".button").button();
  $("#volume").slider ({
    min: 0, max: 100,
    slide: function ( event, ui ) {
        
        $.ajax({
          url  : "/api/mixer",
          data : "volume=" + ui.value,
          type : "PUT"
        });
        
        $("#volume-value").text ( ui.value );
      }
    });
  
  $("#play").click( 
    function( event ) {
        
      $.ajax({
        url  : "/api/player",
        data : "action=play",
        type : "PUT"
      });
      
    });
    
  $("#stop").click( 
    function( event ) {
      
      $.ajax({
        url  : "/api/player",
        data : "action=stop",
        type : "PUT"
      });
      
    });
});
