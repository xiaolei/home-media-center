window.HMC = window.HMC || {};
HMC.Home = HMC.Home || {};
HMC.Common = HMC.Common || {};

HMC.Common.GetQueryStringValue = function getParameterByName(name, defaultValue) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(window.location.search);
    return results == null ? defaultValue : decodeURIComponent(results[1].replace(/\+/g, " "));
};

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