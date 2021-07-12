---
title:  "Word Finder 개발기 2"
excerpt: "Word Finder 개발기 2"

categories:
 Python
tags:
 [Python, word_finder, toy_project]

toc: true
toc_sticky: true
date: 2021-07-04
---

# Word Finder 개발기 2 - 업데이트

내가 모델로 했던 프로그램의 소스코드에서 얻은 것이 있다면 업데이트 로직이라고 하겠다. 다음은 대략적인 순서다. 

1. 서버에서 업데이트된 프로그램의 압축파일을 임시 폴더에 받아온다. 
2. 임시폴더 안의 내용을 모두 압축 해제 한다. 
3. 현재 실행중인 프로그램을 임시폴더로 넣고 이름을 바꾼다. 
4. 임시폴더에 있는 새로운 프로그램을 밖으로 꺼내고 실행시킨다. 

3, 4번 과정에서 원래 켜져 있던 프로그램이 닫히고 새로운 프로그램이 열리게 된다. 많은 경우 웹 서버에 업데이트 파일을 올리고 거기서 내려받는 것을 볼 수 있었다. 하지만 나 같은 경우 라즈베리파이로 만든 NAS에 저장하고 외부 포트를 열어 익명 접속을 통해 파일을 내려받도록 하였다. 

조금 더 구체적인 순서를 보이자면 다음과 같다. 

1. 사용자가 업데이트 메뉴를 클릭한다. 

2. 먼저 FTP 서버에 접속해 현재 프로그램과 서버의 올라온 버전을 비교한다. 

   2-1. 만약 현재 버전이 더 높거나 같다면 업데이트할 필요가 없다는 메세지를 띄우고 돌아간다. 

3. 서버의 버전이 더 높다면 updater 스레드를 생성한다. 

4. updater 스레드는 서버에서 파일을 내려받는다. 

   4-1. 먼저 서버에 로그인하고 타겟 파일의 용량을 스레드 신호로 내보낸다. 

   4-2. 타겟 파일을 내려받는다. 

   4-3. 내려받은 파일의 압축을 푼다. 

   4-4. 현재 돌아가는 exe파일을 임시 폴더에 이름을 바꾸어 넣고, 임시 폴더에 받은 타겟 exe파일을 현재 경로로 꺼낸다.

   4-5. 꺼낸 새 파일을 실행시킨다. 

5. updater 스레드가 타겟 파일의 용량을 신호로 보내면 update_checker 라는 새 스레드를 만든다. 

   5-1. 이 스레드는 현재 임시 폴더에 존재하는 파일의 용량과 타겟 파일의 용량(목표 용량)을 계속 비교한다. 

   5-2. 비교한 값을 백분율로 환산하여 일정 간격마다 신호로 보낸다. 

6. 메인 스레드는 받은 신호, 즉 progress 값을 창의 진행 바로 표시한다. 

7. 모든 절차가 끝나면 현재 창이 닫히고 다운로드한 새 프로그램이 실행된다. 

먼저 다음은 업데이트 메뉴를 클릭했을 때 나타나는 창 클래스이다. 

```{.py}
class Updater_GUI(QDialog, updater_gui):
    def __init__(self, parent, filename):
        super(Updater_GUI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('Update')
        self.show()
        self.filename = filename
        self.total_size = 0

        # 업데이트하는 worker를 생성한다.
        self.threadpool = QThreadPool()
        self.update_worker = updater.Updater(self.filename)
        self.update_worker.set_sever(WORDFINDER_FTP_SERVER)
        self.update_worker.set_dir(TEMP_UPDATE_DIR)
        self.threadpool.start(self.update_worker)

        # 업데이트 worker가 파일 전체 용량을 가르쳐주면 그때부터 진행상황을 체크한다.
        self.update_worker.signal.total_size.connect(self.check_progress)
        self.update_worker.signal.finished.connect(self.close)

    def check_progress(self, size):
        self.total_size = size
        if self.total_size == 0:
            return

        # 업데이트 진행상황을 체크하는 worker 스레드 클래스.
        class _update_checker(QRunnable):
            def __init__(self, filename, total_size):
                super(_update_checker, self).__init__()
                self.signals = check_signal()
                self.filename = filename
                self.total_size = total_size

            @pyqtSlot()
            def run(self):
                current_size = 0
                total = self.total_size
                sleep(3)
                # 업데이트 진행상황을 일정한 간격으로 체크한다.
                while (current_size <= total):
                    if os.path.isfile(os.path.join(TEMP_UPDATE_DIR, self.filename + '.zip')):
                        current_size = os.path.getsize(os.path.join(TEMP_UPDATE_DIR, self.filename + '.zip'))
                    else:
                        return
                    self.signals.progress.emit((int(current_size) / total) * 100)
                    sleep(0.01)

        self.progress_checker = _update_checker(self.filename, self.total_size)
        self.threadpool.start(self.progress_checker)
        self.progress_checker.signals.progress.connect(self.progress_bar.setValue)
```

[전체 코드](https://github.com/altair823/WordFinder/blob/master/gui/update_window_gui.py)는 깃허브에서 볼 수 있다. 


<script src="https://utteranc.es/client.js"
        repo="altair823/blog_comments"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>
