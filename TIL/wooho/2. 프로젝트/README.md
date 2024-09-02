# 1. Ubuntu 20.04 설치방법
1. 시작 메뉴를 열고 "PowerShell"을 검색한 후, 관리자 권한으로 실행
2. 다음 명령어를 실행하여 WSL 기능을 활성화
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
완료 후 컴퓨터를 재부팅
3. WSL 2를 기본 버전으로 설정
wsl --set-default-version 2
4. Microsoft Store를 열고, Ubuntu 20.04 LTS를 찾아 설치
5. 설치 완료 후 사용자 이름과 비밀번호를 설정