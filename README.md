# Game Bar PikPak Auto Upload

Windows Game Bar로 녹화된 영상을 자동으로 감지하여 **PikPak에 업로드하고, 업로드가 성공하면 로컬 파일을 삭제하는 자동화 도구**입니다.

PowerShell과 `rclone`을 이용하며, Windows 로그인 시 백그라운드에서 자동으로 실행되도록 설정할 수 있습니다.

## 주요 기능

* Windows Game Bar 녹화 폴더 자동 감시
* 새로 생성된 MP4 파일 자동 감지
* 녹화 중인 파일 업로드 방지를 위한 대기 처리
* `rclone`을 이용한 PikPak 자동 업로드
* 업로드 성공 후 로컬 원본 자동 삭제
* Windows 로그인 시 자동 실행

## 동작 방식

```text
Windows Game Bar 녹화
        ↓
Captures 폴더에 MP4 생성
        ↓
PowerShell 스크립트가 주기적으로 확인
        ↓
생성 후 일정 시간이 지난 파일 감지
        ↓
rclone을 이용해 PikPak 업로드
        ↓
업로드 성공
        ↓
로컬 원본 파일 삭제
```

업로드 프로그램은 백그라운드에서 계속 실행되며 일정 주기마다 새로운 녹화 파일이 있는지 확인합니다.

## 구성 파일

| 파일명                           | 설명                                          |
| ----------------------------- | ------------------------------------------- |
| `PikPakGameBarUpload.ps1`     | Game Bar 녹화 폴더를 감시하고 PikPak으로 업로드하는 메인 스크립트 |
| `RunPikPakUploaderHidden.vbs` | PowerShell 창을 표시하지 않고 업로더를 백그라운드에서 실행       |
| `install.ps1`                 | 자동 실행 환경을 설치하고 Windows 작업 스케줄러에 등록          |
| `uninstall.ps1`               | 등록된 자동 실행 설정을 제거                            |

## 요구 사항

### 운영체제

* Windows 10 / Windows 11
* Windows Game Bar 녹화 기능

### rclone

PikPak 업로드를 위해 `rclone`이 필요합니다.

rclone을 설치한 뒤 PowerShell 또는 CMD에서 다음 명령어로 설치 여부를 확인합니다.

```powershell
rclone version
```

버전 정보가 정상적으로 출력되면 사용할 수 있습니다.

## rclone PikPak 설정

rclone 설치 후 다음 명령어를 실행합니다.

```powershell
rclone config
```

설정 화면에서 PikPak용 Remote를 생성합니다.

이 프로젝트의 스크립트에서 사용하는 Remote 이름과 `rclone config`에서 생성한 Remote 이름이 동일해야 합니다.

설정이 끝난 후 다음과 같이 연결을 확인할 수 있습니다.

```powershell
rclone lsd pikpak:
```

`pikpak`이라는 Remote를 사용했다면 위 명령어 실행 시 PikPak의 폴더 목록이 표시됩니다.

Remote 이름을 다르게 설정했다면 `pikpak:` 부분을 자신이 설정한 이름으로 변경해야 합니다.

## 설치

### 1. 저장소 다운로드

저장소를 Clone하거나 ZIP으로 다운로드합니다.

예시:

```powershell
git clone <repository-url>
cd gamebar-pikpak-auto-upload
```

### 2. 관리자 권한으로 PowerShell 실행

Windows 검색에서 `PowerShell`을 검색한 뒤 **관리자 권한으로 실행**합니다.

프로젝트 폴더로 이동합니다.

```powershell
cd "G:\gamebar-pikpak-auto-upload"
```

경로는 저장소를 다운로드한 위치에 맞게 변경합니다.

### 3. PowerShell 실행 정책 허용

환경에 따라 `install.ps1` 실행 시 다음과 같은 오류가 발생할 수 있습니다.

```text
파일이 디지털 서명되지 않았습니다.
현재 시스템에서 이 스크립트를 실행할 수 없습니다.
PSSecurityException
```

이 경우 현재 PowerShell 프로세스에서만 스크립트 실행을 허용합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

확인 메시지가 표시되면 `Y`를 입력합니다.

`Process` 범위를 사용하므로 해당 PowerShell 창을 닫으면 설정이 사라지며 시스템 전체 실행 정책을 영구적으로 변경하지 않습니다.

### 4. 설치 스크립트 실행

```powershell
.\install.ps1
```

설치가 완료되면 Windows 작업 스케줄러에 자동 실행 작업이 등록됩니다.

이후 Windows에 로그인하면 업로더가 자동으로 백그라운드에서 실행됩니다.

