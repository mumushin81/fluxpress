# Auto GitHub Blogger

AI API 없이 로컬 Codex 환경과 기존 Aivesto 인프라를 활용해 GitHub 오픈소스 소개 블로그를 자동 생성·발행하는 프로젝트 스캐폴딩입니다.

## 디렉터리 개요
- collectors/  : GitHub 리포지토리 수집기
- analyzers/   : README·트리·코드 분석기
- writers/     : Codex 기반 블로그 글 생성기
- prompts/     : Midjourney 프롬프트 생성기
- database/    : Supabase 저장/조회 래퍼
- pipeline/    : 전체 오케스트레이션 파이프라인
- scripts/     : 실행 스크립트 (CLI 진입점)
- articles/    : 최종 산출물 저장소 (markdown/html)
- config/      : 설정 및 템플릿 파일
- tests/       : 단위 테스트 위치

## 실행 개요
```
python scripts/run_github_blog.py --url https://github.com/example/repo
python scripts/run_image_worker.py
python scripts/publish_wordpress.py
```

## 환경변수
Aivesto 프로젝트의 .env를 재사용합니다. 필요 키는 `config/env.example` 참고.
