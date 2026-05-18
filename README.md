# Secure CI/CD Pipeline

Проект разработан в рамках выпускной квалификационной работы на тему:

**«Разработка и внедрение CI/CD-конвейера для обеспечения безопасности программных приложений»**

Цель проекта — разработать демонстрационный безопасный CI/CD-конвейер, включающий автоматизированную сборку, тестирование, анализ безопасности, мониторинг, управление секретами и уведомления о результатах выполнения pipeline.

---

## Описание проекта

В качестве тестового приложения используется небольшое FastAPI-приложение. Оно контейнеризуется с помощью Docker и проверяется в CI/CD-конвейере GitHub Actions.

В проекте реализованы следующие компоненты:

- FastAPI-приложение;
- unit-тестирование с помощью Pytest;
- контейнеризация через Docker;
- запуск инфраструктуры через Docker Compose;
- CI/CD-конвейер на GitHub Actions;
- SAST-анализ с помощью Bandit;
- поиск секретов с помощью Gitleaks;
- анализ зависимостей с помощью Trivy FS Scan;
- анализ Docker-образа с помощью Trivy Image Scan;
- DAST-анализ с помощью OWASP ZAP;
- управление секретами с помощью GitHub Secrets и HashiCorp Vault;
- мониторинг через Prometheus и Grafana;
- Telegram-уведомления о результате выполнения pipeline.

---

## Используемые технологии

| Назначение | Инструмент |
|---|---|
| Backend-приложение | FastAPI |
| Язык программирования | Python 3.12 |
| Unit-тестирование | Pytest |
| Контейнеризация | Docker |
| Управление контейнерами | Docker Compose |
| CI/CD | GitHub Actions |
| SAST | Bandit |
| Secrets scanning | Gitleaks |
| SCA / анализ зависимостей | Trivy FS Scan |
| Анализ Docker-образа | Trivy Image Scan |
| DAST | OWASP ZAP |
| Управление секретами | GitHub Secrets, HashiCorp Vault |
| Мониторинг | Prometheus |
| Визуализация метрик | Grafana |
| Уведомления | Telegram Bot API |

---

## Структура проекта

