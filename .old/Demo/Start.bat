    @echo off
    setlocal enabledelayedexpansion

    REM Verify Docker daemon is reachable; if not, show clear instructions and exit
    docker info >nul 2>&1 || goto docker_not_running

    :check_versions
    REM Check image versions
    set "latest_version_frontend="
    set "current_version_frontend="
    set "latest_version_backend="
    set "current_version_backend="
    set "update_required=0"
    set "update_list="

    REM Use backticks with usebackq and tokens=* so the docker command is executed and full output is captured
    for /f "usebackq tokens=*" %%i in (`docker inspect --format "{{.Config.Labels.version}}" ghcr.io/ontdekit/climatechecker-frontend:latest 2^>nul`) do set "latest_version_frontend=%%i"
    for /f "usebackq tokens=*" %%i in (`docker inspect --format "{{.Config.Labels.version}}" climatechecker-frontend 2^>nul`) do set "current_version_frontend=%%i"

    for /f "usebackq tokens=*" %%i in (`docker inspect --format "{{.Config.Labels.version}}" ghcr.io/ontdekit/climatechecker-backend:latest 2^>nul`) do set "latest_version_backend=%%i"
    for /f "usebackq tokens=*" %%i in (`docker inspect --format "{{.Config.Labels.version}}" climatechecker-backend 2^>nul`) do set "current_version_backend=%%i"

    REM Frontend checks - use delayed expansion for comparisons inside blocks
    if not defined current_version_frontend (
        set "update_required=1"
        set "update_list=!update_list!Frontend: geen lokale image gevonden; "
    ) else (
        if defined latest_version_frontend (
            if not "!current_version_frontend!"=="!latest_version_frontend!" (
                set "update_required=1"
                set "update_list=!update_list!Frontend: !current_version_frontend! -> !latest_version_frontend!; "
            )
        ) else (
            echo Kon de nieuwste frontend versie niet controleren
        )
    )

    REM Backend checks
    if not defined current_version_backend (
        set "update_required=1"
        set "update_list=!update_list!Backend: geen lokale image gevonden; "
    ) else (
        if defined latest_version_backend (
            if not "!current_version_backend!"=="!latest_version_backend!" (
                set "update_required=1"
                set "update_list=!update_list!Backend: !current_version_backend! -> !latest_version_backend!; "
            )
        ) else (
            echo Kon de nieuwste backend versie niet controleren
        )
    )

    if "!update_required!"=="1" goto ask_update

    goto start_application

    :ask_update
    echo Er zijn mogelijk updates beschikbaar:
    echo !update_list!
    echo.

    REM Read user input with delayed expansion disabled to avoid expansion conflicts
    setlocal DISABLEDELAYEDEXPANSION
    set /p update="Wil je bijwerken naar de nieuwste versies? (j/n): "
    endlocal & set "update=%update%"

    if /i "%update%"=="j" (
        echo Bezig met bijwerken...
        docker-compose down
        docker pull ghcr.io/ontdekit/climatechecker-frontend:latest
        docker pull ghcr.io/ontdekit/climatechecker-backend:latest
        goto start_application
    ) else if /i "%update%"=="n" (
        echo Bijwerken overslaan
        goto start_application
    ) else (
        echo Ongeldige invoer. Voer ^j^ of ^n^ in.
        goto ask_update
    )

    :start_application
    REM If the frontend container is already running, don't start again
    docker-compose ps | find "climatechecker-frontend" >nul 2>&1 && goto already_running

    echo Bezig met starten van de applicatie...
    docker-compose up -d

    REM Wait for frontend to become available
    echo Wachten tot de frontend beschikbaar is...
    set /a attempts=0
    set /a max_attempts=30

    :wait_loop
    timeout /t 5 >nul
    set /a attempts+=1
    curl -s http://localhost:5173 >nul 2>&1

    REM If curl succeeded (exit code 0), proceed
    if not errorlevel 1 (
        goto wait_success
    )

    REM If we've reached the max attempts, fail
    if %attempts% geq %max_attempts% (
        echo Timeout bereikt. De applicatie kon niet gestart worden.
        echo Controleer de logs met: docker-compose logs
        pause
        exit /b 1
    )

    echo Nog niet beschikbaar - poging %attempts% van %max_attempts%...
    goto wait_loop

    :wait_success
    timeout /t 3 >nul
    echo De applicatie is nu beschikbaar!
    start "" "http://localhost:5173"
    docker-compose ps
    echo.
    echo De applicatie draait. Sluit dit venster om te stoppen.
    pause >nul
    echo Bezig met stoppen van de applicatie...
    docker-compose down
    exit /b 0

    :already_running
    echo De applicatie draait al!

    rem Controleer of er updates beschikbaar zijn voor de draaiende instance
    call :running_update_check
    if "%running_update_required%"=="1" goto prompt_running_update

    echo Open je browser en ga naar http://localhost:5173
    echo.
    echo Druk op een toets om af te sluiten...
    pause >nul
    exit /b 0

    :prompt_running_update
    echo.
    echo Er zijn updates beschikbaar:
    echo !running_update_list!
    echo.
    rem Debug: show current and latest IDs/labels for troubleshooting
    echo [DEBUG] frontend: current id=!running_current_frontend_id! latest id=!running_latest_frontend_id!
    echo [DEBUG] frontend labels: current="!running_current_frontend_label!" latest="!running_latest_frontend_label!"
    echo [DEBUG] backend: current id=!running_current_backend_id! latest id=!running_latest_backend_id!
    echo [DEBUG] backend labels: current="!running_current_backend_label!" latest="!running_latest_backend_label!"
    echo.
    rem Use CHOICE and capture its exit code explicitly into CHOICE_RESULT for robust branching
    choice /c JN /n /m "Wil je bijwerken en herstarten? (j/n): "
    set "CHOICE_RESULT=%errorlevel%"
    echo [DEBUG] CHOICE returned: %CHOICE_RESULT%
    if "%CHOICE_RESULT%"=="1" goto do_running_update
    if "%CHOICE_RESULT%"=="2" goto skip_running_update

    echo Ongeldige keuze, bijwerken overslaan.
    goto skip_running_update

    :skip_running_update
    echo Bijwerken overslaan.
    echo Open je browser en ga naar http://localhost:5173
    echo.
    echo Druk op een toets om af te sluiten...
    pause >nul
    exit /b 0

    :do_running_update
    echo Bezig met bijwerken en herstarten...
    docker-compose down
    docker-compose rm -f
    rem Remove local images to force fresh pull (ignore errors)
    docker image rm -f ghcr.io/ontdekit/climatechecker-frontend:latest climatechecker-frontend ghcr.io/ontdekit/climatechecker-backend:latest climatechecker-backend 2>nul
    docker pull ghcr.io/ontdekit/climatechecker-frontend:latest
    docker pull ghcr.io/ontdekit/climatechecker-backend:latest
    docker-compose up -d
    goto wait_loop

    :running_update_check
    rem Determine if the running container images differ from the remote :latest images
    set "running_update_required=0"
    set "running_update_list="
    set "running_latest_frontend_id="
    set "running_current_frontend_id="
    set "running_latest_backend_id="
    set "running_current_backend_id="
    set "running_latest_frontend_label="
    set "running_current_frontend_label="
    set "running_latest_backend_label="
    set "running_current_backend_label="

    rem Pull remote latest images silently so we can inspect their IDs/labels
    docker pull ghcr.io/ontdekit/climatechecker-frontend:latest >nul 2>&1
    for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Id}}" ghcr.io/ontdekit/climatechecker-frontend:latest 2^>nul`) do set "running_latest_frontend_id=%%i"
    for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Config.Labels.version}}" ghcr.io/ontdekit/climatechecker-frontend:latest 2^>nul`) do set "running_latest_frontend_label=%%i"

    docker pull ghcr.io/ontdekit/climatechecker-backend:latest >nul 2>&1
    for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Id}}" ghcr.io/ontdekit/climatechecker-backend:latest 2^>nul`) do set "running_latest_backend_id=%%i"
    for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Config.Labels.version}}" ghcr.io/ontdekit/climatechecker-backend:latest 2^>nul`) do set "running_latest_backend_label=%%i"

    rem --- FRONTEND: determine currently running image's id and label ---
    set "__container_frontend="
    for /f "delims=" %%C in ('docker ps -q -f "name=climatechecker-frontend" 2^>nul') do set "__container_frontend=%%C"
    if defined __container_frontend (
        for /f "delims=" %%I in ('docker inspect --format "{{.Image}}" %__container_frontend% 2^>nul') do set "running_current_frontend_id=%%I"
        if defined running_current_frontend_id (
            for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Config.Labels.version}}" %running_current_frontend_id% 2^>nul`) do set "running_current_frontend_label=%%i"
        )
    ) else (
        rem no running container; try local image by explicit tags as fallback
        for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Id}}" ghcr.io/ontdekit/climatechecker-frontend:latest 2^>nul`) do set "running_current_frontend_id=%%i"
        for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Config.Labels.version}}" ghcr.io/ontdekit/climatechecker-frontend:latest 2^>nul`) do if not defined running_current_frontend_label set "running_current_frontend_label=%%i"
    )
    set "__container_frontend="

    rem --- BACKEND: determine currently running image's id and label ---
    set "__container_backend="
    for /f "delims=" %%C in ('docker ps -q -f "name=climatechecker-backend" 2^>nul') do set "__container_backend=%%C"
    if defined __container_backend (
        for /f "delims=" %%I in ('docker inspect --format "{{.Image}}" %__container_backend% 2^>nul') do set "running_current_backend_id=%%I"
        if defined running_current_backend_id (
            for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Config.Labels.version}}" %running_current_backend_id% 2^>nul`) do set "running_current_backend_label=%%i"
        )
    ) else (
        for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Id}}" ghcr.io/ontdekit/climatechecker-backend:latest 2^>nul`) do set "running_current_backend_id=%%i"
        for /f "usebackq tokens=* delims=" %%i in (`docker inspect --format "{{.Config.Labels.version}}" ghcr.io/ontdekit/climatechecker-backend:latest 2^>nul`) do if not defined running_current_backend_label set "running_current_backend_label=%%i"
    )
    set "__container_backend="

    rem Compare image IDs first (most reliable)
    if defined running_current_frontend_id if defined running_latest_frontend_id if not "%running_current_frontend_id%"=="%running_latest_frontend_id%" (
        set "running_update_required=1"
        if defined running_current_frontend_label (
            set "running_update_list=!running_update_list!Frontend: !running_current_frontend_label! -> !running_latest_frontend_label!; "
        ) else (
            set "running_update_list=!running_update_list!Frontend: image id verschilt; "
        )
    ) else (
        rem If IDs not available, fall back to labels comparison
        if defined running_current_frontend_label if defined running_latest_frontend_label if not "!running_current_frontend_label!"=="!running_latest_frontend_label!" (
            set "running_update_required=1"
            set "running_update_list=!running_update_list!Frontend: !running_current_frontend_label! -> !running_latest_frontend_label!; "
        )
    )

    if defined running_current_backend_id if defined running_latest_backend_id if not "%running_current_backend_id%"=="%running_latest_backend_id%" (
        set "running_update_required=1"
        if defined running_current_backend_label (
            set "running_update_list=!running_update_list!Backend: !running_current_backend_label! -> !running_latest_backend_label!; "
        ) else (
            set "running_update_list=!running_update_list!Backend: image id verschilt; "
        )
    ) else (
        if defined running_current_backend_label if defined running_latest_backend_label if not "!running_current_backend_label!"=="!running_latest_backend_label!" (
            set "running_update_required=1"
            set "running_update_list=!running_update_list!Backend: !running_current_backend_label! -> !running_latest_backend_label!; "
        )
    )

    rem Export results for caller (they are already environment variables)
    exit /b 0

    :docker_not_running
    echo Docker daemon not reachable.
    echo Probeer Docker Desktop te starten...

    rem Zoek mogelijke Docker Desktop uitvoerbare bestanden
    set "docker_exe="
    if exist "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" (
        set "docker_exe=%ProgramFiles%\Docker\Docker\Docker Desktop.exe"
    )
    if exist "%LocalAppData%\Programs\Docker\Docker\Docker Desktop.exe" (
        if "%docker_exe%"=="" set "docker_exe=%LocalAppData%\Programs\Docker\Docker\Docker Desktop.exe"
    )
    if exist "%ProgramFiles%\Docker\Docker\DockerDesktop.exe" (
        if "%docker_exe%"=="" set "docker_exe=%ProgramFiles%\Docker\Docker\DockerDesktop.exe"
    )

    if not defined docker_exe (
        echo Kan Docker Desktop executable niet vinden.
        echo - Start Docker Desktop handmatig en controleer installatie.
        echo - Gezocht: "%ProgramFiles%\Docker\Docker\Docker Desktop.exe" en "%LocalAppData%\Programs\Docker\Docker\Docker Desktop.exe"
        pause
        exit /b 1
    )

    rem Start Docker Desktop en wacht tot docker daemon reageert
    start "" "%docker_exe%"
    echo Docker Desktop gestart (of gestart poging). Wachten tot daemon reageert (max 60s)...
    set /a waited=0
    :wait_loop_docker
    timeout /t 3 >nul
    docker info >nul 2>&1
    if errorlevel 1 (
        set /a waited+=3
        if %waited% lss 60 goto wait_loop_docker
        echo Docker start timeout. Controleer Docker Desktop handmatig.
        pause
        exit /b 1
    )
    echo Docker is gestart.
    goto check_versions
