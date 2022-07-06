function resizeWriteBox () {
    var chatContent = document.getElementsByClassName('chat-content')[0];
    var writeBox = document.getElementsByClassName('chat-write-box')[0];

  writeBox.style.width = chatContent.offsetWidth - 30 + 'px';
}

window.onload = function(){
  var mainContainer = document.getElementsByTagName('main')[0];
  resizeWriteBox();
  mainContainer.scrollTop = mainContainer.offsetHeight;

}

window.onresize = function(event) {
  resizeWriteBox();
};
