# VRSE 요구사항 명세서

## 1. 프로젝트 개요

### 1.1 프로젝트명

**VRSE**

### 1.2 부제

**AI 기반 게임 가격 예측 및 게이밍 환경 추천 플랫폼**

### 1.3 팀명

**DealSync**

여러 플랫폼의 게임 가격, 할인, 장비 데이터를 연결하여 사용자에게 최적의 게임 구매 경험을 제공한다는 의미를 가진다.

### 1.4 서비스 한 줄 소개

VRSE는 게임 가격과 할인 데이터를 분석해 언제, 어디서 사야 하는지 추천하고, 사용자의 플레이 성향과 보유 장비까지 고려해 게임과 게이밍 환경을 함께 추천하는 AI 기반 게임 라이프스타일 플랫폼이다.

### 1.5 서비스 목적

VRSE는 단순한 게임 검색 또는 가격 비교 서비스가 아니라, 사용자가 게임을 구매하고 플레이 환경을 준비하는 전 과정을 돕는 의사결정 플랫폼이다.

사용자는 VRSE를 통해 다음 질문에 대한 답을 한 번에 확인할 수 있다.

- 이 게임이 내 취향에 맞는가?
- 지금 구매해도 좋은 가격인가?
- 어느 플랫폼에서 가장 저렴한가?
- 내 PC 장비로 원활하게 실행 가능한가?
- 부족한 장비가 있다면 무엇을 구매해야 하는가?

## 2. 문제 정의

### 2.1 게임 플랫폼 분산

Steam, Epic Games, Xbox, PlayStation, Ubisoft 등 여러 플랫폼에 게임 정보와 가격 정보가 흩어져 있어 사용자가 직접 여러 사이트를 비교해야 한다.

### 2.2 구매 타이밍 판단의 어려움

현재 할인율이 높아 보여도 역대 최저가와 비교하면 좋은 가격이 아닐 수 있고, 반대로 낮은 할인율이어도 최근 기준으로는 좋은 구매 타이밍일 수 있다.

### 2.3 취향 기반 게임 탐색의 한계

기존 검색은 게임명, 장르, 태그 중심이다. 사용자는 "힐링 게임", "친구와 할 수 있는 게임", "스토리가 좋은 게임"처럼 자연어로 원하는 경험을 표현하고 싶어 한다.

### 2.4 실행 가능 여부 확인의 번거로움

사용자는 게임의 최소 사양과 권장 사양을 자신의 CPU, GPU, RAM, 모니터 환경과 직접 비교해야 한다.

### 2.5 장비 선택의 어려움

부족한 장비를 업그레이드하고 싶어도 어떤 GPU, CPU, 모니터, 주변기기가 적절한지 판단하기 어렵다.

## 3. 해결 방향

VRSE는 다음 흐름을 하나의 서비스로 연결한다.

```text
게임 검색
-> 플랫폼별 가격 비교
-> 할인율 및 최저가 분석
-> 구매 타이밍 추천
-> AI 기반 게임 추천
-> 내 장비 실행 가능 여부 확인
-> 부족한 게이밍 장비 추천
```

## 4. 서비스 대상

### 4.1 주요 사용자

- 여러 플랫폼의 게임 가격을 비교하고 싶은 게이머
- 할인 시점을 기다려 합리적으로 게임을 구매하고 싶은 사용자
- 자신의 취향에 맞는 게임을 추천받고 싶은 사용자
- 보유 PC로 특정 게임을 실행할 수 있는지 알고 싶은 사용자
- 목표 게임 환경에 맞는 장비를 추천받고 싶은 사용자

### 4.2 사용자 가치

- 게임 구매 가격 비교 시간 절약
- 할인율과 역대 최저가 기반의 구매 판단 지원
- 취향 기반 게임 추천
- 장비 실행 가능 여부 자동 분석
- 목적과 예산에 맞는 장비 추천

## 5. 전체 서비스 구조

```text
/
├── Welcome Page
├── Login Page
├── Signup Page
├── Main Page
├── Profile Page
│   ├── Play DNA
│   └── My Gear
├── Game Search Page
├── Game Detail Page
├── Device Search Page
└── Device Detail Page
```

## 6. 화면 명세

### 6.1 Welcome Page

서비스에 처음 접속했을 때 표시되는 랜딩 페이지이다.

