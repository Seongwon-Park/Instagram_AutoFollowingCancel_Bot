from utils import *

# 반복할 시작값과 끝값을 지정
start = 0
end = 700

# 내 아이디 설정
my_id = 'smile._.wonnie'
previous_user_id = 'smile._.wonnie'

# 결과를 저장할 데이터 프레임 생성
result_df = create_result_df()

# 인스카그램 실행 및 최근 팔로잉 목록으로 정렬
set_ordering()

print('중간지점부터 시작하기 위해 스크롤을 시작합니다.')
# 중간부터 시작하기 위한 스크롤
for i in range(0, 40):
    pag.scroll(-3)
    time.sleep(1)

# 반복문 시작
for i in range(start, end + 1):
    # 에러 여부
    id_error = 0
    button_error = 0
    private_error = 0

    # 비공개 계정인지 여부
    private = 0

    # 20개의 데이터가 수집될 때마다 자동저장
    if (i % 20 == 0) and (i > 0):
        result_df = auto_save_excel(result_df)

    # 유저 아이디 인식
    user_id = detect_user_id(i)

    # 이전 유저의 아이디와 같다면 오류
    id_error = compare_user_id(previous_user_id, user_id)

    # 유저 아이디에 대한 오류가 없을 경우
    if id_error != 1:
        previous_user_id = user_id
        # 상대방이 팔로잉을 하고 있는지 여부를 반환
        following = following_detect(my_id)

        # 상대방도 나를 팔로잉하고 있을 경우
        if following == 1:
            result_df = following_true(user_id, result_df, i)

        # 상대방은 나를 맞팔하고 있지 않을 경우
        else:
            # 문구 출력
            print('{} 님은 나를 팔로잉하고 있지 않습니다.'.format(user_id))

            # 뒤로 가기 클릭
            pag.click((1367, 759))
            time.sleep(3)

            # 언팔을 하기 위한 팔로잉 버튼 감지 및 클릭
            button_error, result_df = detect_following_button(user_id, result_df, i)

            # 팔로잉 버튼을 정상적으로 찾았을 경우
            if button_error != 1:
                # 비공개 계정에 대한 알림창이 팝업되었는지 감지
                private = detect_private_popup(private)

                # 비공개 계정일 경우
                if private == 1:
                    result_df = private_user_following_cancel(result_df, user_id, i)

                # 공개 계정일 경우
                elif private == 0:
                    result_df = public_user_following_cancel(result_df, user_id, i)

# 최종 결과를 엑셀로 저장
result_df.to_excel('final_following_result.xlsx')