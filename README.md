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
    - 
 - 상세

| Method    | URL                             |
| --------- | ------------------------------- |
| GET       | api/v1/records                  |
| PUT,PATCH | api/v1/records/record_id        |
| PATCH     | api/v1/records/record_id/delete |
| GET       | api/v1/records/restore          |


  