#### 주요 기능

- VRSE 로고 표시
- 서비스 한 줄 소개 표시
- 로그인 페이지 이동
- 회원가입 페이지 이동
- 핵심 기능 요약 표시

#### 주요 문구

```text
Find your game.
Buy at the right time.
Check your gear.
```

### 6.2 Login Page

사용자 인증을 위한 로그인 페이지이다.

#### 입력 항목

- 이메일
- 비밀번호

#### 기능

- 로그인 요청
- 로그인 성공 시 Main Page 이동
- 로그인 실패 시 오류 메시지 표시
- 회원가입 페이지 이동

### 6.3 Signup Page

신규 사용자가 계정을 생성하는 페이지이다.

#### 입력 항목

- 이메일
- 비밀번호
- 비밀번호 확인
- 닉네임

#### 기능

- 회원가입 요청
- 이메일 중복 확인
- 비밀번호 유효성 검증
- 가입 성공 시 Login Page 또는 Main Page 이동

### 6.4 Main Page

로그인 후 진입하는 개인화 대시보드이다.

#### 주요 구성

- 오늘의 추천 게임
- 지금 구매하기 좋은 게임
- 최근 할인율이 높은 게임
- 내 장비로 실행 가능한 인기 게임
- Profile 이동 카드
- Game Search 이동 카드
- Device Search 이동 카드

### 6.5 Profile Page

사용자의 취향과 보유 장비를 관리하는 페이지이다.

#### 주요 기능

- 사용자 기본 정보 조회
- 선호 장르 등록 및 수정
- 관심 게임 등록 및 조회
- 보유 장비 등록 및 수정
- Play DNA 분석 결과 조회
- 보유 장비 기반 추천 조회

### 6.6 Game Search Page

게임을 검색하고 추천받는 페이지이다.

#### 검색 방식

- 게임명 검색
- 장르 필터
- 플랫폼 필터
- 할인율 필터
- 가격대 필터
- AI 자연어 검색

#### 게임 카드 표시 항목

- 게임명
- 이미지
- 장르
- 현재 최저가
- 할인율
- 구매 추천 상태
- 내 장비 실행 가능 여부

### 6.7 Game Detail Page

선택한 게임의 상세 정보, 가격, 구매 타이밍, 실행 가능 여부를 확인하는 핵심 페이지이다.

#### 제공 정보

- 게임명
- 이미지
- 설명
- 장르
- 태그
- 출시일
- 개발사
- 배급사
- 지원 플랫폼
- 최소 사양
- 권장 사양
- 현재 최저가
- 플랫폼별 가격
- 현재 할인율
- 역대 최저가
- 최근 최저가
- 구매 타이밍 추천
- 가격 예측 결과
- 내 장비 실행 가능 여부

#### 주요 행동

- 게임 가격 확인
- 구매 타이밍 확인
- 내 장비로 실행 가능한지 확인
- 부족한 장비 추천 페이지로 이동
- 관심 게임 등록

### 6.8 Device Search Page

게이밍 장비를 검색하고 추천받는 페이지이다.

#### 주요 기능

- 장비명 검색
- 카테고리 필터
- 가격대 필터
- 브랜드 필터
- 네이버 쇼핑 API 기반 상품 검색
- 게임 요구 사양 기반 추천

#### 장비 카테고리

- GPU
- CPU
- RAM
- 모니터
- 키보드
- 마우스
- 헤드셋
- 게임패드

### 6.9 Device Detail Page

선택한 장비의 상세 정보를 확인하는 페이지이다.

#### 제공 정보

- 상품명
- 이미지
- 가격
- 쇼핑몰명
- 브랜드
- 카테고리
- 상품 링크
- 추천 이유
- 적합한 게임 환경

## 7. 기능 요구사항

### F01. 회원 관리

#### 설명

사용자는 회원가입, 로그인, 로그아웃을 통해 개인화 기능을 이용할 수 있다.

#### 상세 요구사항

- 사용자는 이메일, 비밀번호, 닉네임으로 회원가입할 수 있다.
- 사용자는 이메일과 비밀번호로 로그인할 수 있다.
- 로그인한 사용자는 로그아웃할 수 있다.
- 로그인한 사용자는 자신의 프로필 정보를 조회할 수 있다.

#### 우선순위

필수

