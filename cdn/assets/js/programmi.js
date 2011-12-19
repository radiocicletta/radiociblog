$(document).ready(function() {
		var $calendar = $('#calendar');
		var oraadesso= null;
		$('#calendar').weekCalendar({
			data:eventData,
			timeslotsPerHour: 6,
			useShortDayNames: true,
			dateFormat : "d M, Y",
			timeFormat : "H:i",
			displayEventHeader: true,
			height: function($calendar){return $(window).height() - $("h1").outerHeight(true);},
			
			eventRender : function(calEvent, $event) {
				if(calEvent.title == "ADESSO"){ //renderizzo tutto se becco l'evento con titolo ADESSO cambio le propietà del css
				$event.css("backgroundColor", "#990000"); 
				$event.find(".wc-time").replaceWith('<div class="replaced"></div>');
				oraadesso=calEvent;
				}
			}, 
			eventNew : function(calEvent, $event){},
			eventDrop : function(calEvent, $event){},
			eventResize : function(calEvent, $event){},
			eventClick : function(calEvent, $event){
					$.getJSON('http://www.radiocicletta.it/descr.json',function(data) {//per tutti gli eventi tranne ADESSO estraggo rozzamente
					//il titolo della trasmissione, poi lo appiccico nella barra a destra e cambio la classe del link del titolo (bianco/non sottol.)
					if(calEvent.title!='ADESSO'){var tit=calEvent.title.split(">")[1].split("<")[0];
					displayMessage('<div id="showdetail"><strong>'+calEvent.title+'</strong></div><br/>'+data[tit]);}
					$('#showdetail').find('a').addClass('showd');
				});},
			eventMouseover : function(calEvent,$event){},
			eventMouseout : function(calEvent, $event) {},
			noEvents : function() {	displayMessage('<div id="showdetail"><strong>NESSUNA TRASMISSIONE QUESTA SETTIMANA</strong></div>');},
			
		});
		function displayMessage(message) {$("#infobox").html(message).fadeIn();}
		//stronco la prima colonna vuota, anche nella barra in testa
		$('.wc-grid-timeslot-header').css("width", "0%");
		$('.wc-time-column-header').css("width", "0%"); 
		wdh=$('.wc-scrollbar-shim').css("width"); 
		//aggiusto padding e bordi dell'ultima colonna della barra in testa
		$('.wc-scrollbar-shim').css({"border-left":"medium hidden", "width":wdh-2});
		displayMessage('<div id="showdetail"><strong>HELP</strong><br/><br/>Clicca sul riquadro di un programma per visualizzare la sua descrizione qui.<br/>Clicca sul titolo per aprire la descrizione in una nuova pagina</div>');
		setInterval(function() { 
					        oraadesso.start = Date.parse('now');
                  				oraadesso.end = Date.parse('now');
						$calendar.weekCalendar("removeUnsavedEvents");
						$calendar.weekCalendar("updateEvent", oraadesso);
					}, 60000);


});

