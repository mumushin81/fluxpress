# Vercel 배포 안내 (fluxpress)

1) GitHub repo 연결
- 이미 이 리포지토리를 Vercel에서 Import하면 CI/CD 자동.
- Framework: Other (Static)
- Output directory: articles/final
- Build command: 빌드 없음 (빈 값) — 필요 시 `python scripts/run_github_blog.py --url <repo>`를 빌드 스텝으로 추가할 수 있음.

2) 첫 배포
- Vercel Dashboard → New Project → GitHub에서 fluxpress 선택 → 설정값 입력 → Deploy.
- 첫 배포는 현재 `articles/final/index.html` 플라스홀더가 노출됨.

3) 콘텐츠 업데이트
- 로컬에서 블로그 생성 후 git push 하면 Vercel이 자동 재배포.

4) 환경변수 (선택)
- SUPABASE_URL, SUPABASE_KEY 등은 Vercel Project Settings → Environment Variables에 추가 가능. 단, 현재 정적 배포만 사용하므로 프런트에 직접 노출하지 않도록 주의.