### F02. 멀티 플랫폼 게임 통합 검색

#### 설명

여러 플랫폼의 게임 정보를 통합하여 검색한다.

#### 활용 데이터

- Steam 게임 데이터
- IsThereAnyDeal 게임 식별자
- 공개 게임 메타데이터

#### 제공 정보

- 게임명
- 장르
- 태그
- 출시일
- 개발사
- 배급사
- 플랫폼
- 이미지
- 설명
- 최소 사양
- 권장 사양

#### 우선순위

필수

### F03. 플랫폼별 가격 비교

#### 설명

IsThereAnyDeal API를 활용하여 게임별 현재 가격과 할인 정보를 비교한다.

#### 제공 정보

- 현재 최저가
- 현재 할인율
- 플랫폼별 가격
- 역대 최저가
- 최근 3개월 최저가
- 최근 1년 최저가
- 구매 URL

#### 우선순위

필수

### F04. 구매 타이밍 추천

#### 설명

현재 가격이 구매하기 좋은 가격인지 분석하여 BUY, WAIT, WATCH 중 하나로 추천한다.

#### 추천 상태

| 상태 | 의미 |
| --- | --- |
| BUY | 현재 구매하기 좋은 가격 |
| WAIT | 더 큰 할인 가능성이 있어 기다리기 추천 |
| WATCH | 관심 목록에 넣고 추적 추천 |

#### 분석 요소

- 현재 할인율
- 역대 최저가와의 차이
- 최근 최저가와의 차이
- 할인 빈도
- 할인 주기
- 대형 세일 시즌과의 거리
- 사용자의 관심도

#### 우선순위

필수

### F05. 게임 가격 예측

#### 설명

게임 가격 히스토리와 할인 패턴을 분석하여 다음 할인 가능성을 예측한다.

#### MVP 분석 방식

복잡한 딥러닝 모델 대신 규칙 기반 분석과 간단한 통계 분석을 조합한다.

```text
가격 예측 로직 =
과거 할인 주기
+ 최근 할인 빈도
+ 역대 최저가 근접도
+ 출시일 이후 경과 기간
+ 대형 세일 시즌 여부
+ 최근 할인율 변화
```

#### 출력 정보

- 다음 할인 예상 시점
- 예상 할인율
- 현재 구매 추천 여부
- 추천 이유

#### 우선순위

선택

### F06. AI 기반 자연어 게임 추천

#### 설명

사용자가 자연어로 원하는 게임 경험을 입력하면 AI가 의도를 해석하고 적합한 게임을 추천한다.

#### 입력 예시

```text
친구랑 같이 할 수 있고 너무 어렵지 않은 협동 게임 추천해줘.
가격도 너무 비싸지 않았으면 좋겠어.
```

#### 분석 요소

- 분위기
- 난이도
- 플레이 방식
- 멀티플레이 여부
- 장르
- 가격 조건
- 할인 여부
- 사용자 기존 취향

#### 우선순위

권장

### F07. Play DNA 분석

#### 설명

사용자의 선호 게임, 관심 게임, 장르, 태그를 기반으로 플레이 성향을 분석한다.

#### 성향 유형

| 유형 | 설명 |
| --- | --- |
| Explorer | 오픈월드, 탐험, 자유도 높은 게임 선호 |
| Story Lover | 스토리와 캐릭터 중심 게임 선호 |
| Challenger | 난이도 높은 전투와 도전형 게임 선호 |
| Strategist | 전략, 경영, 시뮬레이션 선호 |
| Relaxer | 힐링, 농장, 생활형 게임 선호 |
| Collector | 수집, 업적, 아이템 파밍 선호 |
| Social Player | 협동, 멀티플레이, 파티 게임 선호 |

#### 우선순위

권장

### F08. Gear Check

#### 설명

사용자의 현재 장비와 게임 요구 사양을 비교하여 실행 가능 여부를 판단한다.

#### 사용자 입력 장비

- CPU
- GPU
- RAM
- 저장공간
- 모니터 해상도
- 모니터 주사율

#### 출력 예시

```text
FHD 60fps: 가능
FHD 144fps: 보통
QHD 144Hz: GPU 업그레이드 권장
4K 60fps: 권장하지 않음
```

#### 우선순위

필수

### F09. 게이밍 장비 추천

#### 설명

