/*jshint browser:true, jquery:true*/
/*global MediaElement:true, Social:true*/

// Bought to you by radiocicletta hack team.
var kPlayerBackgroundRunPos = "0px 0px",
    kPlayerBackgroundWaitPos = "0px -7px",
    kPlayerBackgroundHaltPos = "0px -14px";

$(function(evt) {
    /*jshint $:true*/
    //"use strict"; // jshint ;_;
    var baseurl = "http://api.radiocicletta.it",
        player = document.createElement("div"),
        infobar = document.createElement("div"),
        lastvisit = (window.localStorage ?
                     localStorage.getItem('lastvisit') :
                     null);

    player.id = "commands";
    player.innerHTML =  '<span id="flexibleplayer">' +
                            '<a href="" id="playercmd" class="play" title="Play/Stop"></a>' +
                            '<span id="playerdot"></span>' +
                            '<span id="playervolume"><a href="" id="playerknob"></a></span>' +
                            '<span id="playermetadata">...</span>' +
                        '</span>' +
                        '<a id="playerexternal" title="ascolta la diretta col tuo player (Winamp, iTunes, VLC...)"' +
                            'href="http://radiocicletta.it/listen.pls"></a>' +
                        '<a id="playerdetach" href=""></a>';
    infobar.id = 'infobar';
    infobar.innerHTML = '<ul>' +
                            '<li><span id="infobar-first">Ascolta la radio</span></li>' +
                            '<li><span id="infobar-second">Ascolta con VLC, Winamp, ecc.</span></li>' +
                            '<li><span id="infobar-third">Apri il player separato</span></li>' +
                        '</ul>';

    document.getElementById("player").appendChild(player);
    if (lastvisit === null)  {
        document.getElementById("playercontainer")
            .parentNode
            .insertBefore(infobar,
                          document.getElementById("playercontainer")
                            .nextSibling);
    }

    var metadata = document.getElementById("playermetadata"),
        playerdot = document.getElementById("playerdot"),
        opacity = 0,
        dotinterval = setInterval(function(){
            playerdot.style.opacity = opacity++ % 2;
        }, 1000),

    //playerdot.style.backgroundPosition = kPlayerBackgroundWaitPos;

        me = new MediaElement('audiosrc', {
        enablePluginDebug: true,
        plugins: ['flash', 'silverlight'],
        type: 'audio/mp3',
        pluginPath: 'http://cdn.radiocicletta.it/js/me/',
        flashName: 'flashmediaelement.swf',
        silverlightName: 'silverlightmediaelement.xap',
        pluginWidth: -1,
        pluginHeight: -1,
        timerRate: 250,
        success: function (mediaElement, domObject) { 

            mediaElement.addEventListener('loadstart', function(e) {
                metadata.innerHTML = "Avvio player...";
                playerdot.style.backgroundPosition = kPlayerBackgroundWaitPos;
            }, false);
            mediaElement.addEventListener('pause', function(e) {
                playerdot.style.backgroundPosition = kPlayerBackgroundWaitPos;
            }, false);
            mediaElement.addEventListener('ended', function(e) {
                metadata.innerHTML = "Riproduzione interrotta";
                playerdot.style.backgroundPosition = kPlayerBackgroundHaltPos;
            }, false);
            mediaElement.addEventListener('canplay', function(e){
                playerdot.style.backgroundPosition = kPlayerBackgroundRunPos;
            }, false);
            mediaElement.addEventListener('loadeddata', function(e){
                playerdot.style.backgroundPosition = kPlayerBackgroundRunPos;
            }, false);
            mediaElement.addEventListener('emptied', function(e){
                playerdot.style.backgroundPosition = kPlayerBackgroundHaltPos;
            }, false);
            mediaElement.addEventListener('empty', function(e){
                playerdot.style.backgroundPosition = kPlayerBackgroundHaltPos;
            }, false);
            var progress = 0,
                timing = new Date(),
                lastbufferratio = 10000,
                timingid = setInterval(function(){
                    timing = new Date();
                }, 10000);
            mediaElement.addEventListener('progress', function(e){
                progress++;
                if (progress % 50 === 0 || (new Date()) - timing > 10000) {
                    var bufferratio = ~~(e.bufferedBytes / e.currentTime / 1024);
                    if (bufferratio > lastbufferratio) {
                        playerdot.style.backgroundPosition = kPlayerBackgroundWaitPos;
                        if (!me.paused) {
                            me.pause();
                            me.play();
                        }
                    }
                    else {
                        playerdot.style.backgroundPosition = kPlayerBackgroundRunPos;
                    }
                    lastbufferratio = bufferratio;
                }
            });
            mediaElement.addEventListener('volumechange', function(e){
                var original = metadata.innerHTML,
                    newcontent = "Volume: " + ~~(me.volume * 100) + "%";
                metadata.innerHTML = newcontent;

                setTimeout(function() {
                    if (metadata.innerHTML === newcontent)
                        metadata.innerHTML = original;
                }, 2000);
            }, false);

            var icyinfo = { listeners:0, title:"", genre:"" },
                onairinfo = { title: "No Stop Music", id: -1 },

                xhr_metadata = function(){
                var xhr = new XMLHttpRequest(),
                    xhr2 = new XMLHttpRequest();
                xhr.overrideMimeType("text/plain; charset=utf-8");
                xhr.open("GET", baseurl + "/snd/json.xsl?_=" + new Date().getTime(), true);
                xhr.onreadystatechange = function(evt) {
                    if (xhr.readyState === 4 && xhr.status === 200) {
                        var streams = JSON.parse(xhr.responseText);

                        icyinfo = streams["/stream"] ||
                                  streams["/live"]   ||
                                  streams["/studio"] ||
                                  {listeners:0, title:"", genre:""};
                    }
                };
                xhr.send(null);

                /*xhr2.overrideMimeType("text/plain; charset=utf-8");
                xhr2.open("GET", "http://www.radiocicletta.it/programmi.json?_=" + new Date().getTime(), true);
                xhr2.onreadystatechange = function(evt) {
                    if (xhr2.readyState === 4 && xhr2.status === 200) {
                        var daytable = ["do", "lu", "ma", "me", "gi", "ve", "sa"],
                            schedule = JSON.parse(xhr2.responseText),
                            date = new Date(),
                            filtered = schedule.programmi.filter(function(el, idx, arr){ 
                            return el.stato > 0 &&
                                    el.start[0] == daytable[date.getDay()] &&
                                    el.start[1] == date.getHours(); // FIXME: el.start[1] == 24 => ???
                        });

                        onairinfo = filtered.length && filtered[0] || {title: "No Stop Music", id: -1};
                    }
                };
                xhr2.send(null);*/

            };

            var ui_metadata = function () {
                //metadata.title = metadata.innerHTML = (onairinfo.title + " — " + icyinfo.title).replace(/<[^>]+>/g, "");
                metadata.title = metadata.innerHTML = (icyinfo.title).replace(/<[^>]+>/g, "");
            };

            /*var scrolleft = 0;
            var scrolldirection = 1;
            var ui_scrolltext = function() {
                var oldscroll = metadata.scrollLeft;
            };*/

            xhr_metadata();
            ui_metadata();
            var metadataid = window.setInterval(xhr_metadata, 60000),
                uiid = window.setInterval(ui_metadata, 3000);

        },
        // fires when a problem is detected
        error: function () { 
            metadata.innerHTML = "Impossibile avviare il player. Ay Caramba!";
            playerdot.style.backgroundPosition = kPlayerBackgroundHaltPos;
        }

    });

    function cancelEvent(evt) {
            evt.cancelBubble = true;
            evt.returnValue = false;

            if (!evt.stopPropagation)
                return;

            evt.stopPropagation();
            evt.preventDefault();
    }


    if (me) { 
        $("#playercmd").bind("click tap", function(evt) {
            cancelEvent(evt);
            var target = (evt.target ? evt.target : evt.srcElement);

            if (me.paused) {
                target.className = "stop";
                me.play();
                if (!lastvisit) {
                    lastvisit = new Date().getTime();
                    if (window.localStorage)
                        localStorage.setItem('lastvisit', lastvisit);
                    $("#infobar").remove();
                }
            }
            else {
                target.className = "play";
                me.pause(); 
            }
            return false;
        });

        var knob = false,
            knobwidth = $("#playervolume").width() - 8,
            knobinnerwidth = $("#playerknob").width() - 8,
            backgroundposition = (window.getComputedStyle ? window.getComputedStyle(document.getElementById("playerknob"), null).backgroundPosition : document.getElementById("playerknob").currentStyle.backgroundPosition);
        if(!backgroundposition) // IE Hack :(
            backgroundposition = "75px -198px";

        var playerknob = document.getElementById("playerknob");
        playerknob.title = "Volume: " + ~~(me.volume * 100) + "%";

        playerknob.style.backgroundPosition = backgroundposition.replace(/[0-9]+/, "" + (me.volume * knobinnerwidth));
        var wnd;

        $("#playerknob").bind("mousedown touchstart", function(evt) {
            cancelEvent(evt);
            knob = true;
            return false;
        });
        $("#playerknob").bind("mouseup touchend", function(evt) {
            cancelEvent(evt);
            knob = false;
            return false;
        });
        $("#playerknob").bind("mousemove touchmove", function(evt) {
            cancelEvent(evt);

            if (!knob) return;
            var offset = (evt.offsetX ? evt.offsetX : 
                          evt.clientX - this.getBoundingClientRect().left - this.clientLeft + this.scrollLeft),
                volume = offset / knobinnerwidth;
            me.setVolume(volume);
            this.title = "Volume: " + ~~(volume * 100) + "%";
            this.style.backgroundPosition = backgroundposition.replace(/[0-9]+/, (offset >= knobinnerwidth ? knobinnerwidth: offset));

            return false;
        });
        $("#playerknob").bind("click tap", function(evt){
            cancelEvent(evt);
            var offset = (evt.offsetX ? evt.offsetX : 
                            evt.clientX - this.getBoundingClientRect().left - this.clientLeft + this.scrollLeft),

                volume = offset / knobinnerwidth;
            me.setVolume(volume);
            this.title = "Volume: " + ~~(volume * 100) + "%";
            this.style.backgroundPosition = backgroundposition.replace(/[0-9]+/, (offset >= knobinnerwidth ? knobinnerwidth: offset) );

            return false;
        });
        $("#playerdetach").bind("click", function(evt) {
            cancelEvent(evt);

            if (!wnd || !wnd.document) {
                if (!me.paused)
                    $("#playercmd").trigger("click");

                wnd = window.open("/standalone", "_blank", "menubar=no,location=no,toolbar=no,resize=no,resizable=no,scrollbars=no,status=no,height=31,width=420");
            }

            wnd.focus();
            return false;
        });
        var fixedplayer = false,
            toplevel = $('.toplevel');
        $(document).bind("scroll", function(evt){
            if (window.scrollY < toplevel.height()) {
                if (fixedplayer)
                    document.getElementById('playercontainer').className="static";
                fixedplayer = false;
                return;
            }
            document.getElementById('playercontainer').className="fixed";
            fixedplayer = true;
            
        });


    }

    if ($('.side').length)
    $.getJSON(baseurl + "/socialroot.json", function(data){
        var li = document.createElement("li"),
            a = document.createElement("a"),
            span = document.createElement("span"),
            ul, _li, _a, _span; 
        if (!data)
            return;
        if (data.mixcloud) {
            ul = document.createElement("ul");
            for (var i=0, items = data.mixcloud.recents.data, len = Math.min(5, items.length); i < len; i++){
                _li = li.cloneNode(true);
                _a = a.cloneNode(true);
                _a.appendChild(document.createTextNode(items[i].name));
                _a.href = items[i].url;
                _li.appendChild(_a);
                ul.appendChild(_li);
            }
            document.getElementById("box_mixcloud").appendChild(ul);
        }
        var latestsocial = [];
        if (data.facebook)
            for (var j=0, fbitems = data.facebook.latest; j < fbitems.length; j++)
                latestsocial.push({href: fbitems[j].link ||
                                         'http://facebook.com/' + fbitems[j].id,
                                   text: fbitems[j].message ||
                                         fbitems[j].story   ||
                                         fbitems[j].description ||
                                         fbitems[j].name ||
                                         fbitems[j].caption,
                                   time: fbitems[j].created_time,
                                   name: fbitems[j].from.name,
                                   date: new Date(fbitems[j].updated_time)});
        if (data.twitter)
            for (var k=0, twitems = data.twitter.latest; k < twitems.length; k++)
                latestsocial.push({href: "http://twitter.com/"+ twitems[k].user.screen_name + "/status/" + twitems[k].id_str,
                                   text: twitems[k].text,
                                   time: twitems[k].created_at,
                                   name: twitems[k].user.name,
                                   date: new Date(twitems[k].created_at)});
        latestsocial.sort(function(a, b){return b.date - a.date;});
        ul = document.createElement("ul");
        for (var q = 0; q < latestsocial.length; q++) {
            _li = li.cloneNode(true);
            _a = a.cloneNode(true);
            _span = span.cloneNode(true);
            _a.appendChild(document.createTextNode(latestsocial[q]
                                                   .text
                                                   .replace(/\n/g, ' ')
                                                   .split(/\s+/)
                                                   .slice(0,30)
                                                   .join(' ')));
            _a.href = latestsocial[q].href;
            _span.appendChild(document.createTextNode(latestsocial[q].date.toLocaleDateString() + ' • ' + latestsocial[q].name));
            _span.className = "socialname";
            _li.appendChild(_a);
            _a.appendChild(_span);
            ul.appendChild(_li);
        }
        document.getElementById("box_social").appendChild(ul);
    });

    if ($('.external_social').length) {
        var mixcloud = $('[data-mixcloud]').data('mixcloud'),
            facebook = $('[data-facebook]').data('facebook'),
            twitter = $('[data-twitter]').data('twitter');

    if(mixcloud) 
    $.getJSON(baseurl + '/mixcloud/' + mixcloud + '.json', function(data) {
        var li = document.createElement('li'),
            ul = document.createElement('ul'),
            a = document.createElement('a'),
            span = document.createElement('span'),
            _li, _a, _span, playlist = data.data;
        playlist.sort(function(a, b){
            return new Date(b.created_time) - new Date(a.created_time);
        });

        ul.className = "socialtab";
        for (var i = 0; i < playlist.length; i++) {
            _a = a.cloneNode(false);
            _li = li.cloneNode(false);
            _span = span.cloneNode(false);

            _span.appendChild(document.createTextNode(
                new Date(playlist[i].created_time)
                    .toLocaleDateString()));
            _a.appendChild(document.createTextNode(playlist[i].name));
            _li.style.backgroundImage = "url(" +
                playlist[i].pictures.thumbnail +
                ")";
            _a.href = playlist[i].url;
            
            _li.appendChild(_a);
            _li.appendChild(_span);
            ul.appendChild(_li);
        }
        $('.external_social').append(ul);
    });

    }


    $("#showcase img").on('load', function(evt){
        var target = $(evt.currentTarget),
            w = target.width(),
            h = target.height(),
            parent = target.parent(),
            pw = parent.width(),
            ph = parent.height();
        if ( w < pw)
            target.css({width: pw + 'px', height:'auto'});
        else if (h < ph)
            target.css({width:'auto', height: pw + 'px'});
    });
    //delayed style and heavy objects loading
    var resources = $('[data-src]');
    for (var i = 0; i < resources.length; i++) {
        var src = $(resources[i]).data('src');
        var thumb = $(resources[i]).data('thumbnail');
        if (thumb === "s" || thumb === "l")
            src = src.replace(/.([^.]*$)/, thumb + ".$1");
        resources[i].src = src;
    }

    resources = $('[data-background-image]');
    for (i = 0; i < resources.length; i++)
        $(resources[i]).css('background-image', $(resources[i]).data('background-image'));

    //TODO: add event handling
    //$('nav.toplevel li:first-child').on('tap click', function() {
    //}

});
