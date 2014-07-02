HMC.Home.Handler = function (options) {
    this.Options = {
        KeywordsInputSelector: '#q'
    };
    $.extend(this.Options, options);
    $($.proxy(this.init, this));
}

HMC.Home.Handler.prototype = {
    init: function () {
        var q = HMC.Common.GetQueryStringValue('q');
        $(this.Options.KeywordsInputSelector).val(q);
    }
};