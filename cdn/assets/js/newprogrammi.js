$(document).ready(function() {
		var $calendar = $('#calendar');
		var oraadesso= null;
		var col= null;
		var m1=null;
		var m2=null;
		var sfondo=null;
		var t=null;
		var h=null;
		var descrizie = {};
		$.ajax({url:'http://www.radiocicletta.it/descr.json',async: false,dataType: 'json',success: function(d){$.each(d,function(i,a){descrizie[i]=a;});}});
		var qtipo={"0":"Questo programma non va in onda questa settimana","2":"Programma speciale delle settimana","3":"Programma sostituito per questa settimana","4":"NUOVO PROGRAMMA DI RADIOCICLETTA"};
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
				else { //altrimenti mi ribecco l'intervallo orario e ci sommo le famose 4 ore che avevo tolto
				var h1 = parseInt(calEvent.start.getHours())+4;
				var h2 = parseInt(calEvent.end.getHours())+4;
				//colori delle caselle, default le sceglie tutte, id:"#hexcol" setta solo la casella id del colore html corrispondente a #hexcol
				var colorometro={"1":"#2B72D0","0":"#000000","2":"#FF0000","3":"#33CC00","4":"#ff6600","5":"#009966" };
				//stato 0 -> programma in ferie=offonair
				//stato 1 -> programma no in ferie DEFAULT
				//stato 2 -> special
				//stato 3 -> programma cambiato 
				//stato 4 -> programma nuovo 
				//stato 5 -> replica
				col=colorometro[calEvent.stato+""];
				if (h1 > 24) {h1=h1-24;}
				if (h2 > 24) {h2=h2-24;}
				//mi becco il colore se è specificato e ne creo anche uno più chiaro per lo sfondo.
				sfondo =$.tocolor(col);
				//console.log(sfondo.add("#111111").hexHTML());
				$event.css("backgroundColor", sfondo.add("#555555").hexHTML()); 
				m1=calEvent.start.getMinutes();
				m2=calEvent.end.getMinutes();
				if(m1==0) {m1="00";}
				if(m2==0) {m2="00";}
				//rifaccio la barra del titolo con le ore modificate
				$event.find(".wc-time").replaceWith('<div class="ntit ui-corner-top" style="background-color:'+col+'; border: 0px solid'+col+';">'+h1+":"+m1+" - "+h2+":"+m2+'</div>');
				$event.corner("3px");
				$(".ntit").corner("3px");
				
				}
			}, 
			eventNew : function(calEvent, $event){},
			eventDrop : function(calEvent, $event){},
			eventResize : function(calEvent, $event){},
			eventClick : function(calEvent, $event){
					//per tutti gli eventi tranne ADESSO estraggo rozzamente
					//il titolo della trasmissione, poi lo appiccico nella barra a destra e cambio la classe del link del titolo (bianco/non sottol.)
					if(calEvent.title!='ADESSO'){
						// se metti attaccato<br/> titolo lo splint lo elimina per cercare la descr.
						var tit=calEvent.title.split(">")[1].split("<")[0];
						displayMessage('<div id="showdetail"><strong>'+calEvent.title+'</strong></div><br/>'+descrizie[tit]);}
					$('#showdetail').find('a').addClass('showd');
					},
			eventMouseover : function(calEvent,$event){
					if (calEvent.stato!=1 && calEvent.id!=0){
						$event.qtip(
						{ content:(calEvent.title+'<br/>'+qtipo[calEvent.stato]),
				     		style:{name:'blue'},
				     		position:{corner:{target:'center',tooltip:'center'}},
				     		show:{ready:true,solo:true},
						hide: {delay:1000, when: 'mouseout', fixed: true }
						});
						}	
			},
			eventMouseout : function(calEvent, $event) {},
			noEvents : function() {	displayMessage('<div id="showdetail"><strong>NESSUNA TRASMISSIONE QUESTA SETTIMANA</strong></div>');},
			
		});
		function displayMessage(message) {$("#infobox").html(message).fadeIn();}
		//stronco la prima colonna vuota, anche nella barra in testa
		$('.wc-grid-timeslot-header').css("width", "0%");
		$('.wc-time-header-cell').each(function(){
			t=$(this).text();
			h=t.split(":")[0];
			if(h[0]==0) h=h[1];
			h=parseInt(h)+4; //^---- questo scemo se gli arriva 0n sputa 0 invece di n. quindi mi smazzo i num < 10 a mano
			if(h>24) h=h-24;
			if(h<10) h="0"+h; //ci rimetto lo 0 davanti che fa figura
			$(this).text(h+":"+t.split(":")[1]);
			});
		$('.wc-time-column-header').css("width", "0%"); 
		wdh=$('.wc-scrollbar-shim').css("width"); 

		//aggiusto padding e bordi dell'ultima colonna della barra in testa
		$('.wc-scrollbar-shim').css({"border-left":"medium hidden", "width":wdh-2});
		displayMessage('<div id="showdetail"><strong>HELP</strong><br/><br/>Clicca sul riquadro di un programma per visualizzare la sua descrizione qui.<br/>Clicca sul titolo per aprire la descrizione in una nuova pagina</div>');
		//$calendar.weekCalendar("thishevent",17);
		setInterval(function() { 
					        oraadesso.start = Date.parse('now').add(-4).hour();
                  				oraadesso.end = oraadesso.start;
						$calendar.weekCalendar("removeUnsavedEvents");
						$calendar.weekCalendar("updateEvent", oraadesso);
						
					}, 60000);
return true;


});

