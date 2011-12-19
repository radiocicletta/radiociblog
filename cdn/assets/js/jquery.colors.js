/* Copyright (c) 2008 Gilberto Saraiva (saraivagilberto@gmail.com || http://gsaraiva.projects.pro.br)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 *
 * Version: 2008.0.1.3 -
 * Under development and testing
 *
 * Requires: jQuery 1.2+
 *
 * Support/Site: http://gsaraiva.projects.pro.br/openprj/?page=jquerycolors
 */

(function( $ ){
	$.extend( $ , {
    byteRange: function(v, Ranged){
      if(Ranged != undefined){
        v = Math.round(v);
        if(v > 255) v = 255;
        if(v < 0) v = 0;
      }
      return v
    },
    parseHex2: function(v, Ranged){
      v = Math.round($.byteRange(v, Ranged)).toString(16);
      if (v.length == 1) v = "0" + v;
      return v.toUpperCase();
  	}
  });

  $.color = function( R, G, B, Ranged ) {
		if(!(this instanceof $.color))
      return new $.color( R, G, B );

    this.Data = {
      rgbData: new Array($.byteRange(R || 0, Ranged), $.byteRange(G || 0, Ranged), $.byteRange(B || 0, Ranged))
    };
  };

  $.tocolor = function ( RGB ) {
    if(RGB.charAt(0) == "#"){
      RGB = RGB.substr(1, RGB.length);
    }
    if(RGB == "000") RGB = "000000";
    if(RGB.length == 3){
      r = parseInt("0x" + RGB.substr(0, 1) + "F");
      g = parseInt("0x" + RGB.substr(1, 1) + "F");
      b = parseInt("0x" + RGB.substr(2, 1) + "F");
    }else{
      r = parseInt("0x" + RGB.substr(0, 2));
      g = parseInt("0x" + RGB.substr(2, 2));
      b = parseInt("0x" + RGB.substr(4, 2));
    }
    return $.color( r, g, b, true );
  };

  $.color.prototype = {
    rgb: function (Index, AsHex, Ranged) {
      if(Index != undefined){
        res = $.byteRange(this.Data.rgbData[Index], Ranged)
        if(AsHex)
          res = $.parseHex2(res);
      }else{
        res = this.Data.rgbData;
        if(AsHex != undefined)
          res = Array(
            $.parseHex2(res[0], Ranged),
            $.parseHex2(res[1], Ranged),
            $.parseHex2(res[2], Ranged)
          );
      }

      return res;
    },
    red: function (AsHex, Ranged) {
      return this.rgb(0, AsHex, Ranged);
    },
    green: function (AsHex, Ranged) {
      return this.rgb(1, AsHex, Ranged);
    },
    blue: function (AsHex, Ranged) {
      return this.rgb(2, AsHex, Ranged);
    },
    hexHTML: function () {
      return "#" + this.red(true, true) + "" + this.green(true, true) + "" + this.blue(true, true)
    },
    add: function (mixRGB) {
      if(typeof mixRGB != "object")
        mixRGB = $.tocolor(mixRGB);

      return $.color(
        this.red() + mixRGB.red(),
        this.green() + mixRGB.green(),
        this.blue() + mixRGB.blue()
      );
    },
    sub: function (mixRGB) {
      if(typeof mixRGB != "object")
        mixRGB = $.tocolor(mixRGB);

      return $.color(
        this.red() - mixRGB.red(),
        this.green() - mixRGB.green(),
        this.blue() - mixRGB.blue()
      );
    },
    multiply: function (v){
      if (v == 0)
        return this
      else
        return $.color(
          this.red() * v,
          this.green() * v,
          this.blue() * v
        );
    },
    divide: function (v) {
      if (v == 0)
        return this
      else
        return $.color(
          this.red() / v,
          this.green() / v,
          this.blue() / v
        );
    },
    light: function (v){
      return this.add($.color( v, v, v ));
    },
    shadow: function (v){
      return this.sub($.color( v, v, v ));
    },
    opaque: function (v){
      return this.divide(100).multiply(v);
    }
  };

  $.colorgrad = function( First, Last, Steps ) {
		if(!(this instanceof $.colorgrad))
      return new $.colorgrad( First, Last, Steps );

    Diff = First.sub(Last).divide(Steps);

    this.Data = {
      first: First,
      last: Last,
      diff: Diff,
      steps: Steps
    };
  };

  $.colorgrad.prototype = {
    grad: function(Index){
      if (Index > (this.Data.steps - 1))
        Index = (this.Data.steps - 1);

      if(Index == 0){
        return this.Data.first;
      }else{
        gradDiff = this.Data.diff.multiply(Index);
        return this.Data.first.sub(gradDiff);
      }
    },
    size: function(){
      return this.Data.steps;
    }
  };

  $.colorpalette = function( Color, Light, Shadow, Steps ) {
		if(!(this instanceof $.colorpalette))
      return new $.colorpalette( Color, Light, Shadow, Steps );

    LightDiff = Color.sub(Light).divide(Steps + 1);
    ShadowDiff = Color.sub(Shadow).divide(Steps + 1);

    this.Data = {
      color: Color,
      lightfact: LightDiff,
      shadowfact: ShadowDiff,
      steps: Steps
    };
  };

  $.colorpalette.prototype = {
    pal: function(Index){
      if(Index > (this.Data.steps - 1))
        Index = this.Data.steps;

      if(Index < -(this.Data.steps - 1))
        Index = -this.Data.steps;

      if(Index == 0){
        return this.Data.color;
      }else if(Index > 0){
        gradDiff = this.Data.shadowfact.multiply(Index);
      }else{
        gradDiff = this.Data.lightfact.multiply(Index * -1);
      }
      return this.Data.color.sub(gradDiff);
    },
    light: function(Index){
      return this.pal(Index * -1);
    },
    shadow: function(Index){
      return this.pal(Index);
    },
    size: function(){
      return this.Data.steps;
    }
  };

 })( jQuery );

