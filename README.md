# OS Scheduler Simulator

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**운영체제 CPU 스케줄링 알고리즘 시뮬레이터**

8가지 CPU 스케줄링 알고리즘을 구현하고 성능을 비교하는 Python 시뮬레이션 프로그램입니다.

## 🚀 주요 기능

- ✅ **8가지 알고리즘**: FCFS, SJF, Round Robin, Priority, MLQ, RM, EDF
- ✅ **대화형 모드**: 직관적인 UI로 쉬운 사용
- ✅ **Gantt Chart**: matplotlib를 이용한 시각화
- ✅ **성능 비교**: 알고리즘별 대기시간, 반환시간, CPU 활용률 비교

## 📦 설치

```bash
# 저장소 클론
git clone https://github.com/YOUR_USERNAME/os-scheduler-simulator.git
cd os-scheduler-simulator

# 의존성 설치
pip install matplotlib
```

## 🎮 사용 방법

```bash
cd operating_system
python main.py
```

### 입력 옵션
- `0`: 교수님 데이터 (7개 프로세스)
- `1`: 랜덤 데이터 생성 (10개 프로세스)
- `2`: 커스텀 데이터 선택

### 알고리즘 선택
- `1-8`: 개별 알고리즘 실행
- `all`: 모든 알고리즘 실행 및 비교

## 📊 구현된 알고리즘

| # | 알고리즘 | 유형 | Time Slice |
|---|---------|------|------------|
| 1 | FCFS | 비선점 | - |
| 2 | SJF (SRTF) | 선점 | - |
| 3 | Round Robin | 선점 | 4 |
| 4 | Priority (Static) | 선점 | - |
| 5 | Priority + Aging | 선점 | factor=10 |
| 6 | Multi-Level Queue | 선점 | 3-level |
| 7 | Rate Monotonic | 실시간 | - |
| 8 | EDF | 실시간 | - |

## 📈 결과 예시

프로그램 실행 후 `output/` 폴더에 생성:
- **Gantt Charts**: `gantt_*.png` (8개)
- **비교 그래프**: `comparison.png`
- **상세 결과**: `results.txt`

### 성능 비교 (교수님 데이터)

```
Algorithm                  Avg WT   Avg TAT   CPU Util%
FCFS                       34.71    46.57     94.32
SJF (Preemptive/SRTF)      24.71    36.57     100.00
Round Robin (q=4)          40.86    52.71     100.00
Priority (Static)          25.00    36.86     100.00
...
```

## 🏗️ 프로젝트 구조

```
operating-system-group/
├── README.md
└── operating_system/
    ├── main.py               # 메인 실행 파일
    ├── requirements.txt
    ├── core/                 # 핵심 모듈
    │   ├── process.py
    │   └── scheduler_base.py
    ├── schedulers/           # 알고리즘 구현
    │   ├── basic_schedulers.py
    │   └── advanced_schedulers.py
    ├── utils/                # 유틸리티
    │   ├── input_parser.py
    │   └── visualization.py
    ├── data/                 # 입력 데이터
    │   └── professor_data.txt
    └── output/               # 결과 (자동 생성)
```

## 🔧 기술 스택

- **Language**: Python 3.8+
- **Visualization**: matplotlib
- **Data Processing**: Built-in (csv, dataclass)

## 📝 입력 형식

```csv
# PID,도착시간,우선순위,"실행패턴",주기,마감시한
1,0,3,"15",0,0              # CPU-bound
2,2,2,"3,10,4,12,5",0,0     # I/O-bound
5,0,0,"4",10,10             # 실시간
```

## 🎓 학습 내용

이 프로젝트를 통해 다음을 학습했습니다:
- CPU 스케줄링 알고리즘 구현
- 프로세스 상태 관리 (PCB)
- 인터럽트 처리 (Timer, I/O, Preemption)
- 알고리즘 성능 분석

## 📄 License

MIT License

## 👤 Author

[Your Name] - Operating Systems Course Project (2025)

---

⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!
