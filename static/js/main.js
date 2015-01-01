
var closePopupTimer;

function popupMessage ( message ) {
  $('.popupMessage p').text ( message );
  clearTimeout ( closePopupTimer );
  $('.popupMessage').popup ( "open" );
  closePopupTimer= setTimeout ( function () { $('.popupMessage').popup ( "close" ); }, 5000 );
}

function appendItem ( url ) {
 
 $.ajax({
   url  : "/api/queue",
   data : "url=" + url,
   type : "POST",
   success: function ( data ) {
       popupMessage ( "Added " + url );
     }
   });
        
}

function refreshQueue () {
  $( "#queue" ).load ( "/control/queue", function () {
    $( "#queuelist" ).listview ();
    setTimeout ( refreshQueue, 5000 );
  } );
}

$(document).on ( "pagecreate", "#pagecontrol", function ( event, data ) {
  
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
    
  $("#skip").click( 
    function( event ) {
      
      $.ajax({
        url  : "/api/queue",
        data : "index=0",
        type : "DELETE",
        success: function ( data ) {
           $( "#queue" ).load ( "/control/queue", function () {
             $( "#queuelist" ).listview ();
           });
        }
      });
      
    });
  
  var lastVolumeChangeTime= 0;
  var minCommandTime= 1000;

  $("#volume").change(function() {
    
    var d= new Date();
    var t= d.getTime();

    if ( t-lastVolumeChangeTime > minCommandTime ) {
      lastVolumeChangeTime= t;

      $.ajax({
        url  : "/api/mixer",
        data : "volume=" + $("#volume").val(),
        type : "PUT"
      });

    }
  });

  $("#volume").on( "slidestop", function() {

    $.ajax({
      url  : "/api/mixer",
      data : "volume=" + $("#volume").val(),
      type : "PUT"
    });

  });

  refreshQueue ();
  
});

$(document).on ( "pageshow", "#pagecontrol", function ( event, data ) {

  $( "#queue" ).load ( "/control/queue", function () {
      $( "#queuelist" ).listview ();
   });

});

$(document).on ( "pagecreate", "#pagelibrary", function ( event, data ) {
  
  $( ".item-link" ).click ( function () {
    appendItem ( $( this ).text () );
  });

});

