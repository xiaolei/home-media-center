window.HMC = window.HMC || {};
HMC.Home = HMC.Home || {};
HMC.Common = HMC.Common || {};

HMC.Common.GetQueryStringValue = function getParameterByName(name, defaultValue) {
    name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(window.location.search);
    return results == null ? defaultValue : decodeURIComponent(results[1].replace(/\+/g, " "));
};

HMC.Common.EnableAdminSwitcher = function enableAdminSwitcher(selector) {
    $(selector).animate({ width: 'toggle' });
};

HMC.Common.ActiveMenuItem = function activeMenuItem(selector) {
    $(selector).toggleClass('selected');
};