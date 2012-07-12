var year = new Date().getFullYear();
var month = new Date().getMonth();
var day = new Date().getDate();
function singleshot(s){	return Date.parse(s).add(-4).hour();};
function dd(s) {
		a=s[0];
		b=s[1];
		c=s[2];
		if (a=='s'){return singleshot(b);}
		if(c==null) {c=0;}
		var nb=0;
		(b-4 < 0) ? nb=b-4+24 : nb=b-4;
		//if ($.url.param("retjson")=="yes") {nb=nb+4; if(nb>24) nb=nb-24; if(nb==24) nb=0;}
		uu=Date.parse(a).set({hour:nb,minute:c});
		if(Date.today().toString("ddd")=='dom' && a!='do'){uu.add(-7).days();}
		return uu;
};

function jstoelem(item){
return {"id":item.id, "start": dd(item.start), "end": dd(item.end),"title":item.title, "stato":item.stato,};
};
function retplis(){
	var e=[];
	$.ajax({url: 'programmi.json',async: false,dataType: 'json',success: function(d){$.each(d.events, function(i,item){e.push(jstoelem(item));});} });
return e;};


function inonda(){
	$('#nellaria').html("Musica NO STOP");
	$('#onair').css({"background":"transparent url(http://cdn.radiocicletta.it/images/layout/onair.png) no-repeat 0px -46px"});
	$('#offair h1').html(" ");
	dn=Date.parse('now');
	dnh=dn.getHours();
	dnm=dn.getMinutes();
	$.getJSON('programmi.json', function(d) {
	  	$.each(d.events, function(i,item){
				var elem=jstoelem(item);
				var h1 = parseInt(elem.start.getHours())+4;
				var h2 = parseInt(elem.end.getHours())+4;
				if (h1 > 24) {h1=h1-24;}
				if (h2 > 24) {h2=h2-24;}
				//stato 0 -> programma in ferie=offonair
				//stato 1 -> programma no in ferie
				//stato 2 -> special
				//stato 3 -> programma cambiato
				//stato 4 -> programma nuovo
				//stato 5 -> replica
				if (item.stato!=0){
					if ((elem.id!=0)&&(dn.toString('ddd MMM d') == elem.start.toString('ddd MMM d'))&&(dnh>=h1)&&(dnh<=h2)&&((dnh==h2)?(dnm<=elem.end.getMinutes()):(1==1))){
						$('#nellaria').html((elem.title).split("<br/>")[0]);
						$('#onair').css({"background":"transparent url(http://cdn.radiocicletta.it/images/layout/onair.png) no-repeat top left"});
						$('#offair-prog').html("Musica NO STOP");
						if(d.next[elem.id]!=undefined){
						$.each(d.events,function(i,item){
							if(item.id==d.next[elem.id]) {$('#offair h1').html("A seguire:  "); $('#offair-prog').replaceWith((item.title).split("<br/>")[0]);}
						});
						}
						return;
					}
					return;
				
				}
	});
return;
});
}


function openPopUp(url,target,attributes){
					popup = window.open(url,target,attributes);
					popup.moveTo((window.screen.availWidth -  520) / 2, (window.screen.availHeight - 550) / 2);
			}
$(document).ready(function() {
		var _gaq = _gaq || [];
 		_gaq.push(['_setAccount', 'UA-26545450-1']);
  		_gaq.push(['_trackPageview']);
		(function() {var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    		ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    		var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
 		})();


});
