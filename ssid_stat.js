/***
 * Counts via mapReduce all the unique ssids in the last 3 hours
 */

// Options
var map = function() { emit(this.ssid, 1); };
var reduce = function(k,v) { return v.length; };
var q = { "time": {$gt: new Date(ISODate().getTime() - 1000*60*60*3)} };
var opt = { "query": q, "out": "ssidstats" }; 

// Start MR
db.packets.mapReduce(map,reduce,opt);

// Get sorted list
db.ssidstats.find().sort({"value": -1})
