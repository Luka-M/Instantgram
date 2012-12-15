jQuery(window).load( function($) {

//
  // Flexslider
  //
  if( jQuery(".flexslider").length > 0) {
    jQuery(".flexslider").flexslider({
      'controlNav': true,
      'directionNav': true
    });
  }


});

jQuery(document).ready(function($) {


  var $menu = $("#navigation");
  $menu.superfish({
    animation: {
      opacity: "show",
      height: "show"
    },
    speed: "fast",
    delay: 250
  });

  $(".searchsubmit").bind("click", function() {
    $(this).parent().submit();
  });

  $(".fancybox").fancybox({
    fitToView: true
  });

  $("a[data-lightbox^=fancybox]").fancybox({
    fitToView: true
  });


  // Responsive menu
  $("<select />").appendTo("nav");

  // Create default option "Go to..."
  $("<option />", {
    "selected": "selected",
    "value": "",
    "text": "Go to..."
  }).appendTo("nav select");

  // Populate dropdown with menu items
  $("nav a").each(function () {
    var el = $(this);
    $("<option />", {
      "value": el.attr("href"),
      "text": el.text()
    }).appendTo("nav select");
  });

  $("nav select").change(function () {
    window.location = $(this).find("option:selected").val();
  });

  $(function(){
    $.fn.formLabels();
  });

  $("#jp500").jPlayer({
    ready: function (event) {
      $(this).jPlayer("setMedia", {
        m4a:"http://www.jplayer.org/audio/m4a/TSP-01-Cro_magnon_man.m4a",
        oga:"http://www.jplayer.org/audio/ogg/TSP-01-Cro_magnon_man.ogg"
      });
    },
    swfPath: "js",
    supplied: "m4a, oga",
    wmode: "window",
    cssSelectorAncestor: "#jp-203"
  });

  //fitVids
  $(".inner-container .format-video .entry-image").fitVids();


});

function setWidth() {

  // Page width calculations

  jQuery(window).resize(setContainerWidth);
  var $box = jQuery(".box");

  function setContainerWidth() {
    var columnNumber = parseInt((jQuery(window).width()+15) / ($box.outerWidth(true))),
      containerWidth = (columnNumber * $box.outerWidth(true)) - 15;

    if ( columnNumber > 1 )  {
      jQuery("#box-container").css("width",containerWidth+'px');
    } else {
      jQuery("#box-container").css("width", "100%");
    }

  }

  setContainerWidth();

};