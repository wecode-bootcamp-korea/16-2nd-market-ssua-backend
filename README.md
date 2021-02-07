# TEAM Market Ssua 💟 🛒 🚛 
#### 2021.01.25 ~ 2021.02.05
안녕하세요, 마켓 컬리 [market kurly](https://www.kurly.com/shop/main/index.php) 사이트의 클론 코딩 프로젝트를 진행하게 된 `Team Market ssua` 입니다. 마켓컬리는 대한민국의 온라인 식재료 판매업체입니다. '문 앞 까지 신선함을 제공하는 샛별배송' 이라는 슬로건으로 새벽 배송을 특성화하여 바쁜 현대인들의 일상에 스며들게 되었습니다. 마켓컬리는 여러 식재료 뿐만 아니라 생활용품, 반려동물 용품까지 광범위하게 취급하며, 상품 그룹 마다 별도의 상품 종류를 갖추고 있어 모델링 단계부터 다른 사이트들과의 차별점을 느낄 수 있었습니다.<br>
2주의 프로젝트 기간동안 User - Product - Order application 기능 구현에 힘써, 초기에 계획했던 기능들을 전부 구현하는데에 성공하였습니다. 계획된 기능들로는 로그인, 회원가입, 카카오를 이용한 소셜로그인, 상품 리스트, pagination, 장바구니 및 소비자의 주소 / 최소가격을 이용한 배송비 계산 등이 있습니다.
## Preview 
[![team marketssua](https://images.velog.io/images/sue517/post/fe661ddf-7d57-4d03-84d4-d2f679d9efa2/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-02-06%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%204.29.42.png)]('https://youtu.be/ifrAm2Tn6PE')
##### 이미지를 클릭하면 영상으로 이동됩니다.

## Member 🕺🏻 <br>
### Front <a href="https://github.com/wecode-bootcamp-korea/16-2nd-market-ssua-frontend"> git repo </a> <br>
정재윤 <a href="https://github.com/sbjeong222"> git repo </a> // 이필제 <a href="https://github.com/xxpiiiide"> git repo </a> // 문규찬 <a href="https://github.com/moonkyuchan"> git repo </a> // 김동하 <a href="https://github.com/finalslug"> git repo</a> <br>
### Back <a href="https://github.com/wecode-bootcamp-korea/16-2nd-market-ssua-backend"> git repo </a> <br>
김준형 <a href="https://github.com/ddalkigum"> git repo </a> // 최수아 <a href="https://github.com/sue517"> git repo</a> <br>
## Back Technologies 🛠
- Python
- Django
- MySQL
- JWT, Bcrpyt
- Git & GitHub
- AWS EC2, RDS
- docker

## Progress ⛓
- <a href="https://trello.com/b/JBzF7qXW/market-ssua"> TEAM Trello </a> <br>
trello 를 이용하여 서로간의 진행 상황을 공유할 수 있도록 하였습니다. trello 는 front / back 의 부분으로 나누어져 구분되어 있으며, 진행중인 사항에도 내부에 check list 를 달아 보다 더 상세한 진행 사항을 표시해 두었습니다. 또, 매일 daily stand-up meeting 을 진행하고 해당 회의 결과를 trello 의 왼쪽 카테고리에 기록해두어 지난 회의에 어떤 의견이 오고 갔는지, 진척 상황은 어떻게 되어가는지를 상세히 알 수 있도록 하였습니다.
- <a href="https://www.notion.so/51571f832f014d94a70d2b1ca36c7c39"> API document notion </a> <br>
front / back 간의 의사 소통을 수월히 하기 위하여 Json API document 를 Notion 으로 만들어 공유하였습니다. 

## Modeling 📑
<img src="https://media.vlpt.us/images/sue517/post/3c651f75-a713-4047-8186-ea695ef55ef7/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-01-27%20%E1%84%8B%E1%85%A9%E1%84%8C%E1%85%A5%E1%86%AB%202.13.48.png">

## Functions 🔍
- 회원가입
- bcrypt 를 이용한 비밀번호 암호화
- JWT 를 이용하여 access token 발행
- 로그인 // decorator 생성
- kakao 소셜 로그인
- 상품 리스트, 상세 페이지
- self join 을 통해 상세페이지에서 연관된 상품리스트 확인 가능
- 상품 검색, 필터
- 상품 문의 CRUD
- seed 를 이용헤 database 자동 생성 및 구축
- 장바구니 기능
- 소비자의 주소(location) 및 주문 최소 금액에 따른 배송비 추가/감소
- kakao pay QR 결제
- AWS EC2 server 이용
- RDS database
- docker image build 및 container 배포

## Reference 

- 이 프로젝트는 [market kurly](https://www.kurly.com/shop/main/index.php) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
