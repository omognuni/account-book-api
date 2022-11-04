# 가계부 API

### 설치
- git clone 후 다음 명령어 실행
```
docker-compose up --build
```
- 테스트 결과 확인
```
docker-compose run --rm store sh -c 'python manage.py test'
```
- 테스트 코드는 각 app 들의 tests 폴더 참조
  - stock/core/tests
  - stock/user/tests
  - stock/record/tests
  
<img src='/images/test.PNG'>


### ERD
- DB는 MySQL 5.7 사용
<img src='/images/ERD.png'>

### User
- 이용자
- email & password 로 회원가입

| 내용                 | Method | URL             |
| -------------------- | ------ | --------------- |
| 회원가입             | POST   | api/user/create |
| Token 인증           | POST   | api/user/token  |
| 로그아웃(Token 삭제) | GET    | api/user/logout |

### 가계부 내역(Record)
- 조회
  - category: 카테고리(현금, 카드 등)
  - amount: 금액 

- 상세
  - category: 카테고리(현금, 카드 등)
  - amount: 금액 
  - memo: 메모
  - created_at: 생성 시간
  - updated_at: 업데이트 시간
- 삭제
  - soft delete 구현
  - 해당 URL로 요청을 보낼때마다 is_deleted의 상태가 토글
  - ex) is_deleted=False 인 상태에서 보내면 True로 바뀌고 \
  is_deleted=True 인 상태에서 보내면 False로 바뀜
  - is_deleted = True 일 경우 조회 목록에 나오지 않음
- 복구
  - is_deleted = True인 내역들만 조회
  - 해당 내역의 record_id의 삭제 URL로 다시 요청을 보내면 \
is_deleted = False 로 바뀌는 방식

| 내용                  | Method    | URL                             |
| --------------------- | --------- | ------------------------------- |
| 조회                  | GET       | api/v1/records                  |
| 상세                  | GET       | api/v1/records/record_id        |
| 업데이트              | PUT,PATCH | api/v1/records/record_id        |
| 삭제                  | PATCH     | api/v1/records/record_id/delete |
| 복구를 위한 삭제 내역 | GET       | api/v1/records/restore          |


  