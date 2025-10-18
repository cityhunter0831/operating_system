#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OS 스케줄러 시뮬레이터 - 메인 실행 파일
알고리즘 선택 기능 포함
"""

import sys
import os

# 모듈 임포트
from core.process import Process
from utils.input_parser import InputParser
from schedulers.basic_schedulers import FCFSScheduler, SJFScheduler, RoundRobinScheduler
from schedulers.advanced_schedulers import (PriorityScheduler, PriorityAgingScheduler, 
                                            MLQScheduler, RateMonotonicScheduler, EDFScheduler)
from utils.visualization import Visualizer


# 사용 가능한 알고리즘 정의
ALGORITHMS = {
    '1': {
        'name': 'FCFS (First-Come, First-Served)',
        'class': FCFSScheduler,
        'params': {}
    },
    '2': {
        'name': 'SJF (Shortest Job First - Preemptive)',
        'class': SJFScheduler,
        'params': {}
    },
    '3': {
        'name': 'Round Robin',
        'class': RoundRobinScheduler,
        'params': {'time_slice': 4}
    },
    '4': {
        'name': 'Priority Scheduling (Static)',
        'class': PriorityScheduler,
        'params': {}
    },
    '5': {
        'name': 'Priority Scheduling with Aging',
        'class': PriorityAgingScheduler,
        'params': {'aging_factor': 10}
    },
    '6': {
        'name': 'Multi-Level Queue',
        'class': MLQScheduler,
        'params': {}
    },
    '7': {
        'name': 'Rate Monotonic (RM)',
        'class': RateMonotonicScheduler,
        'params': {}
    },
    '8': {
        'name': 'Earliest Deadline First (EDF)',
        'class': EDFScheduler,
        'params': {}
    },
    'all': {
        'name': 'All Algorithms',
        'class': None,
        'params': {}
    }
}


def print_banner():
    """배너 출력"""
    print("\n" + "="*80)
    print(" "*25 + "OS SCHEDULER SIMULATOR")
    print("="*80 + "\n")


def print_algorithm_menu():
    """알고리즘 선택 메뉴 출력"""
    print("\n" + "="*80)
    print("SELECT SCHEDULING ALGORITHM")
    print("="*80)
    print("\n[Basic Algorithms]")
    print("  1. FCFS (First-Come, First-Served)")
    print("  2. SJF (Shortest Job First - Preemptive/SRTF)")
    print("  3. Round Robin (Time Slice = 4)")
    print("\n[Priority Scheduling]")
    print("  4. Priority Scheduling (Static)")
    print("  5. Priority Scheduling with Aging")
    print("\n[Advanced Algorithms]")
    print("  6. Multi-Level Queue (3-level with Feedback)")
    print("\n[Real-Time Scheduling]")
    print("  7. Rate Monotonic (RM)")
    print("  8. Earliest Deadline First (EDF)")
    print("\n[Special Options]")
    print("  all. Run All Algorithms")
    print("  0. Exit")
    print("="*80)


def get_user_choice():
    """사용자 선택 입력"""
    while True:
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '0':
            print("\nExiting program...")
            sys.exit(0)
        
        if choice in ALGORITHMS:
            return choice
        
        print("[ERROR] Invalid choice. Please try again.")


def run_single_algorithm(algorithm_key, processes, verbose=False):
    """단일 알고리즘 실행"""
    algo_info = ALGORITHMS[algorithm_key]
    
    print(f"\n{'='*80}")
    print(f"Running: {algo_info['name']}")
    print(f"{'='*80}\n")
    
    try:
        scheduler = algo_info['class'](processes, **algo_info['params'])
        result = scheduler.run(verbose=verbose)
        return result
    except Exception as e:
        print(f"[ERROR] Failed to run {algo_info['name']}: {e}")
        import traceback
        traceback.print_exc()
        return None


def run_all_algorithms(processes, verbose=False):
    """모든 알고리즘 실행"""
    results = []
    
    print("\n" + "="*80)
    print("RUNNING ALL SCHEDULING ALGORITHMS")
    print("="*80 + "\n")
    
    for key in ['1', '2', '3', '4', '5', '6', '7', '8']:
        algo_info = ALGORITHMS[key]
        print(f"[{key}/8] Running {algo_info['name']}...")
        
        try:
            scheduler = algo_info['class'](processes, **algo_info['params'])
            result = scheduler.run(verbose=verbose)
            results.append(result)
            print(f"[OK] {algo_info['name']} completed\n")
        except Exception as e:
            print(f"[ERROR] {algo_info['name']} failed: {e}\n")
    
    return results


def save_results(results, output_dir="output"):
    """결과 저장"""
    os.makedirs(output_dir, exist_ok=True)
    
    visualizer = Visualizer()
    
    # 통계 테이블 출력
    print("\n" + "="*80)
    print("RESULTS")
    print("="*80 + "\n")
    visualizer.print_statistics_table(results)
    
    # Gantt Charts 생성
    print("Generating Gantt charts...")
    for result in results:
        algo_name = result['algorithm'].replace(' ', '_').replace('/', '-').replace('(', '').replace(')', '')
        save_path = os.path.join(output_dir, f"gantt_{algo_name}.png")
        visualizer.draw_gantt_chart(result['gantt_chart'], result['algorithm'], 
                                    save_path=save_path, show=False)
    print(f"[OK] Gantt charts saved to '{output_dir}/' directory\n")
    
    # 비교 그래프 (2개 이상일 때만)
    if len(results) > 1:
        print("Generating comparison chart...")
        comparison_path = os.path.join(output_dir, "comparison.png")
        visualizer.compare_algorithms(results, save_path=comparison_path, show=False)
        print("[OK] Comparison chart saved\n")
    
    # 상세 결과 저장
    results_file = os.path.join(output_dir, "results.txt")
    save_results_to_file(results, results_file)
    
    print(f"\n{'='*80}")
    print("SIMULATION COMPLETED")
    print(f"{'='*80}")
    print(f"\nResults saved in '{output_dir}/' directory:")
    print(f"  - Gantt charts: gantt_*.png")
    if len(results) > 1:
        print(f"  - Comparison: comparison.png")
    print(f"  - Detailed results: results.txt")
    print("="*80 + "\n")


def save_results_to_file(results, filename):
    """결과를 텍스트 파일로 저장"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*120 + "\n")
            f.write("OS SCHEDULER SIMULATION RESULTS\n")
            f.write("="*120 + "\n\n")
            
            # 통계 비교
            f.write("PERFORMANCE COMPARISON\n")
            f.write("-"*120 + "\n")
            f.write(f"{'Algorithm':<35} {'Avg WT':>12} {'Avg TAT':>12} {'CPU Util(%)':>15} {'Context SW':>12}\n")
            f.write("-"*120 + "\n")
            
            for result in results:
                algo = result['algorithm']
                stats = result['statistics']
                f.write(f"{algo:<35} "
                       f"{stats['avg_waiting_time']:>12.2f} "
                       f"{stats['avg_turnaround_time']:>12.2f} "
                       f"{stats['cpu_utilization']:>15.2f} "
                       f"{stats['context_switches']:>12}\n")
            
            f.write("="*120 + "\n\n")
            
            # 상세 결과
            for result in results:
                f.write("\n" + "="*120 + "\n")
                f.write(f"Algorithm: {result['algorithm']}\n")
                f.write("="*120 + "\n\n")
                
                f.write("Process Details:\n")
                f.write("-"*100 + "\n")
                f.write(f"{'PID':<6} {'Arrival':>8} {'Priority':>10} {'Start':>8} {'Finish':>8} "
                       f"{'Wait':>8} {'TAT':>8} {'Response':>10}\n")
                f.write("-"*100 + "\n")
                
                for process in result['processes']:
                    f.write(f"{process.pid:<6} "
                           f"{process.arrival_time:>8} "
                           f"{process.initial_priority:>10} "
                           f"{process.start_time:>8} "
                           f"{process.finish_time:>8} "
                           f"{process.waiting_time:>8} "
                           f"{process.turnaround_time:>8} "
                           f"{process.response_time if process.response_time is not None else 'N/A':>10}\n")
                
                f.write("\n")
        
        print(f"[OK] Results saved to {filename}")
        
    except Exception as e:
        print(f"[ERROR] Failed to save results: {e}")


