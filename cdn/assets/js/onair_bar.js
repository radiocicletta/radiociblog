function onair_prog(){
			offair(0);
			var data=new Date();	

			var giornosettimana=data.getDay();

			var ora=data.getHours();
			var min=data.getMinutes();
			var time=(ora*100)+min;
			switch(giornosettimana){
			
				case 1: //lunedi
					if(time>=0000 && time<0030){document.getElementById('onair-prog').innerHTML ="Occhi Pallati";document.getElementById('offair-prog').innerHTML ="L'ultima mezzora"; offair(1);break;}
					if(time>=0030 && time<0100){document.getElementById('onair-prog').innerHTML ="L'ultima mezzora";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					if(time>=1800 && time<1900){document.getElementById('onair-prog').innerHTML ="Eclettica";document.getElementById('offair-prog').innerHTML ="SottoBosco"; offair(1);break;}
					if(time>=1900 && time<2000){document.getElementById('onair-prog').innerHTML ="SottoBosco";document.getElementById('offair-prog').innerHTML ="La(b)nova"; offair(1);break;}
					if(time>=2000 && time<2100){document.getElementById('onair-prog').innerHTML ="La(b)nova";document.getElementById('offair-prog').innerHTML ="Phi^3"; offair(1);break;}
					if(time>=2100 && time<2200){document.getElementById('onair-prog').innerHTML ="Phi^3";document.getElementById('offair-prog').innerHTML ="Giacca a Vento "; offair(1);break;}
					if(time>=2200 && time<2300){document.getElementById('onair-prog').innerHTML ="Giacca a Vento";document.getElementById('offair-prog').innerHTML ="ScrapJazz"; offair(1);break;}
					if(time>=2300 && time<0000){document.getElementById('onair-prog').innerHTML ="ScrapJazz";document.getElementById('offair-prog').innerHTML ="L'ultima mezzora";offair(1); break;}
					break;
					
				case 2: //martedi
					if(time>=0000 && time<0030){document.getElementById('onair-prog').innerHTML ="L'ultima mezztime";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					if(time>=1800 && time<1900){document.getElementById('onair-prog').innerHTML ="Drum Machine";document.getElementById('offair-prog').innerHTML ="Alabama"; offair(1);break;}
					if(time>=1900 && time<2000){document.getElementById('onair-prog').innerHTML ="Alabama";document.getElementById('offair-prog').innerHTML ="Rapsodia"; offair(1);break;}
					if(time>=2000 && time<2100){document.getElementById('onair-prog').innerHTML ="Raposodia";document.getElementById('offair-prog').innerHTML ="Grooveiera"; offair(1);break;}
					if(time>=2100 && time<2200){document.getElementById('onair-prog').innerHTML ="Grooveiera";document.getElementById('offair-prog').innerHTML ="Quando ero piccolo"; offair(1);break;}
					if(time>=2200 && time<2300){document.getElementById('onair-prog').innerHTML ="Quando ero piccolo";document.getElementById('offair-prog').innerHTML ="Smanie di fax"; offair(1);break;}
					if(time>=2300 && time<0000){document.getElementById('onair-prog').innerHTML ="Smanie di fax";document.getElementById('offair-prog').innerHTML ="L'ultima mezzora"; offair(1);break;}
					break;
					
				case 3: //mercoledi
					if(time>=0000 && time<0030){document.getElementById('onair-prog').innerHTML ="L'ultima mezzora";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					if(time>=0800 && time<0900){document.getElementById('onair-prog').innerHTML ="I Politicazzi";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					if(time>=1100 && time<1230){document.getElementById('onair-prog').innerHTML ="Autoradio(Cicletta)";document.getElementById('offair-prog').innerHTML ="RadioCiccetta"; offair(1);break;}
					if(time>=1230 && time<1430){document.getElementById('onair-prog').innerHTML ="RadioCiccetta";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					if(time>=1900 && time<2000){document.getElementById('onair-prog').innerHTML ="Crazy Monkey";document.getElementById('offair-prog').innerHTML ="All 90s Long"; offair(1);break;}
					if(time>=2000 && time<2100){document.getElementById('onair-prog').innerHTML ="All 90s Long";document.getElementById('offair-prog').innerHTML ="Power chords"; offair(1);break;}
					if(time>=2100 && time<2200){document.getElementById('onair-prog').innerHTML ="Power chords";document.getElementById('offair-prog').innerHTML ="Le vagine di ferro"; offair(1);break;}
					if(time>=2200 && time<2300){document.getElementById('onair-prog').innerHTML ="Le vagine di ferro ";document.getElementById('offair-prog').innerHTML ="Radiociclettingham"; offair(1); break;}
					if(time>=2300 && time<0000){document.getElementById('onair-prog').innerHTML ="Radiociclettingham";document.getElementById('offair-prog').innerHTML ="Pizza Maraging"; offair(1);break;}
					break;
					
				case 4: //giovedi
					if(time>=0000 && time<0100){document.getElementById('onair-prog').innerHTML ="Pizza Maraging";document.getElementById('offair-prog').innerHTML ="L'ultima mezzora"; offair(1);break;}
					if(time>=0100 && time<0130){document.getElementById('onair-prog').innerHTML ="L'ultima mezzora";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					if(time>=1800 && time<1900){document.getElementById('onair-prog').innerHTML ="La Parola d'ordine";document.getElementById('offair-prog').innerHTML ="MONO"; offair(1);break;}
					if(time>=1900 && time<2000){document.getElementById('onair-prog').innerHTML ="MONO";document.getElementById('offair-prog').innerHTML ="MON0Serie"; offair(1); break;}
					if(time>=2000 && time<2030){document.getElementById('onair-prog').innerHTML ="MONOSerie";document.getElementById('offair-prog').innerHTML ="MONOSerie"; offair(1);break;}
					if(time>=2030 && time<2200){document.getElementById('onair-prog').innerHTML ="Gli Spacciaserie";document.getElementById('offair-prog').innerHTML ="Cinemando"; offair(1);break;}
					if(time>=2200 && time<2300){document.getElementById('onair-prog').innerHTML ="Cinemando";document.getElementById('offair-prog').innerHTML ="Radom Selection's"; offair(1);break;}
					break;
					
				case 5: //venerdi
					if(time>=1730 && time<1930){document.getElementById('onair-prog').innerHTML ="Hype";document.getElementById('offair-prog').innerHTML ="Caribbean Vintage"; offair(1);break;}
					if(time>=1930 && time<2030){document.getElementById('onair-prog').innerHTML ="Caribbean Vintage";document.getElementById('offair-prog').innerHTML ="La Penultima cena"; offair(1);break;}
					if(time>=2030 && time<2200){document.getElementById('onair-prog').innerHTML ="La Penultima cena";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					break;

				case 6: //sabato 
					if(time>=1400 && time<1500){document.getElementById('onair-prog').innerHTML ="Random Selection's";document.getElementById('offair-prog').innerHTML ="Lady Voice"; offair(1);break;}
					if(time>=1500 && time<1630){document.getElementById('onair-prog').innerHTML ="Lady Voice";document.getElementById('offair-prog').innerHTML ="ONAIR"; offair(1);break;}
					if(time>=1630 && time<1830){document.getElementById('onair-prog').innerHTML ="ONAIR";document.getElementById('offair-prog').innerHTML ="Pendente verso SUD"; offair(1);break;}
					if(time>=1830 && time<2000){document.getElementById('onair-prog').innerHTML ="Pendente verso SUD";document.getElementById('offair-prog').innerHTML ="Lo Sfasciacarozze"; offair(1);break;}
					if(time>=2000 && time<2100){document.getElementById('onair-prog').innerHTML ="Lo sfasciacarozze";document.getElementById('offair-prog').innerHTML ="Random Selection's"; offair(1);break;}
					break;
				
				case 0: //domenica
					if(time>=1600 && time<1700){document.getElementById('onair-prog').innerHTML ="Random Selection's";document.getElementById('offair-prog').innerHTML ="RadioCiclabile"; offair(1);break;}
					if(time>=1700 && time<1800){document.getElementById('onair-prog').innerHTML ="RadioCiclabile";document.getElementById('offair-prog').innerHTML ="A Very late Breakfast"; offair(1);break;}
					if(time>=1800 && time<1900){document.getElementById('onair-prog').innerHTML ="A Very late Breakfast";document.getElementById('offair-prog').innerHTML ="Attualità con Enzo & Nicolò"; offair(1);break;}
					if(time>=1900 && time<2000){document.getElementById('onair-prog').innerHTML ="Attualità con Enzo & Nicolò";document.getElementById('offair-prog').innerHTML ="Read che ti passa"; offair(1);break;}
					if(time>=2000 && time<2100){document.getElementById('onair-prog').innerHTML ="Read che ti passa";document.getElementById('offair-prog').innerHTML ="Il Baro contro Mozart"; offair(1);break;}
					if(time>=2100 && time<2200){document.getElementById('onair-prog').innerHTML ="Il Baro Contro Mozart";document.getElementById('offair-prog').innerHTML ="A Mille ce n'è"; offair(1);break;}
					if(time>=2200 && time<2300){document.getElementById('onair-prog').innerHTML ="A Mille ce n'è";document.getElementById('offair-prog').innerHTML ="Occhi Pallati"; offair(1);break;}
					if(time>=2300 && time<0000){document.getElementById('onair-prog').innerHTML ="Occhi Pallati";document.getElementById('offair-prog').innerHTML ="L'ultima mezzora"; offair(1);break;}
					break;
				default: 
					document.getElementById('onair-prog').innerHTML ="Random Selection's";
					document.getElementById('onair').style.background=" transparent url(http://radiocicletta-static.appspot.com/images/layout/onair.png) no-repeat botton left";
					break;

			
			}
	}
function offair(stato){
	if (stato==0){
		document.getElementById('onair-prog').innerHTML ="Random Selection's";
		document.getElementById('onair').style.background=" transparent url(http://radiocicletta-static.appspot.com/images/layout/onair.png) no-repeat 0px -47px";
	}else{
			document.getElementById('onair').style.background=" transparent url(http://radiocicletta-static.appspot.com/images/layout/onair.png) no-repeat top left";

		}

}
