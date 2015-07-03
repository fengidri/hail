function getPerformance()
{
    var performance = undefined;

    performance = window.performance;
    if (performance)
        return performance;

    performance = window.webkitPerformance
    if (performance)
        return performance;

    performance = window.msPerformance
    if (performance)
        return performance;

    performance = window.mozPerformance;
    if (performance)
        return performance;
    else{
        var msg = 'Unfortunately, This browser does not support the Navigation Timing API';
        console.log(msg);
        return;
    }
}


function getFirstPaint(timing, _times)
{
    var times = _times || {};

    // All timing are relative timing to the start time within the
    // same objects
    var firstPaint = 0;

    // Chrome
    if (window.chrome && window.chrome.loadTimes) {
        // Convert to ms
        firstPaint = window.chrome.loadTimes().firstPaintTime * 1000;
        times.firstPaintTime = firstPaint - (window.chrome.loadTimes().startLoadTime*1000);
    }
    // IE
    else if (typeof timing.msFirstPaint === 'number') {
        firstPaint = timing.msFirstPaint;
        times.firstPaintTime = firstPaint - window.performance.timing.navigationStart;
    }
    times.firstPaint = firstPaint;
}

function getTiming(timing, _times)
{
    var times = _times || {};
    // DNS query time
    times.lookupDomain = timing.domainLookupEnd - timing.domainLookupStart;
    // TCP connection time
    times.connect = timing.connectEnd - timing.connectStart;

    if (timing.secureConnectionStart)
        times.sslcon = timing.connectEnd - timing.secureConnectionStart;
    else
        times.sslcon = 0;

    // Time spent during the request
    times.waiting = timing.responseStart - timing.requestStart;
    // Time spent during the request
    times.download = timing.responseEnd - timing.responseStart;

    if (timing.duration)
    {
        times.loadTime = timing.duration;
    }
    else{
        var end = timing.loadEventStart;
        if (end == 0)
            end = timing.domComplete;

        times.loadTime = end - timing.navigationStart;
    }

    if (timing.name)
        times.name = timing.name;
    else
        times.name = window.location.href;

    return times;
}

function getDomTiming(){
    var performance = getPerformance()
    for (var k  in performance)
    {
        console.log(k);
    }

    if (performance === undefined)
        return;

    var timing = performance.timing;
    var times_array = [];

    if (!timing) return {};

    times_array.push(getTiming(timing));
    //var timings = performance.getEntries();

    //console.log(timings.length);
    //for (var _ in timings)
    //{
    //    var t = getTiming(timings[_]);
    //    times_array.push(t);
    //}
    return times_array;

}

json = JSON.stringify(getDomTiming())
console.log(json)