def select_input_file():
    """입력 파일 선택"""
    print("\n" + "="*80)
    print("SELECT INPUT FILE")
    print("="*80)
    
    # 현재 스크립트 파일의 디렉토리를 기준으로 data 폴더 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    professor_data = os.path.join(data_dir, "professor_data.txt")
    
    print("\n[Input Options]")
    print("  0. Professor Data (Recommended) - professor_data.txt")
    print("  1. Random Data (Auto-generate) - generated_input.txt")
    print("  2. Custom Data (Select from data/ directory)")
    print("="*80)
    
    while True:
        choice = input("\nSelect input option (0-2): ").strip()
        
        if choice == '0':
            # 교수 데이터
            if os.path.exists(professor_data):
                return professor_data
            else:
                print(f"[ERROR] Professor data not found at {professor_data}")
                continue
        
        elif choice == '1':
            # 랜덤 데이터 생성 신호
            return "GENERATE_RANDOM"
        
        elif choice == '2':
            # 커스텀 데이터 선택
            if os.path.exists(data_dir):
                files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]
                if files:
                    print("\n" + "-"*80)
                    print("Available files in data/ directory:")
                    for i, file in enumerate(files, 1):
                        print(f"  {i}. {file}")
                    print("-"*80)
                    
                    file_choice = input("Select file number: ").strip()
                    try:
                        idx = int(file_choice) - 1
                        if 0 <= idx < len(files):
                            return os.path.join(data_dir, files[idx])
                        else:
                            print("[ERROR] Invalid file number.")
                            continue
                    except:
                        print("[ERROR] Invalid input.")
                        continue
                else:
                    print("[ERROR] No .txt files found in data/ directory.")
                    continue
            else:
                print("[ERROR] data/ directory not found.")
                continue
        
        else:
            print("[ERROR] Invalid choice. Please enter 0, 1, or 2.")


