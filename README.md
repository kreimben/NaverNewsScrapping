# News Scrapping on naver news.

1. Environment
    - Python 3.11

1. Requirements
* 크롤링은 데이터를 수집하는 방법 중 하나입니다. 이번 과제에서는 네이버 뉴스 중 IT 카테고리 중 1가지를 선정하여 최근 한달간의 뉴스 데이터를 모아봅시다. 모은 데이터는 정형화하여 데이터베이스에 저장하며 다음 칼럼을 가진 테이블을 만들어서 관리합니다.

1. Requirements
- 최근 3일간 뉴스 데이터를 csv 형식으로 저장하여 제출.
- 실습 과제로 작성한 노트북(ipynb) 파일, 캡쳐 이미지 등 최종 제출물은 하나의 파일로 압축하여 제출.

1. Appendix
- 데이터베이스에 저장한 데이터를 API 형식으로 제공해봅니다. 요청 Request 에 시작 날짜, 종료날짜, 언론사 이름을 넣어서 해당 조건에 해당하는 데이터만 응답하도록 합니다.
- API 응답이 너무 커지면 네트워크 부하, 딜레이, 메모리 낭비 등 여러 단점이 발생합니다. API 에 Page Size, Page number를 Request로부터 입력받아서 데이터 중 일부만 응답할 수 있도록 옵션을 제공합니다.
- 웹 구현까지 완료한 경우 결과 화면 페이지 캡쳐 이미지 제출
- 웹 구현 진행이 어려울 경우 입출력을 위한 function 작성하여 Notebook을 통한 입출력 실행

1. 결과물
- [x] 최근 3일간 뉴스 => [csv](result_from_20240115_end_20240117.csv)
- [x] 실습 과제로 작성한 노트북(ipynb) 파일 => [main.ipynb](main.ipynb)
- [x] 웹 구현 결과 이미지 => ![](res.jpeg)

1. 실행 방법
```bash
$ ./run_server.sh
```