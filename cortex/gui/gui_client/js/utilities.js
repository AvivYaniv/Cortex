/* ---------------------------------- Functions Section ---------------------------------- */
// Binding function for attaching current object to method upon callback
var bind = function (toObject, methodName) {
    return function (...params) {
      toObject[methodName](...params);
    };
  };

  /* ---------------------------------- Dictionary Section ---------------------------------- */
  // Used for overriding default configurations that are given in dictionary
  var copy_override_dictionary = function(dictDefault, dictNonDefault) {
    if('undefined' !== typeof dictNonDefault){
      for(var i in dictNonDefault){
      if('undefined' !== typeof dictNonDefault[i]){
        dictDefault[i] = dictNonDefault[i];
      }
      }
    }
    return dictDefault;
  };
  
// Used to safe get value form dictionary
var safe_get_value_from_dictionary = function(dictionay, key_name) {
  if (!dictionay.hasOwnProperty(key_name) || null === dictionay[key_name]) 
  {
    return "";
  }
  return dictionay[key_name];
}