## 수동 실행 테스트

자동 실행을 설정하기 전에 업로더가 정상적으로 동작하는지 직접 확인할 수 있습니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\Scripts\PikPakGameBarUpload.ps1"
```

설치 위치가 다른 경우 경로를 변경합니다.

실행 후 PowerShell 창이 계속 열려 있는 것은 정상입니다.

업로더는 종료되는 프로그램이 아니라 계속 실행되면서 일정 주기마다 새로운 Game Bar 녹화 파일을 확인합니다.

테스트하려면 Windows Game Bar에서 녹화를 생성한 뒤 PikPak에 파일이 업로드되는지 확인합니다.

업로드가 성공하면 로컬 원본 파일은 자동으로 삭제됩니다.

## 자동 실행

`install.ps1`을 정상적으로 실행했다면 별도로 프로그램을 실행할 필요가 없습니다.

```text
Windows 로그인
      ↓
작업 스케줄러
      ↓
RunPikPakUploaderHidden.vbs
      ↓
PikPakGameBarUpload.ps1
      ↓
백그라운드 감시 시작
```

VBS 스크립트를 통해 PowerShell을 실행하기 때문에 콘솔 창이 계속 화면에 표시되지 않습니다.

컴퓨터를 재부팅한 이후에도 Windows에 로그인하면 자동으로 실행됩니다.

## 제거

자동 실행 설정을 제거하려면 **관리자 권한 PowerShell**에서 프로젝트 폴더로 이동합니다.

```powershell
cd "G:\gamebar-pikpak-auto-upload"
```

필요한 경우 현재 PowerShell 프로세스에 실행 권한을 부여합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

이후 제거 스크립트를 실행합니다.

```powershell
.\uninstall.ps1
```

등록된 자동 실행 작업이 제거됩니다.

## install.ps1 / uninstall.ps1 바로 실행하기

실행 정책을 별도로 변경하지 않고 한 번만 실행하려면 다음과 같이 사용할 수도 있습니다.

### 설치

관리자 PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\install.ps1"
```

### 제거

관리자 PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\uninstall.ps1"
```

이 방식은 해당 PowerShell 실행에 대해서만 `ExecutionPolicy Bypass`를 적용합니다.

## 사용 방법

설치가 완료된 이후에는 별도의 조작이 필요하지 않습니다.

Windows Game Bar에서 평소처럼 녹화하면 됩니다.

```text
Win + Alt + R
```

또는 Game Bar의 녹화 기능을 사용합니다.

녹화가 끝나면 생성된 MP4 파일을 업로더가 자동으로 감지하고 PikPak으로 이동합니다.

## 주의사항

업로드 성공 후에는 **로컬 원본 파일이 삭제됩니다.**

따라서 PikPak 업로드가 정상적으로 동작하는지 충분히 테스트한 뒤 사용하는 것을 권장합니다.

또한 다음 사항을 확인해야 합니다.

* `rclone`이 정상적으로 설치되어 있어야 합니다.
* PikPak Remote 설정이 완료되어 있어야 합니다.
* 스크립트에 설정된 Remote 이름과 rclone Remote 이름이 일치해야 합니다.
* Game Bar 녹화 폴더 경로가 스크립트 설정과 일치해야 합니다.
* PikPak 인증 정보가 변경되면 rclone 설정을 다시 해야 할 수 있습니다.

## 문제 해결

### install.ps1을 실행할 수 없음

다음 오류가 발생하는 경우:

```text
PSSecurityException
파일이 디지털 서명되지 않았습니다.
```

관리자 PowerShell에서 실행합니다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install.ps1
```

### rclone 명령어를 찾을 수 없음

```text
rclone : 'rclone' 용어가 cmdlet...
```

rclone이 설치되어 있는지 확인합니다.

```powershell
rclone version
```

명령어를 찾지 못한다면 rclone을 설치하고 PATH가 정상적으로 설정되어 있는지 확인합니다.

### PikPak 연결 확인

```powershell
rclone lsd pikpak:
```

정상적으로 폴더 목록이 출력되는지 확인합니다.

### 수동 실행하면 CMD/PowerShell 창이 계속 켜져 있음

정상 동작입니다.

`PikPakGameBarUpload.ps1`은 백그라운드 감시를 위해 계속 실행되는 스크립트입니다.

실제 자동 실행 환경에서는 `RunPikPakUploaderHidden.vbs`를 통해 숨김 상태로 실행됩니다.

## 참고

* Windows Game Bar
* PowerShell
* rclone
* PikPak

## License

Personal project.
