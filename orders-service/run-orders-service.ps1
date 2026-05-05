$ErrorActionPreference = "Stop"

Write-Host "Starting PostgreSQL with Docker Compose..." -ForegroundColor Cyan
docker compose up -d

Write-Host "Waiting for PostgreSQL to become healthy..." -ForegroundColor Cyan
$maxAttempts = 18
for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    $health = docker inspect -f "{{.State.Health.Status}}" orders-postgres 2>$null
    if ($health -eq "healthy") {
        break
    }
    Start-Sleep -Seconds 5
}

Write-Host "Starting orders-service on http://localhost:8083 ..." -ForegroundColor Green
mvn spring-boot:run