네이버 쇼핑 검색 API를 활용하여 사용자의 목표 게임 환경에 적합한 장비를 추천한다.

#### 추천 기준

- 게임 권장 사양
- 현재 사용자 장비
- 목표 해상도
- 목표 FPS
- 예산
- 브랜드 선호
- 가격
- 상품명 키워드 적합도

#### 우선순위

필수

### F10. 관심 게임 관리

#### 설명

사용자는 관심 있는 게임을 저장하고, 이후 가격이나 추천 결과를 다시 확인할 수 있다.

#### 상세 요구사항

- 게임 상세 페이지에서 관심 게임으로 등록할 수 있다.
- Profile Page에서 관심 게임 목록을 조회할 수 있다.
- 관심 게임을 삭제할 수 있다.

#### 우선순위

권장

## 8. 비기능 요구사항

### 8.1 성능

- 게임 목록 조회 API는 일반적인 조건에서 2초 이내에 응답하는 것을 목표로 한다.
- 외부 API 응답 지연을 고려하여 필요한 데이터는 DB에 저장하거나 캐싱한다.
- 장비 검색은 네이버 쇼핑 API 실시간 조회를 기본으로 하되, 추천 결과는 저장할 수 있다.

### 8.2 보안

- 비밀번호는 해시 처리하여 저장한다.
- 외부 API 키는 환경 변수로 관리한다.
- 인증이 필요한 API는 토큰 기반 인증을 적용한다.
- 사용자는 자신의 프로필, 장비, 관심 게임 데이터만 수정할 수 있다.

### 8.3 유지보수성

- 프론트엔드와 백엔드를 분리하여 개발한다.
- 외부 API 연동 로직은 서비스 계층으로 분리한다.
- 가격 분석, Play DNA 분석, Gear Check 로직은 독립 모듈로 분리한다.

### 8.4 확장성

- 향후 Steam 라이브러리 연동, 리뷰 감성 분석, 알림 기능, 커뮤니티 기능을 추가할 수 있도록 모델과 API를 설계한다.

## 9. 데이터 모델 명세

### 9.1 User

사용자 계정 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 사용자 ID |
| email | string | 이메일 |
| password | string | 해시된 비밀번호 |
| nickname | string | 닉네임 |
| created_at | datetime | 생성일 |

### 9.2 Game

게임 기본 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 게임 ID |
| itad_id | string | IsThereAnyDeal 게임 ID |
| steam_app_id | integer | Steam 앱 ID |
| title | string | 게임명 |
| description | text | 게임 설명 |
| image_url | string | 이미지 URL |
| genre | string | 대표 장르 |
| release_date | date | 출시일 |
| developer | string | 개발사 |
| publisher | string | 배급사 |
| created_at | datetime | 생성일 |

### 9.3 Store

게임 판매 상점 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 상점 ID |
| name | string | 상점명 |
| slug | string | 상점 식별자 |
| store_url | string | 상점 URL |

### 9.4 GamePrice

게임 가격 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 가격 ID |
| game_id | integer | 게임 ID |
| store_id | integer | 상점 ID |
| current_price | integer | 현재 가격 |
| original_price | integer | 정가 |
| discount_rate | integer | 할인율 |
| historical_low | integer | 역대 최저가 |
| lowest_3m | integer | 최근 3개월 최저가 |
| lowest_1y | integer | 최근 1년 최저가 |
| currency | string | 통화 |
| purchase_url | string | 구매 URL |
| checked_at | datetime | 조회 시각 |

### 9.5 GameRequirement

게임 최소/권장 사양 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 사양 ID |
| game_id | integer | 게임 ID |
| type | string | minimum 또는 recommended |
| cpu | string | CPU |
| gpu | string | GPU |
| ram_gb | integer | RAM 용량 |
| storage_gb | integer | 저장공간 |
| os | string | 운영체제 |

### 9.6 Tag

게임 태그 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 태그 ID |
| name | string | 태그명 |

### 9.7 GameTag

게임과 태그의 다대다 연결 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 연결 ID |
| game_id | integer | 게임 ID |
| tag_id | integer | 태그 ID |

### 9.8 UserGame

사용자의 관심 게임, 플레이 게임, 찜 게임을 관리한다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | ID |
| user_id | integer | 사용자 ID |
| game_id | integer | 게임 ID |
| status | string | 관심, 플레이중, 완료 등 |
| rating | integer | 사용자 평점 |
| is_favorite | boolean | 즐겨찾기 여부 |
| created_at | datetime | 생성일 |