def main():
    """메인 함수"""
    print_banner()
    
    # 입력 파일 선택
    input_file = select_input_file()
    
    # 랜덤 데이터 생성 요청인지 확인
    if input_file == "GENERATE_RANDOM":
        print("\n[INFO] Generating random processes...")
        processes = InputParser.generate_random_processes(num_processes=10, seed=None)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        generated_file = os.path.join(script_dir, "data", "generated_input.txt")
        os.makedirs(os.path.dirname(generated_file), exist_ok=True)
        InputParser.save_processes_to_file(processes, generated_file)
        print(f"[OK] Random processes saved to {generated_file}")
    else:
        # 파일에서 로드
        print(f"\nLoading processes from '{input_file}'...")
        processes = InputParser.parse_file(input_file)
        
        if not processes:
            print("\n[ERROR] Failed to load processes or file is empty.")
            sys.exit(1)
    
    # 프로세스 요약
    InputParser.print_process_summary(processes)
    
    # 알고리즘 선택 루프
    while True:
        print_algorithm_menu()
        choice = get_user_choice()
        
        if choice == 'all':
            # 모든 알고리즘 실행
            results = run_all_algorithms(processes, verbose=False)
            if results:
                save_results(results)
        else:
            # 단일 알고리즘 실행
            result = run_single_algorithm(choice, processes, verbose=False)
            if result:
                save_results([result])
        
        # 계속 여부 확인
        print("\n" + "="*80)
        continue_choice = input("Do you want to run another simulation? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\nThank you for using OS Scheduler Simulator!")
            print("="*80 + "\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
        print("="*80 + "\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
