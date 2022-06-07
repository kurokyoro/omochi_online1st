
$(function () {  // ここはお約束
// <!-- 以下question_mordalを呼び出す用のボタン OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO-->
$(function(){
  $('.js-modal-open').on('click',function(){
      $('.js-modal').fadeIn();
      return false;
  });
  $('.js-modal-close').on('click',function(){
      $('.js-modal').fadeOut();
      return false;
  });
});

  // <!-- 以下question_mordalを呼び出す用のボタン OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO-->




  ////////////////////////////
  // ここからプラグイン用の記述 //
  ///////////////////////////

  // スライドイン
  $(window).fadeThis();

  //ドロワーメニュー
  $(".drawer").drawer();





});