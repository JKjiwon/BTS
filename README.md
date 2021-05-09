# RecomendTour (여행지 추천 REST API)
## 1. 프로젝트 소개
* Django를 이용한 회원(User), 여행지(Lcation) 정보 저장용 REST API 구현
* 여행지 정보에 대한 CRUD 시스템 구현
* JWT 토큰을 이용한 Authentication 및 Authorization 구현

<br>

## 2. 코드 다운로드
Repository 클론

`git clone https://github.com/JKjiwon/RecomendTour.git`

<br>

## 3. Project Dependencies 설치

pipenv 를 통해 가상환경을 구성하고, 다음 명령어를 입력

`pipenv install -r requirements.txt`

`pipenv install -r requirements-dev.txt --dev`

<br>

## 4. 가상환경 시작

`pipenv shell`

<br>

## 5. 데이터 베이스 설치

`python manage.py makemigrations`

`python manage.py migrate`

<br>

## 6. 서버 실행
`python manage.py runserver` 로 서버 실행 후 **127.0.0.1:8000** 로 접근

<br>

## 7. End Points
* 인증( JWT Token) 발급 및 갱신 관련 리소스

|HTTP|Path|Permission|목적|
|---|---|---|---|
|POST|/users/login|NONE|로그인 시  JWT Token 반환|
|POST|/users/refresh|JWT Token|JWT Token 검증 후 새로운 토큰 반환|
|GET|/users/validate|JWT Token|JWT Token 검증|

<br>

* 회원(User) 관련 리소스

|HTTP|Path|Permission|목적|
|---|---|---|---|
|POST|/users|NONE|유저 생성|
|GET|/users|JWT Token + SuperUser|모든 유저 정보 조회|
|GET|/users/{id}|JWT Token + SuperUser|{id}의 유저 정보 조회|
|GET|/users/me|JWT Token|요청한 유저의 정보 반환|
|PUT|/users/me|JWT Token|요청한 유저의 정보 수정|
|PUT|/users/me/changepssword|JWT Token|유저 비빌번호 변경
|DELETE|/users/me|JWT Token|요청한 유저의 정보 삭제|

`SuperUser : python manage.py createsuperuser 로 생성한 유저`

<br>

* 회원이 좋아하는 장소 관련 리소스

|HTTP|Path|Permission|목적|
|---|---|---|---|
|GET|/users/me/favs|JWT Token|요청한 유저의 좋아하는 여행지 조회|
|PUT|/users/me/favs|JWT Token|요청한 유저의 좋아하는 여행지 수정|

<br>

* ID/비밀번호 찾기 관련 리소스

|HTTP|Path|Permission|목적|
|---|---|---|---|
|POST|users/findusername|NONE|회원 이름, 전화번호 입력시 ID 반환|
|POST|users/findpassword|NONE|회원 이름, 전화번호, ID 입력시 password 초기화 후 반환|

<br>

* 여행지(Location) 관련 리소스

|HTTP|Path|Permission|목적|
|---|---|---|---|
|POST|/locations|JWT Token|새로운 여행지 정보 생성|
|GET|/locations|NONE|모든 여행지 정보 조회|
|GET|/locations/{id}|NONE|{id}의 여행지 정보 조회|
|PUT|/locations/{id}|JWT Token|{id}의 여행지 정보 수정|
|DELETE|/locations/{id}|JWT Token|{id}의 여행지 정보 삭제|

<br>

* 여행지(Location) 관련 리소스 : Filtering AND Searching

|HTTP|Path|Permission|목적|
|---|---|---|---|
|GET|/locations|Name, City, Category, Creator|Parms와 일치하는 정보 조회|
|GET|/locations|Search|Name, Description, City 관련 정보 조회|

<br>

* 여행지 사진(Photo) 관련 리소스

|HTTP|Path|Permission|목적|
|---|---|---|---|
|POST|/locations/photos|JWT Token|새로운 여행지 사진 정보 생성|
|GET|/locations/photos|NONE|모든 여행지 사진 정보 생성|
|GET|/locations/{id}|NONE|{id}의 여행지 사진 정보 조회|
|PUT|/locations/{id}|JWT Token|{id}의 여행지 사진 정보 수정|
|DELETE|/locations/{id}|JWT Token|{id}의 여행지 사진 정보 삭제|

<br>

## 8. 데이터베이스 스키마와 관계

<img src="database_schema.png" height="400">

* 하나의 사용자(User) 모델은 다수의 여행지(Location)모델을 가질 수 있다.
* 하나의 여행지(Location)모델은 다수의 사진(Photo) 모델을 가질 수 있다.
* 다수의 사용자(User) 모델은 다수의 여행지(Location)모델을 가질 수 있다.


