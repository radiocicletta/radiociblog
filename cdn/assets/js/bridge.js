/*  BridgeJS 1.0.5
 *  (c) 2010-2011 Nick Stakenburg - http://www.nickstakenburg.com
 *
 *  Bridge is freely distributable under the terms of an MIT-style license.
 *
 *  Adapter API largely based on PrototypeJS (http://www.prototypejs.org)
 *
 *  GitHub: https://github.com/staaky/bridgejs
 */

(function() {
var _Bridge = window.Bridge;

var Bridge = {
  Version: '1.0.5',

  options: {
    adapter: 'auto', // one of 'Prototype', 'jQuery' or 'auto'
    path:    false
  },

  Framework: {
    jQuery: {
      included: !!window.jQuery && jQuery.fn.jquery,
      required: '1.5'
    },
    Prototype: {
      included: !!window.Prototype && Prototype.Version,
      required:  '1.7'
    }
  },

  insertScript: function(source) {
    try {
      document.write("<script type='text/javascript' src='" + source + "'><\/script>");
    } catch(e) {
      var head = document.head || document.getElementsByTagName('head')[0],
          script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = source;
      head.appendChild(script);
    }
  },

  start: function() {
    // Version check, works with 1.2.10.99_beta2 notations
    var VERSION_STRING = /^(\d+(\.?\d+){0,3})([_-]+[A-Za-z0-9]+)?/;
    function convertVersionString(versionString) {
       var vA = versionString.match(VERSION_STRING),
           nA = vA && vA[1] && vA[1].split('.') || [],
           v  = 0;
       for (var i = 0,l = nA.length;i<l;i++)
         v += parseInt(nA[i] * Math.pow(10,6-i*2));
       return vA && vA[3] ? v - 1 : v;
    }
    function hasRequiredVersion(available, required) {
      return (convertVersionString(available) >= convertVersionString(required));
    }

    // extend options if window.Bridge.options is set for easier framework toggling
    if (_Bridge && _Bridge.options) {
      for (var prop in _Bridge.options)
        Bridge.options[prop] = _Bridge.options[prop];
    }

    var isAuto = this.options.adapter == 'auto';
  
    // find a framework when we auto detect or when we don't auto detect
    // and selected framework is not available
    if (isAuto || (!isAuto && this.Framework[this.options.adapter] && 
     !this.Framework[this.options.adapter].included)) {
      this.options.adapter = null;
      for (var framework in this.Framework) {
        var F = this.Framework[framework];
        if (F.included && hasRequiredVersion(F.included, F.required)) {
          this.options.adapter = framework;
        }
      }

      // throw error when we don't have a framework
      if (!this.options.adapter || this.options.adapter == 'auto') {
        var frameworks = [];
        for (framework in this.Framework) {
          frameworks.push(framework + ' >= ' + this.Framework[framework].required);
        }

        var list = frameworks.join(', '),
            lastComma = list.lastIndexOf(', ');

        if (lastComma) {
          list = list.substring(0, lastComma) + ' or ' +
                 list.substring(lastComma + 2);
        }

        alert("BridgeJS requires " + list + " included before bridge.js");
      }
    }

    if (this.options.path && /^(https?:\/\/|\/)/.test(this.options.path)) {
      this.path = this.options.path;
    } else {
      var scripts = document.getElementsByTagName('script'),
          srcMatch = /bridge([\w\d-_.]+)?\.js(.*)/;
      for (var i = 0, l = scripts.length; i < l; i++) {
        var script = scripts[i];
        if (script.src.match(srcMatch)) {
          this.path = script.src.replace(srcMatch, '');
        }
      }
    }

    this.insertScript(this.path + 'adapters/shared.js');
    this.insertScript(this.path + 'adapters/' + this.options.adapter.toLowerCase() + '.js');
  }
};

// TODO: Create Bridge.fx to wrap adapters around Scripty2

window.Bridge = Bridge;
Bridge.start();
})();