### 9.9 PlayDNA

사용자의 플레이 성향 분석 결과이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | ID |
| user_id | integer | 사용자 ID |
| explorer_score | integer | Explorer 점수 |
| story_score | integer | Story Lover 점수 |
| challenger_score | integer | Challenger 점수 |
| strategist_score | integer | Strategist 점수 |
| relaxer_score | integer | Relaxer 점수 |
| collector_score | integer | Collector 점수 |
| social_score | integer | Social Player 점수 |
| updated_at | datetime | 갱신일 |

### 9.10 UserDevice

사용자가 보유한 장비 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 장비 ID |
| user_id | integer | 사용자 ID |
| cpu | string | CPU |
| gpu | string | GPU |
| ram_gb | integer | RAM 용량 |
| storage_gb | integer | 저장공간 |
| monitor_resolution | string | 모니터 해상도 |
| refresh_rate | integer | 주사율 |
| created_at | datetime | 생성일 |

### 9.11 Product

네이버 쇼핑 API로 조회한 장비 상품 정보이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 상품 ID |
| name | string | 상품명 |
| category | string | 카테고리 |
| brand | string | 브랜드 |
| price | integer | 가격 |
| mall_name | string | 쇼핑몰명 |
| product_url | string | 상품 URL |
| image_url | string | 이미지 URL |
| searched_at | datetime | 검색 시각 |

### 9.12 GearRecommendation

장비 추천 결과이다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| id | integer | 추천 ID |
| user_id | integer | 사용자 ID |
| game_id | integer | 게임 ID |
| product_id | integer | 상품 ID |
| target_purpose | string | 목표 환경 |
| gear_score | integer | 추천 점수 |
| reason | text | 추천 이유 |
| created_at | datetime | 생성일 |

## 10. API 명세 초안

### 10.1 인증 API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| POST | /api/accounts/signup/ | 회원가입 | 불필요 |
| POST | /api/accounts/login/ | 로그인 | 불필요 |
| POST | /api/accounts/logout/ | 로그아웃 | 필요 |
| GET | /api/accounts/profile/ | 내 프로필 조회 | 필요 |
| PATCH | /api/accounts/profile/ | 내 프로필 수정 | 필요 |

### 10.2 게임 API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| GET | /api/games/ | 게임 목록 조회 | 선택 |
| GET | /api/games/{game_id}/ | 게임 상세 조회 | 선택 |
| GET | /api/games/search/ | 게임 검색 | 선택 |
| GET | /api/games/recommended/ | 추천 게임 조회 | 필요 |
| POST | /api/games/natural-search/ | AI 자연어 게임 추천 | 필요 |

### 10.3 가격 API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| GET | /api/games/{game_id}/prices/ | 플랫폼별 가격 조회 | 선택 |
| POST | /api/games/{game_id}/prices/sync/ | 외부 가격 데이터 동기화 | 관리자 |
| GET | /api/games/{game_id}/buy-timing/ | 구매 타이밍 추천 조회 | 선택 |
| GET | /api/games/{game_id}/price-prediction/ | 가격 예측 조회 | 선택 |

### 10.4 사용자 게임 API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| GET | /api/users/me/games/ | 내 관심 게임 조회 | 필요 |
| POST | /api/users/me/games/ | 관심 게임 등록 | 필요 |
| PATCH | /api/users/me/games/{user_game_id}/ | 관심 게임 상태 수정 | 필요 |
| DELETE | /api/users/me/games/{user_game_id}/ | 관심 게임 삭제 | 필요 |

### 10.5 Play DNA API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| GET | /api/users/me/play-dna/ | Play DNA 조회 | 필요 |
| POST | /api/users/me/play-dna/analyze/ | Play DNA 분석 실행 | 필요 |

### 10.6 장비 API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| GET | /api/users/me/devices/ | 내 장비 조회 | 필요 |
| POST | /api/users/me/devices/ | 내 장비 등록 | 필요 |
| PATCH | /api/users/me/devices/{device_id}/ | 내 장비 수정 | 필요 |
| DELETE | /api/users/me/devices/{device_id}/ | 내 장비 삭제 | 필요 |
| GET | /api/games/{game_id}/gear-check/ | 게임 실행 가능 여부 조회 | 필요 |