```text
secure-cicd-pipeline/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│       └── test_main.py
│
├── monitoring/
│   └── prometheus.yml
│
├── reports/
│   └── security-results.md
│
├── graphics/
│   ├── architecture_cicd_pipeline.png
│   ├── component_interaction_scheme.png
│   ├── pipeline_algorithm_flowchart.png
│   └── security_findings_chart.png
│
├── .github/
│   └── workflows/
│       └── secure-pipeline.yml
│
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## FastAPI-приложение

Тестовое приложение содержит следующие endpoint:

| Endpoint | Назначение |
|---|---|
| `/` | Главная страница приложения |
| `/health` | Проверка работоспособности приложения |
| `/items/{item_id}` | Тестовый API-endpoint |
| `/metrics` | Метрики для Prometheus |
| `/docs` | Swagger-документация FastAPI |

Endpoint `/metrics` используется Prometheus для сбора метрик приложения.

---

## Локальный запуск приложения

Создание виртуального окружения:

```bash
python -m venv venv
```

Активация окружения в Windows:

```bash
venv\Scripts\activate
```

Установка зависимостей:

```bash
pip install -r app/requirements.txt
```

Запуск приложения:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

После запуска приложение доступно по адресам:

```text
http://localhost:8000
http://localhost:8000/health
http://localhost:8000/docs
http://localhost:8000/metrics
```

---

## Запуск тестов

Для запуска unit-тестов используется Pytest:

```bash
python -m pytest app/tests
```

---

## Запуск через Docker

Сборка Docker-образа:

```bash
docker build -t secure-cicd-app:latest .
```

Запуск контейнера:

```bash
docker run -d -p 8000:8000 --name secure-cicd-app secure-cicd-app:latest
```

Проверка приложения:

```text
http://localhost:8000/health
```

Остановка контейнера:

```bash
docker stop secure-cicd-app
docker rm secure-cicd-app
```

---

## Запуск инфраструктуры через Docker Compose

Для запуска приложения, Prometheus, Grafana и HashiCorp Vault используется Docker Compose:

```bash
docker compose up --build -d
```

После запуска доступны следующие сервисы:

| Сервис | URL |
|---|---|
| FastAPI App | http://localhost:8000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| HashiCorp Vault | http://localhost:8200 |

Остановка всех контейнеров:

```bash
docker compose down
```

---

## CI/CD-конвейер

CI/CD-конвейер реализован с помощью GitHub Actions.

Workflow-файл расположен по пути:

```text
.github/workflows/secure-pipeline.yml
```

Основные этапы pipeline:

| Этап | Назначение |
|---|---|
| `Run unit tests` | Запуск unit-тестов Pytest |
| `SAST with Bandit` | Статический анализ Python-кода |
| `Secrets scanning with Gitleaks` | Поиск секретов в репозитории |
| `SCA dependency scan with Trivy` | Анализ зависимостей проекта |
| `Build Docker image` | Сборка Docker-образа |
| `Container image scan with Trivy` | Анализ Docker-образа |
| `Deploy application in test environment` | Развертывание приложения в тестовой среде |
| `DAST with OWASP ZAP` | Динамическое тестирование безопасности |
| `Telegram notification` | Отправка уведомления о результате pipeline |

---

## Проверки безопасности

### Unit-тестирование

Unit-тесты проверяют корректность работы основных endpoint приложения:

- `/`;
- `/health`;
- `/items/{item_id}`.

### SAST: Bandit

Bandit используется для статического анализа Python-кода и поиска потенциально небезопасных конструкций.

В рамках эксперимента Bandit обнаруживал небезопасный вызов:

```python
subprocess.run(..., shell=True)
```

После демонстрации уязвимость была удалена.

### Secrets scanning: Gitleaks

Gitleaks используется для поиска секретов, токенов и ключей в коде и истории репозитория.

В рамках эксперимента был добавлен фейковый GitHub Personal Access Token, который был обнаружен Gitleaks. Файл с тестовым секретом не был объединён в основную ветку.

### SCA: Trivy FS Scan

Trivy FS Scan используется для анализа зависимостей проекта.

По результатам проверки файла `app/requirements.txt` уязвимости не были выявлены.

### Container Scan: Trivy Image Scan

Trivy Image Scan используется для анализа Docker-образа.

В ходе проверки контейнерного образа были выявлены 4 уязвимости уровня `HIGH`, уязвимости уровня `CRITICAL` отсутствуют. Этап настроен в режиме отчёта, чтобы результаты анализа фиксировались в логах CI/CD, но не блокировали выполнение демонстрационного pipeline.

### DAST: OWASP ZAP

OWASP ZAP используется для динамического анализа работающего приложения.

По результатам ZAP Baseline Scan были выявлены 2 предупреждения уровня `Low` и 1 предупреждение уровня `Informational`. Уязвимости уровней `High` и `Medium` отсутствуют. HTML-отчёт сохраняется как artifact GitHub Actions.

---

## Управление секретами

В проекте используются два механизма работы с секретами:

| Механизм | Назначение |
|---|---|
| GitHub Secrets | Хранение `TELEGRAM_TOKEN` и `TELEGRAM_CHAT_ID` |
| HashiCorp Vault | Демонстрационное хранение секрета `DB_PASSWORD` |

HashiCorp Vault используется в dev-режиме в рамках демонстрационного стенда. В промышленной эксплуатации dev-режим использовать нельзя.

---

## Мониторинг

Приложение предоставляет endpoint:

```text
/metrics
```

Prometheus собирает метрики приложения по адресу внутри Docker-сети:

```text
http://app:8000/metrics
```

Grafana подключается к Prometheus как к источнику данных:

```text
http://prometheus:9090
```

В Grafana создан dashboard для визуализации метрики:

```text
app_requests_total
```

---

## Telegram-уведомления

В pipeline реализована отправка уведомлений в Telegram:

- при успешном завершении всех этапов;
- при ошибке одного из этапов.

Токен бота и идентификатор чата хранятся в GitHub Secrets и не размещаются в исходном коде.

Для статусов используются Unicode-коды:

```yaml
STATUS_OK: "\u2705"
STATUS_FAIL: "\u274C"
```

---

## Результаты тестовых экспериментов

Подробные результаты экспериментов представлены в файле:

```text
reports/security-results.md
```

Краткая сводка:

| Проверка | Количество выявленных проблем |
|---|---:|
| Unit-тесты | 1 |
| SAST Bandit | 1 |
| Secrets Gitleaks | 1 |
| Trivy FS Scan | 0 |
| Trivy Image Scan | 4 |
| OWASP ZAP DAST | 3 |
| Telegram Notification | 0 |

---

## Графические материалы

В папке `graphics/` находятся схемы и диаграммы, подготовленные для пояснительной записки ВКР.

| Файл | Описание |
|---|---|
| `architecture_cicd_pipeline.png` | Архитектура безопасного CI/CD-конвейера |
| `component_interaction_scheme.png` | Схема взаимодействия компонентов разработанного решения |
| `pipeline_algorithm_flowchart.png` | Алгоритм работы безопасного CI/CD-конвейера |
| `security_findings_chart.png` | Количество выявленных проблем по типам проверок |

---

## Примечание

Проект является демонстрационным стендом для выпускной квалификационной работы. Некоторые настройки, например HashiCorp Vault в dev-режиме и Trivy Image Scan в report mode, используются для учебной демонстрации и требуют дополнительного усиления при промышленном внедрении.