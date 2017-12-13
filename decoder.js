/**
 * Decoder function as defined in thethingsnetwork app.
 */
function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};
  var currPos = 0;
  var nextKey = 0;
  var currentKey = '';
  decoded = bytes.map(function(i) {
    return String.fromCharCode(i);
  })
  .reduce(function(obj, char){
    obj.bridgeOpen = (obj.bridgeOpen) ? obj.bridgeOpen : [];
    obj.boatPassed = (obj.boatPassed) ? obj.boatPassed : [];

    currentKey = (!currentKey) ? Object.keys(obj)[nextKey] : currentKey;

    if (char === ' ') {
      currPos++;
      return obj;
    }

    if (char === ';') {
      currPos = 0;
      nextKey++;
      currentKey = Object.keys(obj)[nextKey];
      return obj;
    }
    
    obj[currentKey][currPos] = (obj[currentKey][currPos]) ? obj[currentKey][currPos] + char : char;

    return obj;
  }, {});

  decoded = Object.keys(decoded).reduce(function(obj, key) {
    obj[key] = decoded[key].map(function(value) {
      return parseInt(value);
    });
    return obj;
  }, {});
  // if (port === 1) decoded.text = bytes.toString();
  // decoded.port = port;

  return decoded;
}
