# CI/CD Report

## Pipeline Configuration

The GitHub Actions workflow is `.github/workflows/api-tests.yml`. It runs on every push to `main` and can also run manually. The job:

1. Checks out this repository and the EShop SUT submodule.
2. Sets up Node.js 20.
3. Installs backend packages and Newman.
4. Starts EShop on `http://127.0.0.1:3000` and waits for it to respond.
5. Runs the 120-case characterization baseline with the local environment.
6. Uploads the Newman JSON report even if a test fails.

The workflow runs this command:

```bash
newman run collections/EShop-HW06-ci-baseline.postman_collection.json \
  -e collections/local.postman_environment.json \
  -r cli,json \
  --reporter-json-export ci-results/newman-ci.json \
  --color off
```

The characterization collection records the current known behavior so the CI example can be green. The strict collection remains `collections/EShop-HW06.postman_collection.json`; it keeps requirement assertions and exposes the bugs.

## All-Passing Sample

- Commit: `98f77c3aa64d70662ba6aa3b4d4cfad9fed421e8`
- Run: https://github.com/linhnph05/QA-HW06/actions/runs/32109080739
- Result: 120 cases and 242 baseline assertions passed.
![Passing GitHub Actions run](../images/ci-pass.png)

## Exactly One Failing Sample

- Commit: `b6e490c6de73f3ae811cb0a0f6e0bab75b7d93ef`
- Run: https://github.com/linhnph05/QA-HW06/actions/runs/32109235988
- Result: exactly one assertion failed in `FR03-AI-01`; expected 418 but received 200.
![Failing GitHub Actions run](../images/ci-fail.png)

## Restored State

I restored the expected status to 200 after collecting the red evidence. The final green run is https://github.com/linhnph05/QA-HW06/actions/runs/32109618742.
