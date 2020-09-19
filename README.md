# BaekHyunGomokuAI
20820 이지명, 20802 곽은재, 20822 전현민 과제연구

--------

### 프로젝트 환경
- python 3.7
- tensorflow 2.0.0

------
### 프로젝트 구조
   
   
- Gomoku/
  - Board.py
    - 오목판
    - 착수, 승패 판별 구현
  - Agent.py
    - 사용자가 직접 플레이 가능한 에이전트
    - CLI 기반 에이전트 구현
    - GUI 기반 에이전트 구현
  - Server.py
    - 2개의 에이전트 간 통신으로 오목 대국을 하는 서버 구현
  - GUI.py
    - Tkinter를 이용한 GUI 구현
- MCTS/
  - Tree.py
    - Monte Carlo Tree 구현
    - selection, expansion 구현
  - Node.py
    - Monte Carlo Tree의 node 구현
    - backpropagation, UCB/UCT 구현
  - Agent.py
    - Monte Carlo Tree Search를 통해 수를 도출하는 에이전트
    - Random 기반 MCTS를 사용하는 Pure MCTS Agent 구현
    - Neural Network 기반 MCTS를 사용하는 Deep MCTS Agent 구현
  - policy.py
    - Monte Carlo Tree의 expansion, simulation 단계에 사용하는 정책망 함수
    - Random 기반 정책망, Neural Network 기반 정책망 구현
  - simulation.py
    - Monte Carlo Tree의 simulation 구현
    - 가치망을 이용한 승패 예측 구현
- Network/
  - save/
    - Local Machine에서 학습한 Neural Network 데이터
  - colab/
    - Google Colab에서 학습한 Neural Network 데이터
  - networks.py
    - Tensorflow를 사용해 Convolutional Neural Network 기반 정책망, 가치망 구현
    - Monte Carlo Tree의 expansion 단계에서 사용되는 Tree Policy Network
    - Monte Carlo Tree의 simulation 단계에서 사용되는 Rollout Poclicy Network
    - Monte Carlo Tree의 simulation 단계에서 사용되는 Value Network
  - train.py
    - Neural Network 학습
  - Runner.py
    - 학습된 Neural Nerwork를 통해 착수 확률 예측, 승패 예측
- common.py
  - 프로젝트 모듈 및 utility
- to_build.py
  - 실행파일 빌드용
- selfplay.py, deep_pure_selfplay.py
  - MCTS간 자가대국 데이터 수집용
- gui_test.py, simluation_test.py, network_run_test.py
  - 테스트용 스크립트
------

### 실행 파일
https://drive.google.com/drive/folders/1Aw1GTW3H29or_u790IIuV3_ip_s6Vs09   
자신의 실행 환경에 맞게 AVX2 버전, SSE2 버전 중 하나를 택해 다운로드
