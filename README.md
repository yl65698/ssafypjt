# VRSE

AI 기반 게임 가격 예측 및 게이밍 환경 추천 플랫폼 MVP입니다.

현재 환경에 Node/npm이 없어 Vue 분리형 대신 Django + DRF + 단일 페이지 UI로 구현했습니다. API 구조는 분리형 프론트엔드로 옮기기 쉽게 `/api/` 아래에 정리되어 있습니다.

## 실행

```powershell
python manage.py migrate
python manage.py seed_vrse
python manage.py runserver 127.0.0.1:8000
```

또는:

```powershell
.\run_server.ps1
```

브라우저에서 접속:

```text
http://127.0.0.1:8000/
```

## 테스트

```powershell
python manage.py test
```

## 주요 기능

- 게임 목록/상세 조회
- 플랫폼별 가격 비교
- BUY / WATCH / WAIT 구매 타이밍 추천
- 간단한 가격 예측
- AI 자연어 검색 형태의 규칙 기반 게임 추천
- 회원가입 / 로그인 / 로그아웃
- 보유 장비 등록
- 게임 요구 사양과 내 장비 비교
- 장비 추천
- Play DNA 분석

## 주요 API

| Method | URL | 설명 |
| --- | --- | --- |
| GET | `/api/dashboard/` | 메인 추천 데이터 |
| GET | `/api/games/` | 게임 목록 |
| GET | `/api/games/{id}/` | 게임 상세 |
| POST | `/api/games/natural-search/` | 자연어 게임 추천 |
| GET | `/api/games/{id}/playability/` | 실행 가능 여부 |
| GET | `/api/games/{id}/gear-recommendations/` | 장비 추천 |
| GET | `/api/products/` | 장비 목록 |
| POST | `/api/accounts/signup/` | 회원가입 |
| POST | `/api/accounts/login/` | 로그인 |
| POST | `/api/accounts/logout/` | 로그아웃 |
| GET/POST | `/api/me/devices/` | 내 장비 조회/등록 |
| GET | `/api/me/play-dna/` | Play DNA 분석 |

## 외부 API 연동 위치

현재는 발표와 개발 진행을 위해 샘플 데이터를 사용합니다. 실제 API 연동은 다음 위치에 추가하면 됩니다.

- IsThereAnyDeal 가격 수집: `core/management/commands/seed_vrse.py` 또는 별도 sync command
- Steam 메타데이터 수집: `core/services.py` 또는 별도 service module
- 네이버 쇼핑 검색: `ProductViewSet` 또는 별도 shopping service
- AI 추천: `natural_search`를 OpenAI/Upstage 호출로 교체
