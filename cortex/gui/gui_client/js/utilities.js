// Binding function for attaching current object to method upon callback
var bind = function (toObject, methodName) {
    return function (x) {
      toObject[methodName](x);
    };
  };
  