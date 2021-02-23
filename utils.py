import re
import cv2
import time
import pandas as pd
import pyautogui as pag
import pytesseract

try:
    import Image
except ImportError:
    from PIL import Image


# 결과를 저장할 데이터프레임 생성
def create_result_df():
    result_df = pd.DataFrame(columns=['Instagram_ID', 'Following', 'Private'])
    return result_df


# 현재 시스템의 시간을 반환하는 함수
def get_current_time():
    now = time.localtime()
    return now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min


# 현재까지 저장된 데이터 프레임을 엑셀 파일로 저장하는 함수
def auto_save_excel(result_df):
    result_df = result_df.dropna(axis=0)
    tm_year, tm_mon, tm_day, tm_hour, tm_min = get_current_time()
    result_df.to_excel('following_result_{}_{}_{}_{}:{}.xlsx'.format(tm_year, tm_mon, tm_day, tm_hour, tm_min))
    print('결과 데이터의 중간 저장을 완료하였습니다.')
    return result_df


# 인스타그램 정렬기준을 최신으로 맞추는 클릭까지 포함하는 함수
def set_ordering():
    # scrcpy 창 클릭
    pag.click((1354, 701))
    time.sleep(2)

    # 홈메뉴 클릭
    pag.click((1354, 701))
    time.sleep(2)

    # 인스타그램 어플을 클릭하여 실행
    pag.click((1208, 194))
    print('인스타그램 어플에 접속하였습니다.')
    time.sleep(5)

    # 내 프로필을 클릭하여 실행
    pag.click((1407, 716))
    print('내 프로필로 이동하였습니다.')
    time.sleep(5)

    # 팔로잉 목록을 클릭하여 실행
    pag.click((1390, 184))
    print('팔로잉 목록으로 이동하였습니다.')
    time.sleep(5)

    # 정렬 기준을 최신 순으로 클릭하여 실행
    # 화살표 터치
    pag.click((1418, 476))
    time.sleep(4)

    # 팔로우한 날짜 : 최신순 터치
    pag.click((1417, 671))
    print('정렬을 최신순으로 변경하였습니다.')
    time.sleep(4)

    # 반복시작
    print('맞팔하지 않은 사람의 언팔을 시작합니다.\n\n')


# 유저의 아이디를 인식하여 반환하는 함수
def detect_user_id(i):
    # 사람 프사 클릭 및 대기
    print('{} 번째 회원님을 클릭합니다.'.format(i + 1))
    pag.click((1196, 531))
    print('로딩을 위해 10초간 대기를 시작합니다.')
    time.sleep(10)

    print('유저 아이디를 얻기 위해 캡처를 진행합니다.')

    # 라이브 방송 알림 때문에 아이디가 가려서 인식이 안되는 경우 방지
    while True:
        pag.screenshot('user_id_image.png', region=(2270, 215, 490, 90))

        # 라이브 방송에 대한 알림 창인지 감지
        live_detect_list = pytesseract.image_to_string(Image.open('user_id_image.png'), lang='kor')
        live_detect_list = ''.join(live_detect_list)
        if ('라이브' in live_detect_list) or ('방송' in live_detect_list):
            print('라이브 방송 알림이 감지되었습니다. 새로운 캡처를 진행합니다.')
            time.sleep(3)
        else:
            print('라이브 방송 알림이 감지되지 않았습니다.')
            break

    # 이미지 파일에서 글자 추출 (유저 아이디를 얻기 위해)
    user_id_list = pytesseract.image_to_string(Image.open('user_id_image.png'))

    # 엔터를 기준으로 나누어 리스트에 저장
    user_id_list = re.split('\n', user_id_list)

    # 리스트 내의 첫번째 값을 유저의 이름으로 지정
    user_id = user_id_list[0]
    print('유저 아이디를 인식하는 데에 성공하였습니다. : {}'.format(user_id))
    return user_id


# 에러를 감지하는 함수
def detect_error(user_id):
    # 라이브 방송 알림 때문에 아이디가 가려서 인식이 안되는 경우 방지
    while True:
        pag.screenshot('error_detect_image.png', region=(2270, 215, 490, 90))
        # 라이브 방송에 대한 알림 창인지 감지
        live_detect_list = pytesseract.image_to_string(Image.open('user_id_image.png'), lang='kor')
        live_detect_list = ''.join(live_detect_list)
        if ('라이브' in live_detect_list) or ('방송' in live_detect_list):
            print('라이브 방송 알림이 감지되었습니다. 새로운 캡처를 진행합니다.')
            time.sleep(3)
        else:
            print('라이브 방송 알림이 감지되지 않았습니다.')
            break
    # 이미지 파일에서 글자 추출 (유저 아이디를 얻기 위해)
    error_list = pytesseract.image_to_string(Image.open('error_detect_image.png'))
    # 엔터를 기준으로 나누어 리스트에 저장
    error_list = re.split('\n', error_list)
    # 리스트 내의 첫번째 값을 유저의 이름으로 지정
    error_detect = error_list[0]
    if error_detect == user_id:
        print('에러없이 팔로우 취소가 완료 되었습니다.')
    elif error_detect == 'AALS':
        print('게시글로 들어왔습니다. 유저 프로필 화면으로 돌아갑니다.')
        # 뒤로 가기 클릭
        pag.click((1367, 759))
        time.sleep(3)


# 이전 유저의 아이디와 현재 유저 아이디를 비교
def compare_user_id(previous_user_id, user_id):
    if previous_user_id == user_id:
        error = 1
        print('[ERROR] 이전의 사용자와 같은 사용자입니다.')
        print('초기 팔로잉 목록으로 돌아갑니다.\n\n')
        # 뒤로 가기 클릭 및 스크롤
        pag.click((1367, 759))
        time.sleep(2)
        pag.moveTo((1275, 500))
        time.sleep(2)
        pag.scroll(-1)
        time.sleep(2)
    else:
        error = 0
    return error


# 맞팔인지 여부를 확인하는 함수
def following_detect(my_id):
    # 사람 창에서 팔로잉 클릭
    pag.click((1392, 186))
    print('팔로잉 목록 대기를 위하여 잠시 대기합니다.')
    time.sleep(15)

    # 맨 위와 그 아랫줄 (총 2줄)에서 나의 프로필 명이 인식되는지 확인
    print('팔로잉 목록 내에 사용자가 존재하는지 여부를 확인하기 위해 캡처를 진행합니다.')
    pag.screenshot('following.png', region=(2220, 450, 452, 235))

    # 이미지 파일에서 글자 추출
    converted_str = pytesseract.image_to_string(Image.open('following.png'))

    # 엔터를 기준으로 나누어 리스트에 저장
    following_list = re.split('\n', converted_str)

    if my_id in following_list:
        following = 1
    else:
        following = 0
    return following


# 맞팔하고 있을 경우 실행되는 함수
def following_true(user_id, result_df, i):
    print('{} 님과 맞팔입니다.'.format(user_id), end=' ')
    print('현재 관계를 계속 유지합니다.')
    result_df.loc[i] = [user_id, 'Yes', 'Unknown']
    time.sleep(3)
    print('결과 데이터에 추가를 완료하였습니다.')
    # 뒤로 가기 2번 클릭
    pag.click((1367, 759))
    time.sleep(3)
    pag.click((1367, 759))
    time.sleep(3)
    # 마우스 위치 옮기기 (특정 영역을 벗어나면 스크롤이 되지 않음)
    pag.moveTo((1275, 500))
    time.sleep(3)
    pag.scroll(-1)
    time.sleep(3)
    print('스크롤을 완료하였습니다. 다음 사람에게로 이동합니다.\n\n')
    time.sleep(3)
    return result_df