### 10.7 상품 API

| Method | URL | 설명 | 인증 |
| --- | --- | --- | --- |
| GET | /api/products/search/ | 네이버 쇼핑 장비 검색 | 선택 |
| GET | /api/products/{product_id}/ | 장비 상세 조회 | 선택 |
| GET | /api/games/{game_id}/gear-recommendations/ | 게임 기반 장비 추천 | 필요 |

## 11. 핵심 알고리즘 명세

### 11.1 구매 타이밍 점수

```text
Buy Timing Score =
현재 할인율 점수
+ 역대 최저가 근접도 점수
+ 최근 최저가 근접도 점수
+ 할인 주기 점수
+ 다음 세일 예상 거리 점수
+ 사용자 관심도 점수
```

#### 추천 기준 예시

| 점수 | 추천 상태 |
| --- | --- |
| 80점 이상 | BUY |
| 50점 이상 80점 미만 | WATCH |
| 50점 미만 | WAIT |

### 11.2 게임 추천 점수

```text
Game Recommendation Score =
장르 유사도
+ 태그 유사도
+ Play DNA 적합도
+ 리뷰 평가 점수
+ 현재 할인 매력도
+ 가격 타이밍 점수
```

### 11.3 Playability Score

```text
Playability Score =
CPU 충족 점수
+ GPU 충족 점수
+ RAM 충족 점수
+ 저장공간 충족 점수
+ 목표 해상도/FPS 보정 점수
```

#### 결과 기준 예시

| 점수 | 결과 |
| --- | --- |
| 85점 이상 | 원활 |
| 70점 이상 85점 미만 | 가능 |
| 50점 이상 70점 미만 | 옵션 타협 필요 |
| 50점 미만 | 업그레이드 권장 |

### 11.4 장비 추천 점수

```text
Gear Recommendation Score =
게임 요구 사양 적합도
+ 현재 장비 대비 향상폭
+ 예산 적합도
+ 상품 가격 점수
+ 상품명 키워드 적합도
+ 목표 환경 적합도
```

## 12. 외부 API 연동 명세

### 12.1 IsThereAnyDeal API

#### 사용 목적

- 게임별 현재 최저가 조회
- 플랫폼별 가격 조회
- 역대 최저가 조회
- 활성 번들 및 할인 정보 조회

#### 저장 대상

- Game
- Store
- GamePrice

### 12.2 Steam API

#### 사용 목적

- Steam 앱 목록 조회
- 게임 메타데이터 수집
- 게임 이미지, 설명, 출시일, 개발사, 배급사 정보 보완

#### 저장 대상

- Game
- Tag
- GameTag
- GameRequirement

### 12.3 네이버 쇼핑 검색 API

#### 사용 목적

- GPU, CPU, 모니터 등 게이밍 장비 검색
- 상품명, 가격, 쇼핑몰명, 이미지, 상품 링크 조회

#### 저장 대상

- Product
- GearRecommendation

### 12.4 AI API

#### 사용 목적

- 자연어 게임 추천
- 추천 이유 생성
- Play DNA 설명 생성
- 장비 추천 이유 생성

## 13. 데이터 흐름

### 13.1 게임 가격 데이터 수집

```text
IsThereAnyDeal API
-> 게임 가격/할인 데이터 수집
-> Game / Store / GamePrice 저장
-> 가격 비교 및 구매 타이밍 추천에 활용
```

### 13.2 게임 메타데이터 수집

```text
Steam API / 공개 게임 메타데이터
-> 게임명, 장르, 태그, 출시일, 이미지, 사양 수집
-> Game / Tag / GameRequirement 저장
-> 게임 검색 및 추천에 활용
```

### 13.3 장비 데이터 수집

```text
네이버 쇼핑 검색 API
-> GPU, CPU, 모니터 등 상품 검색
-> Product 저장 또는 실시간 조회
-> 장비 추천 결과 생성
```

### 13.4 사용자 데이터 분석

```text
사용자 관심 게임 / 선호 태그 / 보유 장비
-> Play DNA 분석
-> 개인화 게임 추천
-> 실행 가능 여부 분석
-> 장비 추천
```

## 14. 기술 스택

### 14.1 Frontend

