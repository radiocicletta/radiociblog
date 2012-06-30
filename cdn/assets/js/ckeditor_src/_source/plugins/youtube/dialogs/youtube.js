(function () {
    CKEDITOR.dialog.add('youtube', function (editor) {
        return {
            title: editor.lang.youtube.title,
            minWidth: CKEDITOR.env.ie && CKEDITOR.env.quirks ? 368 : 350,
            minHeight: 240,
            onShow: function () {
                this.getContentElement('general', 'content').getInputElement().setValue('');
            },
            onOk: function () {
                var text = '<object type="application/x-shockwave-flash">' +
                            '<param name="movie" value="https://www.youtube.com/v/'+
                            this.getContentElement('general', 'content').getInputElement().getValue() + 
                            '?version=3&amp;feature=player_embedded">' +
                            '<param name="allowFullScreen" value="true">' +
                            '<param name="allowScriptAccess" value="always">' +
                            '<embed src="https://www.youtube.com/v/' +
                            this.getContentElement('general', 'content').getInputElement().getValue() + 
                            '?version=3&amp;feature=player_embedded"' +
                            'type="application/x-shockwave-flash"' +
                            'allowfullscreen="true" allowScriptAccess="always"/></object>';
                this.getParentEditor().insertHtml(text);
            },
            contents: [{
                label: editor.lang.common.generalTab,
                id: 'general',
                elements: [{
                    type: 'html',
                    id: 'pasteMsg',
                    html: '<div style="white-space:normal;width:500px;"><img style="margin:5px auto;" src="' + CKEDITOR.getUrl(CKEDITOR.plugins.getPath('youtube') + 'images/youtube_large.png') + '"><br />' + editor.lang.youtube.pasteMsg + '</div>'
                }, {
                    type: 'html',
                    id: 'content',
                    style: 'width:340px;height:90px',
                    html: '<input size="25" style="' + 'border:1px solid black;' + 'background:white">',
                    focus: function () {
                        this.getElement().focus();
                    }
                }]
            }]
        };
    });
})();