# 팔로잉 버튼을 감지하는 함수
def detect_following_button(user_id, result_df, i):
    # 팔로잉 버튼 찾기 및 클릭
    row_num = 0
    y_coord = 263
    print('팔로잉 버튼의 좌표값을 찾는 중입니다.')
    for j in range(510, 1200, 31):
        pag.screenshot('find_button.png', region=(2270, j, 400, 45))
        time.sleep(2)
        converted_btn_str = pytesseract.image_to_string(Image.open('find_button.png'), lang='kor')
        time.sleep(2)
        user_id_list = re.split('\n', converted_btn_str)
        button = ''.join(user_id_list)
        print('{0} 번째 데이터 : {1}'.format(row_num, button))
        if ('팔로잉' in button) or ('메시' in button):
            print('{} 님의 자기소개란은 {} 줄 입니다.'.format(user_id, row_num), end=' ')
            pag.moveTo(1177, y_coord)
            print('팔로잉 버튼으로 이동 완료하였습니다.')
            time.sleep(3)
            pag.click()
            time.sleep(3)
            error = 0
            # 팔로우 취소를 클릭
            print('팔로잉 취소 버튼을 누릅니다.')
            pag.click((1130, 707))
            time.sleep(3)
            break
        row_num += 1
        y_coord += 17
        if j > 950:
            print('[ERROR] 팔로잉 버튼을 찾을 수 없습니다.')
            result_df.loc[i] = [user_id, 'No', 'ERROR']
            print('결과 데이터에 추가를 완료하였습니다.')
            print('현재 수행 중인 작업을 중단하고 다음 사람에게로 이동합니다.\n\n')
            # 뒤로 가기 클릭
            pag.click((1367, 759))
            time.sleep(3)
            pag.moveTo((1275, 500))
            time.sleep(2)
            pag.scroll(-1)
            time.sleep(3)
            error = 1
            break
    return error, result_df


# 비공개 계정의 알림창을 감지하는 함수
def detect_private_popup(private):
    print('비공개 계정 유저의 팝업창을 감지 중입니다.')
    # 알림창에서 인식될 수 있는 단어들의 리스트
    private_word = ['생각이', '바뀌면', '팔로우를', '다시', '요청할', '수 있습니다']
    # 비공개 유저의 경우 알림창 나옴
    pag.screenshot('private_user_image.png', region=(2350, 850, 400, 80))
    # opencv 를 이용하여 gray scale 로 전처리
    src = cv2.imread("private_user_image.png", cv2.IMREAD_COLOR)
    dst = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('private_user_image.png', dst)
    # 이미지 파일에서 글자 추출
    converted_str = pytesseract.image_to_string(Image.open('private_user_image.png'), lang='kor')
    # 엔터를 기준으로 나누어 리스트에 저장
    private_list = re.split('\n', converted_str)
    # 한 줄로 통합
    private_list = ''.join(private_list)
    for p in private_word:
        if p in private_list:
            print('비공개 계정 알림창이 감지되었습니다. : {}'.format(p))
            private = 1
            break
    return private


# 비공개 계정을 사용하는 유저의 팔로우 취소
def private_user_following_cancel(result_df, user_id, i):
    print('비공개 계정을 사용 중인 유저입니다.')
    result_df.loc[i] = [user_id, 'No', 'Yes']
    print('결과 데이터에 추가를 완료하였습니다.')
    pag.click((1270, 494))
    time.sleep(5)
    print('{} 님의 팔로우 취소를 완료하였습니다.'.format(user_id))
    detect_error(user_id)
    # 뒤로 가기 클릭
    pag.click((1367, 759))
    time.sleep(3)
    # 마우스 위치 옮기기 (특정 영역을 벗어나면 스크롤이 되지 않음)
    pag.moveTo((1275, 500))
    time.sleep(3)
    pag.scroll(-1)
    time.sleep(3)
    print('스크롤을 완료하였습니다. 다음 사람에게로 이동합니다.\n\n')
    return result_df


# 공개 계정을 사용하는 유저의 팔로우 취소
def public_user_following_cancel(result_df, user_id, i):
    print('공개 계정을 사용 중인 유저입니다.')
    result_df.loc[i] = [user_id, 'No', 'No']
    print('결과 데이터에 추가를 완료하였습니다.')
    print('{} 님의 팔로우 취소를 완료하였습니다.'.format(user_id))
    detect_error(user_id)
    # 뒤로 가기 클릭
    pag.click((1367, 759))
    time.sleep(2)
    # 마우스 위치 옮기기 (특정 영역을 벗어나면 스크롤이 되지 않음)
    pag.moveTo((1275, 500))
    time.sleep(2)
    pag.scroll(-1)
    time.sleep(3)
    print('스크롤을 완료하였습니다. 다음 사람에게로 이동합니다.\n\n')
    return result_df
