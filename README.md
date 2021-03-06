## Instagram Bot : Auto Following Cancel version

* 개요 : 자동으로 팔로잉하는 봇을 만든 이후 팔로잉의 숫자가 너무 많아서 피드가 복잡해졌다.
* 원리 : 모바일 인스타그래 앱으로 접속 시, 상대방의 팔로잉 목록 상단에 내 아이디가 있는지 확인하는 방식으로 맞팔인지 여부를 알 수 있다.
* 구현 : Python (Pyautogui / Pytesseract / OpenCV)

## Algorithm
1) 인스타그램 접속 후, 나의 팔로잉 목록으로 이동한다.
2) 사람들의 팔로잉 목록에 들어가서 pyautogui 를 통해 캡처한다.
3) 캡처된 이미지 속의 글자를 추출한다. 이 때 pytesseract 를 이용한다.
  * 캡처된 이미지 속에서 한국어 글자의 인식율이 떨어지는 경향이 있었다. 
  -> OpenCV를 통하여 Gray Scale로 전처리 후, 인식하도록 하였다.
4) 팔로잉 목록에 내가 존재하면, 관계를 유지한다.
5) 만약 나만 팔로잉하고 있는 상태라면 팔로우를 끊는다.
  * 이 때 끊고자하는 상대방의 계정의 공개여부에 따라 팔로우취소 방법이 달랐다.
  -> 이 역시 팝업창이 떴는지의 인식 및 판단하여 수행하였다.
6) 수집된 유저들의 아이디, 맞팔 여부, 공개 계정 여부 등에 대하여 Dataframe을 작성하여 Excel파일로 export하였다.
  * 향후에 자동화 봇을 만들 때, 맞팔을 안한 아이디는 선팔에 제한을 두는 등의 데이터로 사용 가능 

## Future Works
1) 생각보다 한글의 경우 pytesseract 의 인식율이 매우 낮았다. 
2) 좌표를 통한 pyautogui 를 사소한 좌표 변화에도 크게 작용하였다.
3) 라이브방송, 댓글언급, 팔로우시작 등의 알림창이 앱내에서 계속 동작하여 진행에 어려움이 있었다.

## Development environment
* 노트북 : MacOS Bigsur 11.2
* 모바일 : Android
* 맥북과 안드로이드 폰의 미러링을 위한 "scrcpy" 사용

## Youtube Link
https://www.youtube.com/watch?v=D1THp4d3xQM&feature=youtu.be
