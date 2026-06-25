(function () {
  'use strict';

  var btnTop = document.getElementById('experienciasDetailBtnTop');

  if (!btnTop) {
    return;
  }

  btnTop.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}());