- Vue.js
- Vue Router
- Pinia
- Axios
- Chart.js

### 14.2 Backend

- Django
- Django REST Framework
- SQLite 또는 MySQL 또는 PostgreSQL
- Requests
- django-environ

### 14.3 External API

- IsThereAnyDeal API
- Steam API
- 네이버 쇼핑 검색 API
- OpenAI API 또는 Upstage API

### 14.4 Tools

- Postman
- Git / GitHub
- Figma
- Notion
- Mermaid / Draw.io

## 15. MVP 범위

### 15.1 필수 구현

- 회원가입 / 로그인
- 메인 대시보드
- 게임 목록 조회
- 게임 상세 조회
- IsThereAnyDeal API 기반 가격 정보 저장
- 플랫폼별 가격 비교
- 구매 타이밍 추천
- 사용자 장비 등록
- 게임 요구 사양과 사용자 장비 비교
- 네이버 쇼핑 API 기반 장비 검색
- Django REST Framework 기반 JSON API
- Vue 기반 화면 구성

### 15.2 우선 구현하면 좋은 기능

- 가격 변동 그래프
- Play DNA 분석
- AI 자연어 게임 추천
- 추천 이유 생성
- 관심 게임 저장

### 15.3 시간이 남으면 구현할 기능

- 가격 예측 고도화
- 리뷰 감성 분석
- 장비 상세 추천
- 관련 게임 추천
- 관심 장비 저장
- 사용자별 개인화 대시보드 고도화
- 관심 게임 최저가 알림

## 16. 개발 우선순위

### 16.1 1차 목표: 가격 비교 중심 MVP

- 회원가입 / 로그인
- 게임 목록 및 상세
- IsThereAnyDeal API 연동
- 가격 데이터 저장
- 플랫폼별 가격 비교
- BUY / WAIT / WATCH 추천

### 16.2 2차 목표: 사용자 개인화

- 관심 게임
- 선호 장르
- Play DNA 분석
- 개인화 추천 게임

### 16.3 3차 목표: 장비 분석

- 사용자 장비 등록
- 게임 요구 사양 비교
- Playability Score
- 장비 업그레이드 추천

### 16.4 4차 목표: AI 추천

- 자연어 게임 추천
- 추천 이유 생성
- 장비 추천 이유 생성

## 17. 기대 효과

- 사용자는 여러 플랫폼을 직접 비교하지 않아도 게임 가격을 한 번에 확인할 수 있다.
- 현재 할인율이 실제로 좋은 가격인지 판단할 수 있다.
- 자신의 취향에 맞는 게임을 더 쉽게 찾을 수 있다.
- 현재 장비로 게임을 실행할 수 있는지 빠르게 확인할 수 있다.
- 필요한 장비를 예산과 목적에 맞게 추천받을 수 있다.
- 게임 구매부터 플레이 환경 구성까지 하나의 흐름으로 관리할 수 있다.

## 18. 향후 확장 방향

- 사용자 리뷰 감성 분석 고도화
- 협업 필터링 기반 게임 추천
- Steam 라이브러리 연동
- 가격 예측 모델 고도화
- 게임별 FPS 벤치마크 데이터 연동
- 장비 호환성 분석
- 콘솔 게임 및 구독 서비스 비교
- 관심 게임 최저가 도달 알림
- 커뮤니티 기능

## 19. 발표용 요약

VRSE는 여러 게임 플랫폼에 흩어진 게임 정보와 가격 데이터를 통합하여 사용자의 게임 구매 의사결정을 돕는 서비스이다. IsThereAnyDeal API를 활용해 게임별 현재 최저가, 할인율, 역대 최저가 데이터를 수집하고, 이를 기반으로 구매 타이밍과 가격 변동 가능성을 분석한다. 또한 사용자의 선호 장르와 관심 게임을 바탕으로 Play DNA를 생성하고, AI를 활용해 자연어 기반 게임 추천을 제공한다. 마지막으로 사용자의 현재 PC 장비와 게임 요구 사양을 비교하여 실행 가능 여부를 판단하고, 부족한 장비는 네이버 쇼핑 검색 API를 활용해 추천한다.

## 20. 최종 정의

**VRSE는 게임 구매와 플레이 환경 구성을 하나의 흐름으로 연결하는 AI 기반 게임 의사결정 플랫폼이다.**
