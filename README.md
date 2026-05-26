# Application and Security Scaning
A FastApi-Based TDD crud project
This project includes a full security scanning setup covering 
SAST, DAST, secrets detection, and dependency scanning.

### Stack
- Python/FastApi
- Docker
- Various SAST,DAST,SCA tools


### Security Scanning
This project was scanned using standard DevSecOps tools as part of a security review exercise.

| Scan Type | Tools | Target |
|-----------|------|---------|
| SAST | pre-commits, semgrep, Bandit | Run python source sode |
| DAST | OWASP ZAP | Running FastAPI app |
| Secrets Detection | Trufflehog, detect-secrets, gitleaks | Codebase |
| Dependency Scanning (SCA) | Snyk, pip-audit | Python dependencies |


### Running the Scans
**SAST**
***pre-commit***
```bash
pre-commit install
pre-commit run --all-files
```
***Semgrep***
```bash
semgrep --config=auto .
```
***bandit***
```bash
bandit -r .
```

**Secret-scanning**
***Trufflehog***
```bash
# view secrets in filesystem
docker run --rm -it -v "${PWD}:/pwd" trufflesecurity/trufflehog filesystem /pwd -x tru-exclude.txt --no-verification
# view secrets in git history
docker run --rm -it -v "${PWD}:/pwd" trufflesecurity/trufflehog git /pwd --no-verification
```

***detect-secrets***
```bash
#also in pre-commit
detect-secrets scan > .secrets.baseline
detect-secrets audit .secrets.baseline
```

**Dependency Scan**
***Snyk***
```bash
snyk test --file=src/requirements.txt --package-manager=pip
```
***pip-audit***
```bash
pip-audit -r src/requirements.txt
```

**DAST**
***OWASP-ZAP***
```bash
# scan the running app 
docker run -u zap -v ${PWD}:/zap/wrk/:rw zaproxy/zap-stable zap-api-scan.py -t http://host.docker.internal:8004/openapi.json -f openapi -r zap_report.html -m 5 
```


## Key Findings

***Bandit- SAST***
- 0 high 2 medium severity found - [view report](reports/bandit_report.json)
- Main findings: Hardcoded AWS and github tokens

***Semgrep - SAST***
- 1 high, 1 medium, 5+ low severity found - [view report](reports/semgrep.json)
- Main findings: Use of weak hashing algorithm (md5), hardcoded secrets and errors from zap report html

***Trufflehog - Secrets Detection***
- Found 3 high severity secrets [view report](reports/results.json)
- Main findings: Hardcoded AWS, github tokens and DB url in git history

***Snyk - Dependency Scanning***
- 3 high severity vulnerabilities found - [view report](reports/snyk_report.json)
- Fixed by upgrading the packages to the newest version same

***OWASP ZAP - DAST***
- 1 high, 5+ low severity issue found - [view report](reports/zap_report.html)
- Main Findings: SQL Injection and various errors from the server
- image: [dast-image](reports/Screenshot%202026-05-26%20073624.png)


## Running the project

```bash
# clone
git clone https://github.com/recklessbud/tdd-crud

# assuming docker installed
cd folder/

echo "DB_URL="postgresql://postgres:postgres@db:5432/postgres"" > .env
docker compose up --build
```

---


## Reports
All scan reports are stored in the `/reports` folder.

## Up-Next
- Fix the identified vulnerabilities and secrets including SQL injection
- Implement CI/CD pipeline with integrated security scanning