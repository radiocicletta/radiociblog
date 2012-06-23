/*
Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

(function(){CKEDITOR.dialog.add('youtube',function(a){return{title:a.lang.youtube.title,minWidth:CKEDITOR.env.ie&&CKEDITOR.env.quirks?368:350,minHeight:240,onShow:function(){this.getContentElement('general','content').getInputElement().setValue('');},onOk:function(){var b='<iframe title="YouTube video player" class="youtube-player" type="text/html" width="480" height="390" src="http://www.youtube.com/embed/'+this.getContentElement('general','content').getInputElement().getValue()+'?rel=0" ></iframe>';this.getParentEditor().insertHtml(b);},contents:[{label:a.lang.common.generalTab,id:'general',elements:[{type:'html',id:'pasteMsg',html:'<div style="white-space:normal;width:500px;"><img style="margin:5px auto;" src="'+CKEDITOR.getUrl(CKEDITOR.plugins.getPath('youtube')+'images/youtube_large.png')+'"><br />'+a.lang.youtube.pasteMsg+'</div>'},{type:'html',id:'content',style:'width:340px;height:90px',html:'<input size="25" style="border:1px solid black;background:white">',focus:function(){this.getElement().focus();}}]}]};});})();
