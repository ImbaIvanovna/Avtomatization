# Интерактивный скрипт для коммита изменений
# Если git не найден автоматически, попросит указать путь

Write-Host "Поиск Git..." -ForegroundColor Cyan

# Попытка найти git
$gitExe = $null

# Проверяем стандартные пути
$possiblePaths = @(
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files\Git\cmd\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\git.exe",
    "$env:ProgramFiles\Git\cmd\git.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $gitExe = $path
        Write-Host "✅ Найден Git: $path" -ForegroundColor Green
        break
    }
}

# Если не найден, проверяем через where.exe
if (-not $gitExe) {
    try {
        $whereResult = where.exe git 2>$null
        if ($whereResult) {
            $gitExe = "git"
            Write-Host "✅ Git найден в PATH" -ForegroundColor Green
        }
    } catch {
        # Игнорируем ошибку
    }
}

# Если все еще не найден, просим пользователя указать путь
if (-not $gitExe) {
    Write-Host "⚠️  Git не найден автоматически" -ForegroundColor Yellow
    Write-Host "Пожалуйста, укажите полный путь к git.exe" -ForegroundColor Yellow
    Write-Host "Или нажмите Enter, чтобы попробовать 'git' (если он в PATH после перезапуска терминала)" -ForegroundColor Yellow
    $userPath = Read-Host "Путь к git.exe (или Enter для пропуска)"
    
    if ($userPath -and (Test-Path $userPath)) {
        $gitExe = $userPath
    } elseif (-not $userPath) {
        # Пробуем просто 'git' - возможно, нужен перезапуск терминала
        $gitExe = "git"
        Write-Host "Попытка использовать 'git' из PATH..." -ForegroundColor Yellow
    } else {
        Write-Host "❌ Указанный путь не существует. Попробуйте перезапустить терминал после установки Git." -ForegroundColor Red
        exit 1
    }
}

# Функция для выполнения git команд
function Invoke-GitCommand {
    param([string[]]$Arguments)
    
    if ($gitExe -eq "git") {
        & git $Arguments
    } else {
        & $gitExe $Arguments
    }
    
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
        return $false
    }
    return $true
}

# Проверяем версию git
Write-Host "`nПроверка версии Git..." -ForegroundColor Cyan
try {
    if ($gitExe -eq "git") {
        $version = git --version
    } else {
        $version = & $gitExe --version
    }
    Write-Host $version -ForegroundColor Green
} catch {
    Write-Host "❌ Не удалось выполнить git --version. Возможно, нужен перезапуск терминала." -ForegroundColor Red
    Write-Host "Попробуйте закрыть и открыть терминал заново после установки Git." -ForegroundColor Yellow
    exit 1
}

# Инициализация репозитория
Write-Host "`nИнициализация git репозитория..." -ForegroundColor Cyan
if (-not (Test-Path .git)) {
    Invoke-GitCommand @("init") | Out-Null
    Write-Host "✅ Репозиторий инициализирован" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Репозиторий уже инициализирован" -ForegroundColor Yellow
}

# Настройка git config
Write-Host "`nНастройка git config..." -ForegroundColor Cyan
Invoke-GitCommand @("config", "user.name", "1Usinglable1") | Out-Null
Invoke-GitCommand @("config", "user.email", "ilya.razumov20022711@yandex.ru") | Out-Null
Write-Host "✅ Git config настроен" -ForegroundColor Green

# Добавление файлов
Write-Host "`nДобавление файлов в staging area..." -ForegroundColor Cyan
Invoke-GitCommand @("add", ".") | Out-Null
Write-Host "✅ Файлы добавлены" -ForegroundColor Green

# Создание коммита
Write-Host "`nСоздание коммита..." -ForegroundColor Cyan
$commitMessage = @"
Добавлено поле rating в таблицу records и выгружена актуальная схема БД

- Добавлено поле rating DECIMAL(3,2) в таблицу records
- Создана миграция migration_add_rating.sql
- Выгружена актуальная схема БД в schema/schema.sql
- Создан скрипт export_schema.py для выгрузки схемы
"@

if (Invoke-GitCommand @("commit", "-m", $commitMessage)) {
    Write-Host "`n✅ Коммит создан успешно!" -ForegroundColor Green
    Write-Host "`nДля просмотра истории коммитов используйте: git log" -ForegroundColor Yellow
} else {
    Write-Host "`n⚠️  Возможно, нет изменений для коммита или произошла ошибка" -ForegroundColor Yellow
    Write-Host "Проверьте статус: git status" -ForegroundColor Yellow
}